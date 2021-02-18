from io import BytesIO

from PIL import Image
from PyQt5.QtGui import QPixmap

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
        self.pData = None
        self.waifuState = self.WaifuStateStart
        self.waifuDataSize = 0
        self.waifuData = None
        self.waifuPData = None
        self.waifuTick = 0

    def SetData(self, data):
        if not data:
            self.state = self.DownloadError
            return
        self.data = data
        img = Image.open(BytesIO(data))
        self.format = img.format
        self.w = img.width
        self.h = img.height
        self.scale, self.noise = ToolUtil.GetScaleAndNoise(self.w, self.h)
        self.state = self.DownloadSuc
        self.size = len(data)

    def SetWaifuData(self, data, tick):
        if not data:
            self.waifuState = self.WaifuStateFail
            return
        self.waifuData = data
        if self.data and self.pData:
            self.data = None
        self.waifuState = self.WaifuStateEnd
        self.waifuDataSize = len(self.waifuData)
        self.waifuTick = tick
        return

    def GetPData(self):
        if self.pData:
            return self.pData
        if not self.data:
            return None
        self.pData = QPixmap()
        self.pData.loadFromData(self.data)
        if self.waifuData or self.waifuPData:
            self.data = None

        return self.pData

    def GetWaifuPData(self):
        if self.waifuPData:
            return self.waifuPData
        if not self.waifuData:
            return None
        self.waifuPData = QPixmap()
        self.waifuPData.loadFromData(self.waifuData)
        self.waifuData = None
        return self.waifuPData

