import hashlib
import os
from functools import partial

from config import config
from config.setting import Setting
from server.sql_server import SqlServer
from task.qt_task import TaskBase, QtTaskBase
from task.task_cache import TaskCache
from tools.book import BookMgr, BookEps, Picture
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class FileData(object):
    def __init__(self, data):
        self.data = data
        w, h, fmt, isAnima = ToolUtil.GetPictureSize(data)
        self.w = w
        self.h = h
        self.isAnima = isAnima
        self.fmt = fmt

class QtDownloadTask(object):
    Waiting = Str.Waiting
    Reading = Str.Reading
    ReadingEps = Str.ReadingEps
    ReadingPicture = Str.ReadingPicture
    Downloading = Str.Downloading
    Success = Str.Success
    Error = Str.Error
    Cache = Str.Cache
    SpaceEps = Str.SpaceEps
    UnderReviewBook = Str.UnderReviewBook
    # Str.UnderReviewBook

    def __init__(self, downloadId=0):
        self.downloadId = downloadId
        self.downloadCallBack = None       # addData, laveSize
        self.downloadCompleteBack = None   # data, status
        self.downloadCompleteBack2 = None  # FileData
        self.statusBack = None
        self.isReload = False
        self.fileSize = 0
        self.url = ""
        self.path = ""
        self.originalName = ""
        self.backParam = None
        self.cleanFlag = ""
        self.addSize = 0
        self.isInit = False

        self.loadPath = ""    # 只加载
        self.cachePath = ""   # 缓存路径
        self.savePath = ""    # 下载保存路径
        self.memCacheKey = ""  ## 计算内存缓存Key
        self.isLoadTask = False

        self.isCacheFetch = False

        self.bookId = ""      # 下载的bookId
        self.epsId = 0        # 下载的章节
        self.index = 0        # 下载的索引
        self.resetCnt = 0     # 重试次数
        from qt_owner import QtOwner
        self.isLocal = True
        self.status = self.Waiting


