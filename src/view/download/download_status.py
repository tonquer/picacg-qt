from config import config
from task.qt_task import QtTaskBase
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil
from view.download.download_db import DownloadDb
from view.download.download_item import DownloadItem


class DownloadStatus(QtTaskBase):
    def __init__(self):
        QtTaskBase.__init__(self)
        self.db = DownloadDb()
        self.downloadingList = []  # 正在下载列表
        self.downloadList = []  # 下载队列
        self.downloadDict = {}  # bookId ：downloadInfo
        self.convertList = []
        self.convertingList = []

    def SetNewStatus(self, task, status, statusMsg=""):
        if status == task.status:
            return
        task.status = status
        task.statusMsg = statusMsg
        task.dirty = True
        assert isinstance(task, DownloadItem)
        if status == task.Waiting:
            self._SetTaskWait(task)
        elif status == task.Pause:
            self._SetTaskPause(task)
        elif status == task.Error or status == task.SpaceEps or status == task.UnderReviewBook:
            task.speedStr = ""
            task.speed = 0
            self._SetDownloadTaskNone(task)
        elif status == task.Downloading:
            self._SetTaskDownloading(task)
        elif status == task.Success:
            task.speedStr = ""
            task.speed = 0
            self._SetDownloadTaskNone(task)
        else:
            assert False
        self.UpdateTableItem(task)

    def SetNewCovertStatus(self, task, status, msg=""):
        assert isinstance(task, DownloadItem)
        if task.convertStatus == status:
            return
        task.convertStatus = status
        task.convertMsg = msg
        if status == task.Waiting:
            self._SetTaskConvertWait(task)
        elif status == task.Pause:
            self._SetTaskConvertPause(task)
        elif status == task.Error or status == task.SpaceEps or status == task.UnderReviewBook:
            self._SetTaskConvertNone(task)
        elif status == task.Converting:
            self._SetTaskConverting(task)
        elif status == task.ConvertSuccess:
            self._SetTaskConvertNone(task)
        else:
            assert False
        self.UpdateTableItem(task)

    def _SetTaskWait(self, task):
        if task in self.downloadingList:
            self.downloadingList.remove(task)
        if task not in self.downloadList:
            self.downloadList.append(task)
        return

    def _SetTaskConvertWait(self, task):
        task.convertStatus = task.Waiting
        if task in self.convertingList:
            self.convertingList.remove(task)
        if task not in self.convertList:
            self.convertList.append(task)
        return

    def _SetTaskDownloading(self, task):
        if task not in self.downloadingList:
            self.downloadingList.append(task)
        if task in self.downloadList:
            self.downloadList.remove(task)
        return

    def _SetTaskConverting(self, task):
        if task not in self.convertingList:
            self.convertingList.append(task)
        if task in self.convertList:
            self.convertList.remove(task)
        return

    def _SetTaskPause(self, task2):
        from task.task_download import TaskDownload
        TaskDownload().Cancel(task2.cleanFlag)
        self._SetDownloadTaskNone(task2)
        return

    def _SetTaskConvertPause(self, task2):
        task2.convertStatus = task2.Pause
        from task.task_waifu2x import TaskWaifu2x
        TaskWaifu2x().Cancel(task2.cleanFlag)
        self._SetTaskConvertNone(task2)
        return

    def _SetDownloadTaskNone(self, task):
        if task in self.downloadingList:
            self.downloadingList.remove(task)
        if task in self.downloadList:
            self.downloadList.remove(task)
        return

    def _SetTaskConvertNone(self, task):
        if task in self.convertingList:
            self.convertingList.remove(task)
        if task in self.convertList:
            self.convertList.remove(task)
        return

    def UpdateTableItem(self, task):
        return

    def UpdateTaskDB(self, task):
        assert isinstance(task, DownloadItem)
        if task.dirty:
            task.dirty = False
            self.db.AddDownloadDB(task)
        for info in task.epsInfo.values():
            if info.dirty:
                info.dirty = False
            self.db.AddDownloadEpsDB(info)

    def TimeOutHandler(self):
        downloadNum = config.DownloadThreadNum
        addNum = downloadNum - len(self.downloadingList)
        if addNum > 0:
            for task in list(self.downloadList):
                assert isinstance(task, DownloadItem)
                if task.status != task.Waiting:
                    self.downloadList.remove(task)
                    continue
                self.StartItemDownload(task)
                if task.status == task.Downloading:
                    addNum -= 1
                if addNum <= 0:
                    break

        convertNum = config.ConvertThreadNum
        addNum = convertNum - len(self.convertingList)
        if addNum > 0:
            for task in list(self.convertList):
                assert isinstance(task, DownloadItem)
                if task.convertStatus != task.Waiting:
                    self.convertList.remove(task)
                    continue

                self.StartItemConvert(task)
                if task.convertStatus == task.Converting:
                    addNum -= 1
                if addNum <= 0:
                    break

        for task in self.downloadingList:
            assert isinstance(task, DownloadItem)
            task.speedStr = ToolUtil.GetDownloadSize(task.speed) + "/s"
            task.speed = 0
            self.UpdateSpeed(task)
        return

    def StartItemDownload(self, task):
        assert isinstance(task, DownloadItem)
        newStatus = task.DownloadInit()
        self.SetNewStatus(task, newStatus)
        if newStatus != task.Downloading:
            return
        epsId, index, savePath, isInit = task.GetDownloadPath()

        self.AddDownloadBook(task.bookId, epsId, index, self.DownloadStCallBack, self.DownloadCallBack, self.DownloadCompleteCallBack, task.bookId, savePath=savePath, cleanFlag=task.cleanFlag, isInit=isInit)
        self.UpdateTaskDB(task)
        return

    def DownloadStCallBack(self, data, taskId):
        task = self.downloadDict.get(taskId)
        if not task:
            return
        assert isinstance(task, DownloadItem)
        if task.status != task.Downloading:
            return
        st = data.get("st")
        task.statusMsg = st

        # 获取信息成功， 正式开始下载
        if st == Str.Success:
            maxPic = data.get("maxPic")
            title = data.get("title")
            bookName = data.get("bookName")
            author = data.get("author")
            task.DownloadInitCallBack(bookName, author, title, maxPic)
            self.StartItemDownload(task)
        elif st == Str.Cache:
            # 进行下一个图片
            newStatus = task.DownloadSucCallBack()
            self.SetNewStatus(task, newStatus)
            if newStatus == task.Downloading:
                epsId, index, savePath, isInit = task.GetDownloadPath()
                self.AddDownloadBook(task.bookId, epsId, index, self.DownloadStCallBack, self.DownloadCallBack, self.DownloadCompleteCallBack, task.bookId, savePath=savePath, cleanFlag=task.cleanFlag, isInit=isInit)
            return
        elif st in [Str.Reading, Str.ReadingEps, Str.ReadingPicture, Str.Downloading]:
            task.statusMsg = st
            self.UpdateTableItem(task)
        elif st == Str.SpaceEps:
            self.SetNewStatus(task, task.SpaceEps)
        elif st == Str.UnderReviewBook:
            from tools.book import BookMgr
            info = BookMgr().GetBook(task.bookId)
            if info:
                task.title = info.title
            self.SetNewStatus(task, task.UnderReviewBook)
        else:
            self.SetNewStatus(task, task.Error)
        return

    def DownloadCallBack(self, downloadSize, laveFileSize, taskId):
        task = self.downloadDict.get(taskId)
        if not task:
            return
        if task.status != task.Downloading:
            return

        task.downloadLen += downloadSize
        task.speedDownloadLen += downloadSize
        return

    def DownloadCompleteCallBack(self, data, msg, taskId):
        task = self.downloadDict.get(taskId)
        if not task:
            return
        if task.status != task.Downloading:
            return
        if msg == Status.Ok:
            newStatus = task.DownloadSucCallBack()
            self.SetNewStatus(task, newStatus)
            if newStatus == task.Downloading:
                epsId, index, savePath, isInit = task.GetDownloadPath()
                self.AddDownloadBook(task.bookId, epsId, index, self.DownloadStCallBack, self.DownloadCallBack, self.DownloadCompleteCallBack, task.bookId, savePath=savePath, cleanFlag=task.cleanFlag, isInit=isInit)
            self.UpdateTableItem(task)
            self.UpdateTaskDB(task)
        else:
            self.SetNewStatus(task, task.Error)
        return

    def StartItemConvert(self, task):
        assert isinstance(task, DownloadItem)
        newStatus = task.ConvertInit()
        self.SetNewCovertStatus(task, newStatus)
        if newStatus != task.Converting:
            return
        loadPath, savePath = task.GetConvertPath()
        self.AddConvertTaskByPath(loadPath, savePath, self.AddItemConvertBack, task.bookId, cleanFlag=task.cleanFlag)
        self.UpdateTaskDB(task)
        return

    def AddItemConvertBack(self, data, st, backParam, tick):
        task = self.downloadDict.get(backParam)
        if not task:
            return
        if task.convertStatus != task.Converting:
            return

        assert isinstance(task, DownloadItem)
        if st == Status.Ok:
            newState = task.ConvertSucCallBack(tick)
            self.SetNewCovertStatus(task, newState)
            if newState == task.Converting:
                loadPath, savePath = task.GetConvertPath()
                self.AddConvertTaskByPath(loadPath, savePath, self.AddItemConvertBack, task.bookId, cleanFlag=task.cleanFlag)
            self.UpdateTableItem(task)
            self.UpdateTaskDB(task)
        else:
            self.SetNewCovertStatus(task, task.Error, st)
