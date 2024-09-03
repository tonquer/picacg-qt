import os
import time

from config import config
from config.setting import Setting
from task.qt_task import QtTaskBase
from tools.str import Str
from tools.tool import ToolUtil


class SaveNameType:
    Default = 0
    AuthorAndTitle = 1
    AuthorDir = 2


class DownloadItem(QtTaskBase):
    Success = Str.Success
    Downloading = Str.Downloading
    Waiting = Str.Waiting
    Pause = Str.Pause
    Error = Str.Error
    SpaceEps = Str.SpaceEps
    UnderReviewBook = Str.UnderReviewBook

    Converting = Str.Converting
    ConvertSuccess = Str.ConvertSuccess

    def __init__(self):
        QtTaskBase.__init__(self)
        self.bookId = ""             # 书籍id
        self.title = ""              # 标题
        self.tick = int(time.time())                #
        self.author = ""              # 作者名
        self.savePath = ""           # 保存路径
        self.convertPath = ""        # Waifu2x路径
        self.status = self.Pause       # 状态
        self.statusMsg = ""

        self.tableRow = 0                # 索引
        self.epsInfo = {}                # 下载的章节信息
        self.epsIds = []                 # 下载的章节Id
        self.curDownloadEpsId = -1       # 当前正在下载的章节, 不是索引
        self.convertStatus = self.Pause
        self.convertMsg = ""
        self.curConvertEpsId = -1        # 当前正在转换的章节, 不是索引
        self.speedStr = ""

        self.downloadLen = 0
        self.speedDownloadLen = 0
        self.downloadReset = 0
        self.convertReset = 0
        self.cvTick = 0
        self.dirty = True

    @property
    def curDownloadPic(self):
        if self.status == self.Success:
            return self.maxDownloadPic
        return self.curDownloadEpsInfo.curPreDownloadIndex

    @property
    def maxDownloadPic(self):
        return self.curDownloadEpsInfo.picCnt

    @property
    def curDownloadEps(self):
        if self.status == self.Success:
            return len(self.epsIds)
        if self.curDownloadEpsInfo.curPreDownloadIndex > 0 and self.curDownloadEpsInfo.curPreDownloadIndex >= self.curDownloadEpsInfo.picCnt:
            return self.epsIds.index(self.curDownloadEpsId) + 1
        return self.epsIds.index(self.curDownloadEpsId)

    @property
    def epsCount(self):
        return len(self.epsIds)

    @property
    def speed(self):
        return self.speedDownloadLen

    @speed.setter
    def speed(self, value):
        self.speedDownloadLen = value

    @property
    def convertTick(self):
        return str(self.cvTick) + 's'

    @property
    def curConvertCnt(self):
        if self.convertStatus == self.ConvertSuccess:
            return self.convertCnt
        if not self.curConvertEpsInfo:
            return 0
        return self.curConvertEpsInfo.curPreConvertId

    @property
    def convertCnt(self):
        if not self.curConvertEpsInfo:
            return 0
        return self.curConvertEpsInfo.picCnt

    @property
    def curConvertEps(self):
        if self.convertStatus == self.ConvertSuccess:
            return len(self.epsIds)
        if self.curConvertEpsInfo.curPreConvertId > 0 and self.curConvertEpsInfo.curPreConvertId >= self.curConvertEpsInfo.picCnt:
            return self.epsIds.index(self.curConvertEpsId) + 1
        return self.epsIds.index(self.curConvertEpsId)

    @property
    def convertEpsCnt(self):
        return len(self.epsIds)

    @property
    def curDownloadEpsInfo(self):
        if self.curDownloadEpsId < 0:
            self.curDownloadEpsId = self.epsIds[0]

        epsInfo = self.epsInfo.get(self.curDownloadEpsId)
        if not epsInfo:
            epsInfo = DownloadEpsItem()
            epsInfo.bookId = self.bookId
            epsInfo.epsId = self.curDownloadEpsId
            self.epsInfo[self.curDownloadEpsId] = epsInfo
        return epsInfo

    def IsEpsComplete(self, epsId):
        epsInfo = self.epsInfo.get(epsId)
        if not epsInfo:
            return False
        return epsInfo.isDownloadComplete()

    def IsWaifu2xComplete(self, epsId):
        epsInfo = self.epsInfo.get(epsId)
        if not epsInfo:
            return False
        return epsInfo.isConvertComplete()
    @property
    def curConvertEpsInfo(self):
        if self.curConvertEpsId < 0:
            self.curConvertEpsId = self.epsIds[0]

        epsInfo = self.epsInfo.get(self.curConvertEpsId)
        if not epsInfo:
            epsInfo = DownloadEpsItem()
            epsInfo.bookId = self.bookId
            epsInfo.epsId = self.curConvertEpsId
            self.epsInfo[self.curConvertEpsId] = epsInfo
        return epsInfo

    def GetStatusMsg(self):
        if self.statusMsg:
            return Str.GetStr(self.statusMsg)
        return Str.GetStr(self.status)

    def GetConvertStatusMsg(self):
        if self.convertMsg:
            return Str.GetStr(self.convertMsg)
        return Str.GetStr(self.convertStatus)

    # 初始化下载，检查下载的索引
    def DownloadInit(self):
        if not self.epsIds:
            return self.Error

        if not Setting.SavePath.value:
            return self.Error

        if self.curDownloadEpsId < 0 or self.curDownloadEpsId not in self.epsInfo:
            self.curDownloadEpsId = self.epsIds[0]

        while True:
            if self.curDownloadEpsInfo.isDownloadComplete():
                index = self.epsIds.index(self.curDownloadEpsId)
                if index + 1 >= len(self.epsIds):
                    return self.Success
                self.curDownloadEpsId = self.epsIds[index + 1]
            else:
                break
        return self.Downloading

    # 初始化成功回调
    def DownloadInitCallBack(self, bookName, author, title, maxPic):
        if not self.title:
            self.title = bookName
            self.dirty = True
        if not self.author and author.strip() not in [" ", "无", "無", ]:
            self.author = author

        self.curDownloadEpsInfo.dirty = True
        self.curDownloadEpsInfo.picCnt = maxPic
        self.curDownloadEpsInfo.epsTitle = title
        return

    # 下载成功回调
    def DownloadSucCallBack(self):
        self.dirty = True
        self.curDownloadEpsInfo.dirty = True
        self.curDownloadEpsInfo.curPreDownloadIndex += 1
        while True:
            if self.curDownloadEpsInfo.isDownloadComplete():
                index = self.epsIds.index(self.curDownloadEpsId)
                if index + 1 >= len(self.epsIds):
                    return self.Success
                self.curDownloadEpsId = self.epsIds[index + 1]
            else:
                break
        self.curDownloadEpsInfo.dirty = True
        return self.Downloading

    # 获得下载参数
    def GetDownloadPath(self):
        # 如果没有初始化，先初始化
        if not self.curDownloadEpsInfo.epsTitle or self.curDownloadEpsInfo.picCnt <= 0:
            return self.curDownloadEpsInfo.epsId, 0, "", True

        if not self.savePath and Setting.SavePath.value:
            path = os.path.join(Setting.SavePath.value, config.SavePathDir)
            path2 = os.path.join(path, ToolUtil.GetCanSaveName(self.title))
            self.savePath = os.path.join(path2, "original")
            if Setting.SaveNameType.value == SaveNameType.AuthorAndTitle:
                if self.author:
                    path2 = os.path.join(path, ToolUtil.GetCanSaveName("[{}]".format(self.author)+self.title))
                    self.savePath = os.path.join(path2, "original")
            elif Setting.SaveNameType.value == SaveNameType.AuthorDir:
                if self.author:
                    path2 = os.path.join(path, os.path.join(ToolUtil.GetCanSaveName(self.author), ToolUtil.GetCanSaveName(self.title)))
                else:
                    path2 = os.path.join(path, os.path.join("default", ToolUtil.GetCanSaveName(self.title)))
                self.savePath = os.path.join(path2, "original")

        convertPath = os.path.join(self.savePath, ToolUtil.GetCanSaveName(self.curDownloadEpsInfo.epsTitle))
        savePath = os.path.join(convertPath, "{:04}.{}".format(self.curDownloadEpsInfo.curPreDownloadIndex + 1, "jpg"))
        return self.curDownloadEpsInfo.epsId, self.curDownloadEpsInfo.curPreDownloadIndex, savePath, False

    def ConvertInit(self):
        if not self.epsIds:
            return self.Error

        if not Setting.SavePath.value:
            return self.Error

        if self.curConvertEpsId < 0 or self.curConvertEpsId not in self.epsIds:
            self.curConvertEpsId = min(self.epsIds)

        while True:
            if self.curConvertEpsInfo.isConvertComplete():
                index = self.epsIds.index(self.curConvertEpsId)
                if index + 1 >= len(self.epsIds):
                    return self.ConvertSuccess
                self.curConvertEpsId = self.epsIds[index + 1]
            else:
                break

        if self.curConvertEpsInfo.curPreConvertId >= self.curConvertEpsInfo.curPreDownloadIndex:
            return self.Waiting

        return self.Converting

    def ConvertSucCallBack(self, cvTick):
        self.dirty = True
        self.cvTick = cvTick
        self.curConvertEpsInfo.dirty = True
        self.curConvertEpsInfo.curPreConvertId += 1
        while True:
            if self.curConvertEpsInfo.isConvertComplete():
                index = self.epsIds.index(self.curConvertEpsId)
                if index + 1 >= len(self.epsIds):
                    return self.ConvertSuccess
                self.curConvertEpsId = self.epsIds[index + 1]
            else:
                break

        self.curConvertEpsInfo.dirty = True
        if self.curConvertEpsInfo.curPreConvertId >= self.curConvertEpsInfo.curPreDownloadIndex:
            return self.Waiting
        else:
            return self.Converting

    def GetConvertPath(self):

        if not self.convertPath and Setting.SavePath.value:
            self.convertPath = self.savePath.replace("original", "waifu2x")
            # path = os.path.join(Setting.SavePath.value, config.SavePathDir)
            # path2 = os.path.join(path, ToolUtil.GetCanSaveName(self.title))
            # self.convertPath = os.path.join(path2, "waifu2x")
            # if Setting.SaveNameType.value == SaveNameType.AuthorAndTitle:
            #     if self.author:
            #         path2 = os.path.join(path, ToolUtil.GetCanSaveName("[{}]".format(self.author)+self.title))
            #         self.convertPath = os.path.join(path2, "waifu2x")
            # elif Setting.SaveNameType.value == SaveNameType.AuthorDir:
            #     if self.author:
            #         path2 = os.path.join(path, os.path.join(ToolUtil.GetCanSaveName(self.author), ToolUtil.GetCanSaveName(self.title)))
            #     else:
            #         path2 = os.path.join(path, os.path.join("default", ToolUtil.GetCanSaveName(self.title)))
            #     self.convertPath = os.path.join(path2, "waifu2x")

        downloadPath = os.path.join(self.savePath, ToolUtil.GetCanSaveName(self.curConvertEpsInfo.epsTitle))
        loadPath = os.path.join(downloadPath, "{:04}.{}".format(self.curConvertEpsInfo.curPreConvertId + 1, "jpg"))

        convertPath = os.path.join(self.convertPath, ToolUtil.GetCanSaveName(self.curConvertEpsInfo.epsTitle))
        savePath = os.path.join(convertPath, "{:04}.{}".format(self.curConvertEpsInfo.curPreConvertId + 1, "jpg"))
        return loadPath, savePath


class DownloadEpsItem(QtTaskBase):
    def __init__(self):
        QtTaskBase.__init__(self)
        self.bookId = 0
        self.epsId = 0      # 章节Id
        self.epsTitle = ""  # 章节名
        self.picCnt = 0     # 图片数
        self.curPreDownloadIndex = 0    # 当前要下载的
        self.curPreConvertId = 0        # 当前要转换的

        self.dirty = True

    def isDownloadComplete(self):
        if not self.epsTitle:
            return False
        if self.picCnt <= 0:
            return False
        return self.curPreDownloadIndex >= self.picCnt

    def isConvertComplete(self):
        if not self.epsTitle:
            return False
        if self.picCnt <= 0:
            return False
        return self.curPreConvertId >= self.picCnt
