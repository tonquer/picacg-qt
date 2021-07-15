import hashlib
import os
import threading
import time
from queue import Queue
from types import FunctionType
import json
from PySide2.QtCore import Signal, QObject

from conf import config
from src.util import Singleton, Log
from src.util.status import Status
from src.util.tool import CTime, ToolUtil


class QtTaskQObject(QObject):
    taskBack = Signal(int, str)
    downloadBack = Signal(int, int, bytes)
    convertBack = Signal(int)

    def __init__(self):
        super(self.__class__, self).__init__()


class QtHttpTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""


class QtDownloadTask(object):
    def __init__(self, downloadId=0):
        self.downloadId = downloadId
        self.downloadCallBack = None       # addData, laveSize
        self.downloadCompleteBack = None   # data, status
        self.fileSize = 0
        self.isSaveData = True
        self.saveData = b""
        self.url = ""
        self.path = ""
        self.originalName = ""
        self.backParam = None
        self.cleanFlag = ""
        self.tick = 0
        self.cacheAndLoadPath = ""   # 缓存和加载
        self.loadPath = ""  # 只加载

        self.imgData = b""
        self.scale = 0
        self.noise = 0
        self.model = {
            "model": 1,
            "scale": 2,
            "toH": 100,
            "toW": 100,
        }


class QtTaskBase:
    Id = 1

    def __init__(self):
        self.__taskFlagId = QtTaskBase.Id
        QtTaskBase.Id += 1

    @property
    def req(self):
        return

    # callBack(data)
    # callBack(data, backParam)
    def AddHttpTask(self, req, callBack=None, backParam=None):
        return QtTask().AddHttpTask(req, callBack, backParam, cleanFlag=self.__taskFlagId)

    # downloadCallBack(data, laveFileSize, backParam)
    # downloadCallBack(data, laveFileSize)
    # downloadCompleteBack(data, st)
    # downloadCompleteBack(data, st, backParam)
    def AddDownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, isSaveData=True, backParam=None, isSaveCache=True, filePath=""):
        return QtTask().AddDownloadTask(url, path, downloadCallBack, completeCallBack, isSaveData, backParam, isSaveCache, self.__taskFlagId, filePath)

    # completeCallBack(saveData, taskId, backParam, tick)
    def AddConvertTask(self, path, imgData, model, completeCallBack, backParam=None, filePath=""):
        return QtTask().AddConvertTask(path, imgData, model, completeCallBack, backParam, self.__taskFlagId, filePath)

    def ClearTask(self):
        return QtTask().CancelTasks(self.__taskFlagId)

    def ClearConvert(self):
        return QtTask().CancelConver(self.__taskFlagId)

    def ClearWaitConvertIds(self, taskIds):
        return QtTask().ClearWaitConvertIds(taskIds)

