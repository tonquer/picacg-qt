import pickle

from task.qt_task import TaskBase
from tools.log import Log

class QtSqlTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""


class TaskSql(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.sqlBack.connect(self.HandlerSqlTask)

    def AddSqlTask(self, table, data, taskType, callBack=None, backParam=None, cleanFlag=None):
        info = QtSqlTask(0)
        info.callBack = callBack
        info.backParam = backParam
        taskId = self._RegisterTask(info, cleanFlag)
        try:
            from server.sql_server import SqlServer
            SqlServer().AddSqlTask(table, taskType, data, taskId)
        except Exception:
            self._TakeTask(taskId)
            raise
        return

    def HandlerSqlTask(self, taskId, data):
        try:
            info = self._TakeTask(taskId)
            if not info:
                return
            data = pickle.loads(data)
            assert isinstance(info, QtSqlTask)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(data)
                else:
                    info.callBack(data, info.backParam)
        except Exception as es:
            Log.Error(es)
