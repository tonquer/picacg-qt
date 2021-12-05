from PySide6.QtGui import QImage

from PySide6.QtGui import QImage

from task.qt_task import TaskBase, QtHttpTask
from tools.log import Log


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
                taskId, data = v
            except Exception as es:
                continue
            self._inQueue.task_done()

            if taskId < 0:
                break

            q = QImage()
            try:
                if not data:
                    return
                q.loadFromData(data)
            except Exception as es:
                Log.Error(es)
            finally:
                self.taskObj.imageBack.emit(taskId, q)

    def AddQImageTask(self, data, callBack=None, backParam=None, cleanFlag=None):
        self.taskId += 1
        info = QtHttpTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        self._inQueue.put((self.taskId, data))
        return

    def HandlerTask(self, taskId, data):
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