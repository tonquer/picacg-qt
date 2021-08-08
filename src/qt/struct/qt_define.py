
from PySide2.QtCore import QSize

from conf import config
from src.util import ToolUtil


class QtFileData(object):
    Downloading = "开始下载"
    Converting = "转换中"
    DownloadSuc = "下载完成"
    DownloadError = "下载错误"
    DownloadReset = "重新下载"

    WaifuWait =  "等待中"
    WaifuStateStart = "解码开始"
    WaifuStateCancle = "不解码"
    WaifuStateEnd = "解码完成"
    WaifuStateFail = "解码失败"

    def __init__(self):
        self.size = 0
        self.w = 0
        self.h = 0
        self.scaleW = 0
        self.scaleH = 0
        self.state = self.Downloading
        self.data = None
        self.waifuState = self.WaifuStateCancle
        self.waifuDataSize = 0
        self.waifuData = None
        self.waifuTick = 0
        self.waifu2xTaskId = 0
        self.model = {}

        self.cacheImage = None
        self.cacheWaifu2xImage = None

        self.downloadSize = 0

    @property
    def qSize(self):
        return QSize(self.w, self.h)

    @property
    def waifuQSize(self):
        return QSize(self.scaleW, self.scaleH)

    def SetData(self, data, category):
        if not data:
            self.state = self.DownloadError
            return
        if config.IsOpenWaifu:
            self.waifuState = self.WaifuWait
        self.data = data
        self.w, self.h = ToolUtil.GetPictureSize(data)
        self.model = ToolUtil.GetLookScaleModel(category)
        self.state = self.DownloadSuc
        self.size = len(data)

    def SetWaifuData(self, data, tick):
        if not data:
            self.waifuState = self.WaifuStateFail
            return
        self.waifuData = data
        self.waifuState = self.WaifuStateEnd
        self.waifuDataSize = len(self.waifuData)
        self.scaleW, self.scaleH = ToolUtil.GetPictureSize(data)
        self.waifuTick = tick
        return


