# -*- coding: utf-8 -*-
"""
SQLite 连接池模块
提升数据库并发查询性能
"""

import sqlite3
import threading
import time
from contextlib import contextmanager
from queue import Queue, Empty, Full
from typing import Optional, Any, List, Tuple

from tools.log import Log


class SQLiteConnectionPool:
    """
    SQLite 连接池

    特性:
    - 连接复用，避免频繁创建销毁
    - 支持并发查询
    - 自动优化配置（WAL模式）
    - 线程安全
    """

    def __init__(self, database: str, pool_size: int = 5, timeout: float = 30.0):
        """
        初始化连接池

        Args:
            database: 数据库文件路径
            pool_size: 连接池大小
            timeout: 获取连接超时时间（秒）
        """
        self.database = database
        self.pool_size = pool_size
        self.timeout = timeout

        self.pool: Queue = Queue(maxsize=pool_size)
        self.lock = threading.RLock()

        # 统计信息
        self.created_connections = 0
        self.active_connections = 0
        self.total_queries = 0

        # 预创建连接
        self._initialize_pool()

        Log.Info(f"[DBPool] Initialized for {database}, pool_size={pool_size}")

    def _create_connection(self) -> sqlite3.Connection:
        """创建一个新的数据库连接"""
        try:
            conn = sqlite3.connect(
                self.database,
                check_same_thread=False,  # 允许多线程访问
                isolation_level=None,     # 自动提交模式
                timeout=self.timeout
            )

            # 性能优化配置
            cursor = conn.cursor()

            # WAL模式 - 提升并发性能（可能在某些文件系统上不支持）
            try:
                cursor.execute("PRAGMA journal_mode=WAL")
            except Exception as e:
                Log.Warn(f"[DBPool] WAL mode not supported, using default journal mode: {e}")
                # Fallback to default journal mode

            # 同步模式 - 平衡性能和安全
            try:
                cursor.execute("PRAGMA synchronous=NORMAL")
            except Exception as e:
                Log.Warn(f"[DBPool] Failed to set synchronous mode: {e}")

            # 缓存大小 - 64MB
            try:
                cursor.execute("PRAGMA cache_size=-64000")
            except Exception as e:
                Log.Warn(f"[DBPool] Failed to set cache size: {e}")

            # 临时表存储在内存
            try:
                cursor.execute("PRAGMA temp_store=MEMORY")
            except Exception as e:
                Log.Warn(f"[DBPool] Failed to set temp_store: {e}")

            # 内存映射 - 256MB
            try:
                cursor.execute("PRAGMA mmap_size=268435456")
            except Exception as e:
                Log.Warn(f"[DBPool] Failed to set mmap_size: {e}")

            cursor.close()

            with self.lock:
                self.created_connections += 1

            return conn

        except Exception as e:
            Log.Error(f"[DBPool] Failed to create connection: {e}")
            raise

    def _initialize_pool(self):
        """初始化连接池，预创建连接"""
        for _ in range(self.pool_size):
            try:
                conn = self._create_connection()
                self.pool.put(conn, block=False)
            except Full:
                break
            except Exception as e:
                Log.Error(f"[DBPool] Failed to initialize connection: {e}")

    @contextmanager
    def get_connection(self, timeout: Optional[float] = None):
        """
        获取数据库连接（上下文管理器）

        用法:
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ...")
                result = cursor.fetchall()

        Args:
            timeout: 超时时间，None使用默认

        Yields:
            sqlite3.Connection
        """
        if timeout is None:
            timeout = self.timeout

        conn = None
        try:
            # 尝试从池中获取连接
            try:
                conn = self.pool.get(timeout=timeout)
            except Empty:
                # 池耗尽，创建临时连接
                Log.Warn("[DBPool] Pool exhausted, creating temporary connection")
                conn = self._create_connection()

            with self.lock:
                self.active_connections += 1

            yield conn

        finally:
            # 归还连接
            if conn:
                with self.lock:
                    self.active_connections -= 1

                try:
                    # 如果池未满，归还连接
                    self.pool.put(conn, block=False)
                except Full:
                    # 池已满（临时连接），关闭连接
                    conn.close()

    def execute(self, sql: str, params: Optional[Tuple] = None) -> List[Any]:
        """
        执行SQL查询（快捷方法）

        Args:
            sql: SQL语句
            params: 参数

        Returns:
            查询结果列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)

                with self.lock:
                    self.total_queries += 1

                # 如果是SELECT，返回结果
                if sql.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    return []

            finally:
                cursor.close()

    def executemany(self, sql: str, params_list: List[Tuple]) -> int:
        """
        批量执行SQL（快捷方法）

        Args:
            sql: SQL语句
            params_list: 参数列表

        Returns:
            影响的行数
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            try:
                cursor.executemany(sql, params_list)

                with self.lock:
                    self.total_queries += len(params_list)

                return cursor.rowcount

            finally:
                cursor.close()

    def close_all(self):
        """关闭所有连接"""
        closed = 0

        while not self.pool.empty():
            try:
                conn = self.pool.get(block=False)
                conn.close()
                closed += 1
            except Empty:
                break

        Log.Info(f"[DBPool] Closed {closed} connections")

    def get_stats(self) -> dict:
        """
        获取连接池统计信息

        Returns:
            统计信息字典
        """
        with self.lock:
            return {
                'pool_size': self.pool_size,
                'available': self.pool.qsize(),
                'active': self.active_connections,
                'created': self.created_connections,
                'total_queries': self.total_queries,
            }

    def __del__(self):
        """析构时关闭所有连接"""
        try:
            self.close_all()
        except:
            pass


