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
        self.thread.start()

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

            q = QImage()
            try:
                info = self.tasks.get(taskId)
                if not info:
                    continue

                if not info.data:
                    return
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
        self.taskId += 1
        info = QtQImageTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        info.data = data
        info.radio = radio
        info.toW = toW
        info.toH = toH
        info.model = model

        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        self._inQueue.put(self.taskId)
        return self.taskId

    def ClearQImageTaskById(self, taskId):
        if taskId in self.tasks:
            self.tasks.pop(taskId)

    def HandlerTask(self, taskId, newData):
        try:
            info = self.tasks.get(taskId)
            if not info:
                Log.Warn("[Task] not find taskId:{}".format(taskId))
                return
            assert isinstance(info, QtQImageTask)
            if info.cleanFlag:
                taskIds = self.flagToIds.get(info.cleanFlag, set())
                taskIds.discard(info.taskId)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(newData)
                else:
                    info.callBack(newData, info.backParam)
                del info.callBack
            del self.tasks[taskId]
        except Exception as es:
            Log.Error(es)