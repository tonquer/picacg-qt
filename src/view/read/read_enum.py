from enum import Enum

from PySide6.QtCore import QSize, QPoint

from config import config
from config.setting import Setting
from tools.str import Str
from tools.tool import ToolUtil


class ReadMode(Enum):
    """ 阅读模式 """
    UpDown = 0  # 上下模式
    LeftRight = 1  # 默认
    LeftRightDouble = 2  # 左右双页
    RightLeftDouble = 3  # 右左双页
    LeftRightScroll = 4  # 左右滚动
    RightLeftScroll = 5  # 右左滚动
    RightLeftDouble2 = 6  # 右左双页(滚轮正序)
    Samewight = 7  # 等宽模式

    @staticmethod
    def isDouble(model):
        return model in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2]

    @staticmethod
    def isRightLeft(model):
        return model in [ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2, ReadMode.RightLeftScroll]

    @staticmethod
    def isUpDown(model):
        return model not in [ReadMode.LeftRightScroll, ReadMode.RightLeftDouble2, ReadMode.RightLeftScroll]

    @staticmethod
    def isScroll(model):
        return model in [ReadMode.UpDown, ReadMode.LeftRightScroll, ReadMode.RightLeftScroll]


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
    OverResolution = Str.OverResolution
    AnimationNotAuto = Str.AnimationNotAuto

    def __init__(self):
        self.size = 0
        self.w = 0
        self.h = 0
        self.mat = "jpg"
        self.scaleW = 0
        self.scaleH = 0
        self.state = self.Downloading
        self.data = None
        self._isWaifu2x = -1
        self.waifuState = self.WaifuStateCancle
        self.waifuDataSize = 0
        self.waifuData = None
        self.waifuTick = 0
        self.waifu2xTaskId = 0
        self.model = {}

        self.cacheImage = None
        self.cacheImageScale = ""
        self.cacheImageTaskId = 0
        self.cacheWaifu2xImage = None
        self.cacheWaifu2xImageScale = ""
        self.cacheWaifu2xImageTaskId = 0

        self.downloadSize = 0
        self.isGif = False
        self.saveParams = None

    @property
    def isWaifu2x(self):
        if self._isWaifu2x == -1:
            return Setting.IsOpenWaifu.value
        return self._isWaifu2x

    @isWaifu2x.setter
    def isWaifu2x(self, value):
        self._isWaifu2x = value

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

        self.w, self.h, self.mat, isAni = ToolUtil.GetPictureSize(data)

        if self.cacheImage:
            if Setting.IsOpenWaifu.value:
                self.waifuState = self.WaifuWait
            else:
                self.waifuState = self.WaifuStateCancle

            if max(self.w, self.h) <= Setting.LookMaxNum.value:
                pass
            else:
                if self._isWaifu2x == -1:
                    self.waifuState = self.OverResolution

            if self._isWaifu2x == -1 and isAni:
                self.waifuState = self.AnimationNotAuto

        self.isGif = isAni
        self.data = data
        self.model = ToolUtil.GetLookScaleModel(category, self.w, self.h, self.mat)
        self.state = self.DownloadSuc
        self.size = len(data)

    def SetWaifuData(self, data, tick):
        if not data:
            self.waifuState = self.WaifuStateFail
            return
        self.waifuData = data
        self.waifuState = self.WaifuStateEnd
        self.waifuDataSize = len(self.waifuData)
        self.scaleW, self.scaleH, _, _ = ToolUtil.GetPictureSize(data)
        self.waifuTick = tick
        return

    @staticmethod
    def GetReadScale(stripModel, scaleCnt, maxWidth, maxHeight, isToQImage):
        # 不进行缩放了，因为导致模糊
        if stripModel == ReadMode.LeftRight:
            scale = (1 + scaleCnt * 0.1)
            wight = int(maxWidth * scale)
            height = maxHeight * scale
            toScaleW = wight
            toScaleH = height
        elif stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2]:
            scale = (1 + scaleCnt * 0.1)
            toScaleW =int(maxWidth // 2 * scale)
            toScaleH = maxHeight * scale

        elif stripModel in [ReadMode.LeftRightDouble]:
            scale = (1 + scaleCnt * 0.1)

            toScaleW = int(maxWidth // 2 * scale)
            toScaleH = maxHeight * scale
        elif stripModel in [ReadMode.LeftRightScroll]:
            scale = (1 + scaleCnt * 0.1)
            toScaleW = maxWidth * scale * 10
            toScaleH = min(maxHeight, maxHeight * scale)

        elif stripModel in [ReadMode.RightLeftScroll]:
            scale = (1 + scaleCnt * 0.1)
            toScaleW = maxWidth * scale * 10
            toScaleH = min(maxHeight, maxHeight * scale)

        elif stripModel in [ReadMode.UpDown]:
            scale = (1 + scaleCnt * 0.1)
            toScaleW = min(maxWidth, maxWidth * scale)
            toScaleH = maxHeight * scale * 10
        elif stripModel in [ReadMode.Samewight]:
            scale = (1 + scaleCnt * 0.1)
            toScaleW = maxWidth * scale
            toScaleH = maxHeight * scale * 10
        else:
            return maxWidth, maxHeight

        # if not ReadMode.isScroll(stripModel):
        if isToQImage:
            toScaleH = 0
            toScaleW = 0
        return toScaleW, toScaleH

    @staticmethod
    def GetReadToPos(stripModel, maxWidth, maxHeight, toWidth, toHeight, index, curIndex, oldPos):
        if stripModel in [ReadMode.LeftRight, ReadMode.Samewight]:
            return QPoint(maxWidth // 2 - toWidth // 2, max(0, maxHeight // 2 - toHeight // 2))
        elif stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2]:
            if index == curIndex:
                return QPoint(maxWidth // 2, max(0, maxHeight // 2 - toHeight // 2))
            else:
                return QPoint(maxWidth // 2 - toWidth, max(0, maxHeight // 2 - toHeight // 2))
        elif stripModel in [ReadMode.LeftRightDouble]:
            if index != curIndex:
                return QPoint(maxWidth // 2, max(0, maxHeight // 2 - toHeight // 2))
            else:
                return QPoint(maxWidth // 2 - toWidth, max(0, maxHeight // 2 - toHeight // 2))
        elif stripModel in [ReadMode.LeftRightScroll]:
            return QPoint(oldPos.x(), max(0, maxHeight // 2 - toHeight // 2))

        elif stripModel in [ReadMode.RightLeftScroll]:
            return QPoint(oldPos.x(), max(0, maxHeight // 2 - toHeight // 2))

        elif stripModel in [ReadMode.UpDown]:
            return QPoint(maxWidth // 2 - toWidth // 2, oldPos.y())
        else:
            return QPoint(0, 0)