from config import config
from task.qt_task import QtTaskBase
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil
from view.convert.convert_item import ConvertItem


class ConvertStatus(QtTaskBase):
    def __init__(self):
        QtTaskBase.__init__(self)
        # self.db = ConvertDb()
        self.downloadingList = []  # 正在下载列表
        self.downloadList = []  # 下载队列
        self.downloadDict = {}  # bookId ：downloadInfo

    def SetNewStatus(self, task, status, statusMsg=""):
        if status == task.status:
            return
        task.status = status
        task.statusMsg = statusMsg
        task.dirty = True
        assert isinstance(task, ConvertItem)
        if status == Str.Waiting:
            self._SetTaskWait(task)
        elif status == Str.Pause:
            self._SetTaskPause(task)
        elif status == Str.CvError:
            self._SetDownloadTaskNone(task)
        elif status == Str.Downloading:
            self._SetTaskDownloading(task)
        elif status == Str.CvReading:
            self._SetDownloadTaskNone(task)
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
        assert isinstance(task, ConvertItem)
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
                assert isinstance(task, ConvertItem)
                if task.status != task.Waiting:
                    self.downloadList.remove(task)
                    continue
                self.StartItemDownload(task)
                if task.status == task.Downloading:
                    addNum -= 1
                if addNum <= 0:
                    break

        for task in self.downloadingList:
            assert isinstance(task, ConvertItem)
            task.speedStr = ToolUtil.GetDownloadSize(task.speed) + "/s"
            task.speed = 0
            self.UpdateTableItem(task)
        return

    def StartItemDownload(self, task):
        assert isinstance(task, ConvertItem)
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
        assert isinstance(task, ConvertItem)
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
