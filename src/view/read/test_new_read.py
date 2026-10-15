import functools
import http.server
import os
import random
import sys
import tempfile
import threading

from PySide6.QtCore import (Qt, QRectF, QSize, QBuffer, QByteArray, QIODevice,
                            QUrl, QObject, QRunnable, QThreadPool, Signal)
from PySide6.QtGui import (QImageReader, QImage, QPixmap, QPainter, QColor,
                           QLinearGradient)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                               QGraphicsItem, QStyleOptionGraphicsItem, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                               QCheckBox, QSpinBox, QPushButton, QLabel)

from tools.str import Str
from view.read.read_enum import ReadMode
from view.read.read_new_graphics import ReadNewGraphics
from view.read.read_new_graphics_item import ReadNewGraphicsItem

GAP = 10
MAX_ASPECT = 4.0        # 高度上限 = 宽度 * 4
DEFAULT_ASPECT = 1.2    # 拿到尺寸前的默认宽高比（h/w）
PROBE_MIN_BYTES = 512   # 攒够这么多字节才尝试探测尺寸，避免频繁无效解析


# ---------------- 单张图片 item：几何先定死，后修正 ----------------

class FeedItem(QGraphicsItem):
    def __init__(self, url: QUrl, width: float, est_size: QSize = None):
        super().__init__()
        self.url = url
        self.pixmap = None
        self._w = width
        self._h = width * DEFAULT_ASPECT          # 先按默认比例占位

        # 下载状态
        self._buf = QByteArray()
        self._reply = None
        self._size_known = est_size is not None   # 服务器元数据给了尺寸就视为已知
        self._est = est_size
        self._failed = False

        if est_size is not None:
            self._h = self._height_for(est_size)

    def _height_for(self, image_size: QSize) -> float:
        if not image_size.isValid() or image_size.width() <= 0:
            return self._w * DEFAULT_ASPECT
        h = self._w * image_size.height() / image_size.width()
        return min(max(h, self._w * 0.4), self._w * MAX_ASPECT)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._w, self._h)

    def set_geometry(self, w, h):
        self.prepareGeometryChange()
        self._w, self._h = w, h

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        if self.pixmap is not None:
            painter.drawPixmap(QRectF(0, 0, self._w, self._h), self.pixmap,
                               QRectF(self.pixmap.rect()))
            return
        painter.setPen(QColor(0, 0, 0, 25))
        painter.setBrush(QColor(220, 60, 60, 25) if self._failed else QColor(0, 0, 0, 15))
        painter.drawRoundedRect(QRectF(0, 0, self._w, self._h), 8, 8)
        painter.setPen(QColor(0, 0, 0, 90))
        f = painter.font()
        f.setPixelSize(13)
        painter.setFont(f)
        painter.drawText(QRectF(0, 0, self._w, self._h), Qt.AlignCenter,
                         "加载失败" if self._failed else "加载中…")


# ---------------- 后台解码任务（下载完成后，解码放线程池） ----------------

class _DecodeSignals(QObject):
    loaded = Signal(object, QSize, QPixmap)   # item, 真实尺寸, pixmap


class DecodeTask(QRunnable):
    def __init__(self, item, data: QByteArray, target_w: float, dpr: float):
        super().__init__()
        self.item, self.data = item, data
        self.target_w, self.dpr = target_w, dpr
        self.signals = _DecodeSignals()
        self.setAutoDelete(True)

    def run(self):
        # 注意：不要用 QBuffer(QByteArray) 构造 —— PySide6 下传的是指针，
        # 存在生命周期问题会导致 reader.read() 挂死。setData 是深拷贝，安全。
        buf = QBuffer()
        buf.setData(self.data)
        buf.open(QIODevice.ReadOnly)
        reader = QImageReader(buf)
        reader.setAutoTransform(True)
        img = reader.read()
        if img.isNull():
            return
        real = img.size()
        need = max(1, int(self.target_w * self.dpr))
        if img.width() > need:
            img = img.scaledToWidth(need, Qt.SmoothTransformation)
        self.signals.loaded.emit(self.item, real, QPixmap.fromImage(img))


# ---------------- 文件头尺寸解析（纯字节操作，替代 QImageReader.size()） ----------------
# QImageReader.size() 作用在 QBuffer(QByteArray) 上在 PySide6 下会挂死；
# 手工解析更快（纳秒级）也不依赖 Qt 内部行为。

