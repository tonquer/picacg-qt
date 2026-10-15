from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from view.read.read_new_view import ReadNewView
    from view.read.read_new_task import ReadNewTask
    from view.read.read_new_frame import ReadNewFrame

import math
from tools.log import Log
from tools.tool import ToolUtil
from view.read.read_new_pool import ReadNewPoolManager
from PySide6.QtCore import (Qt, QRectF, QSize, QBuffer, QByteArray, QIODevice,
                            QUrl, QObject, QRunnable, QThreadPool, Signal, QTimer,
                            QAbstractAnimation, QVariantAnimation, QEasingCurve,
                            QElapsedTimer, QPointF)
from PySide6.QtGui import (QImageReader, QImage, QPixmap, QPainter, QColor,
                           QTransform, QSurfaceFormat, QPen)
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
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self._items : list[ReadNewGraphicsItem] = []   # ReadNewGraphicsItem 列表，按阅读顺序排列
        self._mode = mode                         # 当前阅读方向
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
        self._page_pan = QPointF(0.0, 0.0)      # 缩放后 item 左上角相对槽位左上角的
                                                # 偏移（<0；_place_page 里按槽位钳制）
        self._page_panning = False              # 当前是否在拖拽平移（与拖拽翻页互斥）
        self._page_pan_start = QPointF()        # 平移起点的鼠标位置
        self._page_pan_ref = QPointF()          # 平移起点时的 _page_pan（松手前可回退）

        if Setting.IsOpenOpenGL.value:
            self.set_opengl(True)

    @property
    def frame(self) -> ReadNewFrame:
        return self.parent()

    @property
    def read_view(self) -> ReadNewView:
        return self.parent().parent()

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
            self.setViewport(gl)
            self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        else:
            self.setViewport(QWidget())        # 换回普通光栅视口
            self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        def restore():
            if not ReadMode.isScroll(self._mode):
                self._show_page(self._page, 0)     # 页模式：重摆当前页（无滚动位置）
            else:
                self._set_scroll_min_s(s)
            self._load_visible()

        restore()
        # 换视口后 widget 尺寸异步稳定，事件循环下一轮再按一次位置
        QTimer.singleShot(0, restore)

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
        - 页模式：缩放是 item 的 scale 变换；z>1 时左键拖拽变为页内平移
          （_page_pan 钳制在图片边界），翻页仍走滚轮/键盘
        缩放后自动对"源分辨率 > 已解码位图"的可见图重新下载解码（防放大发糊）。
        """
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

    def reset_zoom(self):
        """重置为 100%（适配视口）。"""
        self.set_zoom(1.0)

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
        pc = p.x() if self._mode == ReadMode.UpDown else p.y()
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
        """页模式缩放：item 的 scale 变换。锚点 = 光标所在槽位的内容点；
        z>1 时 _page_pan 把图片在槽位内挪动（_place_page 里钳制到图片边界）。"""
        self._cancel_page_gestures()    # 进行中的滑动动画/平移先就地收尾
        p = QPointF(anchor) if anchor is not None \
            else QPointF(self.viewport().rect().center())
        slots = self._page_slot_rects()
        si = 0
        for i, (x, y, w, h) in enumerate(slots):    # 找包含锚点的槽位
            if x <= p.x() < x + w and y <= p.y() < y + h:
                si = i
                break
        sx, sy, sw, sh = slots[si]
        dx_old, dy_old = self._page_slot_offset(sw, sh)
        # 锚点的内容坐标（未缩放的槽位坐标系）
        lx = (p.x() - sx - dx_old) / self._zoom
        ly = (p.y() - sy - dy_old) / self._zoom
        self._zoom = z
        # 反解新的 pan，让这个内容点缩放后仍在光标下
        self._page_pan = QPointF((p.x() - sx) - lx * z, (p.y() - sy) - ly * z)
        self._show_page(self._page, 0)              # 重新摆放（_place_page 会钳制）
        self._load_visible()
        self._refresh_decodes()

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
        # 把原始 pan 归一化成钳制后的值：被边界拦住的多余位移丢掉，
        # 下一次平移手势从合法位置起算（否则连续拖会"攒"出隐形位移）
        rects = self._page_slot_rects()
        if rects:
            x, y, w, h = rects[0]
            dx, dy = self._page_slot_offset(w, h)
            self._page_pan = QPointF(dx, dy)

    def _refresh_decodes(self):
        """缩放变化后，对"可见且源分辨率明显高于已解码位图"的图重新下载解码。
        解码位图是按当时的 cross×dpr 生成的，放大后不够用会发糊；重新解码
        期间旧 pixmap 保留（_start_download 不清 pixmap），新图就绪才替换。"""
        dpr = self.devicePixelRatioF()
        if not ReadMode.isScroll(self._mode):
            its = []
            for pg in (self._page - 1, self._page, self._page + 1):
                if 0 <= pg <= self._max_page():
                    its.extend(self._page_items(pg))
            # 页模式图最大显示到 视口对角×zoom 物理像素
            max_px = int(max(self.viewport().width(), self.viewport().height())
                         * dpr * max(1.0, self._zoom))
        else:
            L = self._viewport_len()
            s0 = self._scroll_min_s()
            its = [it for it in self._items
                   if it._s + it._len >= s0 - L and it._s <= s0 + L * 2.5]
            # 与 _on_finished 的连续模式公式一致（cross 已含 zoom）
            max_px = int(self._cross * dpr
                         * (1.0 if self._mode == ReadMode.UpDown else self.MAX_ASPECT))
        for it in its:
            if it.pixmap is None or it._reply is not None or it._failed:
                continue
            have = it.pixmap.width()     # 已解码位图的宽（物理像素）
            src = it._size.width() if (it._size and it._size.isValid()) else 0
            # 位图不够 + 原图确实有更高分辨率，才值得重新下载
            if have < max_px * 0.99 and src > have * 1.25:
                self._start_download(it)

    @property
    def scroller(self) -> ReadNewScroller:
        return self._scroller

    def set_auto_scroll(self, speed: float):
        """自动滚动/自动翻页。speed：px/s（沿阅读方向），0 或负数停止。
        连续模式=匀速滚动；页模式=按 页长/速度 换算成每页停留时长自动翻页
        （如 600px 屏、300px/s = 每页停 2 秒）。
        任意鼠标点击/滚轮/拖拽/键盘都会停止；到最后一页也会停止。"""
        if not ReadMode.isScroll(self._mode):
            self._start_page_auto(speed)
        else:
            self._scroller.start_auto(speed)

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

        - 连续模式：所有和视口相交的图（长图+小图可能同屏多张）
        - 页模式：当前页的 1~2 张；翻页滑动/拖拽进行途中邻页也被拖进屏幕，
          这时邻页的图也在列表里
        - 一张图都没有时返回 []
        """
        if not self._items:
            return []
        if not ReadMode.isScroll(self._mode):
            per = self._page_per_screen()
            pages = {self._page}
            # 动画/拖拽途中邻页也露出来了：一并算进去
            nb = self._page_anim_nb if self._page_anim_mode else self._page_drag_neighbor
            if nb is not None and 0 <= nb <= self._max_page():
                pages.add(nb)
            idxs = set()
            for p in pages:                       # 集合乱序，下面再排
                i0 = p * per
                for k in range(min(per, max(0, len(self._items) - i0))):
                    idxs.add(i0 + k)
            return sorted(idxs)
        # 连续模式：item 按 s 升序，扫到第一条看不见的就可以收工（早退很重要，
        # 这个方法在滚动时每帧都会被调用）
        s0 = self._scroll_min_s()
        s1 = s0 + self._viewport_len()
        out = []
        for i, it in enumerate(self._items):
            if it._s >= s1:
                break                             # 后面的都还在视口下方/右方
            if it._s + it._len > s0:              # 和视口有交集
                out.append(i)
        return out

    def current_index(self) -> int:
        """阅读位置所在的图片序号（0 起；一张图都没有时 -1）。

        连续模式 = 屏幕上最靠前的那张（也就是"上方/左边/漫画模式的右边"那张）；
        页模式 = 当前页的第一张。想显示"第 N 张 / 共 M 张"就用 current_index()+1。
        """
        return self._first_visible_index()

    def count(self) -> int:
        """图片总数（len(_items) 的语义化别名）。"""
        return len(self._items)

    def side_of_index(self, idx: int):
        """这张图现在显示在屏幕的哪个物理方位？

        返回 "left"/"right"/"top"/"bottom"（双页模式）、"center"（单页模式）、
        None（连续模式：一屏多张且会滚动，没有固定的半屏概念）。
        漫画模式（rtl）第一张在右半屏——这是日漫跨页的正确顺序。
        """
        if not 0 <= idx < len(self._items):
            return None
        if self._mode == ReadMode.LeftRight:
            return "center"
        if not ReadMode.isDouble(self._mode):
            return None
        k = idx % self._page_per_screen()       # 在本页里的槽位序号：0=阅读起始侧
        if self._mode == ReadMode.UpDown:
            return "top" if k == 0 else "bottom"
        if ReadMode.isLeftRight(self._mode):
            return "left" if k == 0 else "right"
        return "right" if k == 0 else "left"    # rtl：阅读从右往左

    def index_on_side(self, side: str):
        """反过来问："左边那张图是第几张？"（漫画模式要问右边）

        side 支持三种写法：
          "left"/"right"/"top"/"bottom" —— 物理方位（只在双页模式有意义）
          "first"                        —— 阅读起始侧，跨模式通用：
                                           ltr=左、rtl(漫画)=右、ttb=上
          "last"                         —— 另一半屏（双页的第二张）
        当前屏幕上没有这个槽位 / 连续模式下问物理方位 -> None。

        页模式下只考虑**当前页**——翻页动画途中邻页虽半露在屏幕上，问"左边是
        第几张"显然要的是落下后那一页的答案，不是扫过就算。
        """
        if ReadMode.isScroll(self._mode):
            vis = self.visible_indices()
        else:
            per = self._page_per_screen()
            i0 = self._page * per
            vis = list(range(i0, min(i0 + per, len(self._items))))
        if not vis:
            return None
        if side == "first":
            return vis[0]
        if side == "last":
            return vis[-1] if len(vis) > 1 else None
        for i in vis:
            if self.side_of_index(i) == side:
                return i
        return None

    def _first_visible_index(self) -> int:
        """visible_indices 的第 0 项（-1=没有图）。模式切换时要保证不返回
        动画途中邻页的序号，所以这里独立算，不含邻页。"""
        if not ReadMode.isScroll(self._mode):
            return min(self._page * self._page_per_screen(),
                       max(0, len(self._items) - 1))
        v = self.visible_indices()
        return v[0] if v else -1

    def _refresh_index(self):
        """重算"当前第几张"，跨到新的一张时才发 indexChanged。

        调用点都是"阅读位置可能变了"的地方：_load_visible（滚动/翻页/模式切换
        都走它）、_end_page_drag（松手判定后）。60fps 下每帧都会进来，所以
        visible_indices 里的早退很重要。"""
        idx = self.current_index()
        if idx != self._cur_idx:
            self._cur_idx = idx
            self.indexChanged.emit(idx)
    # ---- 页模式（翻页器）：几何 / 显示 / 翻页 ----

    def _page_per_screen(self) -> int:
        """一屏几张图：单页 1，双页 2。"""
        return 1 if self._mode == ReadMode.LeftRight else 2

    def _max_page(self) -> int:
        """最后一页的页码（0 起；双页模式不足一对时最后一页只有 1 张）。"""
        per = self._page_per_screen()
        return max(0, (len(self._items) + per - 1) // per - 1)

    def _page_axis_len(self) -> float:
        """阅读方向上的视口长度：整页翻动/拖拽的滑动距离。"""
        return (self.viewport().height() if self._mode == ReadMode.UpDown
                else self.viewport().width())

    def _reading_dir_vec(self):
        """阅读方向的单位向量（场景坐标）：ttb 向下 (0,1)；ltr (1,0)；rtl (-1,0)。"""
        if self._mode == ReadMode.UpDown:
            return (0.0, 1.0)
        if ReadMode.isLeftRight(self._mode):
            return (1.0, 0.0)
        return (-1.0, 0.0)

    def _page_slot_rects(self):
        """当前页每个槽位的矩形 [(x, y, w, h), ...]。页模式无滚动，
        场景坐标==视口坐标。单页=整屏；双页：ttb 上下叠放、横排左右并排，
        RTL 第一张在右半屏（日漫跨页的正确顺序）。尺寸对齐设备像素。"""
        vw, vh = self.viewport().width(), self.viewport().height()
        if self._mode == ReadMode.LeftRight:
            return [(0.0, 0.0, vw, vh)]
        if self._mode == ReadMode.UpDown:
            h = self._snap_px(vh / 2)
            return [(0.0, 0.0, vw, h), (0.0, h, vw, self._snap_px(vh - h))]
        w = self._snap_px(vw / 2)
        if ReadMode.isLeftRight(self._mode):
            return [(0.0, 0.0, w, vh), (w, 0.0, self._snap_px(vw - w), vh)]
        # rtl：第一张（阅读顺序最前）在右半屏
        return [(w, 0.0, self._snap_px(vw - w), vh), (0.0, 0.0, w, vh)]

    def _page_items(self, page: int):
        """第 page 页的 item 列表（最后一页可能只有 1 张）。"""
        i0 = page * self._page_per_screen()
        return self._items[i0:i0 + self._page_per_screen()]

    def _page_slot_offset(self, w: float, h: float):
        """缩放后 item 左上角相对槽位左上角的偏移 (dx, dy)。
        zoom<=1：图比槽位小，居中放（信箱留白）；zoom>1：用 _page_pan，
        并钳制到图片边缘——不能把图片拖出槽位外留白。"""
        z = self._zoom
        zw, zh = w * z, h * z
        if z <= 1.0:
            return (w - zw) / 2.0, (h - zh) / 2.0
        dx = max(w - zw, min(0.0, self._page_pan.x()))
        dy = max(h - zh, min(0.0, self._page_pan.y()))
        return dx, dy

    def _place_page(self, page: int, offset: float):
        """把第 page 页的 items 摆到"槽位位置 + 缩放平移 + offset×阅读方向向量"
        并显示。缩放用 item 的 scale 变换实现（几何仍是槽位大小，绘制时放大）；
        翻页动画/拖拽期间当前页和邻页各摆一次，实现两页同屏滑动。"""
        rdx, rdy = self._reading_dir_vec()
        z = self._zoom
        for it, (x, y, w, h) in zip(self._page_items(page), self._page_slot_rects()):
            it._fit = True                    # 等比缩放居中画进槽位（信箱留白）
            it.set_geometry(w, h)
            dx, dy = self._page_slot_offset(w, h)
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
        self._page = page
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
        L = max(1.0, self._page_axis_len())
        self._page_auto_timer.start(
            max(300, int(L / self._page_auto_speed * 1000)))

    def _on_page_auto(self):
        if self._page >= self._max_page():
            self._stop_page_auto()    # 最后一页自动停
            return
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
        if not ReadMode.isScroll(self._mode):
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
        if self._mode == ReadMode.UpDown:
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
        return self.verticalScrollBar() if self._mode == ReadMode.UpDown \
            else self.horizontalScrollBar()

    def _viewport_len(self) -> float:
        """视口在滚动轴方向的长度 L（可见区域高/宽，像素）。"""
        return self.viewport().height() if self._mode == ReadMode.UpDown \
            else self.viewport().width()

    def _scroll_min_s(self) -> float:
        """当前视口可见区间的起始 s（阅读方向），含亚像素偏移。

        注意：QGraphicsView 滚动条的 value 就是视口左/上边缘的场景**绝对坐标**
        （不是相对 sceneRect.left() 的偏移），所以 RTL 场景的滚动条值是负数。
        滚动条只承载整数部分，小数部分在 self._sub 里。
        """
        if self._mode == ReadMode.UpDown:
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
        1,2,1,2 像素交替，瞬时速度波动 ±50%（滚动"粘连感"来源之一）。"""
        L = self._viewport_len()
        s = max(0.0, min(s, max(0.0, self._total - L)))
        v = self._s_to_bar(s)
        if snap:
            self._sub = 0.0
            v = round(v)
        else:
            vi = math.floor(v)
            self._sub = v - vi
            v = vi
        self._bar().setValue(int(v))
        self._apply_sub_transform()

    def _apply_sub_transform(self):
        """把亚像素偏移放进视图 transform（沿滚动轴平移 -f）。
        f 是 [0,1) 的小数：滚动条停在整数 v，transform 再补上 v→v+f 的位移。
        去重：偏移没变就不 setTransform（它触发全量重绘，60fps 下也不能白做）。"""
        if abs(self._sub - self._sub_applied) < 1e-9:
            return
        self._sub_applied = self._sub
        f = self._sub
        if self._mode == ReadMode.UpDown:
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
        return self.horizontalScrollBar() if self._mode == ReadMode.UpDown \
            else self.verticalScrollBar()

    def _cross_view_len(self) -> float:
        """视口在 cross 轴方向的尺寸。"""
        return self.viewport().width() if self._mode == ReadMode.UpDown \
            else self.viewport().height()

    def _s_at_view_pos(self, p: QPointF) -> float:
        """视口坐标 p 下的内容点对应的 s（缩放锚点用）。
        视口坐标 -> 场景坐标只差一个亚像素偏移（_scroll_min_s 已含）。"""
        if self._mode == ReadMode.UpDown:
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
        d = -dx if self._mode == ReadMode.UpDown else -dy
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
        c = (self.viewport().width() if self._mode == ReadMode.UpDown
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
        if self._mode == ReadMode.UpDown:
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
        if self._mode == ReadMode.UpDown:
            it.setPos(0, it._s)
        elif ReadMode.isLeftRight(self._mode):
            it.setPos(it._s, 0)
        else:  # rtl：s 增大向左，item 占据 [-(s+len), -s]
            it.setPos(-(it._s + it._len), 0)

    def _update_scene_rect(self):
        """手动维护 sceneRect（不让 Qt 自动扩展——自动扩展会重算滚动位置导致抖动）。"""
        c = self._cross
        if self._mode == ReadMode.UpDown:
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

    # ================ 添加图片 ================

    def init_all_image(self, maxNum, curIndex):
        if not maxNum:
            return

        for item in self._items:
            self._scene.removeItem(item)
            ReadNewPoolManager().AddProxyItem(item)
        self._items = []
        for i in range(maxNum):
            self.add_image(i)
        self.set_mode(self._mode.value, isForce=True)

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
            x, y, w, h = self._page_slot_rects()[-1]
            it._fit = True
            it.setTransform(QTransform.fromScale(self._zoom, self._zoom))
            it.set_geometry(w, h)
            it.setPos(x, y)
            it.setVisible(False)
            self._scene.addItem(it)
            self._items.append(it)
            # 新图正好落在当前页（边加载边追加的最后一页）：刷新显示
            if (len(self._items) - 1) // self._page_per_screen() == self._page:
                self._show_page(self._page, 0)
            return
        w, h, ln = self._dims_for(it)
        it.set_geometry(w, h)
        it._s = self._snap_px(self._total)     # 新图接在末尾（已有内容位置不动）
        it._len = ln
        self._place(it)
        self._scene.addItem(it)
        self._items.append(it)
        self._total = self._snap_px(self._total + ln + self._gap)
        self._update_scene_rect()

    # ================ 惰性加载 ================

    def _load_visible(self):
        """触发"当前该下载"的图片。连续模式：视口 ±1.5/2.5 屏的预取窗口
        （往下多备是因为滚动主要朝阅读方向前进）。页模式：只下载当前页
        和相邻一页（翻页方向的预取）。离屏的图完全不请求。"""
        if not ReadMode.isScroll(self._mode):
            for p in (self._page - 1, self._page, self._page + 1):
                if 0 <= p <= self._max_page():
                    for it in self._page_items(p):
                        self._maybe_download(it)
            return
        L = self._viewport_len()
        s0 = self._scroll_min_s()
        top, bottom = s0 - L * 1.5, s0 + L * 2.5
        for it in self._items:               # 按 s 升序，可提前退出
            if it.pixmap is not None or it._reply is not None or it._failed:
                continue                     # 已加载/下载中/失败过：跳过
            if it._s > bottom:
                break                        # 后面的都更远，不用看了
            if it._s + it._len < top:
                continue                     # 在预取窗口上方（已滚过）
            self._start_download(it)

    def _maybe_download(self, it: ReadNewGraphicsItem):
        """需要的话发起下载（未加载/未在下载/未失败过）。"""
        if it.pixmap is None and it._reply is None and not it._failed:
            self._start_download(it)

    def _start_download(self, item: ReadNewGraphicsItem):
        """发起 HTTP GET，挂接三个回调：有新数据（探测尺寸）/进度/下载完成（解码）。"""
        Log.Info(f"Start download, index{item.index}")

        taskId = self.read_task.AddDownload(item.index,
                                       downloadCallBack=self._on_download_progress,
                                       completeCallBack=self._on_finished)

        item._reply = taskId
        item._progress = None            # 请求刚发出、还不知道总大小：先转圈
        self._spin_timer.start()         # 有下载在跑就保持转圈动画可用
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
            item._progress = None
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

    def _try_probe_size(self, item: ReadNewGraphicsItem):
        """数据够多时解析文件头拿宽高（PNG/JPEG 的宽高都在文件头最前面）。
        拿到就立即修正布局——用户看到占位框变成正确高度通常只滞后几毫秒。"""
        w, h, _, isAnima = ToolUtil.GetPictureSize(item._buf)
        item.isAnima = isAnima
        sz = QSize(w, h)
        if sz is not None:
            self._correct_len(item, sz)

    def _on_finished(self, data: bytes, st: int, index: int):
        """下载结束：成功 -> 丢给线程池后台解码；失败 -> 标记失败。"""
        if index >= len(self._items):
            return
        item = self._items[index]

        reply = item._reply
        if reply is None:
            return
        if st != Str.Ok:
            item._failed = True
            item.update()                    # 触发重画（占位框变红显示"加载失败"）
            return

        reply, item._reply = item._reply, None
        item._progress = None            # 下载结束：进度环不再显示（成功/失败都一样）
        item._buf = data

        self._try_probe_size(item)           # 兜底：万一中途一直没探测到
        dpr = self.devicePixelRatioF()
        if not ReadMode.isScroll(self._mode):
            # 页模式：图要等比缩放进槽位，最大可放大到 视口×zoom
            max_px = int(max(self.viewport().width(),
                             self.viewport().height()) * dpr
                         * max(1.0, self._zoom))
        else:
            # 连续模式：ttb 图片最长边是 cross×dpr；横排的图可以横着长，
            # 最长 cross×MAX_ASPECT×dpr
            max_px = int(self._cross * dpr * (1.0 if self._mode == ReadMode.UpDown else self.MAX_ASPECT))

        # toW, toH = QtFileData.GetReadScale(self._mode, self.read_view.frame.scaleCnt,
        #                                    self.width(),
        #                                    self.height())
        if item._size.width()>0 and item._size.width() > max_px:
            toW = max_px
            toH = math.trunc(max_px/item._size.width()*item._size.heigh())
        else:
            toW = 0
            toH = 0
        # self.read_task.AddQImageTask(data, dpr, toW, toH, self._mode,
        #                                                 self._on_loaded,
        #                                                 (index, toW, toH, self.frame.scaleCnt))

        from view.read.read_new_task import DecodeTask
        task = DecodeTask(item.index, item._buf, max_px, dpr)
        task.signals.loaded.connect(self._on_loaded)
        QThreadPool.globalInstance().start(task)

        # task = DecodeTask(item, item._buf, max_px, dpr)
        # task.signals.loaded.connect(self._on_loaded)
        # QThreadPool.globalInstance().start(task)
        # item._buf = QByteArray()             # 释放下载数据（解码任务里已拷贝）

    def _on_loaded(self, index, real: QSize, img: QImage):
        """后台解码完成（主线程槽）：修正布局 + 像素填进固定矩形。"""
        if index >= len(self._items):
            return
        item = self._items[index]
        if not item._size_known:
            self._correct_len(item, real)    # 探测也没拿到过的最后兜底
        # QPixmap 只在主线程创建（严格模式，跨平台零风险）；
        # dpr 已设在 QImage 上，fromImage 会保留
        item.pixmap = QPixmap.fromImage(img)
        item.update()


    # def _on_loaded(self, img, v):
    #     """后台解码完成（主线程槽）：修正布局 + 像素填进固定矩形。"""
    #     (index, toW, toH, scaleCnt) = v
    #     if index >= len(self._items):
    #         return
    #     item = self._items[index]
    #
    #     if not item._size_known:
    #         self._correct_len(item, QSize(toW, toH))    # 探测也没拿到过的最后兜底
    #     # QPixmap 只在主线程创建（严格模式，跨平台零风险）；
    #     # dpr 已设在 QImage 上，fromImage 会保留
    #     item.pixmap = QPixmap.fromImage(img)
    #     item.update()                        # 只请求重绘，几何不动 -> 无跳动

    # ================ 长度修正：平移后续内容 + 滚动补偿（s 空间，模式无关） ================

    def _correct_len(self, item: ReadNewGraphicsItem, image_size: QSize):
        """拿到图片真实尺寸后，把它的占位长度修正为准确值。

        做三件事保证"不跳动"：
        1) 这张图自己改尺寸；
        2) 阅读顺序在它之后的图整体平移 delta（delta=新长-旧长，可正可负）；
        3) 关键补偿：如果这张图在当前视口"之前"（已滚过），它变长会把视口里的
           内容往下推——必须把滚动位置同步 +delta，视口里的画面才纹丝不动。
        """
        item._size = QSize(image_size)
        item._size_known = True
        if not ReadMode.isScroll(self._mode):
            return        # 页模式槽位固定（由视口决定），真实尺寸只影响绘制
        w, h, ln = self._dims_for(item)
        delta = ln - item._len             # 长度变化量（正=变长）
        if abs(delta) < 0.5:               # 不到半个像素：无感知，不用动
            return
        item.set_geometry(w, h)
        item._len = ln
        self._place(item)

        for other in self._items:          # 阅读顺序在后的 item 整体平移
            if other._s > item._s:
                other._s = self._snap_px(other._s + delta)
                self._place(other)
        self._total = self._snap_px(self._total + delta)
        self._update_scene_rect()

        # 补偿：被修正的 item 在视口"之前"时，视口内容被推移，滚动窗口同步平移
        if item._s < self._scroll_min_s():
            self._scroll_by_s(delta)
            # 同步滚动器的内部位置（自动滚动的 _auto_pos / 动画目标），
            # 否则下个 tick 会把滚动条拉回旧值 -> 内容回跳一下再前进（粘连感）
            self._scroller.on_viewport_shifted(delta)

    # ================ 事件 ================

    def wheelEvent(self, ev):
        # 任意滚轮操作停止自动滚动/自动翻页
        self._scroller.stop_auto()
        self._stop_page_auto()
        # 三种模式统一：滚轮/触控板 -> 阅读方向位移
        ad = ev.angleDelta()          # 滚轮增量：一格 = y 方向 ±120
        if self._mode == ReadMode.UpDown:
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
        if not ReadMode.isScroll(self._mode):
            # 页模式：滚轮一格 = 翻一页（带滑动动画；拖拽中忽略滚轮）
            if not self._page_dragging:
                n = int(round(-d / 120.0))     # 滚轮向下 = 下一页
                self._flip_page(max(-3, min(3, n)))
            ev.accept()
            return
        # 连续模式：一格滚轮 ≈ 视口的 1/6（最少 60px），d/120 归一化为"格数"
        step = max(60.0, self._viewport_len() / 6.0)
        self._scroller.scroll_by(-d / 120.0 * step)   # 滚轮向下 = 往阅读方向前进
        ev.accept()

    def keyPressEvent(self, ev):
        """页模式的键盘翻页：方向键按阅读方向解释（RTL 下左=下一页）、
        PageDown/Space/回车 下一页、PageUp 上一页。连续模式走 Qt 默认行为。
        两种模式通用的缩放快捷键：Ctrl+= 放大 / Ctrl+- 缩小 / Ctrl+0 重置。"""
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
        if ReadMode.isScroll(self._mode):
            super().keyPressEvent(ev)
            return
        self._scroller.stop_auto()      # 键盘操作停止自动滚动/自动翻页
        self._stop_page_auto()
        k = ev.key()
        nxt = back = None               # 本模式下"下一页/上一页"对应的键
        if self._mode == ReadMode.UpDown:
            nxt, back = Qt.Key_Down, Qt.Key_Up
        elif ReadMode.isLeftRight(self._mode):
            nxt, back = Qt.Key_Right, Qt.Key_Left
        else:                           # rtl：往左才是前进
            nxt, back = Qt.Key_Left, Qt.Key_Right
        if k in (Qt.Key_PageDown, Qt.Key_Space, Qt.Key_Return, nxt):
            self._flip_page(1)
        elif k in (Qt.Key_PageUp, back):
            self._flip_page(-1)
        else:
            super().keyPressEvent(ev)
            return
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
        self._scroller.stop_auto()      # 任意点击（含右键）停止自动滚动/自动翻页
        self._stop_page_auto()
        if not ReadMode.isScroll(self._mode):
            if ev.button() == Qt.LeftButton and not self._page_dragging \
                    and not self._page_panning:
                if self._zoom > 1.0:
                    # 放大中：拖拽 = 页内平移（翻页用滚轮/键盘）
                    self._begin_page_pan(ev.position())
                else:
                    self._begin_page_drag(ev.position())
                ev.accept()
                return
            super().mousePressEvent(ev)
            return
        if ev.button() == Qt.LeftButton:
            self._dragging = True
            self._scroller.begin_drag()
            self._scroller.drag_move(ev.position())
            self.viewport().setCursor(Qt.ClosedHandCursor)   # 抓手反馈
            ev.accept()
            return
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self._page_panning:
            self._page_pan_move(ev.position())
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
        if self._page_panning and ev.button() == Qt.LeftButton:
            self._end_page_pan()
            ev.accept()
            return
        if self._page_dragging and ev.button() == Qt.LeftButton:
            self._end_page_drag()       # 松手：判定翻页（够远/够快）或弹回
            ev.accept()
            return
        if self._dragging and ev.button() == Qt.LeftButton:
            self._dragging = False
            self._scroller.end_drag()   # 松手：够快就起惯性
            self.viewport().setCursor(Qt.ArrowCursor)
            ev.accept()
            return
        super().mouseReleaseEvent(ev)

    def scrollContentsBy(self, dx, dy):
        """滚动条位置变了（用户拖滚动条/键盘/我们的 setValue 都会到这）。"""
        super().scrollContentsBy(dx, dy)
        self._was_at_end = self._at_end()   # 记录是否贴末端，rangeChanged 锚点要用
        self._load_visible()                # 滚到新位置 -> 预取新进入窗口的图

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
            self._show_page(min(self._page, self._max_page()), 0)   # 页码保持
        elif self._first_show:
            self._first_show = False
            self._relayout_all()        # 首次：按真实视口尺寸重排
            self._set_scroll_min_s(0.0) # 从第一张图开始
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
            return
        if abs(old_cross - self._cross) >= 1:
            # cross 变了：所有图按新尺寸重排。用锚点保持阅读位置——沿用旧的
            # 滚动条 value 会因为每张图长度都变了而漂到别的内容上
            self._relayout_keep_anchor()
        else:
            self._load_visible()

