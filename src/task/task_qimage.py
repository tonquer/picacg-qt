import threading

from PySide6.QtGui import QImage
from PySide6.QtCore import Qt

from task.qt_task import TaskBase
from tools.log import Log


class QtQImageTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""
        self.data = ""
        self.radio = 1
        self.toH = 0
        self.toW = 0
        self.model = 0


class TaskQImage(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.imageBack.connect(self.HandlerTask)
        self.threadNum = 4
        self.threadList = []
        for i in range(self.threadNum+1):
            thread = threading.Thread(target=self.Run)
            thread.setName("Task-" + str(self.__class__.__name__)+str(i))
            thread.setDaemon(True)
            thread.start()
            self.threadList.append(thread)

    def Stop(self):
        for i in range(self.threadNum+1):
            self._inQueue.put("")
        return

    def Run(self):
        while True:
            try:
                v = self._inQueue.get(True)
                if v == "":
                    break
                taskId = v
            except Exception as es:
                continue
            self._inQueue.task_done()

            if taskId < 0:
                break

            info = self._GetTask(taskId)
            if not info:
                continue
            newQ = QImage()
            try:
                q = QImage()
                q.loadFromData(info.data)
                q.setDevicePixelRatio(info.radio)
                if info.toW > 0:
                    newQ = q.scaled(info.toW * info.radio, info.toH * info.radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                else:
                    newQ = q

            except Exception as es:
                Log.Error(es)
            finally:
                self.taskObj.imageBack.emit(taskId, newQ)

    def AddQImageTask(self, data, radio, toW, toH, model, callBack=None, backParam=None, cleanFlag=None):
        info = QtQImageTask(0)
        info.callBack = callBack
        info.backParam = backParam
        info.data = data
        info.radio = radio
        info.toW = toW
        info.toH = toH
        info.model = model

        taskId = self._RegisterTask(info, cleanFlag)
        self._inQueue.put(taskId)
        return taskId

    def ClearQImageTaskById(self, taskId):
        self._TakeTask(taskId)

    def HandlerTask(self, taskId, newData):
        try:
            info = self._TakeTask(taskId)
            if not info:
                return
            assert isinstance(info, QtQImageTask)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(newData)
                else:
                    info.callBack(newData, info.backParam)
        except Exception as es:
            Log.Error(es)
