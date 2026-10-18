from PySide6.QtCore import (Qt, QRectF, QSize, QBuffer, QByteArray, QIODevice,
                            QUrl, QObject, QRunnable, QThreadPool, Signal, QTimer,
                            QAbstractAnimation, QVariantAnimation, QEasingCurve,
                            QElapsedTimer, QPointF)
from PySide6.QtGui import (QImageReader, QImage, QPixmap, QPainter, QColor,
                           QTransform, QSurfaceFormat, QPen)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                               QGraphicsItem, QStyleOptionGraphicsItem,
                               QWidget, QVBoxLayout, QHBoxLayout,
                               QComboBox, QCheckBox, QSpinBox,
                               QPushButton, QLabel)

from config.setting import Setting
from task.task_download import FileData


class ReadNewGraphicsItem(QGraphicsItem):
    """单张图片的 item。自身不管布局——位置/尺寸全部由 StripView 决定
    （item 只负责"画"，view 负责"摆"），这样布局逻辑可以按模式统一处理。

    为什么不用 QGraphicsPixmapItem（实测见 bench_item_vs_pixmapitem.py）：
    1) 它的 boundingRect 就是位图尺寸，只能靠 setScale **等比**缩放；而本类
       必须做到"显示尺寸"与"位图尺寸"完全解耦——图片尺寸未知时先用占位宽高比
       参与布局，位图是之后按 dpr 解码出来的，且连续模式需要**非等比拉伸**
       （宽固定为 cross、长随图片比例）。
    2) 占位框、加载失败提示、页模式的信箱式居中（_fit）都要自己画。
    3) 它默认 shapeMode=MaskShape，命中测试时会去算 pixmap 的 alpha mask，
       比本类默认的 boundingRect 更贵。
    性能：PixmapItem 确实快一点，但快的几乎全是"PySide6 每次 paint 从 C++
    回调进 Python"的开销（约 10us/item，一屏 2~3 张 = 0.03ms/帧，不足 60fps
    一帧预算的 0.2%）。真正的绘制大头是"绘制时缩放位图"（1x→4x 位图慢 3 倍），
    这个已由 DecodeTask 的降采样（max_px）规避，跟 item 类型无关。"""

    # 图片尺寸未知时（还没探测到文件头）的兜底宽高比 h/w = 1.2，即假设图片比
    # 正方形略"竖"。尺寸一旦探测到就立即修正（见 _correct_len）。
    DEFAULT_ASPECT = 1.2
    # ---- 加载进度环 ----
    PROGRESS_MIN_D = 28.0  # 进度环最小直径（小于它视觉上看不清）
    PROGRESS_MAX_D = 56.0  # 进度环最大直径（再大就喧宾夺主）
    PROGRESS_RATIO = 0.28  # 直径 = 占位框短边 × 这个值（再钳制到上面两个极值）
    SPIN_INTERVAL = 80  # 不确定态（总大小未知）转圈动画的帧间隔 ms
    SPIN_STEP = 0.12  # 每帧相位推进量（1.0 = 转一整圈）
    SPIN_ARC = 100  # 不确定态那段弧的角度（度）

    # 不确定态进度环的旋转相位（0~1，1 = 转满一圈）。模块级全局：所有 item 共享
    # 同一个相位即可（它们本来就应该同步转动），由 StripView._spin_timer 推进。
    SPIN_PHASE = 0.0

    def __init__(self, index: int, default_aspect: float = DEFAULT_ASPECT):
        super().__init__()
        self.index = index              #
        self.pixmap = None          # 解码完成后的图像；None = 还没加载完（画占位框）
        self.isAnima = False
        self._def_aspect = default_aspect     # 兜底宽高比 h/w（尺寸未知时先用它估高度）
        self.fmt = None
        self._size: QSize = None                     # QSize：图片真实尺寸（API 预估/头探测/解码，任一来源）
        self._size_known = False              # True = _size 是精确值，之后不再修正
        self.file_data: FileData = None
        self._reply = None                    # 正在进行的网络请求（None = 没在下载）
        self._re_download_cnt = 0
        self._decoding = False                # 后台解码中（下载完成 -> 等预解码窗口触发）
        self._pending_decode = False           # 有新字节等着解码（下载完 / 位图被 LRU 回收后）
        self._failed = False                  # 下载/解码失败（占位框变红显示"加载失败"）
        self._waifu_failed = False                  # 下载/解码失败（占位框变红显示"加载失败"）
        self._progress = None                 # 下载进度 0.0~1.0（由 QNetworkReply 的
                                              # downloadProgress 写入）；None = 总大小
                                              # 未知（chunked 响应没有 Content-Length），
                                              # 此时进度环画成不停转圈的"不确定态"

        # self._is_waifu2x = False
        self._cur_is_waifu2x_px = False       # 当前是否使用了waifu2x pixmap
        self._waifu2x_state = 0               # 0 == auto, -1 == close, 1 == open
        self._waifu_reply = None              # 正在进行的超分请求（None = 没在下载）
        self._waifu_tick = 0
        self.waifu_file_data: FileData = None

        self._fit = False                     # True = 页模式：图片等比缩放画在矩形里（信箱留白）；
                                              # False = 连续模式：拉伸填满整个矩形（无缝拼接）
        self._fit_align = (0, 0)              # _fit 模式下内容在矩形里的对齐 (ax, ay)：
                                              # -1=靠左/上、0=居中、+1=靠右/下。
                                              # 双页模式两张图都朝中缝贴（±1），其余居中(0)
        # ---- 动图（GIF / 动画 WebP）----
        # QMovie 在主线程创建（它是 QObject，且有内部定时器，必须在 GUI 线程），
        # 由 view 负责创建/回收；item 只持有引用并在 paint 里取当前帧。
        self._movie = None                    # QMovie；None = 没创建（动图但没在播放）
        self._movie_buf = None                # QMovie 的数据源 QBuffer（要跟 movie 同生共死）
        self._raw = QByteArray()              # 动图的原始压缩字节（用来重建 QMovie）
        self._anim_seq = 0                    # 最近一次"该播放"的时间戳（LRU 回收用，越大越新）
        # ---- 布局状态（由 view 写入，item 自己只读）----
        self._s = 0.0        # 在阅读方向上的偏移：图片起点距离第一张图起点的距离
        self._len = 0.0      # 沿滚动轴占据的长度（ttb=高，横排=宽）
        self._w = self._h = 1.0   # item 的显示宽高（boundingRect 用）

    def init(self):
        self.pixmap = None          # 解码完成后的图像；None = 还没加载完（画占位框）
        self.isAnima = False
        self.fmt = None
        self._size: QSize = None                     # QSize：图片真实尺寸（API 预估/头探测/解码，任一来源）
        self._size_known = False              # True = _size 是精确值，之后不再修正
        self.file_data: FileData = None
        self._reply = None                    # 正在进行的网络请求（None = 没在下载）
        self._re_download_cnt = 0
        self._decoding = False                # 后台解码中（下载完成 -> 等预解码窗口触发）
        self._pending_decode = False           # 有新字节等着解码（下载完 / 位图被 LRU 回收后）
        self._failed = False                  # 下载/解码失败（占位框变红显示"加载失败"）
        self._waifu_failed = False                  # 下载/解码失败（占位框变红显示"加载失败"）
        self._progress = None                 # 下载进度 0.0~1.0（由 QNetworkReply 的
                                              # downloadProgress 写入）；None = 总大小
                                              # 未知（chunked 响应没有 Content-Length），
                                              # 此时进度环画成不停转圈的"不确定态"

        self._cur_is_waifu2x_px = False       # 当前是否使用了waifu2x pixmap
        self._waifu2x_state = 0               # 0 == auto, -1 == close, 1 == open
        self._waifu_reply = None              # 正在进行的超分请求（None = 没在下载）
        self._waifu_tick = 0
        self.waifu_file_data: FileData = None

        self._fit = False                     # True = 页模式：图片等比缩放居中画在矩形里（周围留白）；
        self._fit_align = (0, 0)              # _fit 模式下内容在矩形里的对齐 (ax, ay)：
                                              # -1=靠左/上、0=居中、+1=靠右/下。
                                              # 双页模式两张图都朝中缝贴（±1），其余居中(0)
        # ---- 动图（GIF / 动画 WebP）----
        # QMovie 在主线程创建（它是 QObject，且有内部定时器，必须在 GUI 线程），
        # 由 view 负责创建/回收；item 只持有引用并在 paint 里取当前帧。
        self._movie = None                    # QMovie；None = 没创建（动图但没在播放）
        self._movie_buf = None                # QMovie 的数据源 QBuffer（要跟 movie 同生共死）
        self._raw = QByteArray()              # 动图的原始压缩字节（用来重建 QMovie）
        self._anim_seq = 0                    # 最近一次"该播放"的时间戳（LRU 回收用，越大越新）
        # ---- 布局状态（由 view 写入，item 自己只读）----
        self._s = 0.0        # 在阅读方向上的偏移：图片起点距离第一张图起点的距离
        self._len = 0.0      # 沿滚动轴占据的长度（ttb=高，横排=宽）
        self.prepareGeometryChange()   # 改 boundingRect 前必须调用（Qt 规则）
        self._w = self._h = 1.0   # item 的显示宽高（boundingRect 用）

    @property
    def _buf(self):
        if not self.file_data:
            return None
        return self.file_data.data

    @property
    def _waifu_buf(self):
        if not self.waifu_file_data:
            return None
        return self.waifu_file_data.data

    @property
    def is_not_waifu2x(self):
        return self._waifu2x_state == -1

    @property
    def is_need_waifu2x(self):
        return (not self.isAnima and (self._waifu2x_state == 0 and Setting.IsOpenWaifu.value) or (self._waifu2x_state == 1))

    @property
    def is_downloading(self):
        return self._reply is not None

    @property
    def is_need_download(self):
        # 如果没有pixmap，
        return (self.pixmap is None
                and not self.is_downloading)

    @property
    def is_decoding(self):
        return True

    @property
    def is_waifu2xing(self):
        return True

    @property
    def is_waifu_decoding(self):
        return True

    @property
    def is_animated(self) -> bool:
        """这张是不是动图（GIF/动画 WebP）。看 _raw 而不是 _movie —— QMovie
        被 LRU 回收后它依然是动图，只是暂时停在海报帧。"""
        return self._raw

    def set_geometry(self, w, h):
        """设置显示宽高。变化 <0.01px 时跳过——prepareGeometryChange 有开销
        （会让 Qt 重新计算碰撞索引），布局频繁微调时不能每次都触发。"""
        if abs(w - self._w) < 0.01 and abs(h - self._h) < 0.01:
            return
        self.prepareGeometryChange()   # 改 boundingRect 前必须调用（Qt 规则）
        self._w, self._h = w, h

    def boundingRect(self) -> QRectF:
        """item 占据的矩形（本地坐标）。Qt 用它做裁剪/碰撞索引，
        必须覆盖 paint 画到的全部区域。"""
        return QRectF(0, 0, self._w, self._h)

    def _aligned_rect(self, w: float, h: float) -> QRectF:
        """_fit 模式下把 w×h 的内容放进 item 矩形（_w×_h）时的目标矩形。

        对齐由 _fit_align=(ax, ay) 决定：-1 靠左/上、0 居中、+1 靠右/下。
        双页模式用它让同页两张图都朝中缝贴（±1），像翻开的书页拼在一起；
        单页/占位默认 (0,0) 居中。"""
        ax, ay = self._fit_align
        x = 0.0 if ax < 0 else (self._w - w if ax > 0 else (self._w - w) / 2)
        y = 0.0 if ay < 0 else (self._h - h if ay > 0 else (self._h - h) / 2)
        return QRectF(x, y, w, h)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        # _fit=True（单/双页模式）：图片等比缩放进 item 矩形，位置按 _fit_align
        # （单页居中、双页朝中缝贴），信箱式留白；
        # _fit=False（连续模式）：图片拉伸填满整个 item 矩形（无缝拼接）
        #
        # 绘制优先级：QMovie 当前帧 > 静态 QPixmap > 占位框。
        # 注意 currentPixmap() 返回的是内部帧的共享副本，每帧取的开销约等于一次
        # 引用计数，不要缓存它（缓存了就永远停在某一帧）。
        pm = self._movie.currentPixmap() if self._movie is not None else self.pixmap
        if pm is not None and not pm.isNull():
            sr = QRectF(pm.rect())    # 源矩形（PM 自身单位；见下面关于 dpr 的说明）
            if self._fit:
                sc = min(self._w / sr.width(), self._h / sr.height())
                painter.drawPixmap(
                    self._aligned_rect(sr.width() * sc, sr.height() * sc), pm, sr)
            else:
                # 两者宽高比一致，实际无变形
                painter.drawPixmap(QRectF(0, 0, self._w, self._h), pm, sr)
            return
        # 未加载完/失败：画占位框（红色 = 失败，灰色 = 加载中）
        if self._fit:
            # 占位框也按（已知的或兜底的）宽高比、同一个对齐方式画，
            # 加载完成后无缝替换（不会"跳"位置）
            if self._size and self._size.isValid() and self._size.height() > 0:
                rw = self._size.width() / self._size.height()   # 宽高比 w/h
            else:
                rw = 1.0 / self._def_aspect
            pw, ph = self._w, self._w / rw
            if ph > self._h:
                ph, pw = self._h, self._h * rw
            rect = self._aligned_rect(pw, ph)
        else:
            rect = QRectF(0, 0, self._w, self._h)
        # view 开了 DontSavePainterState（Qt 不自动保存/恢复 painter 状态），
        # 这里改过的 pen/brush/font 必须自己 save+restore，否则会污染后画的 item
        painter.save()
        painter.setPen(QColor(0, 0, 0, 25))
        painter.setBrush(QColor(220, 60, 60, 25) if self._failed else QColor(0, 0, 0, 15))
        painter.drawRoundedRect(rect, 8, 8)
        if self._reply is not None:
            # 正在下载：画圆形进度环（比一行文字更直观，也顺便说明"卡在下载"）
            self._draw_progress(painter, rect)
            painter.restore()
            return
        if self._waifu_reply is not None:
            self._draw_progress_ring(painter, rect)
            painter.restore()
            return
        painter.setPen(QColor(0, 0, 0, 90))
        f = painter.font()
        f.setPixelSize(13)
        painter.setFont(f)
        painter.drawText(rect, Qt.AlignCenter,
                         "加载失败" if self._failed
                         else ("解码中…" if self._decoding else "等待加载…"))
        painter.restore()

    def _draw_progress(self, painter: QPainter, rect: QRectF):
        """在 rect 正中画一个圆形进度环。

        两种形态：
        - 确定态（_progress 是 0~1 的数，服务器给了 Content-Length）：
          整圈是轨道，按进度画一段弧，中心写百分比；
        - 不确定态（_progress 是 None，chunked 响应没有总大小）：
          画一段固定 100° 的弧匀速旋转，表示"在动但不知道还要多久"。
          相位来自模块级 SPIN_PHASE（view 的定时器推进），所有 item 同步转。

        注意 view 开了 DontSavePainterState 优化（不自动保存/恢复 painter 状态），
        所以这里改过的画笔/画笔状态必须自己 save+restore，否则会污染后续 item。
        """
        d = min(rect.width(), rect.height()) * self.PROGRESS_RATIO
        d = max(self.PROGRESS_MIN_D, min(self.PROGRESS_MAX_D, d))
        r = d / 2.0
        cx, cy = rect.center().x(), rect.center().y()
        box = QRectF(cx - r, cy - r, d, d)
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 70))          # 底盘：保证任何底图上都看得清
        painter.drawEllipse(QPointF(cx, cy), r + 5, r + 5)
        painter.setBrush(Qt.NoBrush)
        track = QPen(QColor(255, 255, 255, 70), 3)     # 轨道（整圈，暗）
        painter.setPen(track)
        painter.drawEllipse(QPointF(cx, cy), r, r)
        arc = QPen(QColor(255, 255, 255, 235), 3)      # 进度弧（亮）
        arc.setCapStyle(Qt.RoundCap)
        painter.setPen(arc)
        # Qt 的 drawArc：角度单位 1/16 度，0° 在 3 点钟方向，逆时针为正。
        # 从 12 点起顺时针画 -> 起始角 90*16，跨度取负
        if self._progress is None:
            painter.drawArc(box, int((90 - self.SPIN_PHASE * 360.0) * 16), -self.SPIN_ARC * 16)
        else:
            painter.drawArc(box, 90 * 16, int(-self._progress * 360 * 16))
            if d >= 40:                                # 太小就不塞文字了
                f = painter.font()
                f.setPixelSize(12)
                painter.setFont(f)
                painter.setPen(QColor(255, 255, 255, 240))
                painter.drawText(box, Qt.AlignCenter,
                                 f"{int(self._progress * 100)}%")
        painter.restore()

    def _draw_progress_ring(self, painter: QPainter, rect: QRectF,
                           phase: float = 0.0):
        """在 rect 正中画一个进度环——可直接抄进任何 QGraphicsItem.paint 里。

        progress : None = 不确定态（转圈）；0.0~1.0 = 确定态（填充 + 百分比）
        phase    : 不确定态的旋转相位 0~1（由外部定时器推进，不要在 paint 里算时间）

        自己 save/restore，所以调用方就算开了 DontSavePainterState 也不会被污染。
        """
        d = min(rect.width(), rect.height()) * self.PROGRESS_RATIO
        d = max(self.PROGRESS_MIN_D, min(self.PROGRESS_MAX_D, d))
        r = d / 2.0
        cx, cy = rect.center().x(), rect.center().y()
        box = QRectF(cx - r, cy - r, d, d)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)

        # 1) 底盘：保证任何底图上都看得清环
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 90))
        painter.drawEllipse(QPointF(cx, cy), r + 5, r + 5)

        # 2) 轨道：整圈，暗
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(255, 255, 255, 70), 3))
        painter.drawEllipse(QPointF(cx, cy), r, r)

        # 3) 进度弧：亮，圆头
        arc = QPen(QColor(255, 255, 255, 240), 3)
        arc.setCapStyle(Qt.RoundCap)
        painter.setPen(arc)
        # 不确定态：从 12 点偏 phase 处起，画固定 SPIN_ARC 度，随时间转
        painter.drawArc(box, int((90 - phase * 360.0) * 16), -int(self.SPIN_ARC) * 16)

        text_top = rect.center().y() + 42
        painter.drawText(QRectF(rect.left(), text_top, rect.width(), 40),
                         Qt.AlignHCenter | Qt.AlignTop, "waifu2x")
        painter.restore()