def probe_image_size(data: bytes):
    """从（可能不完整的）图片字节流前缀里解析出 QSize；解析不出返回 None。"""
    n = len(data)
    # PNG: 宽高固定在 IHDR，偏移 16/20
    if data[:8] == b"\x89PNG\r\n\x1a\n" and n >= 24:
        return QSize(int.from_bytes(data[16:20], "big"),
                     int.from_bytes(data[20:24], "big"))
    # JPEG: 扫描段找 SOFn 标记
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < n:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                return QSize(int.from_bytes(data[i + 7:i + 9], "big"),
                             int.from_bytes(data[i + 5:i + 7], "big"))
            if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            if i + 4 > n:
                break
            i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
        return None
    # GIF: 逻辑屏幕尺寸在偏移 6
    if data[:4] == b"GIF8" and n >= 10:
        return QSize(int.from_bytes(data[6:8], "little"),
                     int.from_bytes(data[8:10], "little"))
    # BMP
    if data[:2] == b"BM" and n >= 26:
        return QSize(int.from_bytes(data[18:22], "little"),
                     abs(int.from_bytes(data[22:26], "little")))
    # WebP
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        if data[12:16] == b"VP8X" and n >= 30:          # 扩展格式
            return QSize(1 + int.from_bytes(data[24:27], "little"),
                         1 + int.from_bytes(data[27:30], "little"))
        if data[12:16] == b"VP8 " and n >= 30:          # 有损
            return QSize(int.from_bytes(data[26:28], "little") & 0x3FFF,
                         int.from_bytes(data[28:30], "little") & 0x3FFF)
        if data[12:16] == b"VP8L" and n >= 25:          # 无损
            bits = int.from_bytes(data[20:25], "little")
            return QSize((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
    return None


# ---------------- 纵向流视图 ----------------

class FeedView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._nam = QNetworkAccessManager(self)
        self._items = []
        self._content_h = 0.0
        self._content_w = 400.0
        self._was_at_bottom = True
        self._prev_vmax = 0

        vbar = self.verticalScrollBar()
        vbar.rangeChanged.connect(self._on_range_changed)

    # ================ 添加图片 ================

    def add_image(self, url: QUrl, est_size: QSize = None):
        """est_size：如果服务器 API 能返回图片宽高（很多接口都有），传进来
        即可让 item 一创建就是准确高度，连修正都不需要 —— 首选方案。"""
        item = FeedItem(url, self._content_w, est_size)
        item.setPos(0, self._content_h)
        self._scene.addItem(item)
        self._items.append(item)
        self._content_h += item.boundingRect().height() + GAP
        self._scene.setSceneRect(0, 0, self._content_w, self._content_h)

    # ================ 惰性下载：只请求视口附近的图片 ================

    def _load_visible(self):
        v = self.verticalScrollBar().value()
        top, bottom = v - self.height() * 1.5, v + self.height() * 2.5
        for it in self._items:
            if it.pixmap is not None or it._reply is not None or it._failed:
                continue
            if it.y() > bottom:
                break
            if it.y() + it.boundingRect().height() < top:
                continue
            self._start_download(it)

    def _start_download(self, item: FeedItem):
        req = QNetworkRequest(item.url)
        reply = self._nam.get(req)
        item._reply = reply
        reply.readyRead.connect(lambda: self._on_ready_read(item))
        reply.finished.connect(lambda: self._on_finished(item))

    # ================ 渐进式尺寸探测（防跳动的关键之一） ================

    def _on_ready_read(self, item: FeedItem):
        reply = item._reply
        if reply is None:
            return
        item._buf += reply.read(reply.bytesAvailable())
        self._try_probe_size(item)

    def _try_probe_size(self, item: FeedItem):
        if item._size_known or item._buf.size() < PROBE_MIN_BYTES:
            return
        sz = probe_image_size(bytes(item._buf))
        if sz is not None:
            item._size_known = True
            self._correct_height(item, sz)

    # ================ 下载完成 ================

    def _on_finished(self, item: FeedItem):
        reply, item._reply = item._reply, None
        err = reply.error()
        if err == QNetworkReply.NoError:
            item._buf += reply.readAll()
        reply.deleteLater()

        if err != QNetworkReply.NoError or item._buf.isEmpty():
            item._failed = True
            item.update()
            return

        self._try_probe_size(item)  # 最后再试一次（有些格式前面没探测出来）

        task = DecodeTask(item, item._buf, self._content_w, self.devicePixelRatioF())
        task.signals.loaded.connect(self._on_loaded)
        QThreadPool.globalInstance().start(task)
        item._buf = QByteArray()    # 字节已交给解码任务（隐式共享，不拷贝）

    def _on_loaded(self, item: FeedItem, real: QSize, pixmap: QPixmap):
        if not item._size_known:    # 探测失败（罕见），加载完兜底修正
            item._size_known = True
            self._correct_height(item, real)
        item.pixmap = pixmap
        item.update()               # 只重绘，不动几何

    # ================ 高度修正：平移后续内容 + 滚动条补偿 ================

    def _correct_height(self, item: FeedItem, image_size: QSize):
        new_h = item._height_for(image_size)
        old_h = item.boundingRect().height()
        if abs(new_h - old_h) < 0.5:
            return
        delta = new_h - old_h
        item.set_geometry(item.boundingRect().width(), new_h)

        for other in self._items:   # 后续 item 整体下移/上移
            if other.y() > item.y():
                other.setPos(other.x(), other.y() + delta)
        self._content_h += delta
        self._scene.setSceneRect(0, 0, self._content_w, self._content_h)

        # 补偿：被修正的 item 在视口上方时，视口内容会被推移，滚动条同步加 delta
        vbar = self.verticalScrollBar()
        if item.y() < vbar.value():
            vbar.setValue(vbar.value() + delta)

    # ================ 滚动条范围变化：贴底锚点 ================

    def _on_range_changed(self, _min, vmax):
        vbar = self.verticalScrollBar()
        if self._was_at_bottom and vmax > self._prev_vmax:
            vbar.setValue(vmax)      # 原本贴底，追加/长高后仍贴底
        self._prev_vmax = vmax

    # ================ 事件 ================

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        vbar = self.verticalScrollBar()
        self._was_at_bottom = vbar.value() >= vbar.maximum() - 2
        self._load_visible()

    def showEvent(self, ev):
        super().showEvent(ev)
        self._load_visible()

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        new_w = self.viewport().width() - 4
        if abs(new_w - self._content_w) < 1:
            return
        ratio = new_w / self._content_w
        self._content_w = new_w
        y = 0.0
        for it in self._items:
            w, h = it.boundingRect().width(), it.boundingRect().height()
            it.set_geometry(w * ratio, h * ratio)
            it.setPos(0, y)
            y += h * ratio + GAP
        self._content_h = y
        self._scene.setSceneRect(0, 0, self._content_w, self._content_h)
        self._load_visible()


# ---------------- 生成测试图片 + 本地 HTTP 服务器（模拟图源） ----------------

def make_test_images(count=40):
    d = tempfile.mkdtemp(prefix="feed_net_demo_")
    rng = random.Random(7)
    paths = []
    for i in range(count):
        w = rng.randint(320, 720)
        h = rng.randint(200, 2600)
        img = QImage(w, h, QImage.Format_RGB32)
        g = QLinearGradient(0, 0, w, h)
        c1, c2 = rng.randint(40, 200), rng.randint(40, 200)
        g.setColorAt(0.0, QColor(c1, c2, 255 - c1))
        g.setColorAt(1.0, QColor(255 - c1, 255 - c2, c2))
        p = QPainter(img)
        p.fillRect(0, 0, w, h, g)
        p.setPen(QColor(255, 255, 255, 220))
        f = p.font()
        f.setPixelSize(max(24, w // 8))
        p.setFont(f)
        p.drawText(img.rect(), Qt.AlignCenter, f"#{i}  {w}x{h}")
        p.end()
        path = os.path.join(d, f"img_{i:03d}.png")
        img.save(path)
        paths.append(path)
    return d


def start_local_server(directory):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=directory)
    # daemon_threads=True：Qt 会保持 HTTP keep-alive 连接，工作线程不退出，
    # 非 daemon 线程会卡住解释器退出
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv



def main():
    """Demo：本地起 HTTP 服务当图源（模拟网络加载），顶部工具栏可切模式/
    开自动滚动。真实项目里只需关心 StripView + add_image 这几行。"""
    # 多个 QOpenGLWidget 共享 GL 上下文（必须在 QApplication 创建前设置）
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    img_dir = make_test_images(40)              # 生成 40 张随机尺寸测试图
    port = start_local_server(img_dir).server_address[1]   # 本地图源端口

    win = QWidget()
    lay = QVBoxLayout(win)
    top = QHBoxLayout()
    combo = QComboBox()                         # 阅读方向选择
    combo.addItems(["上下滚动（从上到下）", "左右滚动（从左到右）",
                    "右左滚动（漫画模式）"])
    page_combo = QComboBox()                    # 页面模式选择
    page_combo.addItems(["连续滚动", "单页模式", "双页模式"])

    auto_box = QCheckBox("自动滚动")             # 自动滚动开关
    speed_spin = QSpinBox()                     # 速度输入框（px/s）
    speed_spin.setRange(20, 5000)
    speed_spin.setValue(300)
    speed_spin.setSuffix(" px/s")
    gl_box = QCheckBox("OpenGL 加速")            # GPU 渲染开关（运行时可切）
    gl_box.setChecked(True)
    zoom_out_btn = QPushButton("-")              # 缩小一步（÷1.25）
    zoom_reset_btn = QPushButton("100%")         # 重置缩放
    zoom_in_btn = QPushButton("+")               # 放大一步（×1.25）
    zoom_label = QLabel("100%")                  # 当前缩放比（zoomChanged 同步）
    top.addWidget(combo)
    top.addWidget(page_combo)
    top.addWidget(auto_box)
    top.addWidget(speed_spin)
    top.addWidget(gl_box)
    top.addWidget(zoom_out_btn)
    top.addWidget(zoom_reset_btn)
    top.addWidget(zoom_in_btn)
    top.addWidget(zoom_label)
    top.addStretch(1)

    def finished(self, item):
        reply =  item._reply
        err = reply.error()
        data = b""
        if err == QNetworkReply.NoError:
            data += bytes(reply.readAll())     # 最后一批数据
        reply.deleteLater()                  # Qt 网络对象不能直接 del，要 deleteLater

        if err != QNetworkReply.NoError:
            item._failed = True
            item.update()                    # 触发重画（占位框变红显示"加载失败"）
            return
        self._on_finished(data, Str.Ok, item.index)
        return

    def _start_download(self, item: ReadNewGraphicsItem):
        req = QNetworkRequest(item.url)
        reply = self._nam.get(req)
        item._reply = reply
        # reply.readyRead.connect(lambda: self._on_ready_read(item.index))
        reply.finished.connect(lambda: finished(self, item))

    view = ReadNewGraphics(ReadMode.UpDown)
    view._nam = QNetworkAccessManager(view)  # 网络下载器（所有图片共用）
    ReadNewGraphics._start_download = _start_download
    gl_box.toggled.connect(view.set_opengl)      # 运行时热切换 GPU/光栅渲染
    # 下拉框 -> 切换阅读方向（运行时切换，阅读位置按比例保持）
    # combo.currentIndexChanged.connect(
    #     lambda i: view.set_mode([MODE_TTB, MODE_LTR, MODE_RTL][i]))
    # # 页面模式下拉框 -> 切换 连续/单页/双页（进度按"第一条可见图所在页"保持）
    # page_combo.currentIndexChanged.connect(
    #     lambda i: view.set_page_mode([PAGE_STRIP, PAGE_SINGLE, PAGE_DOUBLE][i]))
    # 复选框 -> 开/关自动滚动（速度取输入框的值）
    auto_box.toggled.connect(
        lambda on: view.set_auto_scroll(speed_spin.value() if on else 0))
    # 自动滚动进行中改速度：立即生效（重新 start 会沿用当前位置）
    speed_spin.valueChanged.connect(
        lambda: auto_box.isChecked() and view.set_auto_scroll(speed_spin.value()))
    # 点击停止自动滚动时同步复选框（用户在视图里点击会停止自动，复选框要弹起）
    def sync_auto_box(on):
        auto_box.blockSignals(True)     # 防止 setChecked 再触发 toggled 形成循环
        auto_box.setChecked(on)
        auto_box.blockSignals(False)
    view.autoScrollChanged.connect(sync_auto_box)
    # 缩放按钮（无锚点 = 以视口中心为锚点）；百分比标签跟随 zoomChanged
    zoom_in_btn.clicked.connect(lambda: view.zoom_in())
    zoom_out_btn.clicked.connect(lambda: view.zoom_out())
    zoom_reset_btn.clicked.connect(view.reset_zoom)
    view.zoomChanged.connect(lambda z: zoom_label.setText(f"{z * 100:.0f}%"))

    lay.addLayout(top)
    lay.addWidget(view)

    for i in range(40):
        view.add_image(i)
        view._items[i].url = QUrl(f"http://127.0.0.1:{port}/img_{i:03d}.png")

    win.resize(720, 820)
    win.setWindowTitle("三方向图片流 Demo（ttb / ltr / rtl）")
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()