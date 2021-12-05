import threading
from queue import Queue

from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage

from tools.singleton import Singleton


class QtTaskQObject(QObject):
    taskBack = Signal(int, bytes)
    downloadBack = Signal(int, int, bytes)
    convertBack = Signal(int)
    imageBack = Signal(int, QImage)
    sqlBack = Signal(int, bytes)

    def __init__(self):
        super(self.__class__, self).__init__()


class QtHttpTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""


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
        from task.task_http import TaskHttp
        return TaskHttp().AddHttpTask(req, callBack, backParam, cleanFlag=self.__taskFlagId)

    def AddSqlTask(self, table, data, taskType, callBack=None, backParam=None):
        from task.task_sql import TaskSql
        return TaskSql().AddSqlTask(table, data, taskType, callBack, backParam, cleanFlag=self.__taskFlagId)

    # downloadCallBack(data, laveFileSize, backParam)
    # downloadCallBack(data, laveFileSize)
    # downloadCompleteBack(data, st)
    # downloadCompleteBack(data, st, backParam)
    def AddDownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, isSaveData=True, backParam=None, isSaveCache=True, filePath=""):
        from task.task_download import TaskDownload
        return TaskDownload().AddDownloadTask(url, path, downloadCallBack, completeCallBack, isSaveData, backParam, isSaveCache, self.__taskFlagId, filePath)

    # completeCallBack(saveData, taskId, backParam, tick)
    def AddConvertTask(self, path, imgData, model, completeCallBack, backParam=None, filePath=""):
        from task.task_waifu2x import TaskWaifu2x
        return TaskWaifu2x().AddConvertTask(path, imgData, model, completeCallBack, backParam, self.__taskFlagId, filePath)

    def AddQImageTask(self, data, callBack=None, backParam=None):
        from task.task_qimage import TaskQImage
        return TaskQImage().AddQImageTask(data, callBack, backParam, cleanFlag=self.__taskFlagId)

    def ClearTask(self):
        from task.task_http import TaskHttp
        from task.task_download import TaskDownload
        from task.task_waifu2x import TaskWaifu2x
        TaskDownload().Cancel(self.__taskFlagId)
        TaskHttp().Cancel(self.__taskFlagId)
        TaskWaifu2x().Cancel(self.__taskFlagId)

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
        self.cacheAndLoadPath = ""   # 保存和加载
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
