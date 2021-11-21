from enum import Enum

from PySide6.QtCore import QSize

from config import config
from tools.str import Str
from tools.tool import ToolUtil


class ReadMode(Enum):
    """ 阅读模式 """
    UpDown = 0              # 上下模式
    LeftRight = 1           # 默认
    LeftRightDouble = 2     # 左右双页
    RightLeftDouble = 3     # 右左双页
    LeftRightScroll = 4     # 左右滚动
    RightLeftScroll = 5     # 右左滚动


class QtFileData(object):
    Downloading = Str.Downloading
    Converting = Str.Converting
    DownloadSuc = Str.DownloadSuc
    DownloadError = Str.DownloadError
    DownloadReset = Str.DownloadReset

    WaifuWait = Str.WaifuWait
    WaifuStateStart = Str.WaifuStateStart
    WaifuStateCancle = Str.WaifuStateCancle
    WaifuStateEnd = Str.WaifuStateEnd
    WaifuStateFail = Str.WaifuStateFail

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
