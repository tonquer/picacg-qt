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
from view.read.read_frame import ReadFrame
from view.read.read_new_frame import ReadNewFrame
from view.read.read_new_graphics import ReadNewGraphics
from view.read.read_new_graphics_item import ReadNewGraphicsItem
from view.read.read_new_view import ReadNewView

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
    # 跨线程只传数据（QImage / QByteArray 都可跨线程：隐式共享 + 原子引用计数）。
    # QPixmap 转换、QMovie 创建一律放主线程（见 StripItem.is_animated 的注释）
    loaded = Signal(object, QSize, QImage)      # 静态图：一张位图
    animated = Signal(object, QSize, QByteArray)  # 动图：原始字节（主线程建 QMovie）

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
        # 动图判定必须在这里做（后台线程）：GIF/动画 WebP 需要先解出格式信息，
        # 不能指望响应头的 Content-Type（经常是 application/octet-stream，
        # 而且 WebP 有静态和动画两种，URL 后缀看不出来）。
        # imageCount()!=1 而不是 supportsAnimation()：单帧 GIF 应当按静态图处理
        # （走 decode 降采样路径，省掉 QMovie 的整套开销）。
        if reader.supportsAnimation() and reader.imageCount() != 1:
            # 交给主线程建 QMovie（每帧时延由 QMovie 自己管，我们只负责播放/暂停）。
            # 传原始字节而不是 QMovie：QMovie 是 QObject + 内部定时器，必须属于主线程
            self.signals.animated.emit(self.item, reader.size(),
                                       QByteArray(self.data))
            return

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

def make_test_animations(directory, spec=None):
    """生成几张动图（GIF + 动画 WebP）到 directory，返回文件名列表。

    用 Pillow 生成（只是**测试素材**，运行时代码完全不依赖 Pillow）。
    没装 Pillow 就返回空列表：Demo 会安静地跳过动图，不影响其它功能。

    spec：[(格式, 宽, 高, 帧数, 每帧毫秒), ...]，默认 GIF + WebP 各两张。
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return []                      # 没 Pillow：跳过动图素材

    if spec is None:
        spec = [("gif", 480, 320, 8, 120),
                ("webp", 480, 320, 10, 100),
                ("gif", 400, 600, 6, 200),
                ("webp", 640, 360, 12, 80)]
    names = []
    for i, (fmt, w, h, frames, ms) in enumerate(spec):
        ims = []
        for k in range(frames):
            im = Image.new("RGB", (w, h), (20, 24, 40))
            dr = ImageDraw.Draw(im)
            t = k / frames
            dr.ellipse([int(w * 0.15 + t * w * 0.5), int(h * 0.3),
                        int(w * 0.35 + t * w * 0.5), int(h * 0.5)],
                       fill=(int(255 * (1 - t)), int(255 * t), 200))
            dr.rectangle([0, h - 6, int(w * (k + 1) / frames), h], fill=(255, 120, 60))
            dr.text((8, 8), f"{fmt.upper()} frame {k}/{frames}", fill=(255, 255, 255))
            ims.append(im)
        name = f"anim_{i:02d}.{fmt}"
        kw = dict(save_all=True, append_images=ims[1:], duration=ms, loop=0)
        if fmt == "webp":
            kw.update(quality=80, method=4)     # method 越小越快（0=最快）
        ims[0].save(os.path.join(directory, name), **kw)
        names.append(name)
    return names


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
    anim_names = make_test_animations(img_dir)  # 再生成几张 GIF/动画 WebP（需要 Pillow）
    port = start_local_server(img_dir).server_address[1]   # 本地图源端口

    win = QWidget()
    lay = QVBoxLayout(win)
    top = QHBoxLayout()
    combo = QComboBox()                         # 阅读方向选择
    combo.addItems(["上下模式", "默认", "左右双页",
                    "右左双页", "左右滚动", "右左滚动", "右左双页(滚轮正序)", "等宽模式", "右左滚动(滚轮正序)"])


    # page_combo = QComboBox()                    # 页面模式选择
    # page_combo.addItems(["连续滚动", "单页模式", "双页模式"])

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
    # top.addWidget(page_combo)
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
        if not hasattr(item, "url"):
            return
        req = QNetworkRequest(item.url)
        reply = self._nam.get(req)
        item._reply = reply
        # reply.readyRead.connect(lambda: self._on_ready_read(item.index))
        reply.finished.connect(lambda: finished(self, item))

    # img = ReadNewView()
    # view = img.frame.scrollArea
    view = ReadNewGraphics(ReadMode.UpDown)
    img = view
    view._nam = QNetworkAccessManager(view)  # 网络下载器（所有图片共用）
    ReadNewGraphics._start_download = _start_download
    gl_box.toggled.connect(view.set_opengl)      # 运行时热切换 GPU/光栅渲染
    # 下拉框 -> 切换阅读方向（运行时切换，阅读位置按比例保持）
    combo.currentIndexChanged.connect(view.set_mode)
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
    lay.addWidget(img)

    for i in range(40):
        if i % 6 == 3 and anim_names:
            view.add_image(i)
            view._items[i].url = QUrl(f"http://127.0.0.1:{port}/{anim_names.pop(0)}")
        else:
            view.add_image(i)
            view._items[i].url = QUrl(f"http://127.0.0.1:{port}/img_{i:03d}.png")

    win.resize(720, 820)
    win.setWindowTitle("三方向图片流 Demo（ttb / ltr / rtl）")
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()