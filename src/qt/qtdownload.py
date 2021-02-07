import os
import shutil

from PyQt5 import QtWidgets
import weakref

from PyQt5.QtCore import Qt, QTime, QTimer, QSettings
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem

from conf import config
from src.index.book import BookMgr
from src.util import Log, ToolUtil
from src.util.status import Status
from ui.download import Ui_download


class DownloadStatus(object):
    Success = "完成"
    Reading = "获取信息"
    ReadingEps = "获取章节"
    ReadingPicture = "获取下载地址"
    Downloading = "正在下载"
    Waiting = "等待中"
    Pause = "暂停"
    Error = "出错了"


class DownloadInfo(object):
    def __init__(self):
        self.bookId = ""
        self.title = ""
        self.savePath = ""
        self.saveName = ""
        self.status = 0
        self.tableRow = 0

        self.downloadCount = 1  # 正在下载某章节图片
        self.allDownloadCount = 0  # 总下载图片数
        self.pagesCount = 1  # 总图片数

        self.downloadEps = 1  # 正在下载章节图片地址
        self.preDownloadEps = 1  # 预加载章节图片地址
        self.epsCount = 1

        self.resetCnt = 0

        self.speedDownloadLen = 0
        self.downloadLen = 0

        self.speed = ""
        self.downSize = ""


