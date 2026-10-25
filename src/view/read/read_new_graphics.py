from __future__ import annotations

import bisect
from typing import TYPE_CHECKING

from qt_owner import QtOwner
from task.task_download import FileData

if TYPE_CHECKING:
    from view.read.read_new_view import ReadNewView
    from view.read.read_new_task import ReadNewTask
    from view.read.read_new_frame import ReadNewFrame
    from view.read.read_new_tool import ReadNewTool

import math
from tools.log import Log
from tools.tool import ToolUtil, time_me
from view.read.read_new_pool import ReadNewPoolManager
from PySide6.QtCore import (Qt, QRectF, QSize, QBuffer, QByteArray, QIODevice,
                            QUrl, QObject, QRunnable, QThreadPool, Signal, QTimer,
                            QAbstractAnimation, QVariantAnimation, QEasingCurve,
                            QElapsedTimer, QPointF, QEvent, QPoint, QSizeF)
from PySide6.QtGui import (QImageReader, QImage, QPixmap, QPainter, QColor,
                           QTransform, QSurfaceFormat, QPen, QPalette, QMovie)
# 注意：PySide6 里 QOpenGLWidget 在独立的 QtOpenGLWidgets 模块（不在 QtWidgets）
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                               QGraphicsItem, QStyleOptionGraphicsItem,
                               QWidget, QVBoxLayout, QHBoxLayout,
                               QComboBox, QCheckBox, QSpinBox,
                               QPushButton, QLabel)

from config.setting import Setting
from view.read.read_enum import ReadMode, QtFileData
from view.read.read_new_graphics_item import ReadNewGraphicsItem
from view.read.read_new_scroller import ReadNewScroller
from tools.str import Str


