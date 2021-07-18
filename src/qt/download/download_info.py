import os
import weakref

from conf import config
from src.index.book import BookMgr, Book
from src.qt.util.qttask import QtTaskBase
from src.server import req
from src.util import ToolUtil, Log
from src.util.status import Status


class DownloadInfo(QtTaskBase):
    Success = "下载完成"
    Reading = "获取信息"
    ReadingEps = "获取章节"
    ReadingPicture = "获取下载地址"
    Downloading = "正在下载"
    Waiting = "等待中"
    Pause = "暂停"
    Error = "出错了"
    NotFound = "原始文件不存在"

    Converting = "转换中"
    ConvertSuccess = "转换成功"

    def __init__(self, parent):
        QtTaskBase.__init__(self)
        self.bookId = ""     # 书籍id
        self.title = ""      # 标题
        self.savePath = ""   # 保存路径
        self.convertPath = ""
        self.status = self.Waiting      # 状态
        self.tableRow = 0    # 索引
        self.epsInfo = {}    # 下载的章节信息
        self.downloadEpsIds = []  # 下载的章节Id

        self.curDownloadEpsId = -1   # 当前正在下载的章节
        self.curDownloadEpsInfo = None   # 当前正在下载的章节
        self._parent = weakref.ref(parent)

        self.convertStatus = self.Waiting
        self.curConvertEpsId = -1
        self.curConvertEpsInfo = None
        self.speedStr = ""

    @property
    def db(self):
        return self.parent.db

    @property
    def curDownloadPic(self):
        if self.status == self.Success:
            return self.maxDownloadPic
        if not self.curDownloadEpsInfo:
            return 0
        return self.curDownloadEpsInfo.curPreDownloadIndex

    @property
    def maxDownloadPic(self):
        if not self.curDownloadEpsInfo:
            return 0
        return self.curDownloadEpsInfo.picCnt

    @property
    def curDownloadEps(self):
        if self.status == self.Success:
            return len(self.downloadEpsIds)
        if self.curDownloadEpsId in self.downloadEpsIds:
            return self.downloadEpsIds.index(self.curDownloadEpsId)
        return 0

    @property
    def epsCount(self):
        return len(self.downloadEpsIds)

    @property
    def speed(self):
        if not self.curDownloadEpsInfo:
            return 0
        return self.curDownloadEpsInfo.speedDownloadLen

    @speed.setter
    def speed(self, value):
        if self.curDownloadEpsInfo:
            self.curDownloadEpsInfo.speedDownloadLen = value

    @property
    def parent(self):
        return self._parent()

    @property
    def convertTick(self):
        if not self.curConvertEpsInfo:
            return ""
        return str(self.curConvertEpsInfo.tick) + 's'

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
            return len(self.downloadEpsIds)
        if self.curConvertEpsId in self.downloadEpsIds:
            return self.downloadEpsIds.index(self.curConvertEpsId)
        return 0

    @property
    def convertEpsCnt(self):
        return len(self.downloadEpsIds)

    def GetDownloadCompleteEpsId(self):
        if self.curDownloadEpsId < 0:
            return []
        if self.curDownloadEpsId not in self.downloadEpsIds:
            return []
        index = self.downloadEpsIds.index(self.curDownloadEpsId)
        return self.downloadEpsIds[:index+1]

    def StartDownload(self):
        if not self.downloadEpsIds:
            self.SetStatu(self.Error)
            return
        self.AddBookInfos()

    def AddDownload(self, epsIds):
        epsIds.sort()
        for epsId in epsIds:
            if epsId in self.downloadEpsIds:
                continue
            self.downloadEpsIds.append(epsId)
        return

    def AddBookInfos(self):
        self.SetStatu(self.Reading)
        self.AddHttpTask(req.GetComicsBookReq(self.bookId), self.AddBookInfosBack)

    def AddBookInfosBack(self, msg=""):
        if msg != Status.Ok:
            self.SetStatu(self.Error)
            return
        else:
            book = BookMgr().books.get(self.bookId)
            self.title = book.title
            self.savePath = os.path.join(os.path.join(config.SavePath, config.SavePathDir),
                                         ToolUtil.GetCanSaveName(self.title))
            self.savePath = os.path.join(self.savePath, "原图")
            self.convertPath = os.path.join(os.path.join(config.SavePath, config.SavePathDir),
                                         ToolUtil.GetCanSaveName(self.title))
            self.convertPath = os.path.join(self.convertPath, "waifu2x")
            self.AddBookEpsInfos()
        return

    def AddBookEpsInfos(self):
        self.SetStatu(self.ReadingEps)
        self.AddHttpTask(req.GetComicsBookEpsReq(self.bookId), self.AddBookEpsInfosBack)

    def AddBookEpsInfosBack(self, msg):
        if msg != Status.Ok:
            self.SetStatu(self.Error)
            return
        else:
            book = BookMgr().books.get(self.bookId)
            assert isinstance(book, Book)
            for epsId in self.downloadEpsIds:
                if epsId >= len(book.eps):
                    continue
                epsInfo = book.eps[epsId]
                if epsId not in self.epsInfo:
                    info = DownloadEpsInfo(self)
                    info.bookId = self.bookId
                    info.epsId = epsId
                    info.epsTitle = epsInfo.title
                    self.epsInfo[epsId] = info
                    self.parent.db.AddDownloadEpsDB(info)
            if not self.epsInfo:
                self.SetStatu(self.Error)
                return

            if self.curDownloadEpsId < 0 or self.curDownloadEpsId not in self.epsInfo:
                self.curDownloadEpsId = min(self.downloadEpsIds)

            self.curDownloadEpsInfo = self.epsInfo.get(self.curDownloadEpsId)
            self.curDownloadEpsInfo.AddBookEpsPicInfos()
        return

    def SetStatu(self, status):
        self.status = status
        if self.status == self.Success:
            if self in self.parent.downloadingList:
                self.parent.downloadingList.remove(self)
            self.parent.HandlerDownloadList()
            if config.DownloadAuto:
                self.SetConvertStatu(self.Waiting)
                self.parent.AddConvert(self.bookId)
            else:
                self.SetConvertStatu(self.Pause)
            self.parent.HandlerConvertList()

        if status == self.Pause:
            if self.curDownloadEpsInfo:
                self.curDownloadEpsInfo.Pause()
        self.db.AddDownloadDB(self)
        self.parent.UpdateTableItem(self)

    def SwithNextDownload(self):
        index = self.downloadEpsIds.index(self.curDownloadEpsId)
        if index + 1 >= len(self.downloadEpsIds):
            self.SetStatu(self.Success)
            return
        self.curDownloadEpsId = self.downloadEpsIds[index+1]
        self.curDownloadEpsInfo = self.epsInfo.get(self.curDownloadEpsId)
        self.curDownloadEpsInfo.AddBookEpsPicInfos()
        self.parent.db.AddDownloadDB(self)
        return

    def StartConvert(self):
        if not self.downloadEpsIds:
            self.SetConvertStatu(self.Error)
            return
        if self.curConvertEpsId < 0 or self.curConvertEpsId not in self.epsInfo:
            self.curConvertEpsId = min(self.downloadEpsIds)

        self.curConvertEpsInfo = self.epsInfo.get(self.curConvertEpsId)
        self.curConvertEpsInfo.StartConvert()

    def SetConvertStatu(self, status):
        self.convertStatus = status
        if status == self.Pause:
            if self.curConvertEpsInfo:
                self.curConvertEpsInfo.PauseConvert()
        if self.curConvertEpsInfo:
            self.db.AddDownloadEpsDB(self.curConvertEpsInfo)
        self.parent.HandlerConvertList()
        self.parent.UpdateTableItem(self)
        self.db.AddDownloadDB(self)

    def SwithNextConvert(self):
        index = self.downloadEpsIds.index(self.curConvertEpsId)
        if index + 1 >= len(self.downloadEpsIds):
            self.SetConvertStatu(self.ConvertSuccess)
            return
        self.curConvertEpsId = self.downloadEpsIds[index+1]
        self.curConvertEpsInfo = self.epsInfo.get(self.curConvertEpsId)
        self.curConvertEpsInfo.StartConvert()
        self.parent.db.AddDownloadDB(self)
        return

    def UpdateTableItem(self):
        self.parent.UpdateTableItem(self)


