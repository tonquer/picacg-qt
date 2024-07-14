import hashlib
import os
import threading
from queue import Queue

from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage

from config import config
from config.setting import Setting
from tools.singleton import Singleton


class QtTaskQObject(QObject):
    taskBack = Signal(int, bytes)
    downloadBack = Signal(int, int, bytes)
    downloadStBack = Signal(int, dict)
    convertBack = Signal(int)
    imageBack = Signal(int, QImage)
    sqlBack = Signal(int, bytes)
    localBack = Signal(int, int, list)
    localReadBack = Signal(int, int, bytes)
    uploadBack = Signal(int, int)

    def __init__(self):
        super(self.__class__, self).__init__()


class QtTaskBase:
    Id = 1

    def __init__(self):
        self.__taskFlagId = QtTaskBase.Id
        QtTaskBase.Id += 1

    @property
    def cleanFlag(self):
        return self.__taskFlagId

    @property
    def req(self):
        return

    # callBack(data)
    # callBack(data, backParam)
    def AddHttpTask(self, req, callBack=None, backParam=None, cleanFlag=""):
        from task.task_http import TaskHttp
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskHttp().AddHttpTask(req, callBack, backParam, cleanFlag=cleanFlag)

    def AddSqlTask(self, table, data, taskType, callBack=None, backParam=None):
        from task.task_sql import TaskSql
        return TaskSql().AddSqlTask(table, data, taskType, callBack, backParam, cleanFlag=self.__taskFlagId)

    # downloadCallBack(data, laveFileSize, backParam)
    # downloadCallBack(data, laveFileSize)
    # downloadCompleteBack(data, st)
    # downloadCompleteBack(data, st, backParam)
    def AddDownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, downloadStCallBack=None, backParam=None, loadPath="", cachePath="", savePath="",  cleanFlag="", isReload=False, resetCnt=config.ResetDownloadCntDefault):
        from task.task_download import TaskDownload
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        if not cachePath and not savePath:
            # if not path:
            #     a = hashlib.md5(url.encode("utf-8")).hexdigest() + ".jpg"
            # else:
            #     a = hashlib.md5(path.encode("utf-8")).hexdigest() + ".jpg"
            if Setting.SavePath.value and path:
                filePath2 = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), path)
                cachePath = filePath2
        return TaskDownload().DownloadTask(url, path, downloadCallBack, completeCallBack, downloadStCallBack, backParam, loadPath, cachePath, savePath, cleanFlag, isReload, resetCnt)

    # downloadCallBack(data, laveFileSize, backParam)
    # downloadCallBack(data, laveFileSize)
    # downloadCompleteBack(data, st)
    # downloadCompleteBack(data, st, backParam)
    def AddDownloadBook(self, bookId, epsId, index, statusBack=None, downloadCallBack=None, completeCallBack=None, backParam=None, loadPath="", cachePath="", savePath="", cleanFlag="", isInit=False):
        from task.task_download import TaskDownload
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskDownload().DownloadBook(bookId, epsId, index, statusBack, downloadCallBack, completeCallBack, backParam, loadPath, cachePath, savePath, cleanFlag, isInit)

    def AddDownloadBookCache(self, loadPath, completeCallBack=None, backParam=0, cleanFlag=""):
        from task.task_download import TaskDownload
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskDownload().DownloadCache(loadPath, completeCallBack, backParam, cleanFlag)

    # completeCallBack(saveData, taskId, backParam, tick)
    def AddConvertTask(self, path, imgData, model, completeCallBack, backParam=None, preDownPath=None, noSaveCache=False, cleanFlag=""):
        from task.task_waifu2x import TaskWaifu2x
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskWaifu2x().AddConvertTaskByData(path, imgData, model, completeCallBack, backParam, preDownPath, noSaveCache, cleanFlag)

    # completeCallBack(saveData, taskId, backParam, tick)
    def AddConvertTaskByPath(self, loadPath, savePath, completeCallBack, backParam=None, cleanFlag=""):
        from task.task_waifu2x import TaskWaifu2x
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskWaifu2x().AddConvertTaskByPath(loadPath, savePath, completeCallBack, backParam, cleanFlag)

    def AddQImageTask(self, data, radio, toW, toH, model, callBack=None, backParam=None):
        from task.task_qimage import TaskQImage
        return TaskQImage().AddQImageTask(data, radio, toW, toH, model, callBack, backParam, cleanFlag=self.__taskFlagId)

    def AddLocalTaskLoad(self, type, dir, backparam=None, callBack=None):
        from task.task_local import TaskLocal
        return TaskLocal().AddLoadRead(type, dir, backparam, callBack, cleanFlag=self.__taskFlagId)

    def AddLocalTaskLoadPicture(self, v, index, backparam=None, callBack=None):
        from task.task_local import TaskLocal
        return TaskLocal().AddLoadReadPicture(v, index, backparam, callBack, cleanFlag=self.__taskFlagId)

    def AddUploadTask(self, nas_id, type, srcDir, desFile, upDirPath, backParam=None, callBack=None):
        from task.task_upload import TaskUpload
        return TaskUpload().AddLoadReadPicture(nas_id, type, srcDir, desFile, upDirPath, backParam, callBack, cleanFlag=self.__taskFlagId)

    def ClearQImageTaskById(self, taskId):
        from task.task_qimage import TaskQImage
        return TaskQImage().ClearQImageTaskById(taskId)

    def ClearTask(self):
        from task.task_http import TaskHttp
        from task.task_download import TaskDownload
        from task.task_waifu2x import TaskWaifu2x
        TaskDownload().Cancel(self.__taskFlagId)
        TaskHttp().Cancel(self.__taskFlagId)
        TaskWaifu2x().Cancel(self.__taskFlagId)

    def ClearDownload(self):
        from task.task_download import TaskDownload
        return TaskDownload().Cancel(self.__taskFlagId)

    def ClearConvert(self):
        from task.task_waifu2x import TaskWaifu2x
        return TaskWaifu2x().Cancel(self.__taskFlagId)

    def ClearSql(self):
        from task.task_sql import TaskSql
        return TaskSql().Cancel(self.__taskFlagId)

    def ClearWaitConvertIds(self, taskIds):
        from task.task_waifu2x import TaskWaifu2x
        return TaskWaifu2x().ClearWaitConvertIds(taskIds)

    def ClearQImageTask(self):
        from task.task_qimage import TaskQImage
        return TaskQImage().Cancel(self.__taskFlagId)


class TaskBase(Singleton):
    taskId = 0
    taskObj = QtTaskQObject()

    def __init__(self):
        Singleton.__init__(self)
        self._inQueue = Queue()
        self.thread = threading.Thread(target=self.Run)
        self.thread.setName("Task-" + str(self.__class__.__name__))
        self.thread.setDaemon(True)
        self.tasks = {}
        self.flagToIds = {}

    def Stop(self):
        self._inQueue.put("")
        return

    def Run(self):
        return

    def Cancel(self, cleanFlag):
        taskIds = self.flagToIds.get(cleanFlag, set())
        if not taskIds:
            return
        for taskId in taskIds:
            if taskId in self.tasks:
                del self.tasks[taskId]
        self.flagToIds.pop(cleanFlag)
