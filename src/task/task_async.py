

import pickle

from task.qt_task import TaskBase
from tools.log import Log

class TaskAsync(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.thread.start()

    def Run(self):
        while True:
            try:
                v = self._inQueue.get(True)
                if v == "":
                    break
                key, params = v
                getattr(TaskBase.taskObj, key).emit(*params)
            except Exception as es:
                Log.Error(es)
            finally:
                self._inQueue.task_done()

    def AddAsyncCall(self, key, params):
        self._inQueue.put((key, params))
        return

    def Stop(self):
        self._inQueue.put("")