class QtTask(Singleton, threading.Thread):

    def __init__(self):
        Singleton.__init__(self)
        threading.Thread.__init__(self)
        self._inQueue = Queue()
        self.taskObj = QtTaskQObject()
        self.taskObj.taskBack.connect(self.HandlerTask2)
        self.taskObj.downloadBack.connect(self.HandlerDownloadTask)
        self.taskObj.convertBack.connect(self.HandlerConvertTask)

        self.convertThread = threading.Thread(target=self.RunLoad)
        self.convertThread.setDaemon(True)
        self.convertThread.start()

        self.downloadTask = {}   # id: task
        self.convertLoad = {}  # id: task
        self.convertId = 1000000

        self.taskId = 0
        self.tasks = {}  # id: task

        self.flagToIds = {}  #
        self.convertFlag = {}

    @property
    def convertBack(self):
        return self.taskObj.convertBack

    @property
    def taskBack(self):
        return self.taskObj.taskBack

    @property
    def downloadBack(self):
        return self.taskObj.downloadBack

    def GetDownloadData(self, downloadId):
        if downloadId not in self.downloadTask:
            return b""
        return self.downloadTask[downloadId].saveData

    # def PutTask(self, task):
    #     self._inQueue.put(task)

    def AddHttpTask(self, req, callBack=None, backParam=None, cleanFlag=None):
        self.taskId += 1
        info = QtHttpTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        from src.server import Server
        if isinstance(req, FunctionType):
            req(self.taskId)
        else:
            Server().Send(req, backParam=self.taskId)
        return

    def AddDownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, isSaveData=True, backParam=None, isSaveCache=True, cleanFlag=None, filePath=""):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.isSaveData = isSaveData
        data.backParam = backParam
        data.url = url
        data.path = path
        self.downloadTask[self.taskId] = data
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        if isSaveCache:
            if not path:
                a = hashlib.md5(url.encode("utf-8")).hexdigest()
            else:
                a = hashlib.md5(path.encode("utf-8")).hexdigest()
            filePath2 = os.path.join(os.path.join(config.SavePath, config.CachePathDir), os.path.dirname(path))
            filePath2 = os.path.join(filePath2, a)
            data.cacheAndLoadPath = filePath2
        if filePath:
            data.loadPath = filePath

        Log.Debug("add download info, cachePath:{}, loadPath:{}".format(data.cacheAndLoadPath, data.loadPath))
        from src.server import Server
        from src.server import req
        Server().Download(req.DownloadBookReq(url, path, isSaveCache), bakParams=self.taskId, cacheAndLoadPath=data.cacheAndLoadPath, loadPath=data.loadPath)
        return self.taskId

    def HandlerTask2(self, taskId, data):
        try:
            info = self.tasks.get(taskId)
            if not info:
                Log.Warn("[Task] not find taskId:{}, {}".format(taskId, data))
                return
            assert isinstance(info, QtHttpTask)
            if info.cleanFlag:
                taskIds = self.flagToIds.get(info.cleanFlag, set())
                taskIds.discard(info.taskId)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(data)
                else:
                    info.callBack(data, info.backParam)
                del info.callBack
            del self.tasks[taskId]
        except Exception as es:
            Log.Error(es)

    def HandlerDownloadTask(self, downlodaId, laveFileSize, data, isCallBack=True):
        info = self.downloadTask.get(downlodaId)
        if not info:
            return
        assert isinstance(info, QtDownloadTask)
        if laveFileSize == -1 and data == b"":
            try:
                if info.downloadCompleteBack:
                    if info.backParam is not None:
                        info.downloadCompleteBack(self.GetDownloadData(downlodaId), Status.Error, info.backParam)
                    else:
                        info.downloadCompleteBack(self.GetDownloadData(downlodaId), Status.Error)
            except Exception as es:
                Log.Error(es)
            self.ClearDownloadTask(downlodaId)
            return

        if info.isSaveData:
            info.saveData += data

        if info.downloadCallBack:
            try:
                if info.backParam is not None:
                    info.downloadCallBack(data, laveFileSize, info.backParam)
                else:
                    info.downloadCallBack(data, laveFileSize)
            except Exception as es:
                Log.Error(es)
        if laveFileSize == 0 and data == b"":
            if info.downloadCompleteBack:
                try:
                    if info.cleanFlag:
                        taskIds = self.flagToIds.get(info.cleanFlag, set())
                        taskIds.discard(info.downloadId)
                    if info.backParam is not None:
                        info.downloadCompleteBack(self.GetDownloadData(downlodaId), Status.Ok, info.backParam)
                    else:
                        info.downloadCompleteBack(self.GetDownloadData(downlodaId), Status.Ok)
                except Exception as es:
                    Log.Error(es)
            self.ClearDownloadTask(downlodaId)

    def ClearDownloadTask(self, downlodaId):
        info = self.downloadTask.get(downlodaId)
        if not info:
            return
        del info.saveData
        del self.downloadTask[downlodaId]

    def CancelTasks(self, cleanFlag):
        taskIds = self.flagToIds.get(cleanFlag, set())
        if not taskIds:
            return
        for taskId in taskIds:
            if taskId in self.downloadTask:
                del self.downloadTask[taskId]

            if taskId in self.downloadTask:
                del self.downloadTask[taskId]
        self.flagToIds.pop(cleanFlag)

    def AddConvertTask(self, path, imgData, model, completeCallBack, backParam=None, cleanFlag=None, filePath=""):
        info = QtDownloadTask()
        info.downloadCompleteBack = completeCallBack
        info.backParam = backParam
        self.taskId += 1
        self.convertLoad[self.taskId] = info
        info.downloadId = self.taskId
        info.imgData = imgData
        info.model = model
        if path:
            a = hashlib.md5((path+json.dumps(model)).encode("utf-8")).hexdigest()
            path = os.path.join(os.path.join(config.SavePath, config.CachePathDir), config.Waifu2xPath)
            path = os.path.join(path, a)
            info.cacheAndLoadPath = path
        info.loadPath = filePath
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.convertFlag.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        Log.Debug("add convert info, cachePath:{}, loadPath:{}".format(info.cacheAndLoadPath, info.loadPath))
        self._inQueue.put(self.taskId)
        return self.taskId

    def HandlerConvertTask(self, taskId, isCallBack=True):
        if taskId not in self.convertLoad:
            return
        t1 = CTime()
        info = self.convertLoad[taskId]
        assert isinstance(info, QtDownloadTask)

        if info.cleanFlag:
            taskIds = self.convertFlag.get(info.cleanFlag, set())
            taskIds.discard(info.downloadId)
        info.downloadCompleteBack(info.saveData, taskId, info.backParam, info.tick)
        if info.cleanFlag:
            taskIds = self.convertFlag.get(info.cleanFlag, set())
            taskIds.discard(info.downloadId)
        del self.convertLoad[taskId]
        t1.Refresh("RunLoad")

    def LoadData(self):
        if not config.CanWaifu2x:
            return None
        import waifu2x
        return waifu2x.load(10)

    def RunLoad(self):
        while True:
            time.sleep(0.1)
            while True:
                try:
                    taskId = self._inQueue.get(False)
                    if taskId not in self.convertLoad:
                        continue
                    task = self.convertLoad.get(taskId)
                    isFind = False
                    for cachePath in [task.cacheAndLoadPath, task.loadPath]:
                        data = ToolUtil.LoadCachePicture(cachePath)
                        if data:
                            task.saveData = data
                            self.convertBack.emit(taskId)
                            isFind = True
                            break
                    if isFind:
                        continue
                    if config.CanWaifu2x:
                        import waifu2x
                        sts = waifu2x.add(task.imgData, task.model.get('model', 0), task.downloadId, format="jpg", width=task.model.get("width", 0),
                                               high=task.model.get("high", 0), scale=task.model.get("scale", 0))

                        Log.Warn("add convert info, taskId: {}, model:{}, sts:{}".format(str(task.taskId), task.model,
                                                                                                 str(sts)))
                    else:
                        sts = -1
                    if sts <= 0:
                        self.convertBack.emit(taskId)
                        continue
                except Exception as es:
                    break

            info = self.LoadData()
            if not info:
                continue
            t1 = CTime()
            data, convertId, taskId, tick = info
            if taskId not in self.convertLoad:
                continue
            if not data:
                lenData = 0
            else:
                lenData = len(data)

            Log.Warn("convert suc, taskId: {}, dataLen:{}, sts:{} tick:{}".format(str(taskId), lenData,
                                                                                          str(convertId),
                                                                                          str(tick)))
            info = self.convertLoad[taskId]
            assert isinstance(info, QtDownloadTask)
            info.saveData = data
            info.tick = tick
            if info.cacheAndLoadPath and not os.path.isdir(os.path.dirname(info.cacheAndLoadPath)):
                os.makedirs(os.path.dirname(info.cacheAndLoadPath))
            if info.cacheAndLoadPath and data:
                with open(info.cacheAndLoadPath, "wb+") as f:
                    f.write(data)
                Log.Debug("add convert cache, cachePath:{}".format(info.cacheAndLoadPath))
            else:
                pass
            self.convertBack.emit(taskId)
            t1.Refresh("RunLoad")

    def CancelConver(self, cleanFlag):
        taskIds = self.convertFlag.get(cleanFlag, set())
        if not taskIds:
            return
        for taskId in taskIds:
            if taskId in self.convertLoad:
                del self.convertLoad[taskId]
        Log.Info("cancel convert taskId, {}".format(taskIds))
        self.convertFlag.pop(cleanFlag)
        if config.CanWaifu2x:
            import waifu2x
            waifu2x.remove(list(taskIds))

    def ClearWaitConvertIds(self, taskIds):
        for taskId in taskIds:
            if taskId in self.convertLoad:
                del self.convertLoad[taskId]
        Log.Info("cancel wait convert taskId, {}".format(taskIds))
        if config.CanWaifu2x:
            import waifu2x
            waifu2x.removeWaitProc(list(taskIds))