class QtDownload(QtWidgets.QWidget, Ui_download):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_download.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.downloadingList = []  # 正在下载列表
        self.downloadList = []  # 下载队列
        self.downloadDict = {}  # bookId ：downloadInfo

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["id", "标题", "下载状态", "下载页数", "下载章节", "下载速度", "累计下载"])

        self.timer = QTimer(self.tableWidget)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.UpdateTable)
        self.timer.start()

        self.settings = QSettings('download.ini', QSettings.IniFormat)
        self.InitSetting()

        self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)

        self.downloadMenu = QMenu(self.tableWidget)
        action = self.downloadMenu.addAction("打开目录")
        action.triggered.connect(self.ClickOpenFilePath)
        action = self.downloadMenu.addAction("暂停")
        action.triggered.connect(self.ClickPause)
        action = self.downloadMenu.addAction("刪除记录")
        action.triggered.connect(self.DelRecording)
        action = self.downloadMenu.addAction("刪除记录和文件")
        action.triggered.connect(self.DelRecordingAndFile)

        self.startMenu = QMenu(self.tableWidget)
        action = self.startMenu.addAction("打开目录")
        action.triggered.connect(self.ClickOpenFilePath)
        action = self.startMenu.addAction("开始")
        action.triggered.connect(self.ClickStart)
        action = self.startMenu.addAction("刪除记录")
        action.triggered.connect(self.DelRecording)
        action = self.startMenu.addAction("刪除记录和文件")
        action.triggered.connect(self.DelRecordingAndFile)

        self.checkMenu = QMenu(self.tableWidget)
        action = self.checkMenu.addAction("暂停")
        action.triggered.connect(self.ClickPause)
        action = self.checkMenu.addAction("开始")
        action.triggered.connect(self.ClickStart)
        action = self.checkMenu.addAction("刪除记录")
        action.triggered.connect(self.DelRecording)
        action = self.checkMenu.addAction("刪除记录和文件")
        action.triggered.connect(self.DelRecordingAndFile)

        self.otherMenu = QMenu(self.tableWidget)
        action = self.otherMenu.addAction("打开目录")
        action.triggered.connect(self.ClickOpenFilePath)
        action = self.otherMenu.addAction("刪除记录")
        action.triggered.connect(self.DelRecording)
        action = self.otherMenu.addAction("刪除记录和文件")
        action.triggered.connect(self.DelRecordingAndFile)
        self.tableWidget.doubleClicked.connect(self.OpenBookInfo)

    def InitSetting(self):
        for bookId in self.settings.childKeys():
            data = self.settings.value(bookId)
            task = DownloadInfo()
            task.bookId = bookId
            task.status = DownloadStatus.Pause

            ToolUtil.ParseFromData(task, data)

            self.downloadDict[task.bookId] = task
            self.downloadList.append(task)
            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            self.tableWidget.insertRow(rowCont)
            self.UpdateTableItem(task)
            pass

    def SaveSetting(self, bookId, task=None):
        if not task:
            self.settings.remove(bookId)
        else:
            isinstance(task, DownloadInfo)
            self.settings.setValue(bookId, {
                "allDownloadCount": task.allDownloadCount,
                "downloadCount": task.downloadCount,
                "downloadEps": task.downloadEps,
                "downSize": task.downSize,
                "downloadLen": task.downloadLen,
                "epsCount": task.epsCount,
                "pagesCount": task.pagesCount,
                "title": task.title,
                "savePath": task.savePath
            })

        return

    def SwitchCurrent(self):
        pass

    def GetDownloadSize(self, downloadLen):
        kb = downloadLen / 1024.0
        if kb <= 0.1:
            size = str(downloadLen) + "bytes"
        else:
            mb = kb / 1024.0
            if mb <= 0.1:
                size = str(round(kb, 2)) + "kb"
            else:
                size = str(round(mb, 2)) + "mb"
        return size

    def UpdateTable(self):
        for task in self.downloadingList:
            assert isinstance(task, DownloadInfo)
            downloadLen = task.speedDownloadLen
            size = self.GetDownloadSize(downloadLen)
            allSize = self.GetDownloadSize(task.downloadLen)
            task.speed = size + "/s"
            task.downSize = allSize
            self.UpdateTableItem(task)
            task.speedDownloadLen = 0

    def AddDownload(self, bookId):
        if bookId in self.downloadDict:
            return False
        task = DownloadInfo()
        task.bookId = bookId
        task.status = DownloadStatus.Reading
        self.downloadDict[task.bookId] = task
        self.downloadList.append(task)
        rowCont = self.tableWidget.rowCount()
        task.tableRow = rowCont
        self.tableWidget.insertRow(rowCont)
        self.StartLoadBookInfo(bookId=bookId, isBack=False)
        self.UpdateTableItem(task)
        self.SaveSetting(bookId, task)
        return True

    def UpdateTableItem(self, info):
        self.tableWidget.setItem(info.tableRow, 0, QTableWidgetItem(info.bookId))
        self.tableWidget.setItem(info.tableRow, 1, QTableWidgetItem(info.title))
        self.tableWidget.setItem(info.tableRow, 2, QTableWidgetItem(info.status))
        self.tableWidget.setItem(info.tableRow, 3,
                                 QTableWidgetItem("{}/{}".format(str(info.allDownloadCount), str(info.pagesCount))))
        self.tableWidget.setItem(info.tableRow, 4,
                                 QTableWidgetItem("{}/{}".format(str(info.downloadEps - 1), str(info.epsCount))))
        self.tableWidget.setItem(info.tableRow, 5, QTableWidgetItem(info.speed))
        self.tableWidget.setItem(info.tableRow, 6, QTableWidgetItem(info.downSize))
        self.tableWidget.update()
        return

    # 加载书籍信息
    def StartLoadBookInfo(self, msg="", bookId="", isBack=True):
        info = self.downloadDict.get(bookId)
        if not info:
            return
        assert isinstance(info, DownloadInfo)

        if not isBack:
            self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookById(bookId, x), self.StartLoadBookInfo,
                                            bookId)
        elif msg != Status.Ok:
            info.resetCnt += 1
            if info.resetCnt >= config.ResetCnt:
                info.status = DownloadStatus.Error
            else:
                self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookById(bookId, x), self.StartLoadBookInfo,
                                                bookId)
        else:
            info.resetCnt = 0
            book = BookMgr().books.get(bookId)
            info.status = DownloadStatus.ReadingEps
            info.title = book.title
            info.savePath = os.path.join(os.path.join(config.SavePath, config.SavePathDir),
                                         info.title.replace("/", "").replace("|", "").replace("*", "").
                                         replace("\\", "").replace("?", "").replace(":", "").replace("*", "").
                                         replace("<", "").replace(">", "").replace("\"", ""))
            info.pagesCount = book.pagesCount
            info.epsCount = book.epsCount
            self.StartLoadEpsInfo(bookId=bookId, isBack=False)
        self.UpdateTableItem(info)

    # 加载章节信息
    def StartLoadEpsInfo(self, msg="", bookId="", isBack=True):
        info = self.downloadDict.get(bookId)
        if not info:
            return
        assert isinstance(info, DownloadInfo)
        if not isBack:
            self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookEpsInfo(bookId, x), self.StartLoadEpsInfo,
                                            bookId)
        elif msg != Status.Ok:
            info.resetCnt += 1
            if info.resetCnt >= config.ResetCnt:
                info.status = DownloadStatus.Error
            else:
                self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookEpsInfo(bookId, x), self.StartLoadEpsInfo,
                                                bookId)
        else:
            info.resetCnt = 0
            book = BookMgr().books.get(bookId)
            info.title = book.title
            info.pagesCount = book.pagesCount
            info.epsCount = book.epsCount
            info.status = DownloadStatus.ReadingPicture
            # 先准备好第一章
            self.StartLoadPicUrl(bookId=bookId, isBack=False)
            self.HandlerDownloadList()
        self.UpdateTableItem(info)

    def StartLoadPicUrl(self, msg="", bookId="", isBack=True):
        info = self.downloadDict.get(bookId)
        if not info:
            return
        assert isinstance(info, DownloadInfo)
        if not isBack:
            # 如果已经加载好了
            if info.preDownloadEps > info.epsCount:
                if info.status not in [DownloadStatus.Success, DownloadStatus.Downloading]:
                    info.status = DownloadStatus.Waiting
                return
            self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookEpsPicInfo(bookId, info.preDownloadEps, x),
                                            self.StartLoadPicUrl,
                                            bookId)
        elif msg != Status.Ok:
            info.resetCnt += 1
            if info.resetCnt >= config.ResetCnt:
                info.status = DownloadStatus.Error
            else:
                self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookEpsPicInfo(bookId, info.preDownloadEps, x),
                                                self.StartLoadPicUrl,
                                                bookId)
        else:
            info.resetCnt = 0
            info.preDownloadEps += 1
            if info.status == DownloadStatus.Downloading:
                # 加载完成了
                if info.preDownloadEps > info.epsCount:
                    return
                # 加载下一章
                self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookEpsPicInfo(bookId, info.preDownloadEps, x),
                                                self.StartLoadPicUrl,
                                                bookId)
            elif info.status == DownloadStatus.ReadingPicture:
                info.status = DownloadStatus.Waiting
                self.HandlerDownloadList()
        self.UpdateTableItem(info)

    def HandlerDownloadList(self):
        downloadNum = config.DownloadThreadNum
        addNum = downloadNum - len(self.downloadingList)

        if addNum <= 0:
            return

        for _ in range(addNum):
            if len(self.downloadList) <= 0:
                return
            for task in self.downloadList:
                assert isinstance(task, DownloadInfo)
                if task.status != DownloadStatus.Waiting:
                    continue
                self.downloadList.remove(task)
                self.downloadingList.append(task)
                task.status = DownloadStatus.Downloading
                self.StartLoadPicUrl(bookId=task.bookId, isBack=False)
                self.StartDownload(task)
                self.UpdateTableItem(task)
                break
        pass

    # 开始下载
    def StartDownload(self, task):
        assert isinstance(task, DownloadInfo)
        bookInfo = BookMgr().books.get(task.bookId)
        picInfo = None
        st = None
        while task.downloadEps <= task.epsCount:
            epsInfo = bookInfo.eps[task.downloadEps - 1]

            # 图片路径还没有加载好
            if not epsInfo.pics:
                st = Status.WaitLoad
                break

            if task.downloadCount > len(epsInfo.pics):
                task.downloadCount = 1
                task.downloadEps += 1
            else:
                picInfo = epsInfo.pics[task.downloadCount - 1]
                st = Status.Ok
                break

        if st == Status.Ok:
            task.saveName = picInfo.originalName
            self.owner().qtTask.AddDownloadTask(picInfo.fileServer, picInfo.path,
                                                downloadCallBack=self.DownloadCallBack,
                                                completeCallBack=self.CompleteDownloadPic, backParam=task.bookId,
                                                isSaveCache=False)
            task.allDownloadCount += 1
        else:
            if st == Status.WaitLoad:
                task.status = DownloadStatus.ReadingPicture
                self.StartLoadPicUrl(bookId=task.bookId, isBack=False)
                self.downloadList.append(task)
                self.HandlerDownloadList()
            else:
                task.status = DownloadStatus.Success
            self.UpdateTable()
            self.downloadingList.remove(task)
        self.SaveSetting(task.bookId, task)
        self.UpdateTableItem(task)

    def DownloadCallBack(self, data, laveFileSize, bookId):
        task = self.downloadDict.get(bookId)
        if not task:
            return
        assert isinstance(task, DownloadInfo)
        task.downloadLen += len(data)
        task.speedDownloadLen += len(data)

    def CompleteDownloadPic(self, data, msg, bookId):
        task = self.downloadDict.get(bookId)
        if not task:
            return
        assert isinstance(task, DownloadInfo)

        # 丢弃
        if task.status != DownloadStatus.Downloading:
            return

        if msg != Status.Ok:
            task.resetCnt += 1
            if task.resetCnt >= config.ResetCnt:
                task.status = DownloadStatus.Error
            else:
                if task.status == DownloadStatus.Downloading:
                    self.StartDownload(task)
        else:
            try:
                savePath = os.path.join(task.savePath, str(task.downloadEps))
                if not os.path.isdir(savePath):
                    os.makedirs(savePath)
                f = open(os.path.join(savePath, task.saveName), "wb+")
                f.write(data)
                f.close()
                task.downloadCount += 1
                if task.status == DownloadStatus.Downloading:
                    self.StartDownload(task)
            except Exception as es:
                import sys
                cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
                e = sys.exc_info()[1]
                Log.Error(cur_tb, e)
                task.status = DownloadStatus.Error
                self.downloadingList.remove(task)
            self.UpdateTableItem(task)

    def RemoveRecord(self, bookId):
        task = self.downloadDict.get(bookId)
        if not task:
            return
        assert isinstance(task, DownloadInfo)
        if task in self.downloadingList:
            self.downloadingList.remove(task)
        if task in self.downloadList:
            self.downloadList.remove(task)
        self.downloadDict.pop(bookId)
        self.tableWidget.removeRow(task.tableRow)
        self.SaveSetting(bookId)

    def UpdateTableRow(self):
        count = self.tableWidget.rowCount()
        for i in range(count):
            bookId = self.tableWidget.item(i, 0).text()
            info = self.downloadDict.get(bookId)
            if info:
                info.tableRow = i

    # 右键菜单
    def SelectMenu(self, pos):
        index = self.tableWidget.indexAt(pos)
        if index.isValid():
            selected = self.tableWidget.selectedIndexes()
            selectRows = set()
            for index in selected:
                selectRows.add(index.row())
            if not selectRows:
                return
            if len(selectRows) == 1:
                # 单选
                row = selectRows.pop()
                col = 0
                bookId = self.tableWidget.item(row, col).text()
                task = self.downloadDict.get(bookId)
                if not task:
                    return
                assert isinstance(task, DownloadInfo)
                if task.status in [DownloadStatus.Pause, DownloadStatus.Error]:
                    self.startMenu.exec_(QCursor.pos())
                elif task.status in [DownloadStatus.Downloading, DownloadStatus.Waiting,
                                     DownloadStatus.Reading, DownloadStatus.ReadingPicture, DownloadStatus.ReadingEps]:
                    self.downloadMenu.exec_(QCursor.pos())
                else:
                    self.otherMenu.exec(QCursor.pos())
            else:
                # 多选
                self.checkMenu.exec_(QCursor.pos())
        pass

    def ClickOpenFilePath(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        # 只去第一个
        row = selectRows.pop()
        col = 0
        bookId = self.tableWidget.item(row, col).text()
        task = self.downloadDict.get(bookId)
        # TODO 未实现
        return

    def ClickPause(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task in self.downloadingList:
                self.downloadingList.remove(task)
            task.status = DownloadStatus.Pause
            self.UpdateTableItem(task)
        return

    def ClickStart(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status not in [DownloadStatus.Pause, DownloadStatus.Error]:
                continue
            task.status = DownloadStatus.Reading
            if task not in self.downloadList:
                self.downloadList.append(task)
            self.StartLoadBookInfo(bookId=bookId, isBack=False)
            self.UpdateTableItem(task)

    def DelRecording(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            self.RemoveRecord(bookId)
        self.UpdateTableRow()

    def DelRecordingAndFile(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        try:
            selectRows = list(selectRows)
            selectRows.sort(reverse=True)
            for row in selectRows:
                col = 0
                bookId = self.tableWidget.item(row, col).text()
                bookInfo = self.downloadDict.get(bookId)
                if not bookInfo:
                    continue
                self.RemoveRecord(bookId)
                if os.path.isdir(bookInfo.savePath):
                    shutil.rmtree(bookInfo.savePath)

        except Exception as es:
            import sys
            cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
            e = sys.exc_info()[1]
            Log.Error(cur_tb, e)
        self.UpdateTableRow()

    def OpenBookInfo(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if len(selectRows) > 1:
            return
        if len(selectRows) <= 0:
            return
        row = list(selectRows)[0]
        col = 0
        bookId = self.tableWidget.item(row, col).text()
        if not bookId:
            return
        self.owner().bookInfoForm.OpenBook(bookId)
