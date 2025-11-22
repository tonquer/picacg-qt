# -*- coding: utf-8 -*-
"""
图片内存缓存模块
实现LRU缓存策略，显著提升图片加载性能
"""

import os
import threading
import time
from collections import OrderedDict
from typing import Optional, Tuple
from tools.log import Log


class ImageMemoryCache:
    """
    图片内存LRU缓存

    特性:
    - LRU淘汰策略（最近最少使用）
    - 线程安全
    - 自动内存管理
    - 统计信息（命中率等）
    """

    def __init__(self, max_size_mb: int = 512, max_entries: int = 1000):
        """
        初始化缓存

        Args:
            max_size_mb: 最大缓存大小（MB）
            max_entries: 最大缓存条目数
        """
        self.max_size = max_size_mb * 1024 * 1024  # 转换为字节
        self.max_entries = max_entries
        self.current_size = 0
        self.cache = OrderedDict()  # 保持插入顺序，用于LRU
        self.lock = threading.RLock()  # 可重入锁，支持递归调用

        # 统计信息
        self.hits = 0
        self.misses = 0
        self.evictions = 0

        Log.Info(f"[ImageCache] Initialized with max_size={max_size_mb}MB, max_entries={max_entries}")

    def get(self, key: str) -> Optional[bytes]:
        """
        获取缓存数据

        Args:
            key: 缓存键（通常是文件路径）

        Returns:
            缓存的图片数据，未命中返回None
        """
        with self.lock:
            if key in self.cache:
                # 命中：移到末尾（标记为最近使用）
                self.cache.move_to_end(key)
                self.hits += 1

                data, _ = self.cache[key]

                # 每1000次访问输出一次统计
                if (self.hits + self.misses) % 1000 == 0:
                    self._log_stats()

                return data
            else:
                self.misses += 1
                return None

    def put(self, key: str, data: bytes) -> bool:
        """
        添加数据到缓存

        Args:
            key: 缓存键
            data: 图片数据

        Returns:
            是否成功添加
        """
        if not data:
            return False

        data_size = len(data)

        # 单个文件超过最大缓存大小的10%，不缓存
        if data_size > self.max_size * 0.1:
            Log.Warn(f"[ImageCache] File too large to cache: {key}, size={data_size/1024/1024:.2f}MB")
            return False

        with self.lock:
            # 如果key已存在，先删除旧数据
            if key in self.cache:
                old_data, old_size = self.cache[key]
                self.current_size -= old_size
                del self.cache[key]

            # 驱逐旧数据直到有足够空间
            while (self.current_size + data_size > self.max_size or
                   len(self.cache) >= self.max_entries) and self.cache:
                self._evict_one()

            # 添加新数据
            self.cache[key] = (data, data_size)
            self.current_size += data_size

            return True

    def _evict_one(self):
        """驱逐一个最旧的条目（LRU）"""
        if not self.cache:
            return

        # popitem(last=False) 删除最先插入的项（FIFO/LRU）
        old_key, (old_data, old_size) = self.cache.popitem(last=False)
        self.current_size -= old_size
        self.evictions += 1

        # 每驱逐100次输出一次日志
        if self.evictions % 100 == 0:
            Log.Debug(f"[ImageCache] Evicted: {old_key}, size={old_size/1024:.2f}KB, total_evictions={self.evictions}")

    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.current_size = 0
            Log.Info("[ImageCache] Cache cleared")

    def clear_old_entries(self, keep_ratio: float = 0.5):
        """
        清理旧条目，保留指定比例的最新条目

        Args:
            keep_ratio: 保留比例（0.0-1.0）
        """
        with self.lock:
            keep_count = int(len(self.cache) * keep_ratio)

            # 删除旧条目
            while len(self.cache) > keep_count:
                self._evict_one()

            Log.Info(f"[ImageCache] Cleared old entries, kept {keep_count}/{len(self.cache)} entries")

    def get_stats(self) -> dict:
        """
        获取缓存统计信息

        Returns:
            统计信息字典
        """
        with self.lock:
            total_requests = self.hits + self.misses
            hit_rate = self.hits / total_requests if total_requests > 0 else 0

            return {
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': hit_rate,
                'evictions': self.evictions,
                'entries': len(self.cache),
                'size_mb': self.current_size / (1024 * 1024),
                'max_size_mb': self.max_size / (1024 * 1024),
                'usage_percent': (self.current_size / self.max_size * 100) if self.max_size > 0 else 0,
            }

    def _log_stats(self):
        """输出统计信息到日志"""
        stats = self.get_stats()
        Log.Info(
            f"[ImageCache] Stats: "
            f"hit_rate={stats['hit_rate']*100:.1f}%, "
            f"entries={stats['entries']}, "
            f"size={stats['size_mb']:.1f}MB/{stats['max_size_mb']:.0f}MB "
            f"({stats['usage_percent']:.1f}%), "
            f"evictions={stats['evictions']}"
        )

    def resize(self, new_max_size_mb: int):
        """
        调整缓存大小

        Args:
            new_max_size_mb: 新的最大缓存大小（MB）
        """
        with self.lock:
            old_max = self.max_size / (1024 * 1024)
            self.max_size = new_max_size_mb * 1024 * 1024

            # 如果缩小，驱逐超出部分
            while self.current_size > self.max_size and self.cache:
                self._evict_one()

            Log.Info(f"[ImageCache] Resized from {old_max:.0f}MB to {new_max_size_mb}MB")