class DownloadEpsInfo(QtTaskBase):
    def __init__(self, parent):
        QtTaskBase.__init__(self)
        self._parent = weakref.ref(parent)
        self.epsId = 0        # 章节Id
        self.epsTitle = ""    # 章节名
        self.picCnt = 0       # 图片数
        self.speedDownloadLen = 0
        self.downloadLen = 0
        self.resetCnt = 0

        self.curPreDownloadIndex = 0
        self.curPreConvertId = 0   # 转换
        self.resetConvertCnt = 0
        self.status = DownloadInfo.Downloading
        self.tick = 0

    @property
    def curSavePath(self):
        savePath = os.path.join(self.parent.savePath, ToolUtil.GetCanSaveName(self.epsTitle))
        return os.path.join(savePath, "{:04}.{}".format(self.curPreDownloadIndex + 1, "jpg"))

    @property
    def curConvertPath(self):
        savePath = os.path.join(self.parent.convertPath, ToolUtil.GetCanSaveName(self.epsTitle))
        return os.path.join(savePath, "{:04}.{}".format(self.curPreConvertId + 1, "jpg"))

    @property
    def parent(self):
        assert isinstance(self._parent(), DownloadInfo)
        return self._parent()

    def AddBookEpsPicInfos(self):
        self.parent.SetStatu(DownloadInfo.ReadingPicture)
        self.AddHttpTask(req.GetComicsBookOrderReq(self.parent.bookId, self.epsId+1),
                                        self.AddBookEpsPicInfosBack)

    def AddBookEpsPicInfosBack(self, status):
        if status != Status.Ok:
            self.resetCnt += 1
            if self.resetCnt >= 5:
                self.parent.SetStatu(DownloadInfo.Error)
                return
            self.AddBookEpsPicInfos()
        else:
            self.parent.SetStatu(DownloadInfo.Downloading)
            self.StartDownload()

    def StartDownload(self):
        bookInfo = BookMgr().books.get(self.parent.bookId)
        epsInfo = bookInfo.eps[self.epsId]
        if self.curPreDownloadIndex >= len(epsInfo.pics):
            self.status = DownloadInfo.Success
            self.curPreDownloadIndex = 0
            self.parent.db.AddDownloadEpsDB(self)
            self.parent.SwithNextDownload()
        else:
            self.parent.UpdateTableItem()
            self.AddDownload()
        return

    def AddDownload(self):
        bookInfo = BookMgr().books.get(self.parent.bookId)
        epsInfo = bookInfo.eps[self.epsId]
        isDownloadNext = True
        while self.curPreDownloadIndex < len(epsInfo.pics):
            bookInfo = BookMgr().books.get(self.parent.bookId)
            epsInfo = bookInfo.eps[self.epsId]
            picInfo = epsInfo.pics[self.curPreDownloadIndex]
            self.picCnt = len(epsInfo.pics)
            if os.path.isfile(self.curSavePath):
                self.curPreDownloadIndex += 1
            else:
                isDownloadNext = False
                self.AddDownloadTask(picInfo.fileServer,
                                         picInfo.path,
                                         downloadCallBack=self.AddDownloadBack,
                                         completeCallBack=self.AddDownloadCompleteBack,
                                         isSaveCache=False)
                break
        self.parent.UpdateTableItem()
        if isDownloadNext:
            self.StartDownload()

    def AddDownloadBack(self, data, laveFileSize):
        self.downloadLen += len(data)
        self.speedDownloadLen += len(data)

    def AddDownloadCompleteBack(self, data, msg):
        if msg != Status.Ok:
            self.resetCnt += 1
            if self.resetCnt >= 5:
                self.parent.SetStatu(DownloadInfo.Error)
                return
            self.AddDownload()
        else:
            try:
                savePath = os.path.dirname(self.curSavePath)
                if not os.path.isdir(savePath):
                    os.makedirs(savePath)
                f = open(self.curSavePath, "wb+")
                f.write(data)
                f.close()
                self.curPreDownloadIndex += 1
                self.StartDownload()
            except Exception as es:
                Log.Error(es)
        return

    def StartConvert(self):
        if self.curPreConvertId >= self.picCnt:
            self.status = DownloadInfo.ConvertSuccess
            self.curPreConvertId = 0
            self.parent.SwithNextConvert()
        else:
            self.parent.UpdateTableItem()
            self.AddConvert()
        return

    def AddConvert(self):
        savePath = os.path.join(self.parent.savePath, ToolUtil.GetCanSaveName(self.epsTitle))
        filePath = os.path.join(savePath, "{:04}.{}".format(self.curPreConvertId + 1, "jpg"))
        if not os.path.isfile(filePath):
            self.status = DownloadInfo.NotFound
            self.parent.SetConvertStatu(self.status)
            return
        isConvertNext = True
        while self.curPreConvertId < self.picCnt:
            if os.path.isfile(self.curConvertPath):
                self.curPreConvertId += 1
            else:
                isConvertNext = False
                f = open(filePath, "rb")
                data = f.read()
                f.close()

                w, h = ToolUtil.GetPictureSize(data)
                model = ToolUtil.GetDownloadScaleModel(w, h)
                self.AddConvertTask("", data, model, self.AddConvertBack)
                break
        self.parent.UpdateTableItem()
        if isConvertNext:
            self.StartConvert()
        return

    def AddConvertBack(self, data, waifuId, backParam, tick):
        try:
            if data:
                savePath = os.path.dirname(self.curConvertPath)
                if not os.path.isdir(savePath):
                    os.makedirs(savePath)
                f = open(self.curConvertPath, "wb+")
                f.write(data)
                f.close()
                self.tick = tick
                self.resetConvertCnt = 0
                self.curPreConvertId += 1
                self.StartConvert()
            else:
                self.resetConvertCnt += 1
                if self.resetConvertCnt >= 3:
                    self.status = DownloadInfo.Error
                    self.parent.SetConvertStatu(DownloadInfo.Error)
                else:
                    self.StartConvert()
        except Exception as es:
            Log.Error(es)
            self.status = DownloadInfo.Error
            self.parent.SetConvertStatu(DownloadInfo.Error)
        return

    def Pause(self):
        self.status = DownloadInfo.Pause
        self.ClearTask()
        return

    def PauseConvert(self):
        self.ClearConvert()