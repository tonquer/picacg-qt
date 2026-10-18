import math
from enum import Enum

from PySide6.QtCore import QSize, QPoint

from config import config
from config.setting import Setting
from tools.str import Str
from tools.tool import ToolUtil, time_me


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
    RightLeftScroll2 = 8  # 右左滚动(滚轮正序)

    @staticmethod
    def isUpDown(model):
        return model in [ReadMode.UpDown, ReadMode.Samewight]

    @staticmethod
    def isDouble(model):
        return model in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2]

    @staticmethod
    def isLeftRight(model):
        return model in [ReadMode.LeftRight, ReadMode.LeftRightDouble, ReadMode.LeftRightScroll]

    @staticmethod
    def isWheelLeftRight(model):
        return model in [ReadMode.LeftRight, ReadMode.LeftRightDouble, ReadMode.LeftRightScroll, ReadMode.LeftRightDouble, ReadMode.RightLeftScroll]

    @staticmethod
    def isRightLeft(model):
        return model in [ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2, ReadMode.RightLeftScroll, ReadMode.RightLeftScroll2]

    # @staticmethod
    # def isUpDown(model):
    #     return model not in [ReadMode.LeftRightScroll, ReadMode.RightLeftDouble2, ReadMode.RightLeftScroll, ReadMode.RightLeftScroll2]

    @staticmethod
    def isScroll(model):
        return model in [ReadMode.UpDown, ReadMode.LeftRightScroll, ReadMode.RightLeftScroll, ReadMode.RightLeftScroll2]

    @staticmethod
    def isRightScroll(model):
        return model in [ReadMode.RightLeftScroll, ReadMode.RightLeftScroll2]


class ReadShowState(object):
    def __init__(self) -> None:
        self.index = 0
        self.cacheScaleCnt = 0
        self.scaleCnt = 0
        self.toW = 0
        self.toH = 0
        # self.w = 0
        # self.h = 0
        # self.toW = 0
        # self.toH = 0
        self.isWaifu2x = False

    def Clear(self):
        self.__init__()

    def IsSame(self, other):
        if not other:
            return False
        return (self.index == other.index and
                self.scaleCnt == other.scaleCnt and
                self.cacheScaleCnt == other.cacheScaleCnt and
                self.toW == other.toW and
                self.toH == other.toH and
                self.isWaifu2x == other.isWaifu2x)



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