class ScaledImageCache:
    """
    缩放图片缓存
    缓存不同尺寸的缩放后图片，避免重复缩放
    """

    def __init__(self, max_entries: int = 200):
        """
        初始化缩放图片缓存

        Args:
            max_entries: 最大缓存条目数
        """
        self.max_entries = max_entries
        self.cache = OrderedDict()
        self.lock = threading.RLock()

        Log.Info(f"[ScaledImageCache] Initialized with max_entries={max_entries}")

    def get_key(self, path: str, width: int, height: int) -> str:
        """生成缓存键"""
        return f"{path}_{width}x{height}"

    def get(self, path: str, width: int, height: int):
        """获取缓存的缩放图片"""
        key = self.get_key(path, width, height)

        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            return None

    def put(self, path: str, width: int, height: int, qimage):
        """缓存缩放后的图片"""
        key = self.get_key(path, width, height)

        with self.lock:
            # 如果超过最大条目数，删除最旧的
            if len(self.cache) >= self.max_entries:
                self.cache.popitem(last=False)

            self.cache[key] = qimage

    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            Log.Info("[ScaledImageCache] Cache cleared")


# 全局单例缓存实例
_global_image_cache: Optional[ImageMemoryCache] = None
_global_scaled_cache: Optional[ScaledImageCache] = None
_cache_lock = threading.Lock()


def get_image_cache() -> ImageMemoryCache:
    """获取全局图片缓存实例（单例模式）"""
    global _global_image_cache

    if _global_image_cache is None:
        with _cache_lock:
            if _global_image_cache is None:
                # 默认512MB缓存，1000个条目
                from config.setting import Setting

                # 可以从配置读取，默认512MB
                max_size_mb = getattr(Setting, 'ImageCacheSize', None)
                if max_size_mb is None:
                    max_size_mb = 512
                else:
                    max_size_mb = max_size_mb.value if hasattr(max_size_mb, 'value') else 512

                _global_image_cache = ImageMemoryCache(
                    max_size_mb=max_size_mb,
                    max_entries=1000
                )

    return _global_image_cache


def get_scaled_cache() -> ScaledImageCache:
    """获取全局缩放图片缓存实例（单例模式）"""
    global _global_scaled_cache

    if _global_scaled_cache is None:
        with _cache_lock:
            if _global_scaled_cache is None:
                _global_scaled_cache = ScaledImageCache(max_entries=200)

    return _global_scaled_cache