class CachedQuery:
    """
    带缓存的查询包装器

    使用LRU缓存策略缓存查询结果
    """

    def __init__(self, pool: SQLiteConnectionPool, max_cache_size: int = 1000):
        """
        初始化

        Args:
            pool: 数据库连接池
            max_cache_size: 最大缓存条目数
        """
        self.pool = pool
        self.max_cache_size = max_cache_size

        from collections import OrderedDict
        self.cache = OrderedDict()
        self.lock = threading.RLock()

        # 统计
        self.cache_hits = 0
        self.cache_misses = 0

    def _make_cache_key(self, sql: str, params: Optional[Tuple]) -> str:
        """生成缓存键"""
        if params:
            return f"{sql}|{params}"
        return sql

    def query(self, sql: str, params: Optional[Tuple] = None, use_cache: bool = True) -> List[Any]:
        """
        执行查询（带缓存）

        Args:
            sql: SQL语句
            params: 参数
            use_cache: 是否使用缓存

        Returns:
            查询结果
        """
        if not use_cache:
            return self.pool.execute(sql, params)

        cache_key = self._make_cache_key(sql, params)

        with self.lock:
            # 查缓存
            if cache_key in self.cache:
                # 缓存命中
                self.cache.move_to_end(cache_key)
                self.cache_hits += 1
                return self.cache[cache_key]

            # 缓存未命中
            self.cache_misses += 1

        # 执行查询
        result = self.pool.execute(sql, params)

        with self.lock:
            # 加入缓存
            if len(self.cache) >= self.max_cache_size:
                # 删除最旧的
                self.cache.popitem(last=False)

            self.cache[cache_key] = result

        return result

    def clear_cache(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            Log.Info("[CachedQuery] Cache cleared")

    def get_stats(self) -> dict:
        """获取缓存统计"""
        with self.lock:
            total = self.cache_hits + self.cache_misses
            hit_rate = self.cache_hits / total if total > 0 else 0

            return {
                'cache_size': len(self.cache),
                'max_cache_size': self.max_cache_size,
                'hits': self.cache_hits,
                'misses': self.cache_misses,
                'hit_rate': hit_rate,
            }


# 全局连接池实例（延迟初始化）
_global_pools = {}
_pools_lock = threading.Lock()


def get_connection_pool(database: str, pool_size: int = 5) -> SQLiteConnectionPool:
    """
    获取数据库连接池（单例模式）

    Args:
        database: 数据库路径
        pool_size: 连接池大小

    Returns:
        连接池实例
    """
    global _global_pools

    if database not in _global_pools:
        with _pools_lock:
            if database not in _global_pools:
                _global_pools[database] = SQLiteConnectionPool(database, pool_size)

    return _global_pools[database]