class ReadNewGraphics(QGraphicsView):
    # 单张图沿滚动轴的长宽比上限（len/cross ≤ 4）。防止极端长图（如 1:20 的长条图）
    # 占满好几屏、把布局拉得没法看；超长图会被等比压缩到这个比例。
    MAX_ASPECT = 4.0

    # ---- 缩放（Ctrl+滚轮 / 工具栏按钮 / Ctrl+= - 0）----
    MIN_ZOOM = 0.2  # 缩放下限（20%）：太小已经看不清内容了
    MAX_ZOOM = 5.0  # 缩放上限（500%）：再大受限于原图分辨率，全是马赛克
    ZOOM_STEP = 1.25  # 一次滚轮格/按钮步进的倍率（1.25^n 的等比数列手感均匀）

    # 不确定态进度环的旋转相位（0~1，1 = 转满一圈）。模块级全局：所有 item 共享
    # 同一个相位即可（它们本来就应该同步转动），由 StripView._spin_timer 推进。
    SPIN_PHASE = 0.0

    # ---- 动图（GIF / 动画 WebP）----
    # 同时存在的 QMovie 个数上限。QMovie 默认 CacheAll（解码过的帧全缓存，回放才不卡），
    # 但一个大 GIF 缓存几十 MB 很常见；一屏也就 1~3 张，保持少量即可，更远的用 LRU
    # 回收成静态海报帧。
    ANIM_MAX_MOVIES = 8
    # 保留原始压缩数据的总预算（MB）。动画角色的 QMovie 被回收后要靠它重建，
    # 超预算就把最久没播的那张的原始字节也丢掉（之后只能停在海报帧）
    ANIM_MAX_RAW_MB = 64

    # 首屏/跳转校准期的超时保护：校准期里"当前序号 != 目标"会被压住不发信号
    # （避免中间态闪烁），连续这么多次数都对不上就认命，把真实序号发出去——
    # 否则目标图加载失败时 UI 上的页码会一直停在跳转前的旧值上。
    HOLD_MAX_MISS = 60

    # PREFETCH_BACK = 3  # 已读方向（往回）预取几张
    # PREFETCH_AHEAD = 12  # 未读方向（往后）预取几张

    PIXMAP_BUDGET_MB = 2048    # 已解码位图的总预算（MB）
    # RAW_BUDGET_MB = 64        # 保留的原始压缩字节总预算（MB），用于位图回收后重解

    # ---- 到顶/到底后的"继续滚"触发 ----
    # 已经在最前/最后，还继续往外滚这么多下就发 scrolledPastStart / scrolledPastEnd。
    # 用来接"上/下一章"之类的逻辑（本 Demo 不消费，只发信号）。
    EDGE_SCROLL_TRIGGER = 3

    """三种阅读方向共用的图片流视图。

    布局模型（详见模块注释的变量速查）：
    - 所有 item 沿"阅读顺序坐标 s"排成一条带子；
    - 每张图沿滚动轴的长度由已知尺寸决定（未知时先按兜底宽高比占位，
      探测到真实尺寸后修正——修正时平移后续内容并补偿滚动位置，不跳动）；
    - sceneRect 手动维护（不让 Qt 自动扩展，否则滚动位置会被重算）。
    """

    autoScrollChanged = Signal(bool)   # 自动滚动开/关（点击停止时也会发 False）
    zoomChanged = Signal(float)        # 缩放比变化（UI 上的百分比标签用它同步）
    indexChanged = Signal(int)         # 阅读位置所在的图序号变了（0 起；-1=还没有图）。
                                       # 只在真的跨越到另一张图时发一次，滚动过程中
                                       # 不会每帧都发——可以直接拿它刷新"第 N/M 张"标签
    # ---- "到顶/到底后再往外滚 N 下"的信号（用来接上/下一章之类的逻辑）----
    # 已经在最前（第一张/第一页）还继续往回滚，连续 N 下 -> scrolledPastStart
    # 已经在最后（最后一张/最后一页）还继续往后滚，连续 N 下 -> scrolledPastEnd
    # N 由 set_edge_scroll_trigger() 设置（默认 EDGE_SCROLL_TRIGGER = 3）。
    # 触发后计数自动清零；滚回内容内部、跳转、切模式也会清零。
    scrolledPastStart = Signal()
    scrolledPastEnd = Signal()

    def __init__(self, mode: ReadMode = ReadMode.UpDown, parent=None):
        """mode：阅读方向，ReadMode.UpDown / MODE_LTR / MODE_RTL，可运行时 set_mode 切换。
        gap：相邻图片间距（逻辑像素）。默认 0 = 无缝拼接。
        无缝的关键除了 gap=0，还有 _snap_px 的设备像素对齐（见下）。
        opengl：是否用 GPU 渲染（视口换 QOpenGLWidget）。也可运行时
        set_opengl() 切换；创建多个 view 时记得先设
        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)。"""
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        # 缩放绘制时用平滑插值（没有它缩小后的图全是锯齿）
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        # 两个渲染优化：抗锯齿区域不重算 / 不每次保存恢复 painter 状态。
        # 只画纯图片（无逐像素抗锯齿的图元）时安全且更快
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        # 只重绘脏区域而不是整个视口（滚动时只画新露出来的条）
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        # 背景必须设给 scene（不是 viewport）：QGraphicsView 每次重绘都会用
        # scene 的 backgroundBrush 铺满暴露区域，而 widget 自己的填充
        # （viewport 的 autoFillBackground）在 QOpenGLWidget 视口上不起作用——
        # GL 每帧是 glClear 到透明黑，看过去就是"空白区发黑 / 上一帧残留"。
        self._scene.setBackgroundBrush(self._default_bg())
        # 预下载范围：以当前页 _cur_idx 为基准，往前/往后各几张（与视窗大小无关）
        # self._prefetch_back = self.PREFETCH_BACK
        # self._prefetch_ahead = self.PREFETCH_AHEAD
        # 到顶/到底后"再滚 N 下"触发 scrolledPastStart / scrolledPastEnd
        self._edge_scroll_trigger = max(0, int(self.EDGE_SCROLL_TRIGGER))
        self._edge_start = 0          # 已到最前、连续往外滚的次数
        self._edge_end = 0            # 已到最后、连续往外滚的次数
        # 滚动节流：上次跑 _load_visible 时的滚动位置。scrollContentsBy 每帧可能
        # 被触发多次（平滑滚动/range 重夹），位移不到 0.5px 就没必要重算窗口。
        self._last_load_s = float("nan")
        # 连续模式相邻两张的绘制叠加量（逻辑像素）：盖住 1px 白缝，见 SEAM_OVERLAP
        self._seam_overlap = float(ReadNewGraphicsItem.SEAM_OVERLAP)
        # 窗口 resize 会连发很多次：等它停下来再统一重解一次。放大要重下、
        # 缩小要从保留的压缩字节缩回去（否则绘制一直走缩放慢路径）。
        self._resize_refresh = QTimer(self)
        self._resize_refresh.setSingleShot(True)
        self._resize_refresh.setInterval(180)
        self._resize_refresh.timeout.connect(self._refresh_decodes)

        self._items : list[ReadNewGraphicsItem] = []   # ReadNewGraphicsItem 列表，按阅读顺序排列
        self._mode = mode                         # 当前阅读方向
        self._is_cover_mode = False
        self._gap = 0             # 相邻图片间距
        self._zoom = 1.0          # 当前显示缩放比（1.0=适配；连续模式影响 cross，
                                   # 页模式是 item 的 scale 变换，见 set_zoom）
        self._cross = 400.0      # 垂直于滚动轴的固定尺寸（ttb=统一宽度，横排=统一高度），
                                 # 初始占位值，showEvent/resizeEvent 时按视口重算
        self._total = 0.0        # 内容总长（s 空间）= 所有图长 + 间距之和
        self._was_at_end = False     # 上次滚动时是否贴着内容末端（贴端锚点用）
        self._anchoring = False  # 首次显示后才启用贴端锚点（避免初始跳到底部）
        self._first_show = True  # 是否还没首次显示过：只有首次才定位到第一张图。
                                 # showEvent 在"最小化后恢复""切回标签页"等场景
                                 # 也会触发，不能每次都把阅读位置重置回开头

        # ---- 首屏起点：首次显示时定位到第几张图 ----
        self._initial_idx = 0    # 目标序号（0 起）。None = 未指定（等同 0）
        self._initial_hold = False   # 是否还在"按在首屏目标上"阶段，见
                                     # _align_initial_target：目标图尺寸还是占位值
                                     # 时它的 _s 是估算的，每次尺寸修正都要重对齐
        self._hold_miss = 0          # 校准期里"当前序号 != 目标"的次数（见
                                     # _refresh_index）：超过上限就强制结束校准，
                                     # 免得 UI 上的页码一直停在跳转前的旧值

        self._aligning_target = False  # 重入保护：_align_initial_target 里改滚动条 /
                                       # transform 会（在 OpenGL/高分屏下同步）触发
                                       # rangeChanged -> _on_range_changed -> 再次对齐，
                                       # 形成无限递归，见 _align_initial_target 的说明
        self._pending_scroll_s = None  # 模式切换期间的待定滚动位置：
                                       # 切换后滚动条 range 异步更新，期间每次 range
                                       # 变化都把位置按回这个值，防止跳到别处
        self._sub = 0.0          # 亚像素偏移 [0,1)：滚动条只走整数，小数部分由视图 transform 承载
        self._sub_applied = 0.0  # 已应用到 transform 的偏移（去重，避免无谓的全量重绘）
        self._cur_idx = -1       # 上次发出的"当前是第几张图"（indexChanged 去重；-1=还没有图）

        # 滚动条范围变化 = 内容变长/变短（图片修正、追加、模式切换），
        # 统一在这里处理"末端跟踪/贴端/按住待定位置"
        self.verticalScrollBar().rangeChanged.connect(self._on_range_changed)
        self.horizontalScrollBar().rangeChanged.connect(self._on_range_changed)
        self._apply_policies()

        self._scroller = ReadNewScroller(self)   # 平滑滚动状态机（滚轮/拖拽/自动）
        self._dragging = False                  # 当前是否处于鼠标拖拽平移状态（连续模式）
        self._opengl = False                    # 当前是否用 QOpenGLWidget 视口
        self._openglWidget = None

        # ---- 动图（GIF / 动画 WebP）----
        self._anims = []             # 已确认是动图的 item（无论当前有没有 QMovie）
        self._anim_seq = 0           # 递增的时间戳：标记"最近一次该播放"，LRU 回收用
        self._anims_enabled = True   # 是否播放动画（可运行时关，省 CPU/电）

        # 不确定态进度环（总大小未知时转圈）的动画定时器。按需启停：没有
        # "未知总大小且正在下载"的 item 时就停掉，避免常驻定时器空转
        self._spin_timer = QTimer(self)
        self._spin_timer.setInterval(ReadNewGraphicsItem.SPIN_INTERVAL)
        self._spin_timer.timeout.connect(self._on_spin)

        # ---- 页模式（单页/双页）状态：翻页器，完全没有滚动 ----
        self._page = 0                          # 当前页码（0 起）
        self._page_anim = QVariantAnimation(self)   # 翻页/弹回的滑动动画
        self._page_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._page_anim.setDuration(220)
        self._page_anim.valueChanged.connect(self._on_page_anim_value)
        self._page_anim.finished.connect(self._on_page_anim_finished)
        self._page_anim_mode = None             # None / "slide"：滑动动画是否在跑
        self._page_anim_from = 0.0              # 偏移动画起点（当前页偏移，单位 px）
        self._page_anim_to = 0.0                # 终点（0=弹回原页，±L=完成翻页）
        self._page_anim_shift = 0               # 动画结束后 self._page 的平移量
        self._page_anim_nb = None               # 动画期间同屏滑动的邻页页码
        self._page_anim_nb_delta = 0.0          # 邻页相对当前页偏移的附加量（±L）
        # 拖拽翻页：把邻页拖出来，松手按"位移/速度"判定翻页或弹回
        self._page_dragging = False
        self._page_drag_start = None            # 拖拽起点 QPointF
        self._page_drag_offset = 0.0            # 沿阅读方向的拖拽偏移（>0=往后拖）
        self._page_drag_neighbor = None         # 被拖出来的邻页页码
        self._page_drag_samples = []            # [(t_ms, offset)]，松手测速用
        self._page_drag_clock = QElapsedTimer()
        # 自动翻页（页模式下 set_auto_scroll 的实现）：单发定时器链。
        # 注意 singleShot 定时器在 timeout 回调里 isActive() 已经是 False，
        # 所以用显式标志 _page_auto_on 表示"开着"，不能靠 timer 状态判断
        self._page_auto_timer = QTimer(self, timerType=Qt.PreciseTimer)
        self._page_auto_timer.setSingleShot(True)
        self._page_auto_timer.timeout.connect(self._on_page_auto)
        self._page_auto_speed = 0.0             # px/s，换算成每页停留时长
        self._page_auto_on = False              # 自动翻页是否开启（信号去重用）
        # ---- 页模式缩放平移（zoom>100% 时拖拽平移，见 _zoom_page）----
        self._page_pan = QPointF(0.0, 0.0)      # 相对"基准偏移"(_page_base_offset)的
                                                # 额外平移增量；单页按槽位钳制，双页整体平移
        # 单页等宽模式：当前页沿滚动轴的滚动偏移（0 = 图片顶边贴视口起始边）。
        # 图片按宽度铺满、高度可超出视口，靠这个偏移在页内上下滚；到边界再翻页。
        self._page_scroll = 0.0
        self._sw_drag_pos = None                # 单页等宽：拖拽滚动的上一个鼠标位置
        # 单页等宽的平滑滚动（滚轮缓动 / 拖拽惯性），思路同 SmoothScroller，
        # 但作用在 _page_scroll 上而不是连续模式的 s 空间。
        self._sw_anim = QVariantAnimation(self)
        self._sw_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._sw_anim.valueChanged.connect(self._on_sw_anim_value)
        self._sw_anim.finished.connect(self._on_sw_anim_finished)
        self._sw_target = 0.0                   # 平滑滚动的目标偏移（连滚时叠加）
        self._sw_kinetic = QTimer(self, interval=16, timerType=Qt.PreciseTimer)
        self._sw_kinetic.timeout.connect(self._on_sw_kinetic)
        self._sw_vel = 0.0                       # 拖拽惯性速度 px/ms
        self._sw_clock = QElapsedTimer()
        self._sw_drag_samples = []               # [(t_ms, scroll)]，松手测速用

        self._page_panning = False              # 当前是否在拖拽平移（与拖拽翻页互斥）
        self._page_pan_start = QPointF()        # 平移起点的鼠标位置
        self._page_pan_ref = QPointF()          # 平移起点时的 _page_pan（松手前可回退）

        self._start_press_pos = QPoint()

        if Setting.IsOpenOpenGL.value:
            self.set_opengl(True)
        self.indexChanged.connect(self.after_index_change)
        self.zoomChanged.connect(self.after_zoom_change)
        self.scrolledPastStart.connect(self.after_switch_last_eps)
        self.scrolledPastEnd.connect(self.after_switch_next_eps)
        self._scene.installEventFilter(self)

    @staticmethod
    def _movie_is_paused(mv: QMovie) -> bool:
        """QMovie 是否处于暂停态。Qt6 只有 setPaused() 没有 isPaused()——必须
        通过 state() 判断（NotRunning / Paused / Running 三态）。"""
        return mv.state() == QMovie.Paused

    @property
    def frame(self) -> ReadNewFrame:
        return self.parent()

    @property
    def read_view(self) -> ReadNewView:
        return self.parent().parent()

    @property
    def qtTool(self) -> ReadNewTool:
        return self.frame.qtTool

    @property
    def read_task(self) -> ReadNewTask:
        return self.read_view.readTask

    # ================ OpenGL 加速 ================

    def set_opengl(self, enabled: bool):
        """开/关 GPU 渲染（运行时可随时切）。原理：把视口换成 QOpenGLWidget，
        scene 由 OpenGL 绘制——图片作为纹理缓存在 GPU 上（首次绘制时上传），
        滚动/重绘只做纹理搬运，大图多图时 CPU 占用显著下降。

        两个必须配套的调整：
        1) QOpenGLWidget 不支持局部更新，ViewportUpdateMode 必须换成
           FullViewportUpdate（GL 下全量重绘很便宜，不用担心）；
        2) 换视口会销毁重建滚动条，先记下阅读位置、换完立刻恢复，
           否则会跳回开头。
        """
        if enabled == self._opengl:
            return
        self._opengl = enabled
        s = self._scroll_min_s()               # 记住当前位置
        if enabled:
            gl = QOpenGLWidget()
            fmt = QSurfaceFormat.defaultFormat()
            fmt.setSamples(4)                  # MSAA：占位框圆角/文字更平滑
            gl.setFormat(fmt)
            # gl.setContextMenuPolicy(Qt.CustomContextMenu)
            self._openglWidget = gl
            self.setViewport(gl)
            self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        else:
            self._openglWidget = None
            self.setViewport(QWidget())        # 换回普通光栅视口
            self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)

        def restore():
            if not ReadMode.isScroll(self._mode):
                self._show_page(self._page, 0)     # 页模式：重摆当前页（无滚动位置）
            else:
                self._set_scroll_min_s(s)
            self._load_visible()
            # 换视口后新 widget 还没画过，显式刷一次让背景铺满（GL 视口
            # 尤其需要：它的首帧是 glClear 出来的黑，背景画刷铺上去才正常）
            self.viewport().update()

        restore()
        # 换视口后 widget 尺寸异步稳定，事件循环下一轮再按一次位置
        QTimer.singleShot(0, restore)

    # ================ 背景 ================

    def _default_bg(self) -> QColor:
        """默认背景色：跟随视口调色板（通常是白，跟随系统/应用主题）。"""
        vp = self.viewport()
        role = vp.backgroundRole()
        c = vp.palette().color(role) if role != QPalette.NoRole else QColor()
        if not c.isValid():
            c = self.palette().color(QPalette.Base)
        return c if c.isValid() else QColor(Qt.white)

    def set_background(self, color):
        """设置图片之外的空白区颜色（看漫画常用黑，看图片流常用白）。

        实现上是写 scene 的 backgroundBrush——QGraphicsView 每次重绘都会先用它
        铺满暴露区域。这一步不能省：viewport 的 autoFillBackground 只在普通
        QWidget 视口上有效，换 QOpenGLWidget 后就失效了（GL 每帧 glClear 成
        透明黑，空白区会发黑、或者像"上一帧没擦干净"）。
        """
        self._scene.setBackgroundBrush(QColor(color))
        self.viewport().update()

    def background(self) -> QColor:
        """当前空白区颜色。"""
        return self._scene.backgroundBrush().color()

    # ================ 缩放（Ctrl+滚轮 / 按钮 / Ctrl+= - 0） ================

    def zoom(self) -> float:
        """当前缩放比（1.0 = 适配视口）。"""
        return self._zoom

    def set_zoom(self, z: float, anchor=None):
        """设置缩放比（自动钳制在 [MIN_ZOOM, MAX_ZOOM]）。

        anchor：QPointF（视口坐标）= 缩放过程中屏幕上"钉住不动"的点
        （Ctrl+滚轮传光标位置）。None = 视口中心（按钮/快捷键缩放）。
        两种模式的行为：
        - 连续模式：缩放作用于 cross 轴（cross = 视口×z）后全量重排，滚动位置
          按"锚点内容点"恢复——光标指着哪张图的哪个位置，缩放后还在那；
          z>1 时 cross 轴滚动条出现（AsNeeded），可拖拽平移
        - 页模式：缩放是 item 的 scale 变换，**固定以视口中心为锚点**（单页=图片
          中心，双页=两页中缝；anchor 参数忽略）。放大时内容向四周/两侧外扩，
          双页两张图贴住中缝、不会重叠；z>1 时左键拖拽变为页内平移，翻页仍走
          滚轮/键盘
        缩放后自动对"源分辨率 > 已解码位图"的可见图重新下载解码（防放大发糊）。
        """
        self._release_initial_hold()     # 缩放自带锚点逻辑，别和首屏校准抢位置
        z = max(self.MIN_ZOOM, min(self.MAX_ZOOM, float(z)))
        if abs(z - self._zoom) < 1e-9:
            return
        if not ReadMode.isScroll(self._mode):
            self._zoom_page(z, anchor)
        else:
            self._zoom_strip(z, anchor)
        self.zoomChanged.emit(self._zoom)

    def zoom_in(self, anchor=None):
        """放大一步（×ZOOM_STEP）。"""
        self._zoom_step(1, anchor)

    def zoom_out(self, anchor=None):
        """缩小一步（÷ZOOM_STEP）。"""
        self._zoom_step(-1, anchor)

    def default_zoom_for(self) -> float:
        """某个阅读方向的默认缩放。"""
        return 0.8 if self._mode == ReadMode.UpDown else 1.0

    def reset_zoom(self):
        """重置为当前阅读方向的默认缩放（上下=80%，左右=100%）。"""
        self.set_zoom(self.default_zoom_for())

    def _zoom_step(self, direction: int, anchor):
        """direction：+1 放大一步 / -1 缩小一步。"""
        self.set_zoom(self._zoom * (self.ZOOM_STEP ** direction), anchor)

    def _zoom_strip(self, z: float, anchor):
        """连续模式缩放：改 cross -> 全量重排，锚点内容点恢复原屏幕位置。
        锚点要在两个轴上同时恢复：滚动轴（s）+ cross 轴（z>1 时才有滚动条）。"""
        p = QPointF(anchor) if anchor is not None \
            else QPointF(self.viewport().rect().center())
        # ---- 记录缩放前状态 ----
        s_old = self._s_at_view_pos(p)          # 锚点下的内容 s
        idx, frac = self._anchor_at(s_old)      # (第几张图, 图内位置比例)
        scroll_old = self._scroll_min_s()
        cbar = self._cross_bar()
        pc = p.x() if ReadMode.isUpDown(self._mode) else p.y()
        if cbar.maximum() > cbar.minimum():
            # cross 轴滚动条在（旧 zoom>100%）：内容左缘 = 滚动条值
            frac_c = (cbar.value() + pc) / self._cross
        else:
            # 内容比视口小、居中对齐：内容左缘在 (视口-cross)/2 处
            cvl = self._cross_view_len()
            frac_c = (pc - (cvl - self._cross) / 2.0) / self._cross
        # ---- 应用缩放并重排 ----
        self._scroller.stop()     # 进行中的滚动动画会和恢复的位置互相拉扯
        self._zoom = z
        self._update_cross()
        self._relayout_all()
        # ---- 恢复滚动轴：同一内容点回到同一视口位置 ----
        s_new = self._s_of_anchor(idx, frac)
        self._set_scroll_min_s(s_new - (s_old - scroll_old))
        self._was_at_end = self._at_end()
        # ---- 恢复 cross 轴（仅新内容比视口大时需要动滚动条） ----
        if self._cross > self._cross_view_len():
            cbar.setValue(round(frac_c * self._cross - pc))
        self._load_visible()
        self._refresh_decodes()

    def _zoom_page(self, z: float, anchor):
        """页模式缩放：item 的 scale 变换。

        锚点固定为**视口中心**（单页 = 图片中心，双页 = 两页之间的中缝，
        单页等宽 = 视口中心那一行内容），不使用光标位置。
        - 单页：图片居中放大，四周溢出的部分对称裁掉；
        - 双页：两张图贴住中缝向两侧外扩，**不会互相重叠**；
        - 单页等宽：等比放大，滚动偏移同步换算，**视口中心的内容不跳**。
        同时保证翻页后下一张仍居中显示（不会跑到左上角）。
        anchor 参数为兼容连续模式/旧调用保留，页模式不使用。"""
        self._cancel_page_gestures()    # 进行中的滑动动画/平移先就地收尾
        if self._mode == ReadMode.Samewight:
            self._zoom_single_width_to(z)
        else:
            self._zoom = z
            self._page_pan = QPointF(0.0, 0.0)   # 以中心为锚点：平移复位
        self._zoom = z
        self._page_pan = QPointF(0.0, 0.0)   # 以中心为锚点：平移复位
        self._show_page(self._page, 0)              # 重新摆放
        self._load_visible()
        self._refresh_decodes()

    def _zoom_single_width_to(self, z_new: float):
        """单页等宽模式缩放：保持"视口中心那一行内容"不动（以中心为锚点）。

        等宽图片沿滚动轴的长度 = cross × 真实比例 × zoom，缩放后长度变了，
        滚动偏移必须按比例换算，否则视口里看到的内容会跳走。"""
        items = self._page_items(self._page)
        z_old = self._zoom
        self._zoom = z_new
        self._page_pan = QPointF(0.0, 0.0)
        if not items or z_old <= 1e-9:
            self._page_scroll = 0.0
            return
        L = self._page_axis_len()
        w, h = self._single_width_geometry(items[0])
        ln = h if ReadMode.isUpDown(self._mode) else w
        # 沿滚动轴：短图居中（lead>0），长图顶对齐（lead=0）
        lead_old = (L - ln * z_old) / 2.0 if ln * z_old < L else 0.0
        lead_new = (L - ln * z_new) / 2.0 if ln * z_new < L else 0.0
        # 视口中心对应的内容坐标（未缩放），缩放后仍让它停在视口中心
        c = (L / 2.0 - lead_old + self._page_scroll) / z_old
        self._page_scroll = lead_new + c * z_new - L / 2.0
        self._clamp_page_scroll(self._page)
        self._sw_target = self._page_scroll

    # ---- 页模式缩放平移（zoom>100% 时左键拖拽） ----

    def _begin_page_pan(self, pos: QPointF):
        self._page_panning = True
        self._page_pan_start = QPointF(pos)
        self._page_pan_ref = QPointF(self._page_pan)
        self.viewport().setCursor(Qt.ClosedHandCursor)

    def _page_pan_move(self, pos: QPointF):
        """拖拽平移：_page_pan 跟随鼠标增量，重摆当前页（_place_page 钳制）。"""
        d = pos - self._page_pan_start
        self._page_pan = QPointF(self._page_pan_ref.x() + d.x(),
                                 self._page_pan_ref.y() + d.y())
        self._place_page(self._page, 0.0)

    def _end_page_pan(self):
        self._page_panning = False
        self.viewport().setCursor(Qt.ArrowCursor)
        # 把原始 pan 归一化成"相对基准的有效平移量"：被边界拦住的多余位移丢掉，
        # 下一次平移手势从合法位置起算（否则连续拖会"攒"出隐形位移）。
        # _page_pan 是相对 _page_base_offset 的增量（不是绝对偏移），所以这里必须
        # 减去基准；否则下一次平移会把"基准里的对齐偏移"再叠一遍，位置直接跑飞。
        rects = self._page_slot_rects(self._page)
        if rects:
            x, y, w, h = rects[0]
            al = self._page_slot_aligns(self._page)[0]
            bx, by = self._page_base_offset(w, h, al)
            dx, dy = self._page_slot_offset(w, h, al, self._page)
            self._page_pan = QPointF(dx - bx, dy - by)

    def _refresh_decodes(self):
        """缩放/窗口变化后，把解码位图重新对齐到当前渲染尺寸。

        两个方向都要管：
        - **太小**（放大 / 窗口变大）：位图不够清晰，重新下载解码（保留旧 pixmap
          直到新图就绪）；
        - **太大**（缩小 / 窗口变小）：`drawPixmap` 会从 1:1 快路径掉到缩放路径
          （实测 0.9× 缩放比 1:1 慢 5 倍），而且白占内存。压缩字节还在 `_buf`
          里的直接后台重解（不走网络）；已被 LRU 回收的就不值得为"缩小"重新
          下载了，先留着大图（降采样绘制）。"""
        if not ReadMode.isScroll(self._mode):
            its = []
            for pg in (self._page - 1, self._page, self._page + 1):
                if 0 <= pg <= self._max_page():
                    its.extend(self._page_items(pg))
        else:
            front = Setting.PictureShowFrontCount.value
            after = Setting.PictureShowCount.value
            # L = self._viewport_len()
            # s0 = self._scroll_min_s()
            # top, bottom = s0 - L * 1.5, s0 + L * 2.5
            curIdx = self._cur_idx
            # L = self._viewport_len()
            # s0 = self._scroll_min_s()
            its = self._items[max(0,curIdx - front):curIdx + after + 1]
            # its = [it for it in self._items
            #        if it._s + it._len >= s0 - L and it._s <= s0 + L * 2.5]

        # max_px = self._decode_max_px()        # 与 DecodeTask / QMovie 同一套口径
        for it in its:
            # 动图不重新下载：它的原图字节还在 _raw 里，只需要把每帧解码得更
            # 大一点——_refresh_playing 会发现 setScaledSize 需要更新并改掉
            if it.pixmap is None or it._reply is not None or it._failed:
                continue

            target = self._decode_target_size(it)  # 与 DecodeTask 同一套口径
            if not target.isValid():
                continue
            dpr = self.devicePixelRatioF()
            have = it.pixmap.width()     # 已解码位图的宽（物理像素）
            if have > round(target.width()*dpr) * it.DECODE_SHRINK_RATIO:
                # 位图明显偏大：从保留的压缩字节后台重解（无网络）。
                # 阈值留一点余量，避免为了 1% 的差异反复重解。
                if it._buf:
                    it._pending_decode = True
                    self._start_decode_if_ready(it)
                else:
                    self._start_download(it)
                continue

            src = it._size.width() if (it._size and it._size.isValid()) else 0
            # 位图不够 + 原图确实有更高分辨率，才值得重新下载
            if have < (target.width()*dpr) * 0.99 and src > have * 1.25:
                if it._buf:
                    it._pending_decode = True
                    self._start_decode_if_ready(it)
                else:
                    self._start_download(it)

    @property
    def is_auto(self):
        return self._page_auto_timer.isActive() or self.scroller.is_auto_scrolling()

    def get_item_by_idx(self, idx) -> ReadNewGraphicsItem:
        if idx >= len(self._items):
            return None
        if idx <= 0:
            return None
        return self._items[idx]

    def get_cur_item(self) -> ReadNewGraphicsItem:
        idx = self._cur_idx
        if idx >= len(self._items):
            return None
        if idx < 0:
            return None
        return self._items[idx]

    def stop_auto(self):
        self._scroller.stop_auto()
        self._stop_page_auto()

    @property
    def scroller(self) -> ReadNewScroller:
        return self._scroller

    def set_auto_scroll(self, speed: float):
        """自动滚动/自动翻页。speed：px/s（沿阅读方向），0 或负数停止。
        连续模式=匀速滚动；页模式=按 页长/速度 换算成每页停留时长自动翻页
        （如 600px 屏、300px/s = 每页停 2 秒）。
        任意鼠标点击/滚轮/拖拽/键盘都会停止；到最后一页也会停止。"""
        self._release_initial_hold()     # 自动滚动要接管位置，首屏校准让位
        if not ReadMode.isScroll(self._mode):
            self._start_page_auto(speed)
        else:
            self._scroller.start_auto(speed)

    # ================ 动图（GIF / 动画 WebP）===============

    @property
    def animations_enabled(self) -> bool:
        """是否播放动图（False = 全部停在海报帧，CPU/内存都降到静态图水平）。"""
        return self._anims_enabled

    def set_animations_enabled(self, on: bool):
        """开/关动图播放。关掉只是暂停（QMovie.setPaused），不销毁已解码内容，
        再打开能立刻接着播。做省电模式/性能开关时用这个。"""
        if on == self._anims_enabled:
            return
        self._anims_enabled = on
        self._refresh_playing()

    def _decode_target_size(self, it: ReadNewGraphicsItem) -> QSizeF:
        """这张图"解码后应该多大"（**物理像素**）——按它实际会被渲染的尺寸算。

        ⚠️ 为什么不能用"视口最大边"当宽度上限：竖屏（高>宽）时最大边是"高"，
        拿它当宽度上限会把竖图解成比实际显示大好几倍；横排模式、单页 contain-fit
        也一样。这里按各模式的真实渲染尺寸算，只缩不放，解出来正好够显示。

        渲染尺寸（逻辑像素）：
        - 连续 ttb：宽 = cross，高 = cross×(h/w)
        - 连续 横排：高 = cross，宽 = cross×(w/h)
        - 单页/双页/封面：按 contain-fit 放进槽位
        - 单页等宽：cross 轴铺满，滚动轴按比例

        ⚠️ 连续模式的比例要和 _dims_for 用**同一个钳制**（[0.4, MAX_ASPECT]）。
        否则超长/超扁图解码尺寸和 item 矩形对不上，paint 里就成了"缩放绘制"，
        从 1:1 快路径掉到慢路径（实测慢 4~5 倍），还白占内存。"""
        # dpr = self.devicePixelRatioF()
        sz = it._size
        aspect = (sz.height() / sz.width()) if (
            sz and sz.isValid() and sz.width() > 0) else it._def_aspect   # h/w
        aspect = max(0.05, aspect)
        z = self._zoom

        if ReadMode.isScroll(self._mode):
            cross = self._cross                     # 已经含了 zoom
            if ReadMode.isUpDown(self._mode):
                r = min(max(aspect, 0.4), self.MAX_ASPECT)      # 同 _dims_for
                w, h = cross, cross * r
            else:
                r = min(max(1.0 / aspect, 0.4), self.MAX_ASPECT)  # 同 _dims_for
                w, h = cross * r, cross
        elif self._mode == ReadMode.Samewight:
            vw = float(self.viewport().width())
            vh = float(self.viewport().height())
            if ReadMode.isUpDown(self._mode):
                w, h = vw, vw * aspect
            else:
                w, h = vh / aspect, vh
            w *= z
            h *= z
        else:
            # 单页 / 双页 / 双页(首图单独)：contain-fit 进槽位，再乘 zoom。
            # 注意：解码可能发生在相邻页（page-1/page+1）的预取上，所以要按
            # **这张图自己所在页**的槽位算，不能一律用当前页。
            try:
                idx = self._items.index(it)
            except ValueError:
                idx = 0
            pg = self._page_of_index(idx)
            slots = self._page_slot_rects(pg)
            if not slots:
                return QSizeF()
            i = min(max(idx - self._page_first_index(pg), 0), len(slots) - 1)
            x, y, sw, sh = slots[i]
            if sw <= 0 or sh <= 0:
                return QSizeF()
            if aspect > sh / sw:                    # 比槽位更"竖" -> 高度受限
                w, h = sh / aspect, sh
            else:                                   # 宽度受限
                w, h = sw, sw * aspect
            w *= z
            h *= z
        return QSizeF(max(1, w), max(1, h))

    def _get_decode_to_size(self, size, file_data:FileData):
        dpr = self.devicePixelRatioF()
        scale = min(size.width()*dpr / max(1, file_data.w), size.height() * dpr / max(1, file_data.h))
        # 按目标框等比缩/放（KeepAspectRatio 保证不变形）：
        # - 大图（scale<1）：缩到目标，省内存，绘制 1:1；
        # - 小图（1<scale<=上限）：**放大**到目标，绘制也变成 1:1
        #   （上采样成本按输出面积算，放后台线程付一次远好过每帧付）；
        # - 太小的图（scale>上限）：放弃放大——位图会占"目标面积"，
        #   100×100 铺到 880 要膨胀 77 倍内存，画面并不会更清楚。
        if scale < 1.0 or (scale <= ReadNewGraphicsItem.DECODE_UPSCALE_MAX_SCALE
                           and abs(scale - 1.0) > 1e-6):
            return size.width(), size.height()
        return 0, 0

    def _movie_scaled_size(self, it: ReadNewGraphicsItem) -> QSize:
        """动图的帧解码尺寸（物理像素）：按渲染目标等比缩，只缩不放。

        为什么用 QMovie.setScaledSize 而不是绘制时缩放：让解码器在解码阶段就
        把每帧缩到显示尺寸，绘制时是 1:1 搬运。反过来（原尺寸解码 + 每次 paint
        缩放）会慢好几倍——和静态图走 DecodeTask 降采样是同一个道理。"""
        if it._size is None or not it._size.isValid():
            return QSize()
        w, h = it._size.width(), it._size.height()
        if w <= 0 or h <= 0:
            return QSize()
        target = self._decode_target_size(it)
        dpr = self.devicePixelRatioF()
        tw, th = int(math.trunc(target.width()*dpr)), int(math.trunc(target.height()*dpr))
        if tw > 0 and th > 0 and (w > tw or h > th):
            s = min(tw / w, th / h)                 # 等比缩进目标框
            w = max(1, int(round(w * s)))
            h = max(1, int(round(h * s)))
        return QSize(w, h)

    def _ensure_movie(self, it: ReadNewGraphicsItem):
        """拿到动图的 QMovie（没有就创建）。调用前确保 _raw 非空。"""
        if it._movie is not None:
            return it._movie
        if it._raw.isEmpty():
            return None                      # 原始字节已被内存回收：只能停在海报帧
        self._evict_movies()                 # 超上限先回收最久没播的
        self._anim_seq += 1
        it._anim_seq = self._anim_seq
        # QBuffer 必须和 QMovie 同生共死（QMovie 不接管设备所有权），挂到 view 上
        # 保活即可——item 是 QGraphicsItem，不是 QObject，当不了 QObject 的 parent
        buf = QBuffer(self)
        buf.setData(it._raw)
        buf.open(QIODevice.ReadOnly)
        mv = QMovie(self)
        mv.setDevice(buf)
        sz = self._movie_scaled_size(it)
        if sz.isValid():
            mv.setScaledSize(sz)             # 必须在首次取帧之前设
        mv.frameChanged.connect(lambda _n=0: it.update())   # 换帧 -> 只请求重绘
        it._movie_buf, it._movie = buf, mv
        it.pixmap = None                     # 有 movie 了，别再画静态海报帧
        return mv

    def _evict_movies(self):
        """LRU 回收：QMovie 数量超上限时，干掉最久没播的那个。

        销毁前把当前帧存成静态海报（item.pixmap），这样它即使被滚回来也不会
        退化成占位框——只是不动了，等轮到它播放时会用 _raw 重新建 QMovie。"""
        alive = [x for x in self._anims if x._movie is not None]
        if len(alive) < self.ANIM_MAX_MOVIES:
            return
        busy = set()                         # 现在就在播的不能动
        for x in alive:
            if x._movie.state() == QMovie.Running and not self._movie_is_paused(x._movie):
                busy.add(id(x))
        victim = None
        for x in sorted(alive, key=lambda v: v._anim_seq):
            if id(x) not in busy:
                victim = x
                break
        if victim is None:
            return                           # 全在播且都超上限：这次先放过
        pm = victim._movie.currentPixmap()
        if not pm.isNull():
            victim.pixmap = pm               # 留个海报帧
        victim._movie.stop()
        victim._movie.deleteLater()
        victim._movie, victim._movie_buf = None, None

    def _trim_anim_raw(self):
        """原始压缩数据超预算时，丢掉最久没播那几张的 _raw。

        丢了就无法再重建 QMovie（只能停在海报帧），所以先 жертв 最久没播的。
        这只是防御：常见 GIF 几 MB，几十张也在预算内。"""
        total = sum(x._raw.size() for x in self._anims)
        cap = self.ANIM_MAX_RAW_MB * 1024 * 1024
        if total <= cap:
            return
        busy = {id(x) for x in self._anims if x._movie is not None}
        for x in sorted((v for v in self._anims if not v._raw.isEmpty()),
                        key=lambda v: v._anim_seq):
            if total <= cap:
                break
            if id(x) in busy:
                continue                     # 正在播的不丢
            total -= x._raw.size()
            x._raw = QByteArray()

    def _refresh_playing(self, vis=None):
        """让"该播的播、不该播的停"。

        只播当前屏幕上看得见的：离屏的 GIF 没人看还在解帧纯属浪费 CPU 和电。
        这个方法在滚动时会每帧调用（挂在 _load_visible 上），但 _anims 通常
        只有个位数元素，开销可忽略。

        vis：调用方已经算好的 visible_indices()，传进来省一次重算。"""
        if not self._anims or not self.isVisible():
            return
        if vis is None:
            vis = self.visible_indices()
        live = [self._items[i] for i in vis if i < len(self._items)]
        want = set(id(x) for x in live)
        for it in self._anims:
            if self._anims_enabled and id(it) in want and it.is_animated:
                mv = self._ensure_movie(it)
                if mv is None:
                    continue
                sz = self._movie_scaled_size(it)
                if sz.isValid() and mv.scaledSize() != sz:
                    # 窗口缩放/缩放比变了：改 setScaledSize，后续帧按新尺寸解码
                    mv.setScaledSize(sz)
                self._anim_seq += 1
                it._anim_seq = self._anim_seq
                if mv.state() == QMovie.NotRunning:
                    mv.start()
                elif self._movie_is_paused(mv):
                    mv.setPaused(False)      # setPaused 保帧续播，不像 stop 会回到第 0 帧
            elif it._movie is not None and not self._movie_is_paused(it._movie):
                it._movie.setPaused(True)

    def _pause_all_animations(self):
        """全部暂停（窗口隐藏时调用——不可见还在解帧是纯浪费）。"""
        for it in self._anims:
            if it._movie is not None and not self._movie_is_paused(it._movie):
                it._movie.setPaused(True)

    def _on_animated(self, item: ReadNewGraphicsItem, real: QSize, data: bytes):
        """后台线程判定这是动图（主线程槽）：交给 QMovie 而不是位图。

        布局和静态图完全一样处理（尺寸用 QImageReader 报告的画布尺寸），所以
        滚动        不跳动、可见性判定等既有机制全部复用——区别只有"内容会自己变"。"""
        item._decoding = False
        item._pending_decode = False
        if item not in self._anims:
            self._anims.append(item)
        if not item._size_known:
            self._correct_len(item, real)      # GIF/WebP 的画布尺寸（HTML <img> 同口径）
        item._raw = QByteArray(data)           # COW 浅拷贝，不额外占内存
        self._trim_anim_raw()
        self._trim_caches()                    # 静态位图的回收也顺带跑一次
        item.update()
        self._refresh_playing()                # 它在屏上就立刻开播

    # ================ 位置查询：当前是第几张图 ================
    # 三个概念先分清：
    #   序号 index —— item 在流中的位置，0 起，与阅读顺序一致（_items 的下标）
    #   阅读顺序  —— ltr 左→右、rtl（漫画）右→左、ttb 上→下。visible_indices()
    #                永远按它返回，所以列表第 0 项就是"最靠前的那张"
    #   物理方位  —— 屏幕上的左/右/上/下半屏，只在"双页模式"才有意义
    # 连续模式一屏能看到多张且会滚动，没有固定的"左半屏/右半屏"，所以针对这类
    # 查询返回 None，别硬套。

    def visible_indices(self) -> list:
        """当前屏幕上可见的图片序号（0 起），**按阅读顺序**排列。

        - 连续模式：所有和视口相交的图（长图+小图可能同屏多张）。第 0 项就是
          "阅读起始边那张"——ttb 最上面 / ltr 最左边 / rtl（漫画）最右边，
          也就是 current_index()
        - 页模式：当前页的 1~2 张；翻页滑动/拖拽进行途中邻页也被拖进屏幕，
          这时邻页的图也在列表里
        - 一张图都没有时返回 []
        """
        if not self._items:
            return []
        if not ReadMode.isScroll(self._mode):
            pages = {self._page}
            # 动画/拖拽途中邻页也露出来了：一并算进去
            nb = self._page_anim_nb if self._page_anim_mode else self._page_drag_neighbor
            if nb is not None and 0 <= nb <= self._max_page():
                pages.add(nb)
            idxs = set()
            for p in pages:                       # 集合乱序，下面再排
                i0 = self._page_first_index(p)
                idxs.update(range(i0, i0 + len(self._page_items(p))))
            return sorted(idxs)
        # 连续模式：item 按 _s 升序。先用二分找到"s0 之后的第一张"，再往回看一张
        # （可能有一张起点在 s0 之前、但尾部伸进视口的长图），然后顺序扫到 s1。
        # 这样每次是 O(log n + 可见张数)，不再是"从第 0 张开始扫"的 O(n)。
        s0 = self._scroll_min_s()
        s1 = s0 + self._viewport_len()
        items = self._items
        lo = bisect.bisect_left(items, s0, key=lambda it: it._s)
        if lo > 0 and items[lo - 1]._s + items[lo - 1]._len > s0 + 1.0:
            lo -= 1
        out = []
        for i in range(lo, len(items)):
            it = items[i]
            if it._s >= s1:
                break                             # 后面的都还在视口下方/右方
            # 至少露出 1px 才算"可见"：停在两张图交界处时（比如 jump_to_index
            # 把某张图的起点顶到视口边缘），前一张的末像素经 _snap_px 对齐后
            # 可能比交界点多半像素，否则会被算成可见、让 current_index 来回闪
            if it._s + it._len > s0 + 1.0:
                out.append(i)
        return out

    def current_index(self) -> int:
        """阅读位置所在的图片序号（0 起；一张图都没有时 -1）。

        连续模式（滚动模式）判定规则 = **阅读起始边那张**：
            ttb 上下滚动 -> 屏幕上最**上**面还看得见的那张
            ltr 左右滚动 -> 屏幕上最**左**边还看得见的那张
            rtl 漫画模式 -> 屏幕上最**右**边还看得见的那张
        等价于 visible_indices()[0]——那个列表按阅读顺序排，第 0 项就是起始边
        那张。一屏多张时不取居中那张、也不取占屏最大的那张。
        页模式 = 当前页的第一张。
        """
        return self._first_visible_index()

    def current_page(self) -> int:
        """当前页码（**1 起**；一张图都没有时 0）——"第 N 页 / 共 M 页"直接用它。

        连续模式每页就是一张图（= current_index()+1）；页模式一页 1~2 张，
        页码 = 当前页第一张 +1（双页模式下"第 3 页"= 第 5、6 张）。
        """
        i = self.current_index()
        return 0 if i < 0 else i + 1

    def page_count(self) -> int:
        """总页数（配合 current_page 显示"第 N / 共 M 页"）。

        连续模式 = 图片总数；单页模式 = 图片总数；双页模式 = ceil(图片数/2)；
        双页（首图单独）模式 = 1 + ceil((图片数-1)/2)。"""
        return self._page_count()

    def count(self) -> int:
        """图片总数（len(_items) 的语义化别名）。"""
        return len(self._items)

    # def side_of_index(self, idx: int):
    #     """这张图现在显示在屏幕的哪个物理方位？
    #
    #     返回 "left"/"right"/"top"/"bottom"（双页模式）、"center"（单页模式）、
    #     None（连续模式：一屏多张且会滚动，没有固定的半屏概念）。
    #     漫画模式（rtl）第一张在右半屏——这是日漫跨页的正确顺序。
    #     """
    #     if not 0 <= idx < len(self._items):
    #         return None
    #     if self._mode == ReadMode.LeftRight:
    #         return "center"
    #     if not ReadMode.isDouble(self._mode):
    #         return None
    #     # 在本页里的槽位序号：0=阅读起始侧（首图单独模式下封面页恒为 0）
    #     k = idx - self._page_first_index(self._page_of_index(idx))
    #     if self._mode == ReadMode.UpDown:
    #         return "top" if k == 0 else "bottom"
    #     if ReadMode.isLeftRight(self._mode):
    #         return "left" if k == 0 else "right"
    #     return "right" if k == 0 else "left"    # rtl：阅读从右往左

    # def index_on_side(self, side: str):
    #     """反过来问："左边那张图是第几张？"（漫画模式要问右边）
    #
    #     side 支持三种写法：
    #       "left"/"right"/"top"/"bottom" —— 物理方位（只在双页模式有意义）
    #       "first"                        —— 阅读起始侧，跨模式通用：
    #                                        ltr=左、rtl(漫画)=右、ttb=上
    #                                        连续模式下它就等于 current_index()
    #       "last"                         —— 另一半屏（双页的第二张）
    #     当前屏幕上没有这个槽位 / 连续模式下问物理方位 -> None。
    #
    #     页模式下只考虑**当前页**——翻页动画途中邻页虽半露在屏幕上，问"左边是
    #     第几张"显然要的是落下后那一页的答案，不是扫过就算。
    #     """
    #     if ReadMode.isScroll(self._mode):
    #         vis = self.visible_indices()
    #     else:
    #         # 页模式下只看当前页（封面页只有 1 张）
    #         i0 = self._page_first_index(self._page)
    #         vis = list(range(i0, i0 + len(self._page_items(self._page))))
    #     if not vis:
    #         return None
    #     if side == "first":
    #         return vis[0]
    #     if side == "last":
    #         return vis[-1] if len(vis) > 1 else None
    #     for i in vis:
    #         if self.side_of_index(i) == side:
    #             return i
    #     return None

    # ================ 定位：首屏起点 / 跳到第几张图 ================

    def initial_index(self) -> int:
        """首屏起点：首次显示时定位到哪张图（0 起）。"""
        return self._initial_idx or 0

    def set_initial_index(self, idx: int):
        """指定"首次打开显示第几张图"（0 起，显示给用户时记得 +1）。

        用法（在 show() 之前调用，add_image 之前或之后都行）：

            view = StripView(MODE_TTB, initial_index=12)   # 构造参数，等价下面
            view.set_initial_index(12)                     # 或者显式调用
            ...add_image...
            view.show()

        为什么推荐"add_image 之后、show 之前"：视口尺寸在 show 之后才确定，
        在那之前只能按占位尺寸估算位置；show 那一刻会按真实视口重排并定位，
        之后还有一个"持续校准"阶段（见下）。

        已经显示过再调用 = 立即跳过去（等价于 jump_to_index），不会静默失效。

        位置可能不精确的根源：网络图的尺寸是边下边知道的，目标图前面那些图
        一开始都是占位尺寸。所以首次对齐后还会持续校准——每当某张图的真实
        尺寸修正导致长度变化，就把目标图重新对齐回视口起始边，直到目标图
        自己的尺寸已知为止（_initial_hold）。用户一旦自己滚动/拖拽/翻页，
        校准立即停止（不能跟用户抢位置）。
        """
        self._initial_idx = max(0, int(idx))
        if not ReadMode.isScroll(self._mode):
            # 页模式没有滚动位置：首屏 = 页码。双页时第 12 张在第 6 页
            self._page = self._page_of_index(self._initial_idx)
        if self._first_show:
            # 还没显示：先进入校准期（这样 add_image/resize 期间的中间位置
            # 不会通过 indexChanged 泄漏出去，见 _refresh_index）
            self._initial_hold = bool(self._initial_idx)
            self._hold_miss = 0
        else:
            self.jump_to_index(self._initial_idx)

    def jump_to_index(self, idx: int, frac: float = 0.0):
        """立即定位到第 idx 张图（0 起，越界自动钳到首尾）。

        落点：把这张图的起始边顶到**视口起始边**——ttb 顶到最上面、ltr 顶到最
        左面、rtl 顶到最右面。所以跳完 current_index() 就是 idx（唯一例外见下）。
        frac：图内位置比例，0=该图的起始边（默认）、0.5=该图正中。
        例如 jump_to_index(5, 0.5) 把第 5 张图的中间放到视口起始边。
        页模式忽略 frac——它一次显示一整页，只能翻到该图所在的那一页。

        唯一例外：跳到**最后几张**时内容不够长，滚动位置被钳在末端，目标图没法
        顶到起始边（它下面没内容了）。这时 current_index() 会是最靠起始边的那张
        （比目标小一点点），属于物理上做不到的正常现象，不是没跳过去。

        还没首次显示时调用等同 set_initial_index（要等 show 才有真实视口尺寸）。
        """
        if not self._items:
            self._initial_idx = max(0, int(idx))     # 记下来，show 时生效
            return
        idx = max(0, min(int(idx), len(self._items) - 1))
        self._initial_idx = idx
        self._reset_edge_counts()     # 跳转后重新算"到顶/到底"的连续次数
        if not ReadMode.isScroll(self._mode):
            # self._stop_page_auto()
            self.qtTool.CloseScrollAndTurn()
            self._page = self._page_of_index(idx)
            if self._first_show:
                return          # 等 showEvent 里 _show_page
            self._show_page(self._page, 0)
            self._load_visible()
            return
        self._enter_initial_hold()
        if self._first_show:
            return              # 等 showEvent 按真实视口重排后再定位
        self._align_initial_target(frac)
        self._load_visible()

    def jump_to_page(self, page: int):
        """跳到第 page 页（**1 起**，越界自动钳到首尾）——jump_to_index 的页码版。

        连续模式一页=一张图，所以 jump_to_page(8) == jump_to_index(7)；
        双页模式下 jump_to_page(3) 跳到第 5、6 张那一页。
        """
        self.jump_to_index(max(0, int(page) - 1))

    def _align_initial_target(self, frac: float = 0.0):
        """把目标图重新对齐到视口起始边（首次显示、以及之后每次尺寸修正时）。

        frac 见 jump_to_index。对齐完若目标图自己的尺寸已经确定（或它加载失败
        了，不可能再知道），位置就不会再被前面的图修正影响，校准阶段结束。"""
        # 重入保护（修复"跳转到后面页死循环"）：本方法会改滚动条和视图 transform
        # （_set_scroll_min_s -> _apply_sub_transform -> setTransform）。在高分屏
        # （dpr=1.25 等，_sub 为小数）且用了 OpenGL 视口时，setTransform 会同步
        # 触发 rangeChanged，于是又走 _on_range_changed -> 本方法，形成无限递归
        # 直到栈溢出。用标志位挡住这种"自己引发的 rangeChanged"；真正由图片尺寸
        # 修正（异步）带来的 rangeChanged 在本方法返回后仍会正常进入对齐。
        if self._aligning_target:
            return
        self._aligning_target = True
        try:
            if self._initial_idx is None or not self._items:
                self._initial_hold = False
                return
            it = self._items[self._clamped_initial_idx()]
            self._scroller.stop()            # 别让进行中的动画和这次对齐互相拉扯
            want = it._s + frac * it._len
            room = max(0.0, self._total - self._viewport_len())
            self._set_scroll_min_s(want)
            self._was_at_end = self._at_end()
            if want > room + 0.5:
                # 末端钳制：目标图后面内容不够一屏，根本顶不到起始边（跳最后几张时
                # 常见）。这时必须立刻结束校准——否则 _refresh_index 会因为"当前序号
                # != 目标"一直把 indexChanged 压住，UI 上的页码就一直停在跳转前那个
                # 旧值（看起来像"当前页是中间某一页"）。
                self._initial_hold = False
            if it._size_known or it._failed:
                self._initial_hold = False   # 目标已定型：可以放手了
        finally:
            self._aligning_target = False

    def _clamped_initial_idx(self) -> int:
        """首屏目标序号钳到合法范围（图片还没加够时目标可能越界）。"""
        if not self._items:
            return 0
        return max(0, min(self._initial_idx or 0, len(self._items) - 1))

    def _release_initial_hold(self):
        """用户自己动了（滚动/拖拽/翻页/缩放/自动滚动）：停止首屏校准。
        用户一开始操作就归用户，不能再把位置拽回目标图。"""
        self._initial_hold = False
        self._hold_miss = 0

    def _enter_initial_hold(self):
        """进入校准期（跳转/首屏定位后）。计数清零，超时保护从头开始算。"""
        self._initial_hold = True
        self._hold_miss = 0

    def _first_visible_index(self, vis=None) -> int:
        """visible_indices 的第 0 项（-1=没有图）。模式切换时要保证不返回
        动画途中邻页的序号，所以这里独立算，不含邻页。

        连续模式下"第 0 项"的屏幕含义就是**阅读起始边那张**，因为 s 沿阅读方向
        递增、而视口区间是 [s0, s0+L]：
            ttb：s 向下增大 -> s 最小的可见项 = 最上面那张
            ltr：s 向右增大 -> 最左边那张
            rtl：s 向左增大（场景 x=-s）-> 最右边那张

        vis：调用方已经算好的 visible_indices()，传进来可以省一次重算。"""
        if not ReadMode.isScroll(self._mode):
            return min(self._page_first_index(self._page),
                       max(0, len(self._items) - 1))
        if vis is None:
            vis = self.visible_indices()
        return vis[0] if vis else -1

    def _refresh_index(self, vis=None):
        """重算"当前第几张"，跨到新的一张时才发 indexChanged。

        调用点都是"阅读位置可能变了"的地方：_load_visible（滚动/翻页/模式切换
        都走它）、_end_page_drag（松手判定后）。60fps 下每帧都会进来，所以
        visible_indices 用二分找起点、并且由 _load_visible 传进来复用。

        vis：调用方已经算好的 visible_indices()。"""
        idx = self._first_visible_index(vis)
        if self._initial_hold and idx != self._clamped_initial_idx():
            # 首屏校准期：位置还在被尺寸修正推来推去（目标图前面的图陆续探测到
            # 真实尺寸），这里看到的只是中间态。别发出去——否则 UI 上的
            # "第 N 张"会 7->0->7 闪。稳定后自然会对上目标并正常发信号。
            # 但不能无限期压着：目标图加载失败/尺寸永远拿不到时，UI 会一直显示
            # 跳转前的旧序号（看起来像"当前页是中间某一页"）。超过上限就认命，
            # 结束校准并把眼前真实的序号发出去。
            self._hold_miss += 1
            if self._hold_miss <= self.HOLD_MAX_MISS:
                return
            self._initial_hold = False
        if idx != self._cur_idx:
            self._cur_idx = idx
            self.indexChanged.emit(idx)

    # ---- 页模式（翻页器）：几何 / 显示 / 翻页 ----

    def _page_per_screen(self) -> int:
        """一屏几张图：单页 / 单页等宽 1，双页 / 双页(首图单独) 2。"""
        return 1 if not ReadMode.isDouble(self._mode) else 2

    def _page_cover_offset(self) -> int:
        """首图是否单独占一页（"封面"对齐）。0 = 从第 1 张直接两两配对；
        1 = PAGE_DOUBLE_COVER，第 1 张单独，之后 (2,3)、(4,5)……"""
        return 1 if self._is_cover_mode else 0

    def _is_cover_page(self, page: int) -> bool:
        """page 是不是"首图单独"模式下的封面页（只有第 0 页）。

        封面页按**单页模式**布局：整屏、等比缩放居中（不是挤在半个槽位里）。"""
        return page < self._page_cover_offset()

    def _is_double_mode(self) -> bool:
        """当前是不是"一屏两张图"的模式（含首图单独变体）。"""
        return ReadMode.isDouble(self._mode)

    def _page_first_index(self, page: int) -> int:
        """第 page 页（0 起）的第一张图序号（0 起）。

        普通双页：page*2；首图单独：page 0 -> 0，page>=1 -> 1+(page-1)*2。
        单页模式恒等于 page。"""
        o = self._page_cover_offset()
        if page < o:
            return page                        # 封面页：一张一页
        return o + (page - o) * self._page_per_screen()

    def _page_of_index(self, idx: int) -> int:
        """序号 idx（0 起）落在第几页——_page_first_index 的逆运算。"""
        o = self._page_cover_offset()
        if idx < o:
            return idx
        return o + (idx - o) // self._page_per_screen()

    def _page_count(self) -> int:
        """总页数（页模式；连续模式 = 图片数）。"""
        n = len(self._items)
        if ReadMode.isScroll(self._mode):
            return n
        if n == 0:
            return 0
        per = self._page_per_screen()
        o = self._page_cover_offset()
        return o + (n - o + per - 1) // per

    def _max_page(self) -> int:
        """最后一页的页码（0 起；双页模式不足一对时最后一页只有 1 张）。"""
        return max(0, self._page_count() - 1)

    def _page_axis_len(self) -> float:
        """阅读方向上的视口长度：整页翻动/拖拽的滑动距离。"""
        return (self.viewport().height() if ReadMode.isUpDown(self._mode)
                else self.viewport().width())

    def _reading_dir_vec(self):
        """阅读方向的单位向量（场景坐标）：ttb 向下 (0,1)；ltr (1,0)；rtl (-1,0)。"""
        if ReadMode.isUpDown(self._mode):
            return (0.0, 1.0)
        if ReadMode.isLeftRight(self._mode):
            return (1.0, 0.0)
        return (-1.0, 0.0)

    def _page_slot_rects(self, page: int = None):
        """当前页每个槽位的矩形 [(x, y, w, h), ...]。页模式无滚动，
        场景坐标==视口坐标。单页=整屏；双页：ttb 上下叠放、横排左右并排，
        RTL 第一张在右半屏（日漫跨页的正确顺序）。尺寸对齐设备像素。

        page 传"封面页"时按**单页布局**返回整屏，让第一张图居中铺满视口，
        而不是挤在半个槽位里。"""
        vw, vh = self.viewport().width(), self.viewport().height()
        if page is not None and self._is_cover_page(page):
            return [(0.0, 0.0, vw, vh)]        # 封面页：按单页模式整屏
        if self._mode == ReadMode.LeftRight:
            return [(0.0, 0.0, vw, vh)]
        if ReadMode.isUpDown(self._mode):
            h = self._snap_px(vh)
            return [(0.0, 0.0, vw, h)]
        w = self._snap_px(vw / 2)
        if ReadMode.isLeftRight(self._mode):
            return [(0.0, 0.0, w, vh), (w, 0.0, self._snap_px(vw - w), vh)]
        # rtl：第一张（阅读顺序最前）在右半屏
        return [(w, 0.0, self._snap_px(vw - w), vh), (0.0, 0.0, w, vh)]

    def _page_items(self, page: int):
        """第 page 页的 item 列表（封面页只有 1 张；最后一页可能不足 2 张）。"""
        i0 = self._page_first_index(page)
        n = 1 if page < self._page_cover_offset() else self._page_per_screen()
        return self._items[i0:i0 + n]

    def _page_slot_aligns(self, page: int = None):
        """每个槽位的内容对齐方式 (ax, ay)：-1 靠左/上、0 居中、+1 靠右/下。

        单页：居中。双页：两张图都朝**中缝**贴（像翻开的书页拼在一起），
        多余留白全部留到外侧——否则两张图各自在自己半屏里居中，中间会断开：
            ttb：上半屏的图贴底边（中缝），下半屏的图贴顶边
            ltr：左半屏贴右，右半屏贴左
            rtl：第一张在右半屏，贴左（中缝）；第二张在左半屏，贴右
        最后一页只有一张时也朝中缝贴（阅读视线不用跳到外侧）；首图单独
        模式的**封面页按单页模式居中**（page 传入时）。"""
        if page is not None and self._is_cover_page(page):
            return [(0, 0)]                    # 封面页：居中（同单页模式）
        if not self._is_double_mode():
            return [(0, 0)]
        if ReadMode.isUpDown(self._mode):
            return [(0, +1), (0, -1)]
        if ReadMode.isLeftRight(self._mode):
            return [(+1, 0), (-1, 0)]
        return [(-1, 0), (+1, 0)]

    def _page_base_offset(self, w: float, h: float, align):
        """缩放到当前 zoom、尚未叠加平移时的基准偏移（item 左上角相对槽位左上角）。

        ax/ay = -1 贴起始边（偏移 0）、0 居中（(w-w·z)/2）、+1 贴中缝（w-w·z）。
        缩小（z<=1）时结果为正，图片比槽位小、留白在外侧；放大（z>1）时结果
        为负，图片比槽位大、超出部分在外侧。缩小/放大用同一个公式，因此放大后
        **居中/贴边的锚点与缩小是一致的**，不会突然改成"从左上角开始"。"""
        ax, ay = align
        z = self._zoom
        return (w * (1 - z) * (ax + 1) / 2.0,
                h * (1 - z) * (ay + 1) / 2.0)

    def _page_slot_offset(self, w: float, h: float, align, page: int = None):
        """缩放后 item 左上角相对槽位左上角的偏移 (dx, dy)。

        基准 = _page_base_offset：单页居中（ax=ay=0），双页朝中缝贴（±1）。
        zoom>1 时在基准上叠加 _page_pan：
        - 单页 / 封面页：钳制到 [w-w·z, 0]，保证图片始终盖满槽位（不露留白）；
        - 双页：两张图用**同一个 pan 整体平移**，中缝始终贴合；绘制时前一张
          还会朝中缝多画 SEAM_OVERLAP（1px）盖住白缝，所以包围盒会有 1px
          有意叠加；代价是外侧可能露出留白——想看到被裁掉的部分就拖一下。"""
        bx, by = self._page_base_offset(w, h, align)
        z = self._zoom
        if z <= 1.0:
            return bx, by
        px, py = self._page_pan.x(), self._page_pan.y()
        # 封面页是"按单页布局的一张图"，用单页的钳制规则；其余双页才整体平移
        is_cover = page is not None and self._is_cover_page(page)
        if self._is_double_mode() and not is_cover:
            # 双页：整屏跨页一起平移，不逐槽钳制（逐槽钳制会把某一张卡住、
            # 另一张却继续走，两张图就会互相压过去 —— 正是"放大后重叠"的来源）
            return bx + px, by + py
        # 单页 / 封面页：钳制在图片边界内，图片始终盖满槽位
        lo_x, lo_y = w * (1 - z), h * (1 - z)
        return max(lo_x, min(0.0, bx + px)), max(lo_y, min(0.0, by + py))

    # ---- 单页等宽模式（PAGE_SINGLE_WIDTH）：按宽度铺满、高度可超出、页内上下滚 ----

    def _single_width_geometry(self, it):
        """单页等宽模式下 item 的"未缩放"尺寸 (w, h)。

        垂直于滚动轴的 cross 轴铺满视口（上下滚动 -> 宽度 = 视口宽），
        沿滚动轴的长度按图片真实宽高比算——**不套 MAX_ASPECT 上限**，
        所以很长的条漫也能保持原比例，超出的部分靠页内滚动看。"""
        sz = it._size
        vw, vh = float(self.viewport().width()), float(self.viewport().height())
        if ReadMode.isUpDown(self._mode):                    # 上下滚：宽 = 视口宽
            w = vw
            r = (sz.height() / sz.width()) if (
                sz and sz.isValid() and sz.width() > 0) else it._def_aspect
            return w, w * max(0.05, r)
        h = vh                                        # 左右滚：高 = 视口高
        r = (sz.width() / sz.height()) if (
            sz and sz.isValid() and sz.height() > 0) else (1.0 / it._def_aspect)
        return h * max(0.05, r), h

    def _page_scroll_extent(self, page: int) -> float:
        """当前页沿滚动轴的总长度（含 zoom 缩放）。"""
        items = self._page_items(page)
        if not items:
            return 0.0
        w, h = self._single_width_geometry(items[0])
        ln = h if ReadMode.isUpDown(self._mode) else w
        return ln * self._zoom

    def _page_scroll_max(self, page: int) -> float:
        """当前页能滚动的最大偏移（0 = 一屏放得下，不用滚）。"""
        return max(0.0, self._page_scroll_extent(page) - self._page_axis_len())

    def _clamp_page_scroll(self, page: int):
        if self._page_scroll < 0.0:
            self._page_scroll = 0.0
        hi = self._page_scroll_max(page)
        if self._page_scroll > hi:
            self._page_scroll = hi

    def _scroll_or_flip_page(self, delta: float):
        """单页等宽模式：**立即**沿阅读方向滚动 delta（>0 = 往阅读方向前进）。

        页内还能滚就只滚；滚到顶/底越过边界才翻到上一页/下一页
        （上一页落在它的底部，下一页落在顶部）。
        拖拽/自动翻页用这个（要跟手、不要缓动）；滚轮/键盘走 _sw_scroll_by。"""
        self._sw_anim.stop()
        self._sw_kinetic.stop()
        max_s = self._page_scroll_max(self._page)
        nxt = self._page_scroll + delta
        if nxt < 0.0:
            if self._page > 0:                    # 越过顶部 -> 上一页底部
                self._page -= 1
                self._page_scroll = self._page_scroll_max(self._page)
                self._page_pan = QPointF(0.0, 0.0)
                self._show_page(self._page, 0)
            else:                                 # 首页顶部：停住
                self._page_scroll = 0.0
                self._place_page(self._page, 0.0)
        elif nxt > max_s:
            if self._page < self._max_page():     # 越过底部 -> 下一页顶部
                self._page += 1
                self._page_scroll = 0.0
                self._page_pan = QPointF(0.0, 0.0)
                self._show_page(self._page, 0)
            else:                                 # 末页底部：停住
                self._page_scroll = max_s
                self._place_page(self._page, 0.0)
        else:
            self._page_scroll = nxt
            self._place_page(self._page, 0.0)
        self._sw_target = self._page_scroll
        self._refresh_index()

    # ---- 单页等宽：平滑滚动（滚轮缓动 + 拖拽惯性） ----

    def _sw_scroll_by(self, delta: float):
        """平滑滚动 delta（>0 前进）。滚轮/键盘用；连滚时在目标值上叠加。"""
        running = self._sw_anim.state() == QAbstractAnimation.Running
        base = self._sw_target if running else self._page_scroll
        target = base + delta
        max_s = self._page_scroll_max(self._page)
        if target < 0.0:
            if self._page > 0:                    # 越过顶部 -> 上一页底部
                self._sw_anim.stop()
                self._page -= 1
                self._page_scroll = self._page_scroll_max(self._page)
                self._sw_target = self._page_scroll
                self._page_pan = QPointF(0.0, 0.0)
                self._show_page(self._page, 0)
                self._refresh_index()
            else:
                self._sw_animate_to(0.0)
            return
        if target > max_s:
            if self._page < self._max_page():     # 越过底部 -> 下一页顶部
                self._sw_anim.stop()
                self._page += 1
                self._page_scroll = 0.0
                self._sw_target = 0.0
                self._page_pan = QPointF(0.0, 0.0)
                self._show_page(self._page, 0)
                self._refresh_index()
            else:
                self._sw_animate_to(max_s)
            return
        self._sw_animate_to(target)

    def _sw_animate_to(self, target: float):
        """从当前偏移缓动到 target（OutCubic），距离越远时长越久、封顶。"""
        target = max(0.0, min(target, self._page_scroll_max(self._page)))
        self._sw_target = target
        cur = self._page_scroll
        self._sw_anim.stop()
        dist = abs(target - cur)
        if dist < 0.5:                            # 太近直接到位
            self._page_scroll = target
            self._place_page(self._page, 0.0)
            return
        self._sw_anim.setStartValue(float(cur))
        self._sw_anim.setEndValue(float(target))
        self._sw_anim.setDuration(max(90, min(420, int(120 + dist * 0.5))))
        self._sw_anim.start()

    def _on_sw_anim_value(self, v):
        self._page_scroll = float(v)
        self._place_page(self._page, 0.0)

    def _on_sw_anim_finished(self):
        # 补齐落点（最后一两帧可能没投递），与连续模式的 _on_anim_finished 同理
        self._page_scroll = self._sw_target
        self._place_page(self._page, 0.0)

    def _on_sw_kinetic(self):
        """拖拽松手后的惯性：位置 += 速度×dt，速度指数衰减，到边界停。"""
        dt = max(1, self._sw_clock.restart())
        self._sw_vel *= math.exp(-dt / 240.0)
        if abs(self._sw_vel) < 0.02:
            self._sw_kinetic.stop()
            return
        max_s = self._page_scroll_max(self._page)
        nxt = self._page_scroll + self._sw_vel * dt
        if nxt <= 0.0 or nxt >= max_s:            # 到边界直接停（不做回弹）
            self._page_scroll = max(0.0, min(max_s, nxt))
            self._place_page(self._page, 0.0)
            self._sw_kinetic.stop()
            return
        self._page_scroll = nxt
        self._place_page(self._page, 0.0)

    def _place_page(self, page: int, offset: float):
        """把第 page 页的 items 摆到"槽位位置 + 缩放平移 + offset×阅读方向向量"
        并显示。缩放用 item 的 scale 变换实现（几何仍是槽位大小，绘制时放大）；
        翻页动画/拖拽期间当前页和邻页各摆一次，实现两页同屏滑动。
        槽位/对齐按 page 取：首图单独模式的封面页走单页布局（整屏居中）。
        单页等宽模式额外把当前页按"宽度铺满 + 页内滚动"摆放。"""
        rdx, rdy = self._reading_dir_vec()
        z = self._zoom
        single_w = (self._mode == ReadMode.Samewight)
        if single_w and page == self._page:
            offset -= self._page_scroll          # 滚动偏移：内容整体沿阅读方向反移
        slots = self._page_slot_rects(page)
        aligns = self._page_slot_aligns(page)
        items = self._page_items(page)
        # 双页模式：同一页的两张图是朝中缝贴合的，中缝本身就是一条接缝，
        # 亚像素/取整同样可能露 1px 白线。让**前一张**（阅读顺序靠前的）沿
        # 对齐方向（= 朝中缝）多画 SEAM_OVERLAP，盖住中缝；后一张不动，避免
        # 两边都叠、把重叠量翻倍。单页/封面页只有一张图，对齐是居中 (0,0)，
        # 自然不加 pad。
        ov = self._seam_overlap
        double_seam = (self._is_double_mode() and len(items) == 2 and ov > 0)
        for i, it in enumerate(items):
            x, y, w, h = slots[i]
            al = aligns[i]
            it._fit = True                    # 等比缩放画进槽位（信箱留白）
            it._fit_align = al                # 双页朝中缝贴，单页/封面页居中
            if double_seam and i == 0:
                ax, ay = al                  # 对齐方向就是朝中缝的方向
                it.set_seam_pad((ov if ax < 0 else 0.0,    # left
                                 ov if ay < 0 else 0.0,    # top
                                 ov if ax > 0 else 0.0,    # right
                                 ov if ay > 0 else 0.0))   # bottom
            else:
                it.set_seam_pad((0.0, 0.0, 0.0, 0.0))
            if single_w:
                # 等宽：item 尺寸按真实宽高比；cross 轴始终居中（放大后溢出也对称），
                # 沿滚动轴短图居中、长图顶对齐再由 offset(=-滚动量) 滚动
                w, h = self._single_width_geometry(it)
                ln = (h if ReadMode.isUpDown(self._mode) else w) * z
                lead = (self._page_axis_len() - ln) / 2.0 if ln < self._page_axis_len() else 0.0
                if ReadMode.isUpDown(self._mode):
                    x = (self.viewport().width() - w * z) / 2.0
                    y = lead
                else:
                    x = lead
                    y = (self.viewport().height() - h * z) / 2.0
                it.set_geometry(w, h)
                it.setTransform(QTransform.fromScale(z, z))
                it.setPos(x + rdx * offset, y + rdy * offset)
                it.setVisible(True)
                continue
            it.set_geometry(w, h)
            dx, dy = self._page_slot_offset(w, h, al, page)
            it.setTransform(QTransform.fromScale(z, z))   # 缩放变换（z=1 即单位阵）
            it.setPos(x + rdx * offset + dx, y + rdy * offset + dy)
            it.setVisible(True)

    def _hide_page(self, page: int):
        """隐藏某一页的 items（翻页结束/拖拽换方向时收起）。"""
        for it in self._page_items(page):
            it.setVisible(False)

    def _show_page(self, page: int, anim_from: int = 0):
        """页模式核心：只显示第 page 页的 1~2 张图，其余 item 全部隐藏。
        sceneRect 恒等于视口 -> 滚动条 range 恒为 0，彻底没有滚动。
        anim_from：+1 从上一页位置滑入 / -1 从下一页位置滑回 / 0 直接显示。"""
        page = max(0, min(page, self._max_page()))
        if page != self._page:
            self._page_pan = QPointF(0.0, 0.0)   # 换页了：平移复位（新页从居中开始）
            self._page_scroll = 0.0              # 单页等宽：换页回到顶部
            self._sw_anim.stop()                 # 单页等宽：平滑滚动/惯性也停掉
            self._sw_kinetic.stop()
            self._sw_target = 0.0
            self._sw_drag_samples = []
        self._page = page
        if self._mode == ReadMode.Samewight:
            self._clamp_page_scroll(page)        # 视口/缩放变化后滚动量可能超界
            self._sw_target = self._page_scroll
        for it in self._items:
            it.setVisible(False)              # 全部隐藏，下面只摆当前页
        self._place_page(page, 0.0)
        self._scene.setSceneRect(0.0, 0.0,
                                 self.viewport().width(), self.viewport().height())
        if anim_from != 0 and self._items:
            # 翻页滑动：新页先摆在 ±L 处，旧页摆在原位，一起动画归位
            L = self._page_axis_len()
            self._start_page_slide(anim_from * L, 0.0, 0,
                                   page - anim_from, -anim_from * L)
        self._load_visible()

    def _flip_page(self, n: int):
        """翻 n 页（正=沿阅读方向前进）。带滑动动画；越界不动。"""
        if ReadMode.isScroll(self._mode) or n == 0 or not self._items:
            return
        tgt = self._page + n
        if tgt < 0 or tgt > self._max_page():
            return
        self._stop_page_anim()                # 上一场滑动先就地结束
        self._page = tgt                      # 页码先指向新页（动画摆的是新页）
        self._page_pan = QPointF(0.0, 0.0)    # 换页：平移复位（新页从居中开始）
        self._page_scroll = 0.0               # 单页等宽：新页从顶部开始
        L = self._page_axis_len()
        self._start_page_slide(n * L, 0.0, 0, tgt - n, -n * L)

    def _start_page_slide(self, from_o: float, to_o: float, shift: int,
                          neighbor, nb_delta: float):
        """页模式滑动动画：把"当前页偏移"从 from_o 缓动到 to_o。
        邻页（翻页时的旧页 / 拖拽时拖出的页）摆在 offset+nb_delta 跟随滑动。
        to_o=±L 表示完成翻页（shift=∓1，动画结束后平移页码）；to_o=0 弹回。"""
        self._page_anim.stop()
        self._page_anim_mode = "slide"
        self._page_anim_from = from_o
        self._page_anim_to = to_o
        self._page_anim_shift = shift
        self._page_anim_nb = neighbor
        self._page_anim_nb_delta = nb_delta
        self._page_anim.setStartValue(0.0)
        self._page_anim.setEndValue(1.0)
        self._page_anim.start()
        self._apply_page_slide(0.0)           # 立即摆好起始帧

    def _stop_page_anim(self):
        """立刻完成进行中的滑动动画（摆到终点收尾），供新翻页/切换前清理。
        注意 QVariantAnimation.stop() 不发 finished，收尾必须自己做。"""
        if self._page_anim.state() == QAbstractAnimation.Running:
            self._page_anim.stop()
            if self._page_anim_mode == "slide":
                self._apply_page_slide(1.0)
                self._finish_page_slide()
            return
        self._page_anim_mode = None

    def _on_page_anim_value(self, t):
        if self._page_anim_mode == "slide":
            self._apply_page_slide(t)

    def _apply_page_slide(self, t: float):
        """按进度 t∈[0,1] 摆放当前页和邻页（对偏移做插值）。"""
        o = self._page_anim_from + (self._page_anim_to - self._page_anim_from) * t
        self._place_page(self._page, o)
        nb = self._page_anim_nb
        if nb is not None and 0 <= nb <= self._max_page():
            self._place_page(nb, o + self._page_anim_nb_delta)

    def _on_page_anim_finished(self):
        if self._page_anim_mode == "slide":
            self._finish_page_slide()

    def _finish_page_slide(self):
        """滑动结束：完成翻页的平移页码；最终只留当前页归位显示。"""
        shift, self._page_anim_shift = self._page_anim_shift, 0
        self._page_anim_mode = None
        if shift:
            self._page = max(0, min(self._page + shift, self._max_page()))
        self._show_page(self._page, 0)

    def _cancel_page_gestures(self):
        """取消页模式的拖拽翻页/缩放平移/滑动动画（模式切换、resize 前调用）。"""
        self._page_dragging = False
        self._page_drag_start = None
        self._page_drag_neighbor = None
        self._page_panning = False
        self._stop_page_anim()
        # 单页等宽的平滑滚动/惯性/拖拽也一并停掉
        self._sw_anim.stop()
        self._sw_kinetic.stop()
        self._sw_drag_pos = None
        self._sw_drag_samples = []
        self._sw_vel = 0.0

    # ---- 页模式：拖拽翻页（拖出邻页，松手判定翻页/弹回） ----

    def _begin_page_drag(self, pos):
        self._stop_page_anim()                # 动画没放完就按下：就地结束
        self._page_dragging = True
        self._page_drag_start = QPointF(pos)
        self._page_drag_offset = 0.0
        self._page_drag_neighbor = None
        self._page_drag_samples = [(0.0, 0.0)]
        self._page_drag_clock.restart()
        self.viewport().setCursor(Qt.ClosedHandCursor)   # 抓手反馈

    def _page_drag_move(self, pos: QPointF):
        if self._page_drag_start is None:
            return
        dx = pos.x() - self._page_drag_start.x()
        dy = pos.y() - self._page_drag_start.y()
        rdx, rdy = self._reading_dir_vec()
        o = dx * rdx + dy * rdy       # 沿阅读方向的拖动量（>0 = 往回拖出上一页）
        L = self._page_axis_len()
        # 边界橡皮筋：第一页再往前拖 / 最后一页再往后拖，只给一部分阻力位移
        if (o > 0 and self._page <= 0) or (o < 0 and self._page >= self._max_page()):
            o *= self._scroller.PAGE_EDGE_RESIST
        self._page_drag_offset = o
        self._place_page(self._page, o)
        # 拖出方向上的邻页跟随
        nb = self._page - 1 if o > 0 else self._page + 1
        if nb != self._page_drag_neighbor:
            if self._page_drag_neighbor is not None:
                self._hide_page(self._page_drag_neighbor)   # 换方向：收起另一侧
            self._page_drag_neighbor = nb
        if 0 <= nb <= self._max_page():
            self._place_page(nb, o - (L if o > 0 else -L))
        # 采样测速（松手判定用，只留最近 120ms 窗口）
        t = float(self._page_drag_clock.elapsed())
        self._page_drag_samples.append((t, o))
        while len(self._page_drag_samples) > 2 and \
                t - self._page_drag_samples[0][0] > 120:
            self._page_drag_samples.pop(0)

    def _end_page_drag(self):
        self._page_dragging = False
        self._page_drag_start = None
        self.viewport().setCursor(Qt.ArrowCursor)
        o = self._page_drag_offset
        L = self._page_axis_len()
        # 松手速度（px/ms，最近 120ms 窗口估算）
        v = 0.0
        s = self._page_drag_samples
        if len(s) >= 2 and s[-1][0] - s[0][0] > 1:
            v = (s[-1][1] - s[0][1]) / (s[-1][0] - s[0][0])
        self._page_drag_samples = []
        # 判定：拖过一定比例，或甩动够快 -> 翻页；否则弹回原页
        th = self._scroller.PAGE_COMMIT_FRAC
        v_th = self._scroller.PAGE_FLICK_V
        commit = 0
        if o > L * th or v > v_th:
            commit = -1              # 往回拖（露出上一页）-> 上一页
        elif o < -L * th or v < -v_th:
            commit = 1               # 往前拖（露出下一页）-> 下一页
        if commit == -1 and self._page <= 0:
            commit = 0
        if commit == 1 and self._page >= self._max_page():
            commit = 0
        if commit == -1:
            self._start_page_slide(o, L, -1, self._page - 1, -L)
        elif commit == 1:
            self._start_page_slide(o, -L, 1, self._page + 1, L)
        else:
            nb = self._page_drag_neighbor
            if nb is None or not (0 <= nb <= self._max_page()):
                nb = None
            self._start_page_slide(o, 0.0, 0, nb, (-L if o > 0 else L))
        self._page_drag_neighbor = None
        self._refresh_index()               # 翻页/弹回判定已出，序号可能变了

    # ---- 页模式：自动翻页（页模式下 set_auto_scroll 的实现） ----

    def _start_page_auto(self, speed: float):
        """自动翻页：按 页长/速度 换算每页停留时长（600px 屏、300px/s = 2s/页）。"""
        if speed <= 0 or not self._items:
            self._stop_page_auto()
            return
        if not self._page_auto_on:          # 已开着时改速度：不重复发信号
            self._page_auto_on = True
            self.autoScrollChanged.emit(True)
        self._page_auto_speed = speed
        self._schedule_page_auto()

    def _schedule_page_auto(self):
        # L = max(1.0, self._page_axis_len())
        self._page_auto_timer.start(
            max(300, int(self._page_auto_speed * 1000)))

    def _on_page_auto(self):
        if self._page >= self._max_page():
            # self._stop_page_auto()    # 最后一页自动停
            self.qtTool.CloseScrollAndTurn()
            return

        if self._mode == ReadMode.Samewight:
            # 单页等宽：每次滚一屏，到边界自动翻页（保持连续滚动的手感）
            self._scroll_or_flip_page(max(1.0, self._page_axis_len()))
        else:
            self._flip_page(1)
        self._schedule_page_auto()

    def _stop_page_auto(self):
        self._page_auto_timer.stop()
        if self._page_auto_on:
            self._page_auto_on = False
            self.autoScrollChanged.emit(False)

    # ================ 模式/策略 ================

    def set_mode(self, index: int, isForce=False):
        """运行时切换阅读方向。用户停留在哪（按内容比例），切换后还在哪：
        记录当前 s/total 的比例 -> 重排 -> 按比例恢复位置。

        为什么要"待定位置"这套机制：切换会改滚动条方向/显隐，Qt 对 range 的
        更新是异步分批的（滚动条出现/消失会再触发一次 viewport 尺寸变化），
        期间 rangeChanged 会来好几次，每次都必须把位置按回去，否则会被
        中间态的 range 挤到开头或末尾。
        """
        mode = ReadMode(index)
        if mode == self._mode and not isForce:
            return
        self._reset_edge_counts()        # 切方向后重新算"到顶/到底"的连续次数
        # 切方向时把缩放重置为该方向的默认值（ttb=0.8，左右=1.0）。
        # 必须在 _update_cross / _show_page 之前改：cross 和页模式的 scale
        # 都直接吃 self._zoom。
        z0 = self.default_zoom_for()
        if abs(z0 - self._zoom) > 1e-9:
            self._zoom = z0
            self._sub_applied = float("nan")   # 缩放变了，亚像素 transform 要重设
            self.zoomChanged.emit(self._zoom)

        if not ReadMode.isScroll(mode):
            # 页模式切方向：不经过滚动条机制，重摆当前页即可
            # （双页的槽位方向跟着变：横排左右并排 <-> ttb 上下叠放）
            page = self._page
            self._mode = mode
            # 进页模式：清掉亚像素偏移（页模式不用 transform），显示锚点所在页
            self._sub = 0.0
            self._apply_sub_transform()
            self._cancel_page_gestures()
            self._scroller.stop()
            self._stop_page_auto()
            self._release_initial_hold()     # 切模式是用户操作：首屏校准到此为止
            self._anchoring = False
            self._apply_policies()
            self._update_cross()
            self._page_pan = QPointF(0.0, 0.0)   # 槽位方向变了，平移复位
            self._show_page(page, 0)
            return
        # 连续模式：记录当前阅读位置占内容的比例（0=第一张图，1=末端），
        # 切换后按比例恢复
        old_total = self._total
        frac = self._scroll_min_s() / old_total if old_total > 1 else 0.0
        self._mode = mode
        self._sub_applied = float("nan")   # 滚动轴变了，强制重设 transform
        self._anchoring = False
        # 切换期间滚动条 range 是异步更新的，用"待定位置"反复按住，
        # 稳定后再交还锚点逻辑（必须先占住再 stop：stop 内的静止吸附
        # 看到 pending 就会跳过，否则会起一个抢位置的吸附动画）
        self._pending_scroll_s = 0.0
        self._cancel_page_gestures()     # 终止页模式的拖拽/滑动动画
        self._stop_page_auto()

        self._scroller.stop()          # 切换方向时终止进行中的滚动动画/惯性
        self._release_initial_hold()     # 切模式是用户操作：首屏校准到此为止
        self._apply_policies()

        def restore():
            self._update_cross()               # 视口宽高互换，cross 要重算
            self._relayout_all()               # 全部 item 按新模式重新摆
            self._pending_scroll_s = frac * self._total
            self._apply_pending_scroll()       # 按比例恢复阅读位置
            self._load_visible()

        restore()
        QTimer.singleShot(0, restore)                # policy 改变 viewport 后再来一次
        QTimer.singleShot(150, self._finish_mode_switch)   # 150ms 后认为切换稳定

    def _apply_pending_scroll(self):
        """把位置按到待定值（模式切换期间，range 每变一次就按一次）。"""
        if self._pending_scroll_s is not None:
            self._set_scroll_min_s(self._pending_scroll_s)

    def _finish_mode_switch(self):
        """模式切换收尾（150ms 后）：清掉待定位置，恢复锚点逻辑。"""
        if self._pending_scroll_s is None:
            return
        self._pending_scroll_s = None
        self._was_at_end = self._at_end()
        self._anchoring = True
        self._load_visible()

    def _apply_policies(self):
        """按模式设置滚动条显隐和对齐方式。
        连续模式：滚动轴和 cross 轴都 AsNeeded——cross 轴平时内容恰好适配视口
        不出现，zoom>100% 内容变大后才出现（此时可拖拽平移，见 _pan_cross）。
        页模式：两根滚动条都常关——滚动条出现/消失会改变视口长度，
        页长（=视口长）跟着变就得全量重排，来回抖动；翻页有滚轮/键盘/拖拽够了。"""
        pol = Qt.ScrollBarAlwaysOff
        if ReadMode.isUpDown(self._mode):
            self.setHorizontalScrollBarPolicy(pol)
            self.setVerticalScrollBarPolicy(pol)
            self.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        else:
            self.setVerticalScrollBarPolicy(pol)
            self.setHorizontalScrollBarPolicy(pol)
            # 注意：不能用 AlignRight —— Qt 会把水平滚动条 range 变成负值区间，
            # 破坏 value<->场景坐标 的标准映射。RTL 用负坐标场景 + AlignLeft，
            # 内容不足一屏时靠 sceneRect 左侧留白实现右对齐（见 _update_scene_rect）
            self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    # ================ s 空间 <-> 滚动条 的统一接口 ================
    # 这四个方法是整个类的"模式无关层"：所有滚动/布局逻辑只跟 s 打交道，
    # 模式差异（哪个滚动条、坐标正负）全部封装在这里。

    def _bar(self):
        """当前模式的滚动条：ttb=竖条，横排=横条。"""
        return self.verticalScrollBar() if ReadMode.isUpDown(self._mode) \
            else self.horizontalScrollBar()

    def _viewport_len(self) -> float:
        """视口在滚动轴方向的长度 L（可见区域高/宽，像素）。"""
        return self.viewport().height() if ReadMode.isUpDown(self._mode) \
            else self.viewport().width()

    def _scroll_min_s(self) -> float:
        """当前视口可见区间的起始 s（阅读方向），含亚像素偏移。

        注意：QGraphicsView 滚动条的 value 就是视口左/上边缘的场景**绝对坐标**
        （不是相对 sceneRect.left() 的偏移），所以 RTL 场景的滚动条值是负数。
        滚动条只承载整数部分，小数部分在 self._sub 里。
        """
        if ReadMode.isUpDown(self._mode):
            return self.verticalScrollBar().value() + self._sub
        if ReadMode.isLeftRight(self._mode):
            return self.horizontalScrollBar().value() + self._sub
        # rtl: x = -s（s 向左递增），视口左缘 x_l = 滚动条值 v，
        # 阅读方向最前（最靠右）的可见 s = -(x_l + L)
        return -(self.horizontalScrollBar().value() + self._sub) - self._viewport_len()

    def _rtl_extent(self) -> float:
        """RTL 场景的水平跨度 M：内容不足一屏时补到一屏宽（实现右对齐）。"""
        return max(self._total, self._viewport_len())

    def _s_to_bar(self, s: float) -> float:
        """s 空间位置 -> 滚动条浮点值（三种模式的映射）。"""
        if ReadMode.isRightLeft(self._mode):
            return -(s + self._viewport_len())
        return s

    def _set_scroll_min_s(self, s: float, snap: bool = False):
        """写入滚动位置。snap=False 时启用亚像素渲染：整数部分进滚动条，
        小数部分进视图 transform——否则低速滚动时每帧位移被量化成
        1,2,1,2 像素交替，瞬时速度波动 ±50%（滚动"粘连感"来源之一）。
        ⚠️ 这里有两道防线，都是为了绕开 QGraphicsView 的一个坑：
        `setTransform` 会同步触发 Qt 的 updateScrollBars()，它**按新的 transform
        重新推导滚动条 range 和 value**，于是：
          1) 亚像素平移 |f| > 0.5 时，range 的 min/max 会整体挪 1px；
          2) 即使 |f| < 0.5，value 也可能（受上一帧 transform 残留影响）被挪 1px。
        表现就是用户看到的：setValue(4257) 之后 transform 一设，值又弹回 4256。
        RTL 的 `-(s+L)` 是负数，floor 很容易给出 _sub > 0.5，尤其容易中招。

        防线 1：整数部分用**四舍五入**把 _sub 控在 (-0.5, 0.5)，range 不偏移；
        防线 2：transform 之后把整数位**写回去**，抵消 value 的 ±1 漂移。
        位置语义不变：_scroll_min_s() 仍 = value + _sub = 原 s（误差 ≤1e-9）。"""
        L = self._viewport_len()
        s = max(0.0, min(s, max(0.0, self._total - L)))
        v = self._s_to_bar(s)
        if snap:
            self._sub = 0.0
            v = round(v)
        else:
            vi = int(round(v))
            sub = v - vi
            # 精确落在 ±0.5 正好是 range 会动的边界（LTR 的 +0.5 / RTL 的 -0.5），
            # 收进开区间：位置只差 1e-9，肉眼无感，但 range 不会偏。
            if abs(sub) >= 0.5 - 1e-9:
                sub = math.copysign(0.5 - 1e-9, sub)
            self._sub = sub
            v = vi
        bar = self._bar()
        bar.setValue(int(v))
        self._apply_sub_transform()
        # 防线 2：setTransform 可能让 updateScrollBars 把 value 挪 1px，写回去。
        # 此时 range 已经被防线 1 保住，所以这个 setValue 不会二次被夹。
        if bar.value() != int(v):
            bar.setValue(int(v))

    def _apply_sub_transform(self):
        """把亚像素偏移放进视图 transform（沿滚动轴平移 -f）。

        f = `_sub` ∈ (-0.5, 0.5)：滚动条停在整数 v，transform 再补上 v→v+f 的
        位移。**必须把 |f| 压在 0.5 以内**——Qt 的 setTransform 会触发
        updateScrollBars()，|f| > 0.5 时滚动条 range 会被整体挪 1px、value 被夹
        （见 _set_scroll_min_s 的注释）。"""
        if abs(self._sub - self._sub_applied) < 1e-9:
            return
        self._sub_applied = self._sub
        f = self._sub
        if ReadMode.isUpDown(self._mode):
            self.setTransform(QTransform(1, 0, 0, 1, 0, -f))   # y 轴平移
        else:
            self.setTransform(QTransform(1, 0, 0, 1, -f, 0))   # x 轴平移

    def _snap_to_pixel(self):
        """静止后吸附回整数像素：恢复设备像素对齐（边缘清晰、无重采样模糊）。"""
        if abs(self._sub) < 1e-6:
            return
        self._set_scroll_min_s(round(self._scroll_min_s()), snap=True)

    def _scroll_by_s(self, d: float):
        """相对滚动：当前位置 + d（自动钳制在 [0, total-L]）。"""
        self._set_scroll_min_s(self._scroll_min_s() + d)

    # ---- 缩放相关的坐标辅助（连续模式） ----

    def _cross_bar(self):
        """cross 轴的滚动条：ttb=横条（管左右），横排模式=竖条（管上下）。"""
        return self.horizontalScrollBar() if ReadMode.isUpDown(self._mode) \
            else self.verticalScrollBar()

    def _cross_view_len(self) -> float:
        """视口在 cross 轴方向的尺寸。"""
        return self.viewport().width() if ReadMode.isUpDown(self._mode) \
            else self.viewport().height()

    def _s_at_view_pos(self, p: QPointF) -> float:
        """视口坐标 p 下的内容点对应的 s（缩放锚点用）。
        视口坐标 -> 场景坐标只差一个亚像素偏移（_scroll_min_s 已含）。"""
        if ReadMode.isUpDown(self._mode):
            return self._scroll_min_s() + p.y()
        if ReadMode.isLeftRight(self._mode):
            return self._scroll_min_s() + p.x()
        # rtl：场景 x = 视口左缘 x + p.x()，而 s = -x（见模块注释）
        return -(self.horizontalScrollBar().value() + self._sub + p.x())

    def _anchor_at(self, s: float):
        """内容 s -> (item 序号, 图内位置比例)。缩放会全量重排（每张图的
        长度都变），用"(第几张图, 图内百分比)"才能跨重排表示同一个内容点。"""
        if not self._items:
            return (0, 0.0)
        for i, it in enumerate(self._items):
            if s < it._s + it._len + 1e-9:
                frac = (s - it._s) / it._len if it._len > 1e-9 else 0.0
                return (i, min(1.0, max(0.0, frac)))
        return (len(self._items) - 1, 1.0)

    def _s_of_anchor(self, idx: int, frac: float) -> float:
        """_anchor_at 的逆运算：(序号, 比例) -> 重排后的内容 s。"""
        if not self._items:
            return 0.0
        it = self._items[max(0, min(idx, len(self._items) - 1))]
        return it._s + frac * it._len

    def _relayout_keep_anchor(self):
        """重排并保持阅读位置（视口尺寸、DPI、缩放变化导致每张图长度都变时用）。

        为什么要"锚点"而不是直接沿用滚动条旧 value：重排后场景坐标没变，
        但每张图的长度变了，同一个 value 已经对应到完全不同的内容——会漂。
        锚点取视口中心：记下它落在"第几张图的哪个比例位置"，重排后把同一
        内容点挪回视口中心。"""
        p = QPointF(self.viewport().rect().center())
        s_old = self._s_at_view_pos(p)          # 锚点下的内容 s
        idx, frac = self._anchor_at(s_old)      # (第几张图, 图内比例)
        off = s_old - self._scroll_min_s()      # 锚点相对视口起点的偏移
        if not self._scroller.is_auto_scrolling():
            self._scroller.stop()               # 动画会和恢复的位置互相拉扯
        self._relayout_all()
        self._set_scroll_min_s(self._s_of_anchor(idx, frac) - off)
        self._was_at_end = self._at_end()
        self._load_visible()

    def _pan_cross(self, dx: float, dy: float):
        """拖拽时 cross 轴跟随平移（连续模式，zoom>100% 内容大于视口才有效，
        否则滚动条 range=0 直接跳过）。内容跟手：往右拖 -> 看到更左边的内容
        -> 滚动条值减小。"""
        if not ReadMode.isScroll(self._mode):
            return
        bar = self._cross_bar()
        if bar.maximum() <= bar.minimum():
            return
        d = -dx if ReadMode.isUpDown(self._mode) else -dy
        bar.setValue(int(bar.value() + round(d)))

    def _at_end(self) -> bool:
        """是否贴着内容末端（允许 2px 容差——亚像素偏移和取整误差）。"""
        return self._scroll_min_s() >= self._total - self._viewport_len() - 2

    def _on_range_changed(self, *_):
        """滚动条范围变化 = 内容长度变了。三种情况按优先级处理：
        1) 模式切换中 -> 按住待定位置（防止被中间态挤走）
        2) 滚轮动画正冲向末端 -> 重定向动画终点（内容变长终点跟着走）
        3) 本来就贴着末端 -> 追加内容后仍贴末端（刷微博式的体验）
        """
        if not ReadMode.isScroll(self._mode):
            return          # 页模式 sceneRect 恒等于视口、range 恒 0，无需锚点
        if self._initial_hold:
            # 首屏校准中：内容长度一变就把目标图重新对齐回去，优先级最高
            self._align_initial_target()
            return
        if self._pending_scroll_s is not None:
            # 模式切换中：range 每次跟上都把位置按住
            self._apply_pending_scroll()
            return
        if self._scroller.is_end_tracking():
            # 滚轮动画正冲向内容末端：内容变长则动画终点跟随（不在这里硬 set，
            # 否则和动画插值互相拉扯）
            self._scroller.retarget_end()
            return
        if self._anchoring and self._was_at_end:
            # 贴端锚点：原本在阅读方向末端，追加内容后仍贴末端
            self._set_scroll_min_s(self._total - self._viewport_len())

    # ================ 布局 ================

    def _snap_px(self, v: float) -> float:
        """对齐到设备像素网格。浮点布局坐标经四舍五入后，相邻图片边缘会落在
        半个物理像素上，绘制时露出背景形成白色细缝；所有坐标/长度对齐后消失。"""
        dpr = self.devicePixelRatioF()
        return round(v * dpr) / dpr

    def _update_cross(self):
        """按视口尺寸重算 cross（垂直于滚动轴的固定尺寸）。
        ttb：cross=视口宽（图片统一宽度）；横排：cross=视口高。
        再乘上缩放比：zoom 直接决定图片的固定边有多大。
        减 4 是给边框留的余量，>50 是防御没显示时的小尺寸。"""
        c = (self.viewport().width() if ReadMode.isUpDown(self._mode)
             else self.viewport().height())
        if c > 50:
            self._cross = self._snap_px(c * self._zoom)

    def _dims_for(self, it: ReadNewGraphicsItem):
        """根据模式和已知尺寸算 item 的 (w, h, 沿轴长度 len)。

        - 尺寸已知：len = cross × 宽高比（等比缩放，固定边=cross）
        - 尺寸未知：用兜底宽高比占位，探测到真实尺寸后 _correct_len 修正
        - len 钳制在 [cross×0.4, cross×MAX_ASPECT]：防止极端比例的图
          太扁（留条缝）或太长（占好几屏）破坏浏览体验
        - 所有长度经 _snap_px 对齐设备像素（无缝拼接的关键）
        """
        sz, cross = it._size, self._cross
        if ReadMode.isUpDown(self._mode):
            w = cross                              # 固定宽
            # 高宽比 h/w：已知用真实值，未知用兜底值
            r = (sz.height() / sz.width()) if (sz and sz.isValid() and sz.width() > 0) \
                else it._def_aspect
            h = self._snap_px(min(max(w * r, w * 0.4), w * self.MAX_ASPECT))
            return w, h, h                         # ttb：len = 高
        h = cross                                  # 固定高
        # 宽高比 w/h：已知用真实值；兜底 _def_aspect 是 h/w 所以取倒数
        r = (sz.width() / sz.height()) if (sz and sz.isValid() and sz.height() > 0) \
            else (1.0 / it._def_aspect)
        w = self._snap_px(min(max(h * r, h * 0.4), h * self.MAX_ASPECT))
        return w, h, w                             # 横排：len = 宽

    def _place(self, it: ReadNewGraphicsItem):
        """把 item 摆到场景坐标（s -> x/y 的模式映射，见模块注释）。"""
        if ReadMode.isUpDown(self._mode):
            it.setPos(0, it._s)
        elif ReadMode.isLeftRight(self._mode):
            it.setPos(it._s, 0)
        else:  # rtl：s 增大向左，item 占据 [-(s+len), -s]
            it.setPos(-(it._s + it._len), 0)
        self._apply_seam_pad(it)

    def _apply_seam_pad(self, it: ReadNewGraphicsItem):
        """连续模式下沿阅读方向多画 SEAM_OVERLAP 像素，盖住和下一张的接缝。

        方向 = 阅读前进方向：ttb 向下、ltr 向右、rtl 向左。最后一张不叠加
        （后面没有图，多画只会伸进空白区）。页模式一律清零（页内有留白，
        不存在接缝问题）。"""
        ov = self._seam_overlap
        if (ov <= 0 or not ReadMode.isScroll(self._mode)
                or not self._items or it is self._items[-1]):
            it.set_seam_pad((0.0, 0.0, 0.0, 0.0))
            return
        if ReadMode.isUpDown(self._mode):
            it.set_seam_pad((0.0, 0.0, 0.0, ov))     # 向下多画
        elif ReadMode.isLeftRight(self._mode):
            it.set_seam_pad((0.0, 0.0, ov, 0.0))     # 向右多画
        else:
            it.set_seam_pad((ov, 0.0, 0.0, 0.0))     # rtl：向左多画

    def _update_scene_rect(self):
        """手动维护 sceneRect（不让 Qt 自动扩展——自动扩展会重算滚动位置导致抖动）。"""
        c = self._cross
        if ReadMode.isUpDown(self._mode):
            self._scene.setSceneRect(0, 0, c, self._total)
        elif ReadMode.isLeftRight(self._mode):
            self._scene.setSceneRect(0, 0, self._total, c)
        else:
            # rtl：内容在 [-total, 0]；不足一屏时左侧补空到 -L，保证右对齐
            m = self._rtl_extent()
            self._scene.setSceneRect(-m, 0, m, c)

    def _relayout_all(self):
        """全量重排：所有 item 从 s=0 依次排开。用于模式切换/窗口 resize。
        页模式没有"排开"——只重摆当前页（翻页器语义）。"""
        if not ReadMode.isScroll(self._mode):
            self._show_page(self._page, 0)
            self.viewport().update()      # 见下面的说明
            return
        for it in self._items:
            it._fit = False                   # 回到连续模式：拉伸填满（不留白）
            it.setVisible(True)               # 页模式隐藏过的 item 全部恢复
            it.setTransform(QTransform())     # 清掉页模式的缩放变换（连续模式不用）
        s = 0.0
        for it in self._items:
            w, h, ln = self._dims_for(it)
            it.set_geometry(w, h)
            it._len = ln
            it._s = self._snap_px(s)          # 每张图的起点也做像素对齐
            self._place(it)
            s = self._snap_px(s + ln + self._gap)
        self._total = s
        self._update_scene_rect()
        # 内容变短/变窄后"多露出来"的那圈区域不在 Qt 自己算的脏区域里：
        # item 尺寸变化通知的是"旧矩形∪新矩形"，两侧新露出的部分不在其中。
        # 显式全量重绘一次，让 drawBackground 用背景色把它们擦掉，
        # 否则那里会一直留着上一帧的像素（就是滚动/缩放时看到的"残影"）。
        self.viewport().update()

    # ================ 添加图片 ================

    def init_all_image(self, maxNum, curIndex):
        if not maxNum:
            return

        for item in self._items:
            self._scene.removeItem(item)
            ReadNewPoolManager().AddProxyItem(item)
        self._items = []
        self._total = 0.0
        self._first_show = True
        for i in range(maxNum):
            self.add_image(i)
        self._first_show = False
        # self.set_mode(self._mode.value, isForce=True)
        if maxNum > curIndex >= 0:
            self.set_initial_index(curIndex)
        elif curIndex >= maxNum:
            self.set_initial_index(maxNum)
        else:
            self.set_initial_index(0)

    def add_image(self, index: int, est_size: QSize = None):
        """追加一张图片到流的末尾。

        est_size：可选的预估尺寸 (w,h)。如果后端 API 能直接给出图片宽高
        （或 CDN 响应头里有），传进来可以让 item 一步到位准确占位，
        完全跳过"探测->修正"环节——零跳动的最优解。不传则按兜底宽高比占位。
        """
        it = ReadNewPoolManager().GetProxyItem()
        it.index = index
        if est_size is not None and est_size.isValid():
            it._size = QSize(est_size)
            it._size_known = True
        if not ReadMode.isScroll(self._mode):
            # 页模式：新图先隐藏挂进场景，翻到它所在页才显示
            new_page = self._page_of_index(len(self._items))   # 它将会落在的页
            x, y, w, h = self._page_slot_rects(new_page)[-1]
            it._fit = True
            it._fit_align = self._page_slot_aligns(new_page)[-1]  # 占位框也对齐
            it.setTransform(QTransform.fromScale(self._zoom, self._zoom))
            it.set_geometry(w, h)
            it.setPos(x, y)
            it.setVisible(False)
            self._scene.addItem(it)
            self._items.append(it)
            # 新图正好落在当前页（边加载边追加的最后一页）：刷新显示
            if self._page_of_index(len(self._items) - 1) == self._page:
                self._show_page(self._page, 0)
            else:
                self._refresh_index()       # 没落到当前页也要刷新（总数变了）
            return
        w, h, ln = self._dims_for(it)
        it.set_geometry(w, h)
        it._s = self._snap_px(self._total)     # 新图接在末尾（已有内容位置不动）
        it._len = ln
        self._place(it)
        self._scene.addItem(it)
        self._items.append(it)
        # 追加后"最后一张"变了：新图不该再叠加（后面没图），原来的最后一张
        # 现在要叠加了（它下面接了新图）。_place 是在 append 之前调用的，
        # 那时 it 还不是 _items[-1]，所以这里必须重算这两张的 pad。
        if len(self._items) >= 2:
            self._apply_seam_pad(self._items[-2])
        self._apply_seam_pad(it)
        self._total = self._snap_px(self._total + ln + self._gap)
        self._update_scene_rect()


    # ================ 惰性加载：预下载（按序号）/ 预解码（按视窗） ================

    # def set_prefetch_range(self, back: int, ahead: int):
    #     """设置预下载范围：以当前页 _cur_idx 为基准，往前/往后各预取几张图。
    #
    #     与视窗大小无关——一屏里可能只有 1 张长图、也可能有 10 张小图，按张数
    #     预取才能保证翻到下一张时它已经下好。改完立即触发一次加载。"""
    #     self._prefetch_back = max(0, int(back))
    #     self._prefetch_ahead = max(0, int(ahead))
    #     self._load_visible()
    #
    # def prefetch_range(self):
    #     """当前预下载范围 (back, ahead)，单位：张。"""
    #     return (self._prefetch_back, self._prefetch_ahead)

    # ---- 到顶/到底后"再滚 N 下"触发（接上/下一章等） ----

    def set_seam_overlap(self, px: float):
        """设置连续模式相邻两张的绘制叠加量（逻辑像素，默认 SEAM_OVERLAP=1）。

        只影响绘制：每张图沿阅读方向多画 `px` 像素、盖到下一张的起始处，
        用来消除亚像素滚动/设备像素取整偶尔露出的 1px 白缝。布局（_s/_len/
        总长度）完全不变，所以不会累积偏移。0 = 关闭。"""
        self._seam_overlap = max(0.0, float(px))
        self._relayout_all()        # 重新应用每张图的 pad
        self._load_visible()

    def seam_overlap(self) -> float:
        """当前接缝叠加量（逻辑像素，0 = 关闭）。"""
        return self._seam_overlap

    def set_edge_scroll_trigger(self, count: int):
        """设置"已经在最前/最后，再往外滚几下"触发一次信号（<=0 关闭）。

        触发的是 scrolledPastStart / scrolledPastEnd 两个信号，本 Demo 不消费，
        用来接"加载上一章 / 下一章"这类逻辑。"""
        self._edge_scroll_trigger = max(0, int(count))
        self._reset_edge_counts()

    def edge_scroll_trigger(self) -> int:
        """当前的触发次数阈值（0 = 关闭）。"""
        return self._edge_scroll_trigger

    def _reset_edge_counts(self):
        self._edge_start = 0
        self._edge_end = 0

    def _at_content_start(self) -> bool:
        """阅读位置是否已经在最前（第一张图 / 第一页 / 单页等宽的页首）。"""
        if not ReadMode.isScroll(self._mode):
            if self._page > 0:
                return False
            if self._mode == ReadMode.Samewight:
                return self._page_scroll <= 0.5
            return True
        return self._scroll_min_s() <= 0.5

    def _at_content_end(self) -> bool:
        """阅读位置是否已经在最后（最后一张图 / 最后一页 / 单页等宽的页尾）。"""
        if not ReadMode.isScroll(self._mode):
            if self._page < self._max_page():
                return False
            if self._mode == ReadMode.Samewight:
                return self._page_scroll >= self._page_scroll_max(self._page) - 0.5
            return True
        hi = max(0.0, self._total - self._viewport_len())
        return self._scroll_min_s() >= hi - 0.5

    def _note_edge_scroll(self, forward: bool, at_start: bool, at_end: bool):
        """记一次滚轮/键盘"滚动"。已经在边界还继续往外滚就累加，到阈值发信号。

        at_start/at_end 是**滚之前**的边界状态：这样"刚好翻到最后一页"的那一下
        不算越界，只有之后继续往外的滚动才开始累加。"""
        if self._edge_scroll_trigger <= 0:
            return
        if forward:                       # 往阅读方向（最后面）滚
            if at_end:
                self._edge_end += 1
                self._edge_start = 0
                if self._edge_end >= self._edge_scroll_trigger:
                    self._edge_end = 0
                    self.scrolledPastEnd.emit()
            else:
                self._reset_edge_counts()
        else:                             # 往反方向（最前面）滚
            if at_start:
                self._edge_start += 1
                self._edge_end = 0
                if self._edge_start >= self._edge_scroll_trigger:
                    self._edge_start = 0
                    self.scrolledPastStart.emit()
            else:
                self._reset_edge_counts()

    def _load_visible(self):
        """刷新当前序号/动图，然后做两件互不影响的事：

        1) 预下载：以 _cur_idx 为中心、[_cur_idx-前, _cur_idx+后] 的**序号窗口**
           发起请求（跟视窗多大无关，提前把后面的图拉下来）；
        2) 预解码：视窗 ±1.5/2.5 屏（连续）或当前页 ±1 页（页模式）的**视窗窗口**
           里，把"已下完但还没解码"的图丢给线程池解码。

        下载和预解码解耦是刻意的：下载慢（网络）要提前很多；解码出来的位图很占
        内存（一张 4K 解码后几十 MB），所以只解视窗附近的，滚到附近再解。

        顺带在这里刷新"当前是第几张图"：滚动/翻页/模式切换/追加图片最终都会
        走到这个方法（滚动时每帧都进）。"""
        self._last_load_s = self._scroll_min_s()
        # 可见集合只算一次，_refresh_index/_refresh_playing 复用；页模式且没动图时
        # 两边都用不到，干脆不算（省一次 visible_indices）。
        vis = self.visible_indices() if (
            ReadMode.isScroll(self._mode) or self._anims) else None
        self._refresh_index(vis)
        self._refresh_playing(vis)            # 可见集合变了：该播的播、该停的停
        self._download_around_current()       # 预下载：按序号
        self._decode_visible()                # 预解码：按视窗

    def _download_around_current(self):
        """预下载：[_cur_idx - back, _cur_idx + ahead] 之内、还没下过的图。"""
        n = len(self._items)
        if n == 0:
            return
        cur = self._cur_idx if self._cur_idx >= 0 else max(0, self.current_index())
        _prefetch_back = Setting.PicturePrefetchFrontCount.value
        _prefetch_ahead = Setting.PicturePrefetchCount.value
        lo = max(0, cur - _prefetch_back)
        hi = min(n - 1, cur + _prefetch_ahead)
        for i in range(lo, hi + 1):
            self._maybe_download(self._items[i])

    def _decode_visible(self):
        """预解码：视窗窗口内"已下完但还没解码"的图 -> 丢给线程池。"""
        if not ReadMode.isScroll(self._mode):
            for p in (self._page - 1, self._page, self._page + 1):
                if 0 <= p <= self._max_page():
                    for it in self._page_items(p):
                        self._start_decode_if_ready(it)
            return
        front = Setting.PictureShowFrontCount.value
        after = Setting.PictureShowCount.value
        # L = self._viewport_len()
        # s0 = self._scroll_min_s()
        # top, bottom = s0 - L * 1.5, s0 + L * 2.5
        curIdx = self._cur_idx
        for it in self._items[max(0,curIdx - front):curIdx + after+1]:
            # if it._s > bottom:
            #     break                        # 后面的都更远，不用看了
            # if it._s + it._len < top:
            #     continue                     # 在窗口上方（已滚过）
            self._start_decode_if_ready(it)

    def _maybe_download(self, it: ReadNewGraphicsItem):
        """需要的话发起下载（没下过/没在下载/没在解码/没失败过）。"""
        if it.pixmap is not None or it._reply is not None \
                or it._decoding or it._failed:
            return
        if it._buf:
            return                           # 已经下完，等预解码窗口触发，别重复下
        self._start_download(it)

    def _start_decode_if_ready(self, it: ReadNewGraphicsItem):
        """条件满足就丢给线程池解码：已下完（_buf 非空）、没在解码、没失败。"""
        isForce = False
        if it.is_need_waifu2x and not it._cur_is_waifu2x_px:
            isForce = True
        if not it.is_need_waifu2x and it._cur_is_waifu2x_px:
            isForce = True

        if it._failed:
            return
        if it._decoding:
            return
        if not isForce and (it.pixmap is not None and not it.pixmap.isNull()):
            return
        if it.is_need_waifu2x and not it._waifu_buf:
            if it._waifu_reply is None and it._buf:
                self._start_waifu2x(it)
            return
        if not it._buf:
            return
        if not isForce and not it._pending_decode:
            return                           # 没有新字节（已解过 / 还没下完）

        Log.Info(f"Start decode, index{it.index}, is_force:{isForce}, is_waifu:{it.is_need_waifu2x}")
        it._decoding = True
        toW, toH = 0, 0
        it.update()                          # 立刻显示"解码中…"
        if it.isAnima:
            self._on_animated(it, it._size, it._buf)
        elif it.is_need_waifu2x:
            size = self._decode_target_size(it)
            toW, toH = self._get_decode_to_size(size, it.waifu_file_data)
            self.read_task.AddQImageTask(it._waifu_buf, self.devicePixelRatioF(), toW, toH, Qt.IgnoreAspectRatio,
                                         callBack=self._on_loaded, backParam=(it.index, True))
        else:
            size = self._decode_target_size(it)
            toW, toH = self._get_decode_to_size(size, it.file_data)
            self.read_task.AddQImageTask(it._buf, self.devicePixelRatioF(), toW, toH, Qt.IgnoreAspectRatio, callBack=self._on_loaded, backParam=(it.index, False))

    def _maybe_decode(self, it: ReadNewGraphicsItem):
        """下载刚完成时调用：只有落进"预解码窗口"才立刻解，否则留着字节等滚到附近。"""
        curIdx = self._cur_idx
        front = Setting.PictureShowFrontCount.value
        after = Setting.PictureShowCount.value
        if curIdx - front <= it.index <= curIdx+after:
        # if self._in_decode_window(it):
            self._start_decode_if_ready(it)

    # def _in_decode_window(self, it: ReadNewGraphicsItem) -> bool:
    #     """这张图是否落在当前"预解码窗口"内（视窗 ±1.5/2.5 屏，或页模式 ±1 页）。"""
    #     if not ReadMode.isScroll(self._mode):
    #         try:
    #             idx = self._items.index(it)
    #         except ValueError:
    #             return False
    #         return abs(self._page_of_index(idx) - self._page) <= 1
    #     L = self._viewport_len()
    #     s0 = self._scroll_min_s()
    #     return (it._s + it._len >= s0 - L * 1.5) and (it._s <= s0 + L * 2.5)

    # ---- 解码位图 / 压缩字节的 LRU 回收（200 张大图也不会把内存吃光）----

    def _trim_caches(self):
        """按预算回收位图/压缩字节：离当前页最远的先丢，当前可见的永远不动。"""
        self._trim_pixmaps()
        self._trim_pixmaps_max_len()
        # self._trim_buffers()

    def _trim_pixmaps(self):
        """已解码位图超预算 -> 从离当前页最远的开始回收 pixmap（压缩字节留着）。

        回收后置 `_pending_decode=True`：等它再次滚进预解码窗口时用 `_buf` 重新
        解码，不需要重新下载。当前屏幕上可见的、以及动图（`_raw` 有自己的预算）
        都不动。"""
        budget = self.PIXMAP_BUDGET_MB * 1024 * 1024
        keep = set(self.visible_indices())     # 当前屏幕上真正可见的：绝不回收
        total = 0
        cands = []
        for i, it in enumerate(self._items):
            if it.pixmap is None:
                continue
            total += it.pixmap.width() * it.pixmap.height() * 4   # RGBA 每像素 4 字节
            if i not in keep and not it.is_animated:
                cands.append((i, it))
        if total <= budget:
            return
        cur = self._cur_idx if self._cur_idx >= 0 else 0
        cands.sort(key=lambda t: -abs(t[0] - cur))   # 离得越远越先丢
        for i, it in cands:
            if total <= budget:
                break
            total -= it.pixmap.width() * it.pixmap.height() * 4
            it.pixmap = None
            if it._buf:
                it._pending_decode = True         # 有字节：滚回来能直接重解
            it.update()
            Log.Info(f"free over budget pixmap, {it.index}")

    def _trim_pixmaps_max_len(self):
        """已解码位图超预算 数量限制"""
        # min_budget = 5
        # max_budget = 10
        keep = set(self.visible_indices())     # 当前屏幕上真正可见的：绝不回收
        # min_cands = []
        max_cands = []
        curIdx = self._cur_idx
        front = Setting.PictureShowFrontCount.value
        after = Setting.PictureShowCount.value
        for i, it in enumerate(self._items):
            if it.pixmap is None:
                continue
            if i in keep or it.is_animated:
                continue
            if not (curIdx - front <= it.index <= curIdx+after):
                max_cands.append((i, it))

        if len(max_cands) <= 0:
            return
        cur = self._cur_idx if self._cur_idx >= 0 else 0
        max_cands.sort(key=lambda t: -abs(t[0] - cur))   # 离得越远越先丢
        for i, it in max_cands:
            it.pixmap = None
            if it._buf:
                it._pending_decode = True         # 有字节：滚回来能直接重解
            it.update()
            Log.Info(f"free over index pixmap, {it.index}")

    # def _trim_buffers(self):
    #     """压缩字节超预算 -> 从离当前页最远的开始丢（丢了之后要用会重新下载）。"""
    #     budget = RAW_BUDGET_MB * 1024 * 1024
    #     total = 0
    #     cands = []
    #     for i, it in enumerate(self._items):
    #         if it._buf.isEmpty() or it.is_animated:
    #             continue
    #         total += it._buf.size()
    #         cands.append((i, it))
    #     if total <= budget:
    #         return
    #     cur = self._cur_idx if self._cur_idx >= 0 else 0
    #     cands.sort(key=lambda t: -abs(t[0] - cur))
    #     for i, it in cands:
    #         if total <= budget:
    #             break
    #         if it._decoding:
    #             continue                          # 正在解码用的字节不能删
    #         total -= it._buf.size()
    #         it._buf = QByteArray()
    #         it._pending_decode = False
    #         it.update()                           # 没位图的话会显示"等待加载…"

    def _start_download(self, item: ReadNewGraphicsItem):
        """发起 HTTP GET，挂接回调：有新数据（探测尺寸）/进度/下载完成（不立刻解码）。"""
        if self._first_show:
            return
        Log.Info(f"Start download, index{item.index}")
        if item._buf:
            item._reply = 0
            self._on_finished(item.file_data, Str.Ok, item.index)
        else:
            taskId = self.read_task.AddDownload(item.index,
                                           downloadCallBack=self._on_download_progress,
                                           completeCallBack2=self._on_finished)

            item._reply = taskId
            item._progress = None            # 请求刚发出、还不知道总大小：先转圈
            self._spin_timer.start()         # 有下载在跑就保持转圈动画可用
            self.update_tool_label(item.index)
            item.update()

    def _on_download_progress(self, got: int, total: int, index: int):
        """下载进度回调。total > 0（响应带 Content-Length）时换算成 0~1 的确定
        进度；total < 0（chunked，没有总大小）保持 None，进度环转圈表示"在动"。
        只 update 请求重绘，不动几何——进度变化绝不能影响布局。"""
        if index >= len(self._items):
            return
        item = self._items[index]
        if item.pixmap is not None:
            return
        if total > 0:
            item._progress = max(0.0, min(1.0, got / float(total)))
        else:
            item._progress = max(0.0, min(1.0, got / float(10000)))
            if not self._spin_timer.isActive():
                self._spin_timer.start()
        item.update()

    def _on_spin(self):
        """推进不确定态进度环的相位并请求重绘；没有"未知进度且仍在下载"的
        item 时自动停掉定时器（_on_download_progress 会在需要时重新拉起）。"""
        ReadNewGraphicsItem.SPIN_PHASE = (ReadNewGraphicsItem.SPIN_PHASE + ReadNewGraphicsItem.SPIN_STEP) % 1.0
        alive = False
        for it in self._items:
            if it.pixmap is None and it._reply is not None and it._progress is None:
                alive = True
                it.update()          # 离屏 item 的 update 只打标记，开销可忽略
        if not alive:
            self._spin_timer.stop()

    # def _on_ready_read(self, item: ReadNewGraphicsItem):
    #     """网络数据分块到达（一张图可能来好几次）。把新数据追加进缓冲，
    #     并尝试用"已有的前几百字节"探测图片尺寸——不用等整张图下载完。"""
    #     reply = item._reply
    #     if reply is None:
    #         return
    #     item._buf += reply.read(reply.bytesAvailable())
    #     self._try_probe_size(item)

    def _try_probe_size(self, item: ReadNewGraphicsItem, fileData: FileData):
        """数据够多时解析文件头拿宽高（PNG/JPEG 的宽高都在文件头最前面）。
        拿到就立即修正布局——用户看到占位框变成正确高度通常只滞后几毫秒。"""
        if item._size_known:
            return
        item.isAnima = fileData.isAnima
        item.fmt = fileData.fmt
        sz = QSize(fileData.w, fileData.h)
        if sz is not None:
            self._correct_len(item, sz)

    def _on_finished(self, fileData: FileData, st: int, index: int):
        """下载结束：成功 -> 丢给线程池后台解码；失败 -> 标记失败。"""
        if index >= len(self._items):
            return
        item = self._items[index]

        reply = item._reply
        if reply is None:
            return
        if st != Str.Ok:
            # 重新下载
            item._reply = None
            item._re_download_cnt += 1
            item._progress = None
            item.update()                    # 触发重画（占位框变红显示"加载失败"）
            self._start_download(item)
            return

        reply, item._reply = item._reply, None
        item.file_data = fileData

        self._try_probe_size(item, fileData)           # 兜底：万一中途一直没探测到
        item._pending_decode = True          # 有新字节等着解
        item.update()
        if item.is_need_waifu2x:
            model = ToolUtil.GetLookScaleModel(self.read_view.category, item._size.width(), item._size.height(), item.fmt)
            if not model or item.isAnima:
                item._waifu2x_state = -1
            else:
                self._start_waifu2x(item)
                return
        self._maybe_decode(item)             # 在视窗窗口里就立刻解，否则等滚到附近
        self.update_tool_label(item.index)

            # from view.read.read_new_task import DecodeTask
            # task = DecodeTask(item.index, item._buf, max_px, dpr)
            # task.signals.loaded.connect(self._on_loaded)
            # QThreadPool.globalInstance().start(task)

    # def _on_loaded(self, index, real: QSize, img: QImage):
    #     """后台解码完成（主线程槽）：修正布局 + 像素填进固定矩形。"""
    #     if index >= len(self._items):
    #         return
    #     item = self._items[index]
    #     if not item._size_known:
    #         self._correct_len(item, real)    # 探测也没拿到过的最后兜底
    #     # QPixmap 只在主线程创建（严格模式，跨平台零风险）；
    #     # dpr 已设在 QImage 上，fromImage 会保留
    #     item.pixmap = QPixmap.fromImage(img)
    #     item.update()

    def _start_waifu2x(self, item: ReadNewGraphicsItem):
        """发起 HTTP GET，挂接回调：有新数据（探测尺寸）/进度/下载完成（不立刻解码）。"""
        if self._first_show:
            return
        if not item._buf:
            return

        Log.Info(f"Start waifu2x, index{item.index}")
        if item.waifu_file_data:
            item._waifu_reply = 0
            self._on_waifu_finished(item.waifu_file_data, 0, item.index, item._waifu_tick)
        else:
            item._progress = None  # 请求刚发出、还不知道总大小：先转圈
            model = ToolUtil.GetLookScaleModel(self.read_view.category, item._size.width(), item._size.height(), item.fmt)
            if not model or item.isAnima:
                item._waifu2x_state = -1
                self._maybe_decode(item)
            else:
                item._waifu_reply = self.read_task.AddCovertData(item.index, item._buf, model, self._on_waifu_finished)

            self.update_tool_label(item.index)
            item.update()

    def _on_waifu_finished(self, fileData: FileData, waifuId, index, tick):
        if index >= len(self._items):
            return
        item = self._items[index]

        reply = item._waifu_reply
        if reply is None:
            return
        if not fileData or not fileData.data:
            item._waifu_failed = True
            item._waifu_reply = None
            item.update()                    # 触发重画（占位框变红显示"加载失败"）
            return

        reply, item._waifu_reply = item._waifu_reply, None
        item.waifu_file_data = fileData
        item._waifu_tick = tick
        self._try_probe_size(item, fileData)           # 兜底：万一中途一直没探测到

        if item.isAnima:
            self._on_animated(item, item._size, QByteArray(fileData.data))
        else:
            self._maybe_decode(item)

    @time_me
    def _on_loaded(self, img: QImage, v):
        """后台解码完成（主线程槽）：修正布局 + 像素填进固定矩形。"""
        (index, isWaifu2x) = v
        if index >= len(self._items):
            return
        item = self._items[index]
        if img.isNull():
            self._on_decode_failed(item)
            return

        Log.Info(f"finish decode, index{index}, size:{img.size()}, is_waifu:{isWaifu2x}")
        item._progress = None
        item._decoding = False
        item._pending_decode = False
        item._cur_is_waifu2x_px = isWaifu2x
        # 注意：压缩字节 _buf **不释放**。位图会被 _trim_pixmaps 按预算回收，
        # 回收后靠这份字节重新解码（不用重新下载）；总量由 _trim_buffers 兜底。

        if not item._size_known:
            self._correct_len(item, QSize(img.width(), img.height()))    # 探测也没拿到过的最后兜底
        # QPixmap 只在主线程创建（严格模式，跨平台零风险）；
        # dpr 已设在 QImage 上，fromImage 会保留

        self.update_tool_label(item.index)
        item.pixmap = QPixmap.fromImage(img)
        item.update()                        # 只请求重绘，几何不动 -> 无跳动
        self._trim_caches()                  # 位图可能超预算：回收离当前页最远的

    def _on_decode_failed(self, item: ReadNewGraphicsItem):
        """解码失败：清状态并标记失败，避免卡在"解码中"或被反复重试。"""
        item._decoding = False
        item._failed = True
        item._pending_decode = False
        item.update()

    # ================ 长度修正：平移后续内容 + 滚动补偿（s 空间，模式无关） ================

    def _correct_len(self, item: ReadNewGraphicsItem, image_size: QSize):
        """拿到图片真实尺寸后，把它的占位长度修正为准确值。

        做三件事保证"不跳动"：
        1) 这张图自己改尺寸；
        2) 阅读顺序在它之后的图整体平移 delta（delta=新长-旧长，可正可负）；
        3) 关键补偿：修正会推移视口里的内容，滚动位置必须同步平移，画面才
           纹丝不动。平移量 = delta × 视口顶在这张图里的"完成度" f（见下面
           的详细推导）——不是简单的"补 / 不补"。
        """
        item._size = QSize(image_size)
        item._size_known = True
        if not ReadMode.isScroll(self._mode):
            # 页模式槽位一般由视口决定、真实尺寸只影响绘制；但"单页等宽"的
            # 页面高度是按真实宽高比算的，尺寸一到就必须重摆当前页，否则会
            # 一直停在兜底比例（1.2）上，高度/可滚动范围都不对。
            if self._mode == ReadMode.Samewight \
                    and item in self._page_items(self._page):
                self._clamp_page_scroll(self._page)
                self._place_page(self._page, 0.0)
            return
        w, h, ln = self._dims_for(item)
        old_len = item._len  # 旧长度：判断"是否已滚过"要用它（见下）
        delta = ln - old_len  # 长度变化量（正=变长）
        if abs(delta) < 0.5:  # 不到半个像素：无感知，不用动
            return
        item.set_geometry(w, h)
        item._len = ln
        self._place(item)

        for other in self._items:  # 阅读顺序在后的 item 整体平移
            if other._s > item._s:
                other._s = self._snap_px(other._s + delta)
                self._place(other)
        self._total = self._snap_px(self._total + delta)

        # ---- 补偿：视口顶那一行像素原地不动 ----
        # 设视口顶 s0 在这张图里的相对位置 f = (s0 - 图的起点) / 旧长度：
        #   f <= 0  视口还在这张图之前：它之后的图平移了，但视口看不到 -> 不补
        #   0<f<1   视口停在这张图内部：这张图被拉长/压缩后，原本在视口顶的
        #           那一行像素跑到了 s0 + f×delta -> 补 f×delta（**按比例**）
        #   f >= 1  整张已滚过：它之后的所有内容整体平移了 delta -> 全额补 delta
        # 早期版本只有"全额补 / 不补"两种（条件是"图起点 < 视口顶"），视口停在
        # 图里时画面必然跳一段（(1-f)×delta 或 f×delta）——加载途中连续修正，
        # 表现就是滚动"一顿一顿"。按比例补则视口顶那一行始终原地不动。
        # 另外必须在 _update_scene_rect 之前做：setSceneRect 会让 Qt 自己动一次
        # 滚动条（Qt 的 updateScrollBars 会按新 range 重新夹一次 value），那次
        # 改动会同步触发 scrollContentsBy -> _load_visible -> 观测到"还没补偿"
        # 的中间态，表现为 current_index 一闪（7->6->7）。先补偿再更新
        # sceneRect，中间态就不会被任何人看到。
        s0 = self._scroll_min_s()
        f = 0.0 if old_len <= 1e-6 else (s0 - item._s) / old_len
        f = min(1.0, max(0.0, f))
        comp = delta * f
        if abs(comp) >= 0.5:  # 不到半像素：无感知，不折腾滚动条
            self._scroll_by_s(comp)
            # 同步滚动器的内部位置（自动滚动的 _auto_pos / 动画目标），
            # 否则下个 tick 会把滚动条拉回旧值 -> 内容回跳一下再前进（粘连感）
            self._scroller.on_viewport_shifted(comp)
        self._update_scene_rect()

    # ================ 事件 ================

    def wheelEvent(self, ev):
        # 任意滚轮操作停止自动滚动/自动翻页
        # self._scroller.stop_auto()
        # self._stop_page_auto()
        self.qtTool.CloseScrollAndTurn()
        self._release_initial_hold()
        # 三种模式统一：滚轮/触控板 -> 阅读方向位移
        ad = ev.angleDelta()          # 滚轮增量：一格 = y 方向 ±120
        if ReadMode.isUpDown(self._mode):
            d = ad.y()                # 上下模式：直接用竖直滚轮
        else:
            # 横排模式：竖滚轮和触控板横向手势都映射到阅读方向
            d = ad.y() if abs(ad.y()) >= abs(ad.x()) else -ad.x()
        if d == 0:
            return
        # Ctrl+滚轮：缩放（以光标为锚点），优先于滚动/翻页
        if ev.modifiers() & Qt.ControlModifier:
            self._zoom_step(1 if d > 0 else -1, ev.position())
            ev.accept()
            return

        # 先记下"滚之前"是否已经在边界：这样刚好翻到最后一页的那一下不算越界
        at_start, at_end = self._at_content_start(), self._at_content_end()
        forward = -d > 0              # 滚轮向下 = 往阅读方向（最后面）前进
        if self._mode == ReadMode.Samewight:
            # 单页等宽：滚轮平滑滚当前页，滚到顶/底再翻页
            step = max(60.0, self._page_axis_len() / 6.0)
            self._sw_scroll_by(-d / 120.0 * step)   # 滚轮向下 = 前进

        elif not ReadMode.isScroll(self._mode):
            # 页模式：滚轮一格 = 翻一页（带滑动动画；拖拽中忽略滚轮）
            if not self._page_dragging:
                n = int(round(-d / 120.0))     # 滚轮向下 = 下一页
                self._flip_page(max(-3, min(3, n)))
                self._note_edge_scroll(forward, at_start, at_end)
            ev.accept()
            return
        else:
            # 连续模式：一格滚轮 ≈ 视口的 1/6（最少 60px），d/120 归一化为"格数"
            step = max(60.0, self._viewport_len() / 6.0)
            self._scroller.scroll_by(-d / 120.0 * step)   # 滚轮向下 = 往阅读方向前进
        # 到顶/到底后继续往外滚 -> 累加，够次数发 scrolledPastStart/End
        if not self._page_dragging:      # 页模式拖拽中滚轮被忽略，不参与计数
            self._note_edge_scroll(forward, at_start, at_end)

    def keyPressEvent(self, ev):
        """页模式的键盘翻页：方向键按阅读方向解释（RTL 下左=下一页）、
        PageDown/Space/回车 下一页、PageUp 上一页。连续模式走 Qt 默认行为。
        两种模式通用的缩放快捷键：Ctrl+= 放大 / Ctrl+- 缩小 / Ctrl+0 重置。
        翻页/滚动键也会参与"到顶/到底后再按 N 下"的触发计数。"""
        # 缩放快捷键（以视口中心为锚点）
        if ev.modifiers() & Qt.ControlModifier:
            k = ev.key()
            c = QPointF(self.viewport().rect().center())
            if k in (Qt.Key_Equal, Qt.Key_Plus):
                self.zoom_in(c)
                ev.accept()
                return
            if k == Qt.Key_Minus:
                self.zoom_out(c)
                ev.accept()
                return
            if k == Qt.Key_0:
                self.reset_zoom()
                ev.accept()
                return
        k = ev.key()
        # 本模式下"前进/后退"对应的键（RTL 下左才是前进）
        if ReadMode.isUpDown(self._mode):
            nxt, back = Qt.Key_Down, Qt.Key_Up
        elif ReadMode.isLeftRight(self._mode):
            nxt, back = Qt.Key_Right, Qt.Key_Left
        else:
            nxt, back = Qt.Key_Left, Qt.Key_Right
        is_fwd = k in (Qt.Key_PageDown, Qt.Key_Space, Qt.Key_Return, nxt)
        is_back = k in (Qt.Key_PageUp, back)

        if ReadMode.isScroll(self._mode):
            self._release_initial_hold()   # 方向键/PageUp 等：用户接管位置
            if not (is_fwd or is_back):
                super().keyPressEvent(ev)
                return
            at_start, at_end = self._at_content_start(), self._at_content_end()
            super().keyPressEvent(ev)
            self._note_edge_scroll(is_fwd, at_start, at_end)
            return
        self._scroller.stop_auto()      # 键盘操作停止自动滚动/自动翻页
        self._stop_page_auto()
        self._release_initial_hold()
        if not (is_fwd or is_back):
            super().keyPressEvent(ev)
            return
        at_start, at_end = self._at_content_start(), self._at_content_end()
        if is_fwd:
            if self._mode == ReadMode.Samewight:
                self._sw_scroll_by(max(60.0, self._page_axis_len() * 0.9))
            else:
                self._flip_page(1)
        else:
            if self._mode == ReadMode.Samewight:
                self._sw_scroll_by(-max(60.0, self._page_axis_len() * 0.9))
            else:
                self._flip_page(-1)
        self._note_edge_scroll(is_fwd, at_start, at_end)
        ev.accept()

    def _snap_rest(self):
        """静止后的对齐（连续模式）：吸附回整数像素——恢复设备像素对齐，
        边缘清晰、无重采样模糊。页模式没有滚动，无需处理
        （拖拽停半页的归位由松手弹回动画负责）。"""
        if self._pending_scroll_s is not None:
            return                      # 模式切换中：位置由"待定位置"机制管理
        if not ReadMode.isScroll(self._mode):
            return
        self._snap_to_pixel()

    # ---- 鼠标：连续模式=拖拽平移+惯性；页模式=拖出邻页翻页 ----

    def mousePressEvent(self, ev):
        self._release_initial_hold()    # 用户接管：不再把位置校准回首屏目标
        if self.qtTool.IsStartScrollAndTurn():
            self.qtTool.CloseScrollAndTurn()
            ev.accept()
            super().mouseReleaseEvent(ev)
            return

        if ev.button() == Qt.RightButton:
            self.read_view.SelectMenu(self._openglWidget)
            ev.accept()
            super().mouseReleaseEvent(ev)
            return

        if not ReadMode.isScroll(self._mode):
            if ev.button() == Qt.LeftButton and not self._page_dragging \
                    and not self._page_panning:
                if self._mode == ReadMode.Samewight:
                    # 单页等宽：拖拽 = 页内滚动（内容跟手，松手带惯性）
                    self._sw_anim.stop()
                    self._sw_kinetic.stop()
                    self._sw_drag_samples = []
                    self._sw_drag_pos = ev.position()
                    self._sw_clock.start()
                    self.viewport().setCursor(Qt.ClosedHandCursor)
                elif self._zoom > 1.0:
                    # 放大中：拖拽 = 页内平移（翻页用滚轮/键盘）
                    self._begin_page_pan(ev.position())
                else:
                    self._begin_page_drag(ev.position())
                ev.accept()
            super().mousePressEvent(ev)
            return
        if ev.button() == Qt.LeftButton:
            self._dragging = True
            self._scroller.begin_drag()
            self._scroller.drag_move(ev.position())
            self.viewport().setCursor(Qt.ClosedHandCursor)   # 抓手反馈
            ev.accept()
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self._page_panning:
            self._page_pan_move(ev.position())
            ev.accept()
            return
        if self._sw_drag_pos is not None:
            # 单页等宽：拖拽滚动当前页（内容跟手），同时采样轨迹供松手测速
            p = ev.position()
            rdx, rdy = self._reading_dir_vec()
            d = (p.x() - self._sw_drag_pos.x()) * rdx + (p.y() - self._sw_drag_pos.y()) * rdy
            self._sw_drag_pos = p
            self._scroll_or_flip_page(-d)
            t = float(self._sw_clock.elapsed())
            self._sw_drag_samples.append((t, self._page_scroll))
            while len(self._sw_drag_samples) > 2 and \
                    t - self._sw_drag_samples[0][0] > 120:
                self._sw_drag_samples.pop(0)
            ev.accept()
            return
        if self._page_dragging:
            self._page_drag_move(ev.position())
            ev.accept()
            return
        if self._dragging:
            self._scroller.drag_move(ev.position())
            ev.accept()
            return
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        if self._sw_drag_pos is not None and ev.button() == Qt.LeftButton:
            self._sw_drag_pos = None
            self.viewport().setCursor(Qt.ArrowCursor)
            # 松手测速（最近 120ms 窗口）：够快就起惯性
            v = 0.0
            s = self._sw_drag_samples
            if len(s) >= 2 and s[-1][0] - s[0][0] > 1:
                v = (s[-1][1] - s[0][1]) / (s[-1][0] - s[0][0])
            self._sw_drag_samples = []
            if abs(v) > 0.15:
                self._sw_vel = v
                self._sw_clock.restart()
                self._sw_kinetic.start()
            ev.accept()
            super().mouseReleaseEvent(ev)
            return
        if self._page_panning and ev.button() == Qt.LeftButton:
            self._end_page_pan()
            # ev.accept()
            super().mouseReleaseEvent(ev)
            return
        if self._page_dragging and ev.button() == Qt.LeftButton:
            self._end_page_drag()       # 松手：判定翻页（够远/够快）或弹回
            # ev.accept()
            super().mouseReleaseEvent(ev)
            return
        if self._dragging and ev.button() == Qt.LeftButton:
            self._dragging = False
            self._scroller.end_drag()   # 松手：够快就起惯性
            self.viewport().setCursor(Qt.ArrowCursor)
            # ev.accept()
            # return
        super().mouseReleaseEvent(ev)

    def scrollContentsBy(self, dx, dy):
        """滚动条位置变了（用户拖滚动条/键盘/我们的 setValue 都会到这）。

        注意：平滑滚动时每帧会多次进来（动画写 setValue、亚像素 transform 重算
        range、尺寸修正补偿……），位移不到 0.5px 的那些没必要重算加载窗口——
        可见集合/预取窗口都不可能在这个尺度上变化。真正需要刷新时（跳转/切
        模式/追加图片）都是直接调 _load_visible()，不经过这里。"""
        super().scrollContentsBy(dx, dy)
        self._was_at_end = self._at_end()   # 记录是否贴末端，rangeChanged 锚点要用
        if abs(self._scroll_min_s() - self._last_load_s) < 0.5:
            return
        self._load_visible()                # 滚到新位置 -> 刷新预下载/预解码

    def hideEvent(self, ev):
        """窗口隐藏/最小化：暂停所有动图。看不见还在解码帧是纯粹的浪费
        （CPU 和电都在烧），回来时 showEvent -> _load_visible 会自动恢复播放。"""
        super().hideEvent(ev)
        self._pause_all_animations()

    def showEvent(self, ev):
        """首次显示 / 最小化后恢复 / 从隐藏的标签页切回来 —— 都会触发。

        注意：showEvent 不是"只跑一次的初始化"。以前这里无条件
        `_set_scroll_min_s(0)`，导致每次最小化恢复窗口阅读位置都归零。
        现在只有"首次显示"才定位到第一张图，其余情况一律保持当前位置。"""
        super().showEvent(ev)
        old_cross = self._cross         # _update_cross 之后才是新值，先记旧的
        self._update_cross()            # 视口尺寸确定后才能算 cross
        if not ReadMode.isScroll(self._mode):
            self._sub = 0.0             # 页模式不用亚像素 transform，确保清零
            self._apply_sub_transform()
            # 页模式也要清 _first_show——否则它一直为 True，jump_to_index 的
            # 页模式分支会永远走"等 showEvent"路径，跳页只改页码不刷新显示
            self._first_show = False
            self._show_page(min(self._page, self._max_page()), 0)   # 页码保持
        elif self._first_show:
            self._first_show = False
            self._relayout_all()        # 首次：按真实视口尺寸重排
            if self._initial_idx:
                # 指定了首屏起点：定位到那张图，并进入"持续校准"阶段——
                # 前面的图还是占位尺寸，真实尺寸陆续修正时会把它们重新对齐
                self._enter_initial_hold()
                self._align_initial_target()
            else:
                self._set_scroll_min_s(0.0)     # 默认：从第一张图开始
        elif abs(old_cross - self._cross) >= 1:
            # 恢复显示且视口尺寸确实变了（跨屏拖动、DPI 变化等）：重排，
            # 但锚住当前内容点，位置不漂
            self._relayout_keep_anchor()
        else:
            self._was_at_end = self._at_end()   # 位置不动，只刷新"贴末端"标记
        self._anchoring = True          # 开始启用贴端锚点
        self._load_visible()

    def resizeEvent(self, ev):
        old_cross = self._cross         # super 之后视口已是新尺寸，先记旧值
        super().resizeEvent(ev)
        self._update_cross()            # 视口变了 cross 要重算
        if not ReadMode.isScroll(self._mode):
            # 页模式：槽位随视口变化，重摆当前页（终止进行中的拖拽/动画）
            self._cancel_page_gestures()
            self._show_page(self._page, 0)
            self._resize_refresh.start()
            return
        if abs(old_cross - self._cross) >= 1:
            # cross 变了：所有图按新尺寸重排。用锚点保持阅读位置——沿用旧的
            # 滚动条 value 会因为每张图长度都变了而漂到别的内容上
            if self._initial_hold:
                self._relayout_all()        # 还在首屏校准：重排后重新对齐目标图
                self._align_initial_target()
            else:
                self._relayout_keep_anchor()
        else:
            self._load_visible()
        # 尺寸稳定后重解：放大 -> 重下更清晰的；缩小 -> 缩回 1:1（省内存 + 快路径）
        self._resize_refresh.start()

    def after_index_change(self, index):
        if self._first_show:
            return
        if index < 0:
            return
        self.qtTool.slider.setValue(index+1)
        Log.Info(f"change index, {index}")
        self.update_tool_label(index)

    def after_zoom_change(self, zoom):
        Log.Info(f"change zoom, {zoom}")
        self.qtTool.zoomSlider.setValue(int(zoom*100))
        return

    def update_tool_label(self, index):
        index = self._cur_idx
        if index != self._cur_idx:
            return
        if index >= len(self._items):
            return
        item = self._items[index]
        size = 0
        dataLen = 0
        status = QtFileData.Downloading
        waifuSize = None
        waifuDataLen = 0
        waifuState = ""
        if item.file_data:
            size = QSize(item.file_data.w, item.file_data.h)
        if item.file_data:
            dataLen = len(item.file_data.data)
            status = QtFileData.DownloadSuc
        elif item._failed:
            status = QtFileData.DownloadReset
        elif item._reply:
            status = QtFileData.Downloading
        if item.isAnima:
            waifuState = QtFileData.AnimationNotAuto

        if item.waifu_file_data:
            waifuSize = QSize(item.waifu_file_data.w, item.waifu_file_data.h)
            waifuState = QtFileData.WaifuStateEnd
        if item.waifu_file_data:
            waifuDataLen = len(item.waifu_file_data.data)
        if item.is_not_waifu2x:
            waifuState = QtFileData.WaifuStateCancle
        if item._waifu_reply:
            waifuState = QtFileData.WaifuStateStart

        self.qtTool.SetData(size, dataLen, status, waifuSize, waifuDataLen, waifuState, item._waifu_tick)

    def eventFilter(self, obj, ev) -> bool:
        # print(obj, ev.type())
        if obj == self._scene:
            if ev.type() == QEvent.KeyPress:
                return True
            elif ev.type() == QEvent.KeyRelease:
                if not self.frame.helpLabel.isHidden():
                    self.frame.helpLabel.hide()
                    return True
                # if ev.key() == Qt.Key_Down:
                #     self.ScrollValue(self.height() / 2)
                # elif ev.key() == Qt.Key_Up:
                #     self.ScrollValue(-self.height() / 2)
                # elif ev.key() == Qt.Key_Left:
                #     self.ScrollLastPage()
                # elif ev.key() == Qt.Key_Right:
                #     self.ScrollNextPage()
                elif ev.key() == Qt.Key_Escape:
                    self.qtTool.ReturnPage()
                elif ev.key() == Qt.Key_F5:
                    self.qtTool.SwitchScrollAndTurn()
                elif ev.key() == Qt.Key_F10:
                    self.change_double_page()
                elif ev.key() == Qt.Key_F11:
                    self.qtTool.FullScreen()
                elif ev.key() == Qt.Key_F2:
                    self.qtTool.curWaifu2x.click()

                elif ev.key() == Qt.Key_F4:
                    self.read_view.CopyLastFile()
                elif ev.key() == Qt.Key_F3:
                    self.read_view.CopyFile()
                elif ev.key() == Qt.Key_F1:
                    self.read_view.CopyPicture()

                elif ev.key() == Qt.Key_F12:
                    self.read_view.ShowAndCloseTool()
                # elif ev.key() == Qt.Key_Space:
                #     self.ScrollValue(self.height())
                elif ev.modifiers() == Qt.ShiftModifier and ev.key() == Qt.Key_Left:
                    self.qtTool.OpenLastEps()
                elif ev.modifiers() == Qt.ShiftModifier and ev.key() == Qt.Key_Right:
                    self.qtTool.OpenNextEps()
                elif ev.key() == Qt.Key_Plus or ev.key() == Qt.Key_Equal:
                    self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() + 10)
                elif ev.key() == Qt.Key_Minus:
                    self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() - 10)
                return True
            elif ev.type() == QEvent.GraphicsSceneMousePress:
                if ev.button() == Qt.MouseButton.LeftButton:
                    self._start_press_pos = ev.screenPos()
            elif ev.type() == QEvent.GraphicsSceneMouseRelease:
                if not self.frame.helpLabel.isHidden():
                    self.frame.helpLabel.hide()
                    return True

                if ev.button() == Qt.MouseButton.LeftButton:
                    if not self.frame.helpLabel.isHidden():
                        self.frame.helpLabel.hide()
                        return True
                    endPos = ev.screenPos()
                    subPos = (endPos - self._start_press_pos)
                    if abs(subPos.x()) <= 20 and abs(subPos.y()) <= 20:
                        curPos = endPos - QtOwner().owner.pos()

                        # print(curPos, endPos, QtOwner().owner.pos(), self.width(), self.height())
                        if curPos.x() <= self.width() // 3:
                            if curPos.y() <= self.height() // 2:
                                self.read_view.ShowAndCloseTool()
                            else:
                                if ReadMode.isScroll(self._mode) or self._mode == ReadMode.Samewight:
                                    self.scroll_to_next(1, self._get_item_scroll_len())
                                else:
                                    self.qtTool.LastPage()
                        elif curPos.x() <= self.width() // 3 * 2:
                            if curPos.y() <= self.height() // 2:
                                self.scroll_to_next(1, self._viewport_len())
                            else:
                                self.scroll_to_next(-1, self._viewport_len())
                        else:
                            if curPos.y() <= self.height() // 2:
                                self.read_view.ShowAndCloseTool()
                            else:
                                if ReadMode.isScroll(self._mode)or self._mode == ReadMode.Samewight:
                                    self.scroll_to_next(-1, self._get_item_scroll_len())
                                else:
                                    self.qtTool.NextPage()
        return False

    def change_double_page(self):
        if not ReadMode.isDouble(self._mode):
            return
        self._is_cover_mode = not self._is_cover_mode
        self.set_mode(self._mode.value, True)

    def _get_item_scroll_len(self):
        if self._cur_idx >= len(self._items) or self._cur_idx < 0:
            return 0
        else:
            item = self._items[self._cur_idx]
            if ReadMode.isUpDown(self._mode):
                return min(self._viewport_len(), item._h + 1)
            else:
                return min(self._viewport_len(), item._w + 1)

    def scroll_to_next(self, d2, value):
        if not (ReadMode.isScroll(self._mode) or self._mode == ReadMode.Samewight):
            return

        if ReadMode.isUpDown(self._mode):
            d = 120 * d2
            step = value
        elif ReadMode.isRightLeft(self._mode):
            d = -120 * d2
            step = value
        else:
            d = 120 * d2
            step = value
        # step = max(60.0, value / 6.0)
        if self._mode == ReadMode.Samewight:
            step = max(60.0, self._page_axis_len())
            self._sw_scroll_by(-d / 120.0 * step)   # 滚轮向下 = 前进
        else:
            self._scroller.scroll_by(-d / 120.0 * step)   # 滚轮向下 = 往阅读方向前进

    def switch_cur_waifu2x_state(self):
        item = self.get_cur_item()
        if not item:
            return
        if item._waifu2x_state == 0:
            item._waifu2x_state = 1
        elif item._waifu2x_state == 1:
            item._waifu2x_state = -1
        elif item._waifu2x_state == -1:
            item._waifu2x_state = 1
        self._load_visible()

    def check_waifu2x_state(self):
        self._load_visible()

    def after_switch_last_eps(self):
        self.qtTool.OpenLastEps()

    def after_switch_next_eps(self):
        self.qtTool.OpenNextEps()

    def clear_all_item(self):
        self._reset_edge_counts()     # 跳转后重新算"到顶/到底"的连续次数
        self.stop_auto()
        self._release_initial_hold()
        for item in self._items:
            self._scene.removeItem(item)
            ReadNewPoolManager().AddProxyItem(item)
        self._items = []
