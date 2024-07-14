from config import config
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil
from view.download.download_db import DownloadDb
from view.download.download_item import DownloadItem
from view.nas.nas_item import NasUploadItem


class NasStatus(QtTaskBase):
    def __init__(self):
        QtTaskBase.__init__(self)
        self.downloadingList = []  # 正在下载列表
        self.downloadList = []  # 下载队列
        self.downloadDict = {}  # bookId ：downloadInfo

    def SetNewStatus(self, task, status, statusMsg=0):
        if status == task.status:
            return
        task.status = status
        task.statusMsg = statusMsg
        task.dirty = True
        assert isinstance(task, NasUploadItem)
        if status == task.Waiting:
            self._SetTaskWait(task)
        elif status == task.WaitWaifu2x:
            self._SetTaskWait(task)
        elif status == task.Pause:
            self._SetTaskPause(task)
        elif status == task.Error:
            self._SetDownloadTaskNone(task)
        elif status == task.Success:
            self._SetDownloadTaskNone(task)
        elif status == task.Uploading:
            self._SetTaskDownloading(task)
        else:
            assert False
        self.UpdateTableItem(task)

    def _SetTaskWait(self, task):
        if task in self.downloadingList:
            self.downloadingList.remove(task)
        if task not in self.downloadList:
            self.downloadList.append(task)
        return

    def _SetTaskDownloading(self, task):
        if task not in self.downloadingList:
            self.downloadingList.append(task)
        if task in self.downloadList:
            self.downloadList.remove(task)
        return

    def _SetTaskPause(self, task2):
        from task.task_download import TaskDownload
        TaskDownload().Cancel(task2.cleanFlag)
        self._SetDownloadTaskNone(task2)
        return

    def _SetDownloadTaskNone(self, task):
        if task in self.downloadingList:
            self.downloadingList.remove(task)
        if task in self.downloadList:
            self.downloadList.remove(task)
        return

    def UpdateTableItem(self, task):
        return

    def UpdateTaskDB(self, task):
        assert isinstance(task, NasUploadItem)
        if task.dirty:
            task.dirty = False
            self.db.AddUploadDB(task)

    def TimeOutHandler(self):
        downloadNum = config.DownloadThreadNum
        addNum = downloadNum - len(self.downloadingList)
        if addNum > 0:
            for task in list(self.downloadList):
                assert isinstance(task, NasUploadItem)
                if task.status not in [task.Waiting, task.WaitWaifu2x]:
                    self.downloadList.remove(task)
                    continue
                self.StartItemDownload(task)
                if task.status == task.Uploading:
                    addNum -= 1
                if addNum <= 0:
                    break

        # for task in self.downloadingList:
        #     assert isinstance(task, NasUploadItem)
        #     task.speedStr = ToolUtil.GetDownloadSize(task.speed) + "/s"
        #     task.speed = 0
        #     self.UpdateTableItem(task)
        return

    def StartItemDownload(self, task):
        assert isinstance(task, NasUploadItem)
        newStatus = task.UploadInit()
        self.SetNewStatus(task, newStatus)
        if newStatus != task.Uploading:
            return
        task.type = 0
        newStatus, (nasInfo, srcDir, desFile, upDirPath) = task.GetNextParams()
        if newStatus == task.Uploading:
            task.type = 1
            self.AddUploadTask(nasInfo, task.type, srcDir, desFile, upDirPath, task.key, self.UploadStCallBack)
        self.SetNewStatus(task, newStatus)
        self.UpdateTableItem(task)
        self.UpdateTaskDB(task)
        return

    def UploadStCallBack(self, st, taskId):
        task = self.downloadDict.get(taskId)
        if not task:
            return
        assert isinstance(task, NasUploadItem)
        if task.status != task.Uploading:
            return
        if st == Status.Ok:
            newStatus = task.UploadSucCallBack()
            if newStatus == task.Uploading:
                newStatus, (nasInfo, srcDir, desFile, upDirPath) = task.GetNextParams()
                if newStatus == task.Uploading:
                    self.AddUploadTask(nasInfo, task.type, srcDir, desFile, upDirPath, task.key, self.UploadStCallBack)
            self.SetNewStatus(task, newStatus)
            self.UpdateTableItem(task)
            self.UpdateTaskDB(task)
        else:
            self.SetNewStatus(task, task.Error, st)
        return
