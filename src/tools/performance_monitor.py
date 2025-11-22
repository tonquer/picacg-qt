# -*- coding: utf-8 -*-
"""
性能监控模块
监控应用性能指标，便于优化
"""

import time
import threading
import os
from typing import Dict, List, Optional
from collections import deque

from tools.log import Log

# 可选依赖：psutil（用于系统资源监控）
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    Log.Warn("[PerfMonitor] psutil not installed, system resource monitoring disabled. Install with: pip install psutil")


class PerformanceMonitor:
    """
    性能监控器

    监控指标:
    - 内存使用
    - CPU使用
    - 图片加载时间
    - 缓存命中率
    - 数据库查询时间
    - 网络吞吐量
    """

    def __init__(self, history_size: int = 1000):
        """
        初始化监控器

        Args:
            history_size: 历史数据保留数量
        """
        self.history_size = history_size

        # 性能指标
        self.metrics = {
            'image_load_time': deque(maxlen=history_size),
            'db_query_time': deque(maxlen=history_size),
            'network_requests': deque(maxlen=history_size),
            'cache_operations': deque(maxlen=history_size),
        }

        # 实时指标
        self.counters = {
            'images_loaded': 0,
            'db_queries': 0,
            'network_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
        }

        self.lock = threading.RLock()
        self.start_time = time.time()

        # 进程信息（如果psutil可用）
        self.process = None
        if HAS_PSUTIL:
            try:
                self.process = psutil.Process(os.getpid())
            except Exception as e:
                Log.Warn(f"[PerfMonitor] Failed to initialize psutil Process: {e}")

        Log.Info("[PerfMonitor] Initialized")

    def record_image_load(self, duration_ms: float):
        """记录图片加载时间"""
        with self.lock:
            self.metrics['image_load_time'].append(duration_ms)
            self.counters['images_loaded'] += 1

    def record_db_query(self, duration_ms: float):
        """记录数据库查询时间"""
        with self.lock:
            self.metrics['db_query_time'].append(duration_ms)
            self.counters['db_queries'] += 1

    def record_network_request(self, duration_ms: float, bytes_transferred: int = 0):
        """记录网络请求"""
        with self.lock:
            self.metrics['network_requests'].append({
                'duration': duration_ms,
                'bytes': bytes_transferred,
                'time': time.time(),
            })
            self.counters['network_requests'] += 1

    def record_cache_hit(self):
        """记录缓存命中"""
        with self.lock:
            self.counters['cache_hits'] += 1

    def record_cache_miss(self):
        """记录缓存未命中"""
        with self.lock:
            self.counters['cache_misses'] += 1

    def get_memory_usage(self) -> Dict[str, float]:
        """
        获取内存使用情况

        Returns:
            内存使用字典（MB）
        """
        if not HAS_PSUTIL or not self.process:
            return {'rss_mb': 0, 'vms_mb': 0, 'percent': 0}

        try:
            mem_info = self.process.memory_info()
            mem_percent = self.process.memory_percent()

            return {
                'rss_mb': mem_info.rss / (1024 * 1024),  # 物理内存
                'vms_mb': mem_info.vms / (1024 * 1024),  # 虚拟内存
                'percent': mem_percent,
            }
        except Exception as e:
            Log.Error(f"[PerfMonitor] Failed to get memory usage: {e}")
            return {'rss_mb': 0, 'vms_mb': 0, 'percent': 0}

    def get_cpu_usage(self) -> float:
        """
        获取CPU使用率

        Returns:
            CPU使用率（0-100）
        """
        if not HAS_PSUTIL or not self.process:
            return 0.0

        try:
            return self.process.cpu_percent(interval=0.1)
        except Exception as e:
            Log.Error(f"[PerfMonitor] Failed to get CPU usage: {e}")
            return 0.0

    def get_statistics(self) -> Dict:
        """
        获取统计信息

        Returns:
            完整的统计信息字典
        """
        import statistics

        with self.lock:
            stats = {
                'uptime_seconds': time.time() - self.start_time,
                'counters': dict(self.counters),
                'memory': self.get_memory_usage(),
                'cpu_percent': self.get_cpu_usage(),
            }

            # 计算各指标的统计数据
            for metric_name, values in self.metrics.items():
                if not values:
                    continue

                if metric_name == 'network_requests':
                    # 网络请求特殊处理
                    durations = [v['duration'] for v in values]
                    bytes_list = [v['bytes'] for v in values]

                    stats[metric_name] = {
                        'count': len(values),
                        'avg_duration_ms': statistics.mean(durations) if durations else 0,
                        'total_bytes': sum(bytes_list),
                    }
                else:
                    # 数值型指标
                    values_list = list(values)

                    stats[metric_name] = {
                        'count': len(values_list),
                        'avg': statistics.mean(values_list),
                        'min': min(values_list),
                        'max': max(values_list),
                        'p50': statistics.median(values_list),
                        'p95': statistics.quantiles(values_list, n=20)[18] if len(values_list) > 20 else max(values_list),
                    }

            # 缓存命中率
            total_cache_ops = stats['counters']['cache_hits'] + stats['counters']['cache_misses']
            if total_cache_ops > 0:
                stats['cache_hit_rate'] = stats['counters']['cache_hits'] / total_cache_ops
            else:
                stats['cache_hit_rate'] = 0

            return stats

    def print_report(self):
        """打印性能报告"""
        stats = self.get_statistics()

        print("\n" + "="*60)
        print("性能监控报告".center(60))
        print("="*60)

        # 运行时间
        uptime_mins = stats['uptime_seconds'] / 60
        print(f"\n运行时间: {uptime_mins:.1f} 分钟")

        # 内存和CPU
        print(f"\n资源使用:")
        print(f"  内存: {stats['memory']['rss_mb']:.1f} MB ({stats['memory']['percent']:.1f}%)")
        print(f"  CPU:  {stats['cpu_percent']:.1f}%")

        # 计数器
        print(f"\n操作统计:")
        for key, value in stats['counters'].items():
            print(f"  {key}: {value:,}")

        # 缓存命中率
        print(f"  缓存命中率: {stats['cache_hit_rate']*100:.1f}%")

        # 性能指标
        if 'image_load_time' in stats and stats['image_load_time']['count'] > 0:
            img_stats = stats['image_load_time']
            print(f"\n图片加载:")
            print(f"  平均: {img_stats['avg']:.1f} ms")
            print(f"  中位数: {img_stats['p50']:.1f} ms")
            print(f"  P95: {img_stats['p95']:.1f} ms")

        if 'db_query_time' in stats and stats['db_query_time']['count'] > 0:
            db_stats = stats['db_query_time']
            print(f"\n数据库查询:")
            print(f"  平均: {db_stats['avg']:.1f} ms")
            print(f"  中位数: {db_stats['p50']:.1f} ms")
            print(f"  P95: {db_stats['p95']:.1f} ms")

        if 'network_requests' in stats and stats['network_requests']['count'] > 0:
            net_stats = stats['network_requests']
            print(f"\n网络请求:")
            print(f"  总数: {net_stats['count']}")
            print(f"  平均延迟: {net_stats['avg_duration_ms']:.1f} ms")
            print(f"  总流量: {net_stats['total_bytes'] / (1024*1024):.2f} MB")

        print("\n" + "="*60 + "\n")

    def log_stats(self):
        """输出统计到日志"""
        stats = self.get_statistics()

        Log.Info(
            f"[PerfMonitor] "
            f"mem={stats['memory']['rss_mb']:.0f}MB, "
            f"cpu={stats['cpu_percent']:.1f}%, "
            f"cache_hit={stats['cache_hit_rate']*100:.0f}%, "
            f"images={stats['counters']['images_loaded']}, "
            f"db_queries={stats['counters']['db_queries']}"
        )


