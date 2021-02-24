from io import BytesIO

from PIL import Image
from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QImage

from src.util import ToolUtil


class QtFileData(object):
    Downloading = "开始下载"
    DownloadSuc = "下载完成"
    DownloadError = "下载错误"
    DownloadReset = "重新下载"

    WaifuStateStart = "解码开始"
    WaifuStateCancle = "不解码"
    WaifuStateEnd = "解码完成"
    WaifuStateFail = "解码失败"

    def __init__(self):
        self.size = 0
        self.w = 0
        self.h = 0
        self.format = ""
        self.scale = 0
        self.noise = 0
        self.state = self.Downloading
        self.data = None
        self.waifuState = self.WaifuStateStart
        self.waifuDataSize = 0
        self.waifuData = None
        self.waifuTick = 0

        self.downloadSize = 0

    @property
    def qSize(self):
        return QSize(self.w, self.h)

    @property
    def waifuQSize(self):
        return QSize(self.w*self.scale, self.h*self.scale)

    def SetData(self, data):
        if not data:
            self.state = self.DownloadError
            return
        self.data = data
        imgIo = BytesIO(data)
        img = Image.open(imgIo)
        self.format = img.format
        self.w = img.width
        self.h = img.height
        imgIo.close()
        self.scale, self.noise = ToolUtil.GetScaleAndNoise(self.w, self.h)
        self.state = self.DownloadSuc
        self.size = len(data)

    def SetWaifuData(self, data, tick):
        if not data:
            self.waifuState = self.WaifuStateFail
            return
        self.waifuData = data
        self.waifuState = self.WaifuStateEnd
        self.waifuDataSize = len(self.waifuData)
        self.waifuTick = tick
        return


