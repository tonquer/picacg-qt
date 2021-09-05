import os
import shutil

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QTimer, QUrl
from PySide2.QtGui import QCursor, QDesktopServices
from PySide2.QtWidgets import QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem, QAction

from conf import config
from src.qt.download.download_db import DownloadDb
from src.qt.download.download_info import DownloadInfo
from src.qt.qtmain import QtOwner
from src.util import Log, ToolUtil
from ui.download import Ui_download


class QtDownload(QtWidgets.QWidget, Ui_download):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_download.__init__(self)
        self.setupUi(self)
        self.downloadingList = []  # 正在下载列表
        self.downloadList = []  # 下载队列
        self.downloadDict = {}  # bookId ：downloadInfo
        self.convertList = []
        self.convertingList = []

        # if config.Language == "English":
        #     HorizontalHeaderLabels = ["id", "Title", "Download Status", "Download Progress", "Download Chapters", "Download Speed", "Convert Progress", "Covert Chapters", "Covert Time", "Convert Status"]
        # else:
        #     HorizontalHeaderLabels = ["id", "标题", "下载状态", "下载进度", "下载章节", "下载速度", "转换进度", "转换章节", "转换耗时", "转换状态"]

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.setColumnCount(10)
        # self.tableWidget.setHorizontalHeaderLabels(HorizontalHeaderLabels)
        self.timer = QTimer(self.tableWidget)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.UpdateTable)
        self.timer.start()

        # self.settings = QSettings('download.ini', QSettings.IniFormat)
        # self.InitSetting()

        self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)

        self.tableWidget.doubleClicked.connect(self.OpenBookInfo)

        self.tableWidget.horizontalHeader().sectionClicked.connect(self.Sort)
        self.order = {}

        self.db = DownloadDb()
        self.radioButton.setChecked(config.DownloadAuto)
        datas = self.db.LoadDownload(self)
        for task in datas.values():
            self.downloadDict[task.bookId] = task
            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            if task.status != DownloadInfo.Success:
                task.status = DownloadInfo.Pause
            if task.convertStatus != DownloadInfo.ConvertSuccess:
                task.convertStatus = DownloadInfo.Pause
            self.tableWidget.insertRow(rowCont)
            self.UpdateTableItem(task)

    def Close(self):
        self.timer.stop()

    def GetDownloadEpsId(self, bookId):
        if bookId not in self.downloadDict:
            return []
        return self.downloadDict[bookId].downloadEpsIds

    def GetDownloadCompleteEpsId(self, bookId):
        if bookId not in self.downloadDict:
            return []
        return self.downloadDict[bookId].GetDownloadCompleteEpsId()

    def GetConvertFilePath(self, bookId, epsId, index):
        if bookId not in self.downloadDict:
            return ""
        task = self.downloadDict[bookId]
        if epsId not in task.epsInfo:
            return ""
        epsTitle = task.epsInfo[epsId].epsTitle
        savePath = os.path.join(task.convertPath, ToolUtil.GetCanSaveName(epsTitle))
        return os.path.join(savePath, "{:04}.{}".format(index + 1, "jpg"))

    def GetDonwloadFilePath(self, bookId, epsId, index):
        if bookId not in self.downloadDict:
            return ""
        task = self.downloadDict[bookId]
        if epsId not in task.epsInfo:
            return ""
        epsTitle = task.epsInfo[epsId].epsTitle
        savePath = os.path.join(task.savePath, ToolUtil.GetCanSaveName(epsTitle))
        return os.path.join(savePath, "{:04}.{}".format(index + 1, "jpg"))

    def SwitchCurrent(self):
        pass

    def UpdateTable(self):
        for task in self.downloadingList:
            assert isinstance(task, DownloadInfo)
            self.UpdateTableItem(task)
            task.speedStr = ToolUtil.GetDownloadSize(task.speed) + "/s"
            task.speed = 0

    def AddDownload(self, bookId, downloadIds):
        if bookId not in self.downloadDict:
            task = DownloadInfo(self)
            task.bookId = bookId
            self.downloadDict[task.bookId] = task
            self.downloadList.append(task)
            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            self.tableWidget.insertRow(rowCont)
        else:
            task = self.downloadDict.get(bookId)
            if task.status == task.Success:
                task.status = task.Waiting
                if task not in self.downloadList:
                    self.downloadList.append(task)
            if task.convertStatus == task.Converting:
                task.SetConvertStatu(task.Pause)
            elif task.convertStatus == task.ConvertSuccess:
                task.SetConvertStatu(task.Waiting)
        task.AddDownload(downloadIds)
        self.UpdateTableItem(task)
        self.HandlerDownloadList()
        self.db.AddDownloadDB(task)
        return True

    def AddConvert(self, bookId):
        if bookId not in self.downloadDict:
            return False
        task = self.downloadDict.get(bookId)
        if task not in self.convertList:
            self.convertList.append(task)
        self.HandlerConvertList()

    def HandlerDownloadList(self):
        downloadNum = config.DownloadThreadNum
        addNum = downloadNum - len(self.downloadingList)

        if addNum <= 0:
            return

        for _ in range(addNum):
            if len(self.downloadList) <= 0:
                return
            for task in list(self.downloadList):
                assert isinstance(task, DownloadInfo)
                if task.status != DownloadInfo.Waiting:
                    continue
                self.downloadList.remove(task)
                self.downloadingList.append(task)
                task.status = DownloadInfo.Downloading
                task.StartDownload()
                self.UpdateTableItem(task)
                break
        pass

    def HandlerConvertList(self):
        downloadNum = config.DownloadThreadNum
        addNum = downloadNum - len(self.convertingList)

        if addNum <= 0:
            return

        for _ in range(addNum):
            if len(self.convertList) <= 0:
                return
            for task in list(self.convertList):
                assert isinstance(task, DownloadInfo)
                if task.status != DownloadInfo.Success:
                    continue
                if task.convertStatus != DownloadInfo.Waiting:
                    continue
                self.convertList.remove(task)
                self.convertingList.append(task)
                task.convertStatus = DownloadInfo.Converting
                task.StartConvert()
                self.UpdateTableItem(task)
                break
        pass

    def GetStatusText(self, status):
        if status == DownloadInfo.Success:
            status = self.tr("下载完成")
        elif status == DownloadInfo.Reading:
            status = self.tr("获取信息")
        elif status == DownloadInfo.ReadingEps:
            status = self.tr("获取章节")
        elif status == DownloadInfo.ReadingPicture:
            status = self.tr("获取下载地址")
        elif status == DownloadInfo.Downloading:
            status = self.tr("正在下载")
        elif status == DownloadInfo.Waiting:
            status = self.tr("等待中")
        elif status == DownloadInfo.Pause:
            status = self.tr("暂停")
        elif status == DownloadInfo.Error:
            status = self.tr("出错了")
        elif status == DownloadInfo.NotFound:
            status = self.tr("原始文件不存在")
        elif status == DownloadInfo.Converting:
            status = self.tr("转换中")
        elif status == DownloadInfo.ConvertSuccess:
            status = self.tr("转换成功")
        return status

    def UpdateTableItem(self, info):
        assert isinstance(info, DownloadInfo)

        self.tableWidget.setItem(info.tableRow, 0, QTableWidgetItem(info.bookId))
        self.tableWidget.setItem(info.tableRow, 1, QTableWidgetItem(info.title))
        self.tableWidget.setItem(info.tableRow, 2, QTableWidgetItem(self.GetStatusText(info.status)))
        self.tableWidget.setItem(info.tableRow, 3,
                                 QTableWidgetItem("{}/{}".format(str(info.curDownloadPic), str(info.maxDownloadPic))))
        self.tableWidget.setItem(info.tableRow, 4,
                                 QTableWidgetItem("{}/{}".format(str(info.curDownloadEps), str(info.epsCount))))
        self.tableWidget.setItem(info.tableRow, 5, QTableWidgetItem(info.speedStr))
        self.tableWidget.setItem(info.tableRow, 6, QTableWidgetItem("{}/{}".format(str(info.curConvertCnt), str(info.convertCnt))))
        self.tableWidget.setItem(info.tableRow, 7, QTableWidgetItem("{}/{}".format(str(info.curConvertEps), str(info.convertEpsCnt))))
        self.tableWidget.setItem(info.tableRow, 8, QTableWidgetItem("{}".format(str(info.convertTick))))
        self.tableWidget.setItem(info.tableRow, 9, QTableWidgetItem(self.GetStatusText(info.convertStatus)))
        self.tableWidget.update()
        return

    def RemoveRecord(self, bookId):
        task = self.downloadDict.get(bookId)
        if not task:
            return
        assert isinstance(task, DownloadInfo)
        task.SetStatu(task.Pause)
        task.SetConvertStatu(task.Pause)
        if task in self.downloadingList:
            self.downloadingList.remove(task)
        if task in self.downloadList:
            self.downloadList.remove(task)
        if task in self.convertList:
            self.convertList.remove(task)
        if task in self.convertingList:
            self.convertingList.remove(task)
        self.downloadDict.pop(bookId)
        self.tableWidget.removeRow(task.tableRow)
        self.db.DelDownloadDB(bookId)

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
        openDirAction = QAction(self.tr("打开目录"), self)
        openDirAction.triggered.connect(self.ClickOpenFilePath)

        pauseAction = QAction(self.tr("暂停"), self)
        pauseAction.triggered.connect(self.ClickPause)

        removeAction = QAction(self.tr("刪除记录"), self)
        removeAction.triggered.connect(self.DelRecording)

        removeFileAction = QAction(self.tr("刪除记录和文件"), self)
        removeFileAction.triggered.connect(self.DelRecordingAndFile)

        # self.openDirAction = QAction("打开目录", self)
        # self.openDirAction.triggered.connect(self.ClickOpenFilePath)

        selectEpsAction = QAction(self.tr("选择下载章节"), self)
        selectEpsAction.triggered.connect(self.ClickDownloadEps)

        startAction = QAction(self.tr("开始"), self)
        startAction.triggered.connect(self.ClickStart)

        startConvertAction = QAction(self.tr("开始转换"), self)
        startConvertAction.triggered.connect(self.ClickConvertStart)

        pauseConvertAction = QAction(self.tr("暂停转换"), self)
        pauseConvertAction.triggered.connect(self.ClickConvertPause)

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

                menu = QMenu(self.tableWidget)

                menu.addAction(openDirAction)
                menu.addAction(selectEpsAction)
                assert isinstance(task, DownloadInfo)
                if task.status in [DownloadInfo.Pause, DownloadInfo.Error]:
                    menu.addAction(startAction)
                elif task.status in [DownloadInfo.Downloading, DownloadInfo.Waiting,
                                     DownloadInfo.Reading, DownloadInfo.ReadingPicture, DownloadInfo.ReadingEps]:
                    menu.addAction(pauseAction)
                else:
                    if task.convertStatus in [DownloadInfo.Converting]:
                        menu.addAction(pauseConvertAction)
                    elif task.convertStatus in [DownloadInfo.Pause, DownloadInfo.Error, DownloadInfo.NotFound]:
                        menu.addAction(startConvertAction)
            else:
                menu = QMenu(self.tableWidget)

            menu.addAction(removeAction)
            menu.addAction(removeFileAction)
            menu.exec_(QCursor.pos())
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
        assert isinstance(task, DownloadInfo)
        QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(task.savePath)))
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
            if task.status in [DownloadInfo.Success]:
                continue
            if task in self.downloadingList:
                self.downloadingList.remove(task)
            task.SetStatu(task.Pause)
        self.HandlerDownloadList()
        return

    def ClickConvertPause(self):
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
            if task.convertStatus in [DownloadInfo.ConvertSuccess]:
                continue
            if task in self.convertingList:
                self.convertingList.remove(task)
            task.SetConvertStatu(task.Pause)
        self.HandlerConvertList()
        return

    def ClickDownloadEps(self):
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
            QtOwner().owner.epsInfoForm.OpenEpsInfo(task.bookId)

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
            if task.status not in [DownloadInfo.Pause, DownloadInfo.Error]:
                continue
            # task.status = DownloadInfo.Reading

            if task not in self.downloadList:
                self.downloadList.append(task)
            task.SetStatu(task.Waiting)
        self.HandlerDownloadList()

    def ClickConvertStart(self):
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
            if task.convertStatus not in [DownloadInfo.Pause, DownloadInfo.Error]:
                continue
            # task.status = DownloadInfo.Reading
            if task not in self.convertList:
                self.convertList.append(task)
            task.SetConvertStatu(task.Waiting)
        self.HandlerConvertList()

    def DelRecording(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in sorted(selectRows, reverse=True):
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
            for row in sorted(selectRows, reverse=True):
                col = 0
                bookId = self.tableWidget.item(row, col).text()
                bookInfo = self.downloadDict.get(bookId)
                if not bookInfo:
                    continue
                self.RemoveRecord(bookId)
                path = os.path.dirname(bookInfo.savePath)
                if os.path.isdir(path):
                    shutil.rmtree(path, True)

        except Exception as es:
            Log.Error(es)
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
        QtOwner().owner.bookInfoForm.OpenBook(bookId)

    def StartAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status not in [DownloadInfo.Pause, DownloadInfo.Error]:
                continue

            if task not in self.downloadList:
                self.downloadList.append(task)
            task.SetStatu(task.Waiting)
        self.HandlerDownloadList()

    def StopAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status in [DownloadInfo.Success]:
                continue
            if task in self.downloadingList:
                self.downloadingList.remove(task)
            task.SetStatu(task.Pause)

    def StartConvertAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status not in [DownloadInfo.Success]:
                continue
            if task.convertStatus not in [DownloadInfo.Pause, DownloadInfo.Error]:
                continue
            # task.status = DownloadInfo.Reading
            if task not in self.convertList:
                self.convertList.append(task)
            task.SetConvertStatu(task.Waiting)
        self.HandlerConvertList()

    def StopConvertAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.convertStatus in [DownloadInfo.ConvertSuccess]:
                continue
            if task in self.convertingList:
                self.convertingList.remove(task)
            task.SetConvertStatu(task.Pause)

    def SetAutoConvert(self):
        config.DownloadAuto = int(self.radioButton.isChecked())

    def Sort(self, col):
        order = self.order.get(col, 1)
        if order == 1:
            self.tableWidget.sortItems(col, Qt.AscendingOrder)
            self.order[col] = 0
        else:
            self.tableWidget.sortItems(col, Qt.DescendingOrder)
            self.order[col] = 1
        self.UpdateTableRow()
