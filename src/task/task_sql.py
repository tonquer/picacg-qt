import pickle

from task.qt_task import TaskBase, QtHttpTask
from tools.log import Log


class TaskSql(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.sqlBack.connect(self.HandlerSqlTask)

    def AddSqlTask(self, table, data, taskType, callBack=None, backParam=None, cleanFlag=None):
        self.taskId += 1
        info = QtHttpTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        from server.sql_server import SqlServer
        SqlServer().AddSqlTask(table, taskType, data, self.taskId)
        return

    def HandlerSqlTask(self, taskId, data):
        try:
            data = pickle.loads(data)
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

    def Cancel(self, cleanFlag):
        taskIds = self.flagToIds.get(cleanFlag, set())
        if not taskIds:
            return
        for taskId in taskIds:
            if taskId in self.tasks:
                del self.tasks[taskId]
        self.flagToIds.pop(cleanFlag)