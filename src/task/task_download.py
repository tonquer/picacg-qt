import hashlib
import os

from config import config
from config.setting import Setting
from task.qt_task import TaskBase, QtDownloadTask
from tools.log import Log
from tools.status import Status


class TaskDownload(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.downloadBack.connect(self.HandlerTask)

    def AddDownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, isSaveData=True, backParam=None, isSaveCache=True, cleanFlag=None, filePath=""):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.isSaveData = isSaveData
        data.backParam = backParam
        data.url = url
        data.path = path
        self.tasks[self.taskId] = data
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        if isSaveCache:
            if not path:
                a = hashlib.md5(url.encode("utf-8")).hexdigest()
            else:
                a = hashlib.md5(path.encode("utf-8")).hexdigest()
            if Setting.SavePath.value:
                filePath2 = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), os.path.dirname(path))
                filePath2 = os.path.join(filePath2, a)
                data.cacheAndLoadPath = filePath2
        if filePath:
            data.loadPath = filePath

        Log.Debug("add download info, cachePath:{}, loadPath:{}".format(data.cacheAndLoadPath, data.loadPath))
        from server.server import Server
        from server import req
        Server().Download(req.DownloadBookReq(url, path, isSaveCache), backParams=self.taskId, cacheAndLoadPath=data.cacheAndLoadPath, loadPath=data.loadPath)
        return self.taskId

    def HandlerTask(self, downloadId, laveFileSize, data, isCallBack=True):
        info = self.tasks.get(downloadId)
        if not info:
            return
        assert isinstance(info, QtDownloadTask)
        if laveFileSize < 0 and data == b"":
            try:
                if info.downloadCompleteBack:
                    if info.backParam is not None:
                        info.downloadCompleteBack(self.GetDownloadData(downloadId), laveFileSize, info.backParam)
                    else:
                        info.downloadCompleteBack(self.GetDownloadData(downloadId), laveFileSize)
            except Exception as es:
                Log.Error(es)
            self.ClearDownloadTask(downloadId)
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
                        info.downloadCompleteBack(self.GetDownloadData(downloadId), Status.Ok, info.backParam)
                    else:
                        info.downloadCompleteBack(self.GetDownloadData(downloadId), Status.Ok)
                except Exception as es:
                    Log.Error(es)
            self.ClearDownloadTask(downloadId)

    def ClearDownloadTask(self, downloadId):
        info = self.tasks.get(downloadId)
        if not info:
            return
        del info.saveData
        del self.tasks[downloadId]

    def GetDownloadData(self, downloadId):
        if downloadId not in self.tasks:
            return b""
        return self.tasks[downloadId].saveData