class PerformanceTimer:
    """
    性能计时器（上下文管理器）

    用法:
        with PerformanceTimer() as timer:
            # 执行操作
            do_something()

        print(f"耗时: {timer.elapsed_ms} ms")
    """

    def __init__(self, name: str = "", auto_log: bool = False, threshold_ms: float = 100):
        """
        初始化计时器

        Args:
            name: 计时器名称
            auto_log: 是否自动记录到日志
            threshold_ms: 日志阈值（超过此值才记录）
        """
        self.name = name
        self.auto_log = auto_log
        self.threshold_ms = threshold_ms

        self.start_time = 0
        self.end_time = 0
        self.elapsed_ms = 0

    def __enter__(self):
        """进入上下文"""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        self.end_time = time.time()
        self.elapsed_ms = (self.end_time - self.start_time) * 1000

        if self.auto_log and self.elapsed_ms >= self.threshold_ms:
            name_str = f" [{self.name}]" if self.name else ""
            Log.Warn(f"[PerfTimer]{name_str} {self.elapsed_ms:.1f} ms")

        return False  # 不抑制异常


# 全局监控器实例
_global_monitor: Optional[PerformanceMonitor] = None
_monitor_lock = threading.Lock()


def get_performance_monitor() -> PerformanceMonitor:
    """获取全局性能监控器实例（单例）"""
    global _global_monitor

    if _global_monitor is None:
        with _monitor_lock:
            if _global_monitor is None:
                _global_monitor = PerformanceMonitor()

    return _global_monitor
