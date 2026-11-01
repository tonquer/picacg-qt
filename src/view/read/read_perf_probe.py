# -*- coding: utf-8 -*-
"""函数耗时探针：装饰器 / 上下文管理器 / 批量包装类或模块。

四种用法，按侵入性从低到高：

1) 单个函数（改代码）:
       from perf_probe import timed

       @timed                      # 函数名自动作为 label
       def foo(): ...

       @timed(name="解码")          # 自定义 label（⚠️ 多个函数用同一个 name 会合并）
       @timed(log_slow_ms=4)       # 超过 4ms 额外打印一行
       def bar(): ...

2) 一段代码（不动函数）:
       from perf_probe import start, end, time_block

       t = start("render")          # 手动 start/end（可跨函数/回调）
       ...
       end(t)                       # 或 t.stop()；返回 ms

       with time_block("render") as t:   # 上下文管理器
           ...

3) 整个类（不改业务代码，适合 profile 现有项目）:
       from perf_probe import profile_class, report, reset

       reset()
       unpatch = profile_class(StripView, pattern=r"^_")   # 包住所有 _xxx 方法
       ...  # 跑一会儿
       report(sort_by="total")
       unpatch()

4) 模块里的多个普通函数:
       unpatch = profile_functions(globals(), pattern=r"^load_")

关于"只显示第一个"：每个被 @timed 的函数都会在**装饰时登记**。report() 默认只列
调用过的；没被调用的会在末尾提示一行（report(show_uncalled=True) 可把它们也列成
calls=0）。如果两个函数用了同一个 name=，会打印一条 "label 重复" 警告并把它们
合并成一行 —— 给其中一个换个名字即可。

关于"多线程下墙钟不准"：每次计时同时记两个指标：
- **wall**（perf_counter）：墙钟，包含被 OS 抢占、等 GIL、阻塞 I/O 的时间；
- **cpu**（thread_time）：本线程真正在 CPU 上的时间。
report 里的 `wait%` = (wall - cpu) / wall，就是"被切走/在等"的比例。
⚠️ Windows 上 thread_time 的颗粒约 15.6ms，单次短调用可能读到 0；
判断一次 1ms 的调用请用总计/平均值，或者用 py-spy 这类采样器看栈。

说明：
- 计时用 `time.perf_counter()`（单调、纳秒级），单次包装开销约 1~2µs；
- 线程安全（后台解码线程也会进来）；
- 统计的是**包含子调用**的耗时（inclusive）：A 调 B，A 的时间包含 B；
- p50/p95 来自每个函数最近 2000 次样本（内存有界），大量调用时用它们看抖动；
- 不包装 dunder、property、staticmethod、classmethod（需要的话自己用 @timed）。

⚠️ Qt 的 C++ 虚函数（`paint` / `wheelEvent` / `scrollContentsBy` 等）由 Qt 的
vtable 直接调用，**实例属性覆盖无效**；PySide 的虚函数分发也不保证认“类创建后
再替换的方法”。要 profile 这类函数，用子类覆盖后再调 super()，例如：

    class TimedItem(d.StripItem):
        @timed(name="StripItem.paint")
        def paint(self, *a, **k):
            return super().paint(*a, **k)

本工具的 `profile_class` 对**普通 Python 方法**（`_load_visible`、
`_set_scroll_min_s` 这种被 Python 代码调用的）是可靠的。
"""
import functools
import re
import sys
import threading
import time
from collections import deque
from contextlib import contextmanager

_MAX_SAMPLES = 2000          # 每个函数保留的最近样本数（算 p50/p95）

# 每个线程的 CPU 时间。注意：
# - Linux/macOS 上是纳秒级；**Windows 上是 GetThreadTimes，颗粒约 15.6ms**，
#   所以单次短调用可能读到 0 —— 它适合看"总计/大量调用的平均"，
#   不适合判断一次 1ms 调用的精确 CPU。
# - 没有 thread_time 的平台退化成 process_time（全进程，含别的线程）或 None。
_CPU_NOW = getattr(time, "thread_time", None) or getattr(time, "process_time", None)
# thread_time 的颗粒度：Windows 是调度时钟 15.6ms，Linux/macOS 是 ns 级。
# 总耗时不到两个 tick 时，cpu 可能读到 0，wait% 就不可信（显示 --）。
_CPU_GRANULARITY_MS = 15.6 if sys.platform == "win32" else 0.1


def _cpu_now():
    return _CPU_NOW() if _CPU_NOW is not None else None



