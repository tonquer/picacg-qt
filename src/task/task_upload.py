import os
import threading
import uuid
from queue import Queue
import zipfile

from config import config
from config.setting import Setting
from task.qt_task import TaskBase, QtTaskBase
from tools.log import Log
from tools.status import Status
from tools.str import Str


class UpLoadBase:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.address = ""
        self.port = 0
        self.service_name = ""
        self.isV2 = True
        self.path = ""
        self.client = None


class QtUpTask:
    Check = 1
    MakeZip = 2
    Upload = 3

    def __init__(self, taskId):
        self.taskId = taskId
        self.nasInfo = None
        self.type = 0
        self.callBack = None
        self.backParam = 0
        self.cleanFlag = 0
        self.srcDir = ""
        self.desFile = ""
        self.upDirPath = ""


class TaskUpload(TaskBase, QtTaskBase):
    def __init__(self) -> None:
        TaskBase.__init__(self)
        QtTaskBase.__init__(self)

        # self.thread.start()
        #
        # self.cacheBookZipName = ""
        # self.cacheBookZip = None
        self._inQueue = Queue()
        self._loadQueue = Queue()
        self.thread.start()

        self.taskObj.uploadBack.connect(self.HandlerTask)

    def AddLoadReadPicture(self, nasInfo, type, srcDir, desFile, upDirPath, backParam, callBack, cleanFlag):
        self.taskId += 1
        info = QtUpTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        info.nasInfo = nasInfo
        info.type = type
        info.srcDir = srcDir
        info.desFile = desFile
        info.upDirPath = upDirPath

        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        self._inQueue.put(self.taskId)
        return self.taskId

    def Run(self):
        while True:
            taskId = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                if taskId == "":
                    break
                self._LoadRead(taskId)
            except Exception as es:
                Log.Error(es)
        pass

    def Stop(self):
        self._inQueue.put("")

    def _LoadRead(self, taskId):
        task = self.tasks.get(taskId)
        if not task:
            return
        assert isinstance(task, QtUpTask)
        Log.Info("task_id:{}, type_id:{}".format(taskId, task.type))
        type = task.type
        if type == task.Check:
            st = self.CheckLink(task)
        elif type == task.MakeZip:
            st = self.MakeZip(task)
        elif type == task.Upload:
            st = self.UpData(task)

        self.taskObj.uploadBack.emit(taskId, st)

    def CheckLink(self, task):
        from qt_owner import QtOwner
        from view.nas.nas_item import NasInfoItem
        nasInfo = task.nasInfo
        assert isinstance(nasInfo, NasInfoItem)
        from task.upload_webdav import WebdavClient
        from task.upload_smb import SmbClient
        if task.nasInfo.type == 0:
            client = WebdavClient()
        else:
            client = SmbClient()

        client.Init(nasInfo)
        return client.Connect()

    def MakeZip(self, task):
        assert isinstance(task, QtUpTask)
        return self.MakeZipFile(task.srcDir, task.desFile)

    def UpData(self, task):
        from qt_owner import QtOwner
        assert isinstance(task, QtUpTask)
        nasInfo = task.nasInfo
        from view.nas.nas_item import NasInfoItem
        assert isinstance(nasInfo, NasInfoItem)
        from task.upload_webdav import WebdavClient
        from task.upload_smb import SmbClient
        if task.nasInfo.type == 0:
            client = WebdavClient()
        else:
            client = SmbClient()
        client.Init(nasInfo)
        return client.Upload(task.desFile, task.upDirPath)

    def HandlerTask(self, taskId, st):
        try:
            info = self.tasks.get(taskId)
            if not info:
                Log.Warn("[TaskLocal] not find taskId:{}".format(taskId))
                return
            assert isinstance(info, QtUpTask)
            if info.cleanFlag:
                taskIds = self.flagToIds.get(info.cleanFlag, set())
                taskIds.discard(info.taskId)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(st)
                else:
                    info.callBack(st, info.backParam)
                del info.callBack
            del self.tasks[taskId]
        except Exception as es:
            Log.Error(es)

    @classmethod
    def MakeZipFile(cls, srcDirPath, fileName):
        try:
            if not os.path.isdir(srcDirPath):
                return Str.FileError
            cacheZipPath = os.path.dirname(fileName)
            if not os.path.isdir(cacheZipPath):
                os.makedirs(cacheZipPath)
            zipFileName = fileName
            zip_file = zipfile.ZipFile(zipFileName, "w")
            for item in os.scandir(srcDirPath):
                if item.is_dir():
                    pass
                elif item.is_file():
                    arcname = os.path.basename(item.path)
                    zip_file.write(item.path, arcname=arcname, compress_type=zipfile.ZIP_DEFLATED)

            zip_file.close()
        except Exception as es:
            Log.Error(es)
            return Str.CvZipError
        return Str.Ok
