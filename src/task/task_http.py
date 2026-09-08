import pickle
from types import FunctionType

from task.qt_task import TaskBase
from tools.log import Log


class QtHttpTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""


class TaskHttp(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.taskBack.connect(self.HandlerTask)

    def AddHttpTask(self, req, callBack=None, backParam=None, cleanFlag=None):
        info = QtHttpTask(0)
        info.callBack = callBack
        info.backParam = backParam
        taskId = self._RegisterTask(info, cleanFlag)
        try:
            if isinstance(req, FunctionType):
                req(taskId)
            else:
                from server.server import Server
                Server().Send(req, backParam=taskId)
        except Exception:
            self._TakeTask(taskId)
            raise
        return

    def HandlerTask(self, taskId, data):
        try:
            info = self._TakeTask(taskId)
            if not info:
                return
            data = pickle.loads(data)
            assert isinstance(info, QtHttpTask)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(data)
                else:
                    info.callBack(data, info.backParam)
        except Exception as es:
            Log.Error(es)
