import math

from PySide6.QtCore import (Qt, QRectF, QSize, QBuffer, QByteArray, QIODevice,
                            QUrl, QObject, QRunnable, QThreadPool, Signal, QTimer,
                            QAbstractAnimation, QVariantAnimation, QEasingCurve,
                            QElapsedTimer, QPointF)
from PySide6.QtGui import (QImageReader, QImage, QPixmap, QPainter, QColor,
                           QTransform, QSurfaceFormat, QPen)

from view.read.read_enum import ReadMode


# ---------------- 平滑滚动器 ----------------
# 说明：QScrollBar 只是输入/显示部件，滚动手感"生硬"来自一次性 setValue 大步长。
# 平滑 = 在 value 写入路径上做缓动插值 + 拖拽惯性，无需替换滚动条。
# 所有位置都走 StripView 的 s 空间接口，因此三种阅读模式通用。

class ReadNewScroller(QObject):
    """平滑滚动手感的全部状态机。三种运动源互斥工作：

    1) 滚轮     -> QVariantAnimation 缓动到目标位置（可叠加/中途变向）
    2) 拖拽     -> 直接跟随鼠标；松手时按最近速度起惯性
    3) 自动滚动 -> 定时器按固定速度匀速前进

    所有位置都用 view 的 s 空间接口（_scroll_min_s/_set_scroll_min_s），
    因此三种阅读模式（含 RTL）无需任何分支处理。
    """

    # ---- 可调参数（手感相关）----
    WHEEL_DURATION = 600     # 滚轮一次缓动的时长上限 ms：距离越远越久，但最多 600ms
    KINETIC_TAU = 240        # 惯性衰减时间常数 ms：速度每过 240ms 衰减到 1/e≈37%，
                             # 数值越大"甩"得越远，越小停得越急
    KINETIC_STOP = 0.02      # 惯性速度低于此值(px/ms)就彻底停止：20px/s，肉眼已看不出动
    FLICK_MIN_V = 0.15       # 松手速度超过此值(px/ms)才算"甩"，才启动惯性；
                             # 慢慢挪开手指时不应有惯性（150px/s 以下）
    SAMPLE_WINDOW = 120      # 松手测速只看最近 120ms 的位移：太长会把早期的快速度
                             # 平均进来，导致轻甩感觉"过冲"
    AUTO_TICK = 15           # 自动滚动的定时器间隔 ms（≈60fps 一帧）
    AUTO_DT_MAX = 0.05       # 单次 tick 的时间上限 s：主线程卡顿后不"补课"跳变

    # ---- 页模式拖拽翻页的手感参数（改这几个值可以调"灵不灵敏"）----
    # 松手后"翻页 vs 弹回"的判定：拖过一定比例 或 甩得够快 -> 翻页；否则弹回原页
    PAGE_COMMIT_FRAC = 0.25  # 拖过屏幕的 25% 就翻页：调小更灵敏（0.1 = 轻轻一拖就翻）
    PAGE_FLICK_V = 0.5       # 甩动速度阈值 px/ms：500px/s 以上即使没拖够距离也翻页
    PAGE_EDGE_RESIST = 0.3   # 首页/末页再往外拖时的橡皮筋阻力系数：0=完全拖不动，
                             # 1=完全跟手（iOS 常用 0.3 左右，手感有"到头了"的反馈）

    def __init__(self, view):
        super().__init__(view)
        self._view = view    # 宿主 StripView（弱约定：scroller 不拥有 view）

        # ---- 滚轮缓动动画 ----
        self._anim = QVariantAnimation(self)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)   # 先快后慢，自然的收尾
        self._anim.valueChanged.connect(self._on_anim_value)
        # 自然结束（非手动 stop）时补齐落点 + 吸附像素，见 _on_anim_finished
        self._anim.finished.connect(self._on_anim_finished)
        self._anim.finished.connect(self._snap_if_idle)   # 自然结束（非手动 stop）后吸附像素
        self._target_s = 0.0    # 动画目标位置。动画进行中再滚滚轮时在它上面累加，
                                # 而不是从当前位置累加（否则连滚会越来越慢）
        self._anim_v_prev = 0.0  # 动画上一帧的插值。每帧按"增量"施加到滚动位置
                                 # （见 _on_anim_value），这样动画途中发生尺寸修正
                                 # 补偿时，补偿量不会被旧轨迹的绝对值抹掉
        self._anim_pos = 0.0     # 动画"意图位置"：自己记账，不从滚动条读回再叠加。
                                 # 滚动条会因亚像素 transform 重算 range 而夹掉个别
                                 # 帧的值，读回叠加会累积成几像素的落点偏差
        self._anim_blocked = False  # True = 正在重配动画，丢弃 Qt 同步发出的杂散 valueChanged
        self._to_end = False    # 动画目标是否为"内容末端"。是的话，滚过去途中
                                # 内容变长（新图修正高度）时终点要跟着走

        # ---- 松手惯性 ----
        # PreciseTimer：默认 CoarseTimer 在 Windows 上按 ~15.6ms 系统节拍对齐，
        # tick 间隔不均匀（15.6/31.2ms 交替），是滚动"粘连感"的元凶之一
        self._kinetic = QTimer(self, interval=16, timerType=Qt.PreciseTimer)
        self._kinetic.timeout.connect(self._kinetic_tick)
        self._vel = 0.0              # 当前惯性速度 px/ms（正值沿阅读方向前进）
        self._kclock = QElapsedTimer()   # 惯性/拖拽共用的计时器：算每帧 dt 用

        # ---- 自动滚动 ----
        self._auto = QTimer(self, interval=self.AUTO_TICK, timerType=Qt.PreciseTimer)
        self._auto.timeout.connect(self._auto_tick)
        self._auto_speed = 0.0     # 速度 px/s（阅读方向）
        self._auto_pos = 0.0       # 浮点累积位置。滚动条只能存整数，直接用滚动条
                                   # 累积会在低速时被截断卡死（50px/s=0.75px/tick），
                                   # 所以自己存浮点，每 tick 再写入滚动条
        self._aclock = QElapsedTimer()   # 自动滚动专用计时器：测每 tick 实际 dt

        # ---- 拖拽 ----
        self._drag_pos = None      # 上次鼠标位置；None = 当前没在拖
        self._samples = []         # [(时刻ms, 位置s)]：拖拽中的轨迹采样，松手时估速度

    # ---- 滚轮：缓动滚动（可叠加/变向） ----

    def scroll_by(self, d_s: float):
        """沿阅读方向滚动 d_s（正=往阅读方向前进）。用于滚轮。
        动画进行中再调用会在目标值上叠加，并从当前位置重新缓动——
        连续滚滚轮 = 目标越来越远但始终平滑追进。"""
        view = self._view
        cur = view._scroll_min_s()
        running = self._anim.state() == QAbstractAnimation.Running
        base = self._target_s if running else cur      # 动画中在目标值上继续叠加
        lo = 0.0
        hi = max(0.0, view._total - view._viewport_len())   # 可滚动区间 [0, total-L]
        target = max(lo, min(hi, base + d_s))               # 钳制在内容范围内
        self._to_end = target >= hi - 0.5              # 目标贴末端则开启末端跟踪
        self._animate_to(cur, target)

    def scroll_to(self, target: float):
        """滚到绝对位置 s=target（自动钳制在内容范围内），带缓动。翻页用：
        页模式的目标都是页边界的整数倍，动画结束天然对齐页边界。"""
        view = self._view
        lo = 0.0
        hi = max(0.0, view._total - view._viewport_len())
        target = max(lo, min(hi, target))
        self._to_end = target >= hi - 0.5
        self._animate_to(view._scroll_min_s(), target)

    def _animate_to(self, cur: float, target: float):
        """启动/重启缓动动画：从 cur 平滑滑到 target。

        重配期间必须屏蔽 valueChanged，原因见 _on_anim_value 的注释：
        Qt 的 stop/setStartValue/setEndValue/start 会同步发出一串新旧轨迹混杂的
        杂散值，接了就会让画面单帧跳一两百像素再倒退（连滚滚轮时尤其明显）。"""
        self._target_s = target
        self._anim_blocked = True
        try:
            self._anim.stop()
            dist = abs(target - cur)
            if dist < 0.5:          # 太近就不动画，直接到位
                self._view._set_scroll_min_s(target)
                return
            # 距离越远时长越久，封顶；连续滚轮叠加时从当前位置重新缓动
            dur = int(min(self.WHEEL_DURATION, 120 + dist))
            self._anim.setStartValue(float(cur))
            self._anim.setEndValue(float(target))
            self._anim.setDuration(max(60, dur))
            self._anim_v_prev = float(cur)      # 增量施加的基准（见 _on_anim_value）
            self._anim_pos = float(cur)         # 意图位置从当前真实位置起算
            self._anim.start()
        finally:
            self._anim_blocked = False

    # ---- 末端跟踪：动画冲向内容末端时，内容变长则终点跟随 ----

    def is_end_tracking(self) -> bool:
        """滚轮动画的目标是内容末端且还在播放？（view 的 rangeChanged 用它
        决定是否要在内容变长时重定向动画终点）"""
        return self._to_end and self._anim.state() == QAbstractAnimation.Running

    def retarget_end(self):
        """内容变长后重新瞄准新的末端（从当前位置重新缓动）。

        注意必须判断"末端真的变了"才重配：滚动时每帧都会改亚像素 transform，
        Qt 因此每帧重算滚动条并 rangeChanged 一次，若不判断就每帧重启缓动，
        动画永远跑不完（越接近末端越慢，像卡住一样爬）。"""
        view = self._view
        hi = max(0.0, view._total - view._viewport_len())
        if abs(hi - self._target_s) < 0.5:      # 终点没动：别重启，让它跑完
            return
        self._animate_to(view._scroll_min_s(), hi)

    def _on_anim_value(self, v):
        """动画每帧回调。关键：按**增量**写入（本帧插值 - 上帧插值），而不是
        把插值当绝对位置直接写。

        为什么：动画播放途中，图片尺寸探测完成会触发 _correct_len 的滚动补偿
        （on_viewport_shifted 已把 _target_s 同步平移）。若按绝对值写，下一帧
        会把滚动位置拽回"补偿前的旧轨迹"——画面瞬间回跳，indexChanged 出现
        1->0->1 的反复（实测序列见 smoke_test_index_stable.py）。
        增量写法则只负责"再往前走多少"，外部补偿自然并入动画轨迹：
        最终落点 = 旧目标 + 补偿量，与 _target_s 的平移恰好一致。

        _anim_blocked：重配动画（stop/setStartValue/setEndValue/start）期间 Qt 会
        **同步**发一串 valueChanged，值是新旧轨迹混杂的（实测同一毫秒内连发
        434 -> 391 -> 180，而新轨迹是 180 -> 600）。绝对值写法只是抖一下，
        增量写法会把它们当真实位移累加 -> 单帧 +211px 再 -43px，滚动"一顿一顿"。
        重配期间一律丢弃，连回来时动画已经在新轨迹上。"""
        if self._anim_blocked:
            return
        nv = float(v)
        self._anim_pos += nv - self._anim_v_prev    # 自己记账：不读回滚动条，避免
        self._anim_v_prev = nv                      # 被夹掉的帧累积成落点偏差
        self._view._set_scroll_min_s(self._anim_pos)

    def _on_anim_finished(self):
        """动画自然跑完：把"还没走完的位移"一次补齐，再吸附像素。

        增量写法下落点 = 已施加位移之和；最后一两帧若没被投递（定时器抖动、
        主线程卡顿）就会差几个像素。这里按 _target_s 补齐尾差，落点与帧投递无关。
        _target_s 已含期间发生的尺寸修正补偿（on_viewport_shifted 同步平移过），
        所以补齐量自动包含补偿。"""
        rest = self._target_s - self._anim_v_prev
        if abs(rest) >= 0.05:
            self._anim_pos += rest
            self._anim_v_prev = self._target_s
            self._view._set_scroll_min_s(self._anim_pos)
        self._snap_if_idle()

    # ---- 拖拽平移 + 松手惯性 ----

    def begin_drag(self):
        """鼠标按下：终止其它一切滚动，开始记录轨迹。"""
        self.stop()
        self._kclock.start()      # 轨迹计时的起点（松手测速要用）
        self._drag_pos = None
        self._samples = []

    def drag_move(self, pos: QPointF):
        """鼠标移动：内容跟手平移，同时记录轨迹采样。"""
        if self._drag_pos is not None:
            dx = pos.x() - self._drag_pos.x()
            dy = pos.y() - self._drag_pos.y()
            d_s = self._drag_delta_s(dx, dy)
            if d_s:
                self._view._scroll_by_s(d_s)
            # zoom>100% 时 cross 轴内容大于视口：拖拽的 cross 分量用来平移
            self._view._pan_cross(dx, dy)
        self._drag_pos = QPointF(pos)
        t = self._kclock.elapsed()
        self._samples.append((t, self._view._scroll_min_s()))
        # 只保留最近 SAMPLE_WINDOW 毫秒的采样（窗口外丢弃）
        while self._samples and t - self._samples[0][0] > self.SAMPLE_WINDOW:
            self._samples.pop(0)

    def end_drag(self):
        """松手：按最近采样估速度，够快就启动惯性。"""
        v = 0.0
        if len(self._samples) >= 2:
            t1, s1 = self._samples[0]
            t2, s2 = self._samples[-1]
            dt = t2 - t1
            if dt > 1:
                v = (s2 - s1) / dt      # px/ms：首尾两个采样的平均速度
        self._drag_pos = None
        self._samples = []
        if abs(v) > self.FLICK_MIN_V:
            self._vel = v
            self._kclock.restart()
            self._kinetic.start()
        else:
            self._snap_if_idle()       # 松手无惯性：直接吸附回整数像素

    def _drag_delta_s(self, dx: float, dy: float) -> float:
        """屏幕位移 -> 阅读方向位移（内容跟随手指）。"""
        m = self._view._mode
        if m == ReadMode.UpDown:
            return -dy
        if ReadMode.isLeftRight(m):
            return -dx
        return dx    # rtl：向右拖露出更左侧（s 更大）的内容

    def _kinetic_tick(self):
        """惯性每帧：位置 += 速度×dt，速度指数衰减，撞边界立即停。"""
        dt = max(1, self._kclock.restart())   # 实测帧间隔 ms（定时器有误差，不能假定 16）
        view = self._view
        lo = 0.0
        hi = max(0.0, view._total - view._viewport_len())
        nxt = view._scroll_min_s() + self._vel * dt
        if nxt <= lo or nxt >= hi:                 # 到边界直接停（不做回弹）
            view._set_scroll_min_s(max(lo, min(hi, nxt)))
            self._kinetic.stop()
            self._snap_if_idle()
            return
        view._set_scroll_min_s(nxt)
        self._vel *= math.exp(-dt / self.KINETIC_TAU)   # 指数衰减：v *= e^(-dt/τ)
        if abs(self._vel) < self.KINETIC_STOP:
            self._kinetic.stop()
            self._snap_if_idle()

    def stop(self):
        """一刀切停掉所有滚动（动画/惯性/自动），拖拽状态也复位。
        用于：用户点击、模式切换等需要立即静止的场景。"""
        self._anim.stop()
        self._kinetic.stop()
        self.stop_auto()
        self._to_end = False
        self._drag_pos = None
        self._samples = []

    # ---- 自动滚动：指定速度匀速前进，点击/滚轮/拖拽/到末端即停 ----

    def start_auto(self, speed: float):
        """speed：px/s（沿阅读方向）。<=0 等同 stop_auto()。"""
        if speed <= 0:
            self.stop_auto()
            return
        self._anim.stop()
        self._kinetic.stop()
        self._auto_speed = float(speed)
        self._auto_pos = self._view._scroll_min_s()
        self._aclock.start()
        self._auto.start()
        self._view.autoScrollChanged.emit(True)

    def stop_auto(self):
        """停止自动滚动（若本来就没开，只做静止吸附检查，不发信号）。"""
        was = self._auto.isActive()
        self._auto.stop()
        self._auto_speed = 0.0
        if was:
            self._view.autoScrollChanged.emit(False)   # 通知 UI 同步复选框
        self._snap_if_idle()

    def is_auto_scrolling(self) -> bool:
        return self._auto.isActive()

    def on_viewport_shifted(self, d_s: float):
        """视口内容被外部整体平移（如尺寸修正的滚动补偿）时同步内部位置。
        否则下个 tick 会把滚动条拉回旧值，表现为内容回跳一下再前进。"""
        if self._drag_pos is not None:
            # 拖拽中：补偿位移不算"手指划出来的"，但已经写进滚动条了，
            # 采样里记录的还是旧值 -> 必须把这 d_s 加到已有采样上，让整条轨迹
            # 回到同一个参考系。否则松手估速会带上这段（可能很大的）补偿量，
            # 惯性朝反方向甩出去 —— 就是"拖着拖着内容回弹/窜回去"的现象。
            self._samples = [(t, s + d_s) for (t, s) in self._samples]
            return
        self._auto_pos += d_s
        self._target_s += d_s
        self._anim_pos += d_s      # 动画的意图位置同步平移（见 _anim_pos 的说明）

    def _snap_if_idle(self):
        """所有运动源都停止后，把渲染位置对齐（连续模式吸附整数像素；
        页模式吸附最近页边界，见 view._snap_rest）。"""
        if (not self._auto.isActive()
                and not self._kinetic.isActive()
                and self._anim.state() != QAbstractAnimation.Running
                and self._drag_pos is None):
            self._view._snap_rest()

    def _auto_tick(self):
        # dt 封顶：主线程一次卡顿（解码/布局）后不一次性补跳 speed*dt，
        # 宁可短暂低于标称速度，也不要"停一下再窜一下"的粘连感
        dt = min(self._aclock.restart() / 1000.0, self.AUTO_DT_MAX)
        view = self._view
        hi = max(0.0, view._total - view._viewport_len())
        self._auto_pos = min(hi, self._auto_pos + self._auto_speed * dt)
        view._set_scroll_min_s(self._auto_pos)
        if self._auto_pos >= hi - 0.01:     # 到内容末端自动停
            self.stop_auto()