class TaskDownload(TaskBase, QtTaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        QtTaskBase.__init__(self)
        from task.task_cache import TaskCache
        TaskCache().InitDownload()
        self.taskObj.downloadBack.connect(self.HandlerTask)
        self.taskObj.downloadStBack.connect(self.HandlerTaskSt)
        self.thread.start()

    def Run(self):
        while True:
            v = self._inQueue.get(True)
            self._inQueue.task_done()
            if v == "":
                break
            self.HandlerDownload({"st": Status.Ok}, (v, QtDownloadTask.Waiting))

    def DownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, downloadStCallBack=None, backParam=None, loadPath="", cachePath="", savePath="", cleanFlag="", isReload=False, resetCnt=1, completeCallBack2=None, otherParams=None):
        data = QtDownloadTask()
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.downloadCompleteBack2 = completeCallBack2
        data.backParam = backParam
        data.statusBack = downloadStCallBack
        data.isReload = isReload
        data.url = url
        data.path = path
        data.loadPath = loadPath
        data.cachePath = cachePath
        data.savePath = savePath
        if isinstance(otherParams, dict):
            data.bookId = otherParams.get("bookId", "")
            data.epsId = otherParams.get("epsId", 0)
            data.index = otherParams.get("index", "")
        if cachePath:
            data.memCacheKey = TaskCache().GetPathCacheKey(cachePath)
        Log.Debug("add download info, cachePath:{}, loadPath:{}, savePath:{}".format(data.cachePath, data.loadPath, data.savePath))
        taskId = self._RegisterTask(data, cleanFlag, id_attr="downloadId")
        try:
            # from server.server import Server
            # from server import req
            TaskCache().AddDownloadFromCache(data, resetCnt)
            # Server().Download(req.DownloadBookReq(url, data.loadPath, data.cachePath, data.savePath, data.isReload, resetCnt=resetCnt), backParams=taskId)
        except Exception:
            self._TakeTask(taskId)
            raise
        return taskId

    def HandlerTask(self, downloadId, addFileSize, fileSize, data, isCallBack=True):
        isTerminal = (addFileSize < 0 and data == b"") or addFileSize == -2 or (addFileSize == 0 and data != b"")
        info = self._TakeTask(downloadId) if isTerminal else self._GetTask(downloadId)
        if not info:
            return
        assert isinstance(info, QtDownloadTask)

        # 表示保存失败了
        if addFileSize == -2:
            v = {"st": Status.SaveError}
            self.CallBookBack(v, info)
            return
        st = Str.Error
        if addFileSize < -2:
            st = - addFileSize

        if addFileSize < 0 and data == b"":
            try:
                if info.downloadCompleteBack:
                    if info.backParam is not None:
                        info.downloadCompleteBack(b"", st, info.backParam)
                    else:
                        info.downloadCompleteBack(b"", st)
                if info.downloadCompleteBack2:
                    if info.backParam is not None:
                        info.downloadCompleteBack2(None, st, info.backParam)
                    else:
                        info.downloadCompleteBack2(None, st)

            except Exception as es:
                Log.Error(es)
            return

        if addFileSize > 0:
            info.addSize += addFileSize

            try:
                if info.downloadCallBack:
                    if info.backParam is not None:
                        info.downloadCallBack(info.addSize, fileSize, info.backParam)
                    else:
                        info.downloadCallBack(info.addSize, fileSize)
            except Exception as es:
                Log.Error(es)

        if addFileSize == 0 and data != b"":
                try:
                    if info.downloadCompleteBack:
                        if info.backParam is not None:
                            info.downloadCompleteBack(data, Status.Ok, info.backParam)
                        else:
                            info.downloadCompleteBack(data, Status.Ok)

                    if info.downloadCompleteBack2:
                        if info.backParam is not None:
                            info.downloadCompleteBack2(FileData(data), Status.Ok, info.backParam)
                        else:
                            info.downloadCompleteBack2(FileData(data), Status.Ok)

                except Exception as es:
                    Log.Error(es)

    def DownloadBook(self, bookId, epsId, index, statusBack=None, downloadCallBack=None, completeCallBack=None,
                    backParam=None, loadPath="", cachePath="", savePath="", cleanFlag=None, isInit=False, downloadCompleteBack2=None):
        data = QtDownloadTask()
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.downloadCompleteBack2 = downloadCompleteBack2
        data.isInit = isInit
        data.statusBack = statusBack
        data.backParam = backParam
        data.bookId = bookId
        data.epsId = epsId
        data.index = index
        data.loadPath = loadPath
        data.cachePath = cachePath
        data.savePath = savePath
        Log.Debug("add download book, savePath:{}, loadPath:{}".format(data.savePath, data.loadPath))
        taskId = self._RegisterTask(data, cleanFlag, id_attr="downloadId")
        self._inQueue.put(taskId)
        return taskId

    def DownloadCache(self, filePath, completeCallBack=None, backParam = 0, cleanFlag="", downloadCompleteBack2=None):
        data = QtDownloadTask()
        data.downloadCompleteBack = completeCallBack
        data.downloadCompleteBack2 = downloadCompleteBack2
        data.loadPath = filePath
        data.backParam = backParam
        data.isLoadTask = True
        taskId = self._RegisterTask(data, cleanFlag, id_attr="downloadId")
        self._inQueue.put(taskId)
        return taskId

    def HandlerDownload(self, data, v):
        if not data:
            data = {"st": Status.Error}
        (taskId, newStatus) = v
        task = self._GetTask(taskId)
        if not task:
            return
        backData = {}
        from server import req, ToolUtil
        try:
            assert isinstance(task, QtDownloadTask)
            if task.isLoadTask:
                imgData = ToolUtil.LoadCachePicture(task.loadPath)
                if imgData:
                    TaskBase.taskObj.downloadBack.emit(taskId, len(imgData), len(imgData), b"")
                    TaskBase.taskObj.downloadBack.emit(taskId, 0, len(imgData), imgData)
                else:
                    TaskBase.taskObj.downloadBack.emit(taskId, -Status.FileError, 0, b"")
                return

            isReset = False
            st = data['st']
            if data["st"] != Status.Ok:
                task.resetCnt += 1

                if data['st'] == Status.UnderReviewBook:
                    self.SetTaskStatus(taskId, backData, task.UnderReviewBook)
                    return

                # 失败了
                if task.resetCnt >= 10:
                    self.SetTaskStatus(taskId, backData, task.Error)
                    return

                isReset = True
            else:
                # 防止死循环
                if task.resetCnt >= 50:
                    self.SetTaskStatus(taskId, backData, task.Error)
                    return
                task.status = newStatus

            info = BookMgr().GetBook(task.bookId)
            if task.status == task.Waiting:
                # isReset or self.SetTaskStatus(taskId, backData, task.Reading)
                if not info:
                    if task.isLocal:
                        task.isLocal = False
                        task.resetCnt += 1
                        self.AddSqlTask("book", task.bookId, SqlServer.TaskTypeCacheBook, self.HandlerDownload, (taskId, task.Waiting))
                    else:
                        task.resetCnt += 1
                        self.AddHttpTask(req.GetComicsBookReq(task.bookId), self.HandlerDownload, (taskId, task.Reading), task.cleanFlag)
                    return

                task.status = task.Reading
            if task.status == task.Reading:
                # isReset or self.SetTaskStatus(taskId, backData, task.ReadingEps)
                if info.maxLoadEps <= 0:
                    task.resetCnt += 1
                    self.AddHttpTask(req.GetComicsBookEpsReq(task.bookId), self.HandlerDownload, (taskId, task.Reading), task.cleanFlag)
                    return

                if task.epsId >= info.epsCount:
                    self.SetTaskStatus(taskId, backData, task.Error)
                    return

                if task.epsId not in info.epsDict:
                    loadPage = (info.epsCount - task.epsId - 1) // info.epsLimit

                    task.resetCnt += 1
                    self.AddHttpTask(req.GetComicsBookEpsReq(task.bookId, loadPage+1), self.HandlerDownload, (taskId, task.Reading), task.cleanFlag)
                    return

                task.status = task.ReadingEps
            if task.status == task.ReadingEps:
                # isReset or self.SetTaskStatus(taskId, backData, task.ReadingPicture)
                if task.epsId not in info.epsDict:
                    Log.Warn("eps space error, book_id:{}, eps_id:{}".format(task.bookId, task.epsId))
                    self.SetTaskStatus(taskId, backData, task.SpaceEps)
                    return

                epsInfo = info.epsDict[task.epsId]
                assert isinstance(epsInfo, BookEps)

                if epsInfo.isSpace:
                    Log.Warn("eps space error, book_id:{}, eps:{}".format(task.bookId, epsInfo))
                    self.SetTaskStatus(taskId, backData, task.SpaceEps)
                    return

                if epsInfo.maxPicPages <= 0:
                    task.resetCnt += 1
                    self.AddHttpTask(req.GetComicsBookOrderReq(task.bookId, task.epsId+1), self.HandlerDownload, (taskId, task.ReadingEps), task.cleanFlag)
                    return
                if task.index not in epsInfo.pics:
                    loadPage = task.index // epsInfo.picLimit + 1
                    task.resetCnt += 1
                    self.AddHttpTask(req.GetComicsBookOrderReq(task.bookId, task.epsId+1, loadPage), self.HandlerDownload, (taskId, task.ReadingPicture), task.cleanFlag)
                    return

                task.status = task.ReadingPicture
            if task.status == task.ReadingPicture:
                epsInfo = info.epsDict[task.epsId]
                assert isinstance(epsInfo, BookEps)
                if epsInfo.isSpace:
                    Log.Warn("eps space error, book_id:{}, eps:{}".format(task.bookId, epsInfo))
                    self.SetTaskStatus(taskId, backData, task.SpaceEps)
                    return
                if epsInfo.maxPics <= 0:
                    Log.Warn("eps maxPics error, book_id:{}, eps:{}".format(task.bookId, epsInfo))
                    self.SetTaskStatus(taskId, backData, task.SpaceEps)
                    return

                backData["maxPic"] = epsInfo.maxPics
                backData["title"] = epsInfo.title
                backData["maxEps"] = info.epsCount
                backData["bookName"] = info.title
                backData["author"] = info.author

                if task.isInit:
                    self.SetTaskStatus(taskId, backData, task.Success)
                    return

                if task.savePath:
                    if ToolUtil.IsHaveFile(task.savePath):
                        self.SetTaskStatus(taskId, backData, task.Cache)
                        return
                else:
                    path = ToolUtil.GetRealPath(task.index+1, "book/{}/{}".format(task.bookId, task.epsId+1))
                    cachePath2 = os.path.join(Setting.GetCachePath(), path)
                    checkPaths = [task.loadPath]

                    if Setting.SavePath.value:
                        checkPaths.append(cachePath2)
                        task.cachePath = cachePath2

                    # 修改优先mem缓存
                    for cachePath in checkPaths:
                        if cachePath:
                            task.memCacheKey = TaskCache().GetPathCacheKey(cachePath)
                            imgData = TaskCache().GetMemDataByKey(task.memCacheKey)
                            if imgData:
                                task.isCacheFetch = True
                                TaskBase.taskObj.downloadBack.emit(taskId, len(imgData), len(imgData), b"")
                                TaskBase.taskObj.downloadBack.emit(taskId, 0, len(imgData), imgData)
                                isReset or self.SetTaskStatus(taskId, backData, task.Cache)
                                return

                    for cachePath in checkPaths:
                        if cachePath:
                            task.memCacheKey = TaskCache().GetPathCacheKey(cachePath)
                            imgData = ToolUtil.LoadCachePicture(cachePath)
                            if imgData:
                                TaskBase.taskObj.downloadBack.emit(taskId, len(imgData), len(imgData), b"")
                                TaskBase.taskObj.downloadBack.emit(taskId, 0, len(imgData), imgData)
                                isReset or self.SetTaskStatus(taskId, backData, task.Cache)
                                return

                if task.index not in epsInfo.pics:
                    self.SetTaskStatus(taskId, backData, task.Error)
                    return

                isReset or self.SetTaskStatus(taskId, backData, task.Downloading)

                picInfo = epsInfo.pics[task.index]
                assert isinstance(picInfo, Picture)
                # from server.server import Server
                url = ToolUtil.GetRealUrl(picInfo.fileServer, picInfo.path)
                resetCnt = config.ResetDownloadCnt

                otherParams = {"bookId": task.bookId, "epsId": task.epsId, "type": "book", "index": task.index}
                self.AddDownloadTask(
                    url, "", task.downloadCallBack, task.downloadCompleteBack, task.statusBack,
                    task.backParam, task.loadPath, task.cachePath, task.savePath, task.cleanFlag, resetCnt=resetCnt, completeCallBack2=task.downloadCompleteBack2, otherParams=otherParams)
        except Exception as es:
            Log.Error(es)
            self.SetTaskStatus(taskId, backData, task.Error)
        return

    def SetTaskStatus(self, taskId, backData, status):
        backData["st"] = status
        # print(status)
        self.taskObj.downloadStBack.emit(taskId, dict(backData))
        return

    def CallBookBack(self, data, task):
        try:
            if not task.statusBack:
                return
            if task.backParam is not None:
                task.statusBack(data, task.backParam)
            else:
                task.statusBack(data)
        except Exception as es:
            Log.Error(es)

    def HandlerTaskSt(self, downloadId, data):
        task = self._GetTask(downloadId)
        if not task:
            return
        assert isinstance(task, QtDownloadTask)
        try:
            status = data.get("st") or task.status
            # Downloading 表示元数据已交接给另一个下载任务，不是图片下载完成。
            if status in (task.Success, task.Downloading, task.Error, task.SpaceEps, task.Cache, task.UnderReviewBook):
                task = self._TakeTask(downloadId)
                if not task:
                    return
            self.CallBookBack(data, task)
            st = data.get("st")
            if st:
                task.status = st
        except Exception as es:
            Log.Error(es)

    def ClearDownloadTask(self, downloadId):
        self._TakeTask(downloadId)
