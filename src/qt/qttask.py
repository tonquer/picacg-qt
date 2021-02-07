import hashlib
import os
import time
import weakref
from queue import Queue

from PyQt5.QtCore import pyqtSignal, QObject

from conf import config
from src.util import Singleton, Log
from src.util.status import Status


class QtTaskQObject(QObject):
    taskBack = pyqtSignal(int, str)
    downloadBack = pyqtSignal(int, int, bytes)

    def __init__(self):
        super(self.__class__, self).__init__()


class QtHttpTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""


class QtDownloadTask(object):
    def __init__(self, downloadId):
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


class QtTask(Singleton):

    def __init__(self):
        Singleton.__init__(self)
        self._inQueue = Queue()
        self._owner = None
        self.taskObj = QtTaskQObject()
        self.taskObj.taskBack.connect(self.HandlerTask2)
        self.taskObj.downloadBack.connect(self.HandlerDownloadTask)

        self.downloadTask = {}   # id: task

        self.taskId = 0
        self.tasks = {}  # id: task

        self.flagToIds = {}  #

    @property
    def taskBack(self):
        return self.taskObj.taskBack

    @property
    def downloadBack(self):
        return self.taskObj.downloadBack

    @property
    def owner(self):
        from src.qt.qtmain import BikaQtMainWindow
        assert isinstance(self._owner(), BikaQtMainWindow)
        return self._owner()

    def GetDownloadData(self, downloadId):
        if downloadId not in self.downloadTask:
            return b""
        return self.downloadTask[downloadId].saveData

    def SetOwner(self, owner):
        self._owner = weakref.ref(owner)

    # def PutTask(self, task):
    #     self._inQueue.put(task)

    def AddHttpTask(self, func, callBack=None, backParam=None, cleanFlag=""):
        self.taskId += 1
        info = QtHttpTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        func(self.taskId)
        return

    def AddDownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, isSaveData=True, backParam=None, isSaveCache=True, cleanFlag=""):
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

        data = self.LoadCachePicture(url, path)
        if data:
            self.HandlerDownloadTask(self.taskId, 0, data, isCallBack=False)
            self.HandlerDownloadTask(self.taskId, 0, b"", isCallBack=False)
            return 0

        from src.server import Server
        from src.server import req
        Server().Download(req.DownloadBookReq(url, path, isSaveCache), bakParams=self.taskId)
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

            if info.backParam is None:
                info.callBack(data)
            else:
                info.callBack(data, info.backParam)
            del info.callBack
            del self.tasks[taskId]
        except Exception as es:
            import sys
            cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
            e = sys.exc_info()[1]
            Log.Error(cur_tb, e)

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
                import sys
                cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
                e = sys.exc_info()[1]
                Log.Error(cur_tb, e)
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
                import sys
                cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
                e = sys.exc_info()[1]
                Log.Error(cur_tb, e)
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
                    import sys
                    cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
                    e = sys.exc_info()[1]
                    Log.Error(cur_tb, e)
            self.ClearDownloadTask(downlodaId)

    def ClearDownloadTask(self, downlodaId):
        info = self.downloadTask.get(downlodaId)
        if not info:
            return
        del info.saveData
        del self.downloadTask[downlodaId]

    def LoadCachePicture(self, url, path):
        try:
            md5Str = path
            a = hashlib.md5(md5Str.encode("utf-8")).hexdigest()
            filePath = os.path.join(os.path.join(config.SavePath, config.CachePathDir), os.path.dirname(path))
            if not os.path.isdir(filePath):
                os.makedirs(filePath)

            if not os.path.isfile(os.path.join(filePath, a)):
                return None
            with open(os.path.join(filePath, a), "rb") as f:
                data = f.read()
                return data
        except Exception as es:
            import sys
            cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
            e = sys.exc_info()[1]
            Log.Error(cur_tb, e)
        return None

    def CancelTasks(self, cleanFlag):
        taskIds = self.flagToIds.get(cleanFlag, set())
        for taskId in taskIds:
            if taskId in self.downloadTask:
                del self.downloadTask[taskId]

            if taskId in self.downloadTask:
                del self.downloadTask[taskId]