class _Stats:
    """全局统计表（线程安全）。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}      # name -> {"n","total","max","samples"}
        # 装饰时登记的"函数清单"：label -> 来源(file:line)。reset() 不清，
        # 这样 report() 能列出"已加 @timed 但一次都没被调用"的函数。
        self._registry = {}
        self._called_ever = set()   # 从未被调用过（跨 reset 累计）

    def register(self, name: str, origin: str):
        """登记一个被装饰的函数。返回已存在的来源（重复 label 时非 None）。"""
        with self._lock:
            old = self._registry.get(name)
            if old is not None and old != origin:
                return old
            self._registry[name] = origin
            return None

    def record(self, name: str, wall_ms: float, cpu_ms: float = 0.0):
        with self._lock:
            self._called_ever.add(name)
            d = self._data.get(name)
            if d is None:
                d = self._data[name] = {
                    "n": 0, "total": 0.0, "cpu": 0.0, "max": 0.0,
                    "samples": deque(maxlen=_MAX_SAMPLES),
                }
            d["n"] += 1
            d["total"] += wall_ms
            d["cpu"] += cpu_ms
            if wall_ms > d["max"]:
                d["max"] = wall_ms
            d["samples"].append(wall_ms)

    def reset(self):
        """清空计时数据；保留"已装饰函数"清单（否则没法提示未调用）。"""
        with self._lock:
            self._data.clear()

    def uncalled(self):
        """已装饰但**从未**被调用过的 label（跨 reset 累计）。"""
        with self._lock:
            return sorted(set(self._registry) - self._called_ever)

    def rows(self, include_uncalled=False):
        with self._lock:
            snapshot = {
                name: (d["n"], d["total"], d["cpu"], d["max"], list(d["samples"]))
                for name, d in self._data.items()
            }
            names = set(snapshot)
            if include_uncalled:
                names |= set(self._registry)
        out = []
        for name in names:
            n, total, cpu, mx, samples = snapshot.get(name, (0, 0.0, 0.0, 0.0, []))
            samples.sort()

            def pct(p):
                if not samples:
                    return 0.0
                i = min(len(samples) - 1, max(0, int(round((len(samples) - 1) * p))))
                return samples[i]

            # wait = 墙钟里没跑在本线程 CPU 上的部分（被抢占 / 等 GIL / 阻塞 I/O）。
            # CPU 指标是否可信：平均单次调用必须 >= 一个 tick（Windows 15.6ms）。
            # 短调用会把 tick 落到调用之间的空隙里，cpu 读成 0 或某个调用"吞掉"
            # 一整个 tick —— 这时 cpu / wait% 都没意义，显示 --。
            wait = max(0.0, total - cpu)
            avg = total / n if n else 0.0
            reliable = avg >= _CPU_GRANULARITY_MS
            out.append({
                "name": name, "calls": n,
                "total": total, "avg": avg,
                "p50": pct(0.50), "p95": pct(0.95), "max": mx,
                "cpu_total": cpu,
                "cpu": (cpu / n) if (n and reliable) else None,
                "wait_pct": (wait / total * 100.0) if reliable else None,
            })
        return out


STATS = _Stats()


# ---------------- 1) 装饰器 ----------------

_WARNED = set()


def _origin(f) -> str:
    """函数来源（文件名:行号），用于发现重复 label。"""
    code = getattr(f, "__code__", None)
    if code is not None:
        path = code.co_filename.replace("\\", "/").rsplit("/", 1)[-1]
        return f"{path}:{code.co_firstlineno}"
    return getattr(f, "__qualname__", "?")


def timed(fn=None, *, name=None, log_slow_ms=0.0):
    """给函数/方法加计时。可裸用 `@timed`，也可 `@timed(name=..., log_slow_ms=...)`。

    每个被装饰的函数都会在装饰时登记（即使一次都没调用，report 也能看到）。
    """
    def deco(f):
        if getattr(f, "__perf_wrapped__", False):
            return f                      # 避免重复包装（同一函数叠了多个 @timed）
        label = name or f"{getattr(f, '__module__', '')}.{getattr(f, '__qualname__', f)}"
        origin = _origin(f)
        dup = STATS.register(label, origin)
        if dup is not None:
            key = (label, origin, dup)
            if key not in _WARNED:        # 只提示一次，别刷屏
                _WARNED.add(key)
                print(f"[perf_probe] label 重复: {label!r} 已被 {dup} 使用，"
                      f"现在又被 {origin} 使用 —— 它们会合并成一行。"
                      f"给其中一个加 @timed(name='...') 区分。")

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            c0 = _cpu_now()
            try:
                return f(*args, **kwargs)
            finally:
                wall = (time.perf_counter() - t0) * 1000.0
                cpu = ((_cpu_now() - c0) * 1000.0
                       if c0 is not None else 0.0)
                STATS.record(label, wall, cpu)
                if log_slow_ms and wall >= log_slow_ms:
                    print(f"[slow] {label} wall={wall:.2f} ms "
                          f"cpu={cpu:.2f} ms（差值是抢占/GIL/IO）")

        wrapper.__perf_wrapped__ = True
        return wrapper

    return deco(fn) if fn is not None else deco


# ---------------- 2) 手动 start/end + 上下文管理器 ----------------

class Timer:
    """手动计时器：`start()` / `stop()`（别名 `end()`）可以跨函数、跨回调使用。

    三种写法都支持：

        # a) 显式 start/end（开始和结束不在同一处时最有用）
        t = Timer("decode")
        t.start()
        ...
        t.stop()                 # 记录一次；返回耗时 ms

        # b) 模块级快捷方式
        t = start("decode")
        ...
        end(t)

        # c) 上下文管理器
        with Timer("render") as t:
            ...
        print(t.elapsed_ms())

    同一个 Timer 可以反复 start/stop（每次 stop 记一个样本）。
    重复 start 未 stop 会丢掉上一段（不会重复计时）。
    """

    def __init__(self, name: str, *, log_slow_ms: float = 0.0):
        self.name = name
        self._t0 = None
        self._c0 = None
        self._log_slow_ms = log_slow_ms
        self._last = 0.0
        self._last_cpu = 0.0

    def start(self) -> "Timer":
        self._t0 = time.perf_counter()
        self._c0 = _cpu_now()
        return self

    def pref(self, label) -> float:
        """不结束打印中间一次，返回**墙钟**耗时（ms）。没 start 过则返回 0、不记录。"""
        if self._t0 is None:
            return 0.0
        wall = (time.perf_counter() - self._t0) * 1000.0
        cpu = ((_cpu_now() - self._c0) * 1000.0
               if self._c0 is not None else 0.0)
        self._last = wall
        self._last_cpu = cpu
        if self._log_slow_ms and wall >= self._log_slow_ms:
            print(f"[slow] {self.name} {label} wall={wall:.2f} ms cpu={cpu:.2f} ms")
        return wall

    def stop(self) -> float:
        """结束并记录一次，返回**墙钟**耗时（ms）。没 start 过则返回 0、不记录。"""
        if self._t0 is None:
            return 0.0
        wall = (time.perf_counter() - self._t0) * 1000.0
        cpu = ((_cpu_now() - self._c0) * 1000.0
               if self._c0 is not None else 0.0)
        self._t0 = None
        self._c0 = None
        self._last = wall
        self._last_cpu = cpu
        STATS.record(self.name, wall, cpu)
        if self._log_slow_ms and wall >= self._log_slow_ms:
            print(f"[slow] {self.name} wall={wall:.2f} ms cpu={cpu:.2f} ms")
        return wall

    end = stop                     # 别名：t.end() 和 t.stop() 等价

    def elapsed_ms(self) -> float:
        """当前墙钟耗时：运行中返回"已过多久"，已停返回"上次的墙钟耗时"。"""
        if self._t0 is None:
            return self._last
        return (time.perf_counter() - self._t0) * 1000.0

    def cpu_ms(self) -> float:
        """当前线程的 CPU 耗时。运行中返回已用的 CPU，已停返回上次的。

        ⚠️ Windows 上颗粒约 15.6ms，短调用可能读到 0；看总计/平均更可靠。
        """
        if self._t0 is None or self._c0 is None:
            return self._last_cpu
        c = _cpu_now()
        return (c - self._c0) * 1000.0 if c is not None else 0.0

    def wait_ms(self) -> float:
        """墙钟 - CPU = 没跑在本线程上的时间（抢占 / 等 GIL / 阻塞 I/O）。"""
        return max(0.0, self.elapsed_ms() - self.cpu_ms())

    def __enter__(self) -> "Timer":
        return self.start()

    def __exit__(self, exc_type, exc, tb):
        self.stop()
        return False               # 不吞异常


def start(name: str, *, log_slow_ms: float = 0.0) -> Timer:
    """开始手动计时，返回 Timer。用 `end(t)` 或 `t.stop()` 结束。

    适合"开始和结束不在同一个函数/回调里"的场景（网络请求、动画、事件）。
    """
    return Timer(name, log_slow_ms=log_slow_ms).start()


def end(timer: Timer) -> float:
    """结束 `start()` 返回的计时器并记录一次，返回耗时（ms）。"""
    return timer.stop()


@contextmanager
def time_block(name: str):
    """with time_block("render"): ... —— 统计这一段代码的耗时（yield 出 Timer）。"""
    t = Timer(name).start()
    try:
        yield t
    finally:
        t.stop()


# ---------------- 3) 批量包装类方法 ----------------

def profile_class(cls, *, include=None, exclude=None, pattern=None):
    """把 cls 上的普通方法批量替换成计时包装，返回 unpatch()。

    include: 只包这些名字（集合）
    exclude: 不包这些名字（集合）
    pattern: 正则，匹配方法名（如 r"^_" 只包私有方法）
    三者都不给 = 包住类里所有普通方法（跳过 dunder/property/static/classmethod）。
    """
    saved = {}
    rx = re.compile(pattern) if pattern else None
    for name, attr in list(vars(cls).items()):
        if not callable(attr):
            continue
        if isinstance(attr, (staticmethod, classmethod, property)):
            continue
        if name.startswith("__") and name.endswith("__"):
            continue
        if include is not None and name not in include:
            continue
        if exclude is not None and name in exclude:
            continue
        if rx is not None and not rx.search(name):
            continue
        saved[name] = attr
        setattr(cls, name, timed(attr, name=f"{cls.__name__}.{name}"))

    def unpatch():
        for name, orig in saved.items():
            setattr(cls, name, orig)
        saved.clear()

    return unpatch


def profile_functions(namespace, *, names=None, pattern=None, only_module=None):
    """给模块/字典里的多个**普通函数**批量加计时，返回 unpatch()。

    namespace: 传 `globals()` 或模块的 `__dict__`
    names:     只包这些名字（集合）
    pattern:   正则匹配函数名
    only_module: 只包 `__module__` 等于它的函数；默认取 `namespace["__name__"]`，
                 避免把 `from xxx import func` 进来的函数也包上。

    例：unpatch = profile_functions(globals(), pattern=r"^load_")
    """
    import inspect

    saved = {}
    rx = re.compile(pattern) if pattern else None
    mod = only_module if only_module is not None else namespace.get("__name__")
    for name, obj in list(namespace.items()):
        if not inspect.isfunction(obj):
            continue
        if mod is not None and getattr(obj, "__module__", None) != mod:
            continue
        if names is not None and name not in names:
            continue
        if rx is not None and not rx.search(name):
            continue
        saved[name] = obj
        namespace[name] = timed(obj, name=name)

    def unpatch():
        for name, orig in saved.items():
            namespace[name] = orig
        saved.clear()

    return unpatch


# ---------------- 报告 ----------------

def report(sort_by: str = "total", top: int = None, min_calls: int = 1,
           show_uncalled: bool = False):
    """打印统计表。

    sort_by: total / avg / p95 / max / calls / cpu / wait_pct
    min_calls: 只显示调用次数 >= 它的函数（默认 1，排除没跑过的）
    show_uncalled: True = 把"加了 @timed 但一次都没调用"的函数也列出来（calls=0）

    列说明：
      total/avg/p50/p95/max = **墙钟**（perf_counter），多线程下包含被抢占/等 GIL/IO；
      cpu                   = 本线程 **CPU** 平均值（thread_time，Windows 颗粒 ~15.6ms）；
      wait%                 = 墙钟里没跑在本线程 CPU 上的比例（抢占/GIL/阻塞 I/O）。
    """
    rows = STATS.rows(include_uncalled=show_uncalled)
    if show_uncalled:
        min_calls = 0          # 未调用的行 calls=0，不能被默认的 1 过滤掉
    rows = [r for r in rows if r["calls"] >= min_calls]
    rows.sort(key=lambda r: r[sort_by], reverse=True)
    if top:
        rows = rows[:top]
    if not rows:
        print("（没有样本）")
    else:
        print(f"{'function':40} {'calls':>7} {'total ms':>10} {'avg':>8} "
              f"{'p50':>8} {'p95':>8} {'max':>8} {'cpu':>8} {'wait%':>7}")
        print("-" * 112)
        for r in rows:
            cpu_txt = (f"{r['cpu']:8.3f}" if r["cpu"] is not None else "      --")
            wait_txt = (f"{r['wait_pct']:6.1f}%"
                        if r["wait_pct"] is not None else "     --")
            print(f"{r['name']:40} {r['calls']:7d} {r['total']:10.2f} {r['avg']:8.3f} "
                  f"{r['p50']:8.3f} {r['p95']:8.3f} {r['max']:8.3f} "
                  f"{cpu_txt:>8} {wait_txt:>7}")
    # 提示"已装饰但从未被调用"的函数：这才是"只显示第一个"的常见原因
    missing = STATS.uncalled()
    if missing and not show_uncalled:
        print(f"\n（另有 {len(missing)} 个已加 @timed 但**从未被调用过**："
              f"{', '.join(missing[:8])}{' …' if len(missing) > 8 else ''}）"
              f"\n  想看它们：report(show_uncalled=True)，或检查调用路径。")


def reset():
    """清空计时数据（保留已装饰函数清单）。"""
    STATS.reset()
