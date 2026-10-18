from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from view.read.read_new_view import ReadNewView
    from view.read.read_new_frame import ReadNewFrame

from PySide6.QtCore import Signal
from PySide6.QtCore import QBuffer, QIODevice, QRunnable, QSize, QObject
from PySide6.QtGui import QImageReader, Qt, QImage

from task.task_local import LocalData
from tools.tool import ToolUtil

from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from config.setting import Setting


class ReadNewTask(QtTaskBase):
    def __init__(self, parent):
        QtTaskBase.__init__(self)
        self.parent = parent

    @property
    def readView(self) -> ReadNewView:
        return self.parent

    @property
    def isLocal(self):
        return self.readView.isLocal

    @property
    def isOffline(self):
        return self.readView.isOffline

    @property
    def cacheBook(self) -> LocalData:
        return self.readView.cacheBook

    @property
    def bookId(self):
        return self.readView.bookId

    @property
    def epsId(self):
        return self.readView.epsId

    def AddDownload(self, i, downloadCallBack=None, completeCallBack2=None):
        loadPath = QtOwner().downloadView.GetDownloadFilePath(self.bookId, self.epsId, i)
        if self.isLocal:
            assert isinstance(self.cacheBook, LocalData)
            return self.AddLocalTaskLoadPicture(self.cacheBook, i, completeCallBack2=completeCallBack2, backparam=i)
        elif not self.isOffline:
            return self.AddDownloadBook(self.bookId, self.epsId, i,
                                 downloadCallBack=downloadCallBack,
                                 completeCallBack2=completeCallBack2,
                                 backParam=i, loadPath=loadPath)
        else:
            return self.AddDownloadBookCache(loadPath, completeCallBack2=completeCallBack2, backParam=i)

    def AddCovertData(self, i, data, model, callBack=None):
        path = ToolUtil.GetRealPath(i + 1, "book/{}/{}".format(self.bookId, self.epsId + 1))
        if Setting.PreDownWaifu2x.value:
            filePath = QtOwner().downloadView.GetDownloadWaifu2xFilePath(self.bookId, self.epsId, i)
        else:
            filePath = ""

        if self.isLocal:
            return self.AddConvertTask(path, data, model, completeCallBack2=callBack, backParam=i, noSaveCache=True)
        else:
            return self.AddConvertTask(path, data, model, completeCallBack2=callBack, backParam=i, preDownPath=filePath)


class _DecodeSignals(QObject):
    # 跨线程只传 QImage（QImage 可重入 + 原子引用计数的隐式共享，
    # 官方文档明确允许跨线程拷贝）；QPixmap 转换在主线程 _on_loaded 里做
    loaded = Signal(int, QSize, QImage)


class DecodeTask(QRunnable):
    """在 QThreadPool 后台线程解码图片 + 生成缩小的位图。
    为什么放后台：解码一张 4000px 的图要几十上百毫秒，放主线程会卡滚动。

    参数：
      data   完整的图片字节（从网络下载的 _buf）
      max_px 缩放上限（物理像素）：解码后宽度超过它就等比缩小。
             窗口里图片最多显示 cross×dpr 宽，没必要保留 4K 原图，
             缩小既省内存又让后续绘制更快。
      dpr    设备像素比，设到 QImage 上：1 物理像素 = 1/dpr 逻辑像素，
             这样 pixmap 的"逻辑尺寸"正好等于 item 矩形，绘制时 1:1 无缩放
             （高分屏不发虚）。
    """

    def __init__(self, index, data: bytes, max_px: int, dpr: float = 1.0):
        super().__init__()
        self.index, self.data, self.max_px, self.dpr = index, data, max_px, dpr
        self.signals = _DecodeSignals()
        self.setAutoDelete(True)     # run() 结束后 Qt 自动 delete 这个任务对象

    def run(self):
        # 不要用 QBuffer(QByteArray) 构造（PySide6 指针生命周期问题会挂死），
        # setData 是深拷贝进 buffer 内部，安全
        buf = QBuffer()
        buf.setData(self.data)
        buf.open(QIODevice.ReadOnly)
        reader = QImageReader(buf)
        reader.setAutoTransform(True)   # 按 EXIF 旋转（手机竖拍的照片）
        img = reader.read()
        if img.isNull():
            return                      # 解码失败：静默丢弃（占位框继续显示"加载中"）
        real = img.size()               # 原图尺寸，回传给 view 修正布局
        if img.width() > self.max_px:
            img = img.scaledToWidth(self.max_px, Qt.SmoothTransformation)
        # dpr 设在 QImage 上，fromImage 转换时会保留
        img.setDevicePixelRatio(self.dpr)
        self.signals.loaded.emit(self.index, real, img)   # 跨线程信号 -> 主线程槽

