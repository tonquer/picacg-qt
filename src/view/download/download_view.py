import os
import shutil

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QCursor, QDesktopServices, QAction
from PySide6.QtWidgets import QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem

from config import config
from config.setting import Setting
from interface.ui_download import Ui_Download
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil
from view.download.download_db import DownloadDb
from view.download.download_item import DownloadItem
from view.download.download_status import DownloadStatus


class DownloadView(QtWidgets.QWidget, Ui_Download, DownloadStatus):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Download.__init__(self)
        DownloadStatus.__init__(self)
        self.setupUi(self)

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
        self.timer.timeout.connect(self.TimeOutHandler)

        # self.settings = QSettings('download.ini', QSettings.IniFormat)
        # self.InitSetting()

        self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)

        self.tableWidget.doubleClicked.connect(self.OpenBookInfo)

        self.tableWidget.horizontalHeader().sectionClicked.connect(self.Sort)
        self.order = {}
        self.radioButton.setChecked(Setting.DownloadAuto.value)
        datas = self.db.LoadDownload(self)
        for task in datas.values():
            self.downloadDict[task.bookId] = task
            if not task.epsIds:
                Log.Warn("not fond task, epsIds, bookId:{}, title:{}".format(task.bookId, task.title))
                continue

            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            self.tableWidget.insertRow(rowCont)
            self.RepairData(task)
            self.UpdateTableItem(task)

    # 修复下数据
    def RepairData(self, task):
        assert isinstance(task, DownloadItem)
        task.status = self.GetNewStatus(task.status)
        task.convertStatus = self.GetNewStatus(task.convertStatus)
        if task.status != task.Success:
            task.status = task.Pause
        if task.convertStatus != task.ConvertSuccess:
            task.convertStatus = task.Pause

        for info in task.epsInfo.values():
            # 如果下载完成了，要修改下 curPreDownloadIndex和 curPreConvertId
            if task.status == task.Success:
                info.curPreDownloadIndex = info.picCnt
            if task.convertStatus == task.ConvertSuccess:
                info.curPreConvertId = info.picCnt
        return

    def GetNewStatus(self, status):
        if status.isnumeric():
            return int(status)
        # 兼容老數據
        infos = [DownloadItem.Success, DownloadItem.Downloading, DownloadItem.Waiting, Str.ReadingPicture, Str.Reading, Str.ReadingEps, Str.NotFound,
         DownloadItem.Pause, DownloadItem.Error, DownloadItem.ConvertSuccess, DownloadItem.Converting]
        for i in infos:
            if Str.GetStr(i) == status:
                return i
        return DownloadItem.Pause

    def Close(self):
        self.timer.stop()

    def Init(self):
        self.timer.start()

    def GetDownloadEpsId(self, bookId):
        if bookId not in self.downloadDict:
            return []
        return self.downloadDict[bookId].epsIds

    # def GetDownloadCompleteEpsId(self, bookId):
    #     if bookId not in self.downloadDict:
    #         return []
    #     return self.downloadDict[bookId].GetDownloadCompleteEpsId()

    def GetDownloadFilePath(self, bookId, epsId, index):
        if bookId not in self.downloadDict:
            return ""
        task = self.downloadDict[bookId]
        if epsId not in task.epsInfo:
            return ""
        epsTitle = task.epsInfo[epsId].epsTitle
        savePath = os.path.join(task.savePath, ToolUtil.GetCanSaveName(epsTitle))
        return os.path.join(savePath, "{:04}.{}".format(index + 1, "jpg"))

    def SwitchCurrent(self, **kwargs):
        pass

    def AddDownload(self, bookId, downloadIds):
        if not downloadIds:
            return

        if bookId not in self.downloadDict:
            task = DownloadItem()
            task.bookId = bookId
            self.downloadDict[task.bookId] = task
            downloadIds.sort()
            for epsId in downloadIds:
                if epsId in task.epsIds:
                    continue
                task.epsIds.append(epsId)

            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            self.tableWidget.insertRow(rowCont)
            self.SetNewStatus(task, task.Waiting)
            if Setting.DownloadAuto.value:
                self.SetNewCovertStatus(task, task.Waiting)
        else:
            task = self.downloadDict.get(bookId)
            downloadIds.sort()
            for epsId in downloadIds:
                if epsId in task.epsIds:
                    continue
                task.epsIds.append(epsId)

            if task.status == task.Success:
                self.SetNewStatus(task, task.Waiting)
            if task.convertStatus == task.ConvertSuccess:
                if Setting.DownloadAuto.value:
                    self.SetNewCovertStatus(task, task.Waiting)
                else:
                    self.SetNewCovertStatus(task, task.Pause)

        self.UpdateTableItem(task)
        self.db.AddDownloadDB(task)
        return True

    def UpdateTableItem(self, info):
        assert isinstance(info, DownloadItem)
        self.tableWidget.setItem(info.tableRow, 0, QTableWidgetItem(info.bookId))
        item = QTableWidgetItem(info.title)
        item.setToolTip(info.title)
        self.tableWidget.setItem(info.tableRow, 1, item)

        self.tableWidget.setItem(info.tableRow, 2, QTableWidgetItem(info.GetStatusMsg()))
        self.tableWidget.setItem(info.tableRow, 3,
                                 QTableWidgetItem("{}/{}".format(str(info.curDownloadPic), str(info.maxDownloadPic))))
        self.tableWidget.setItem(info.tableRow, 4,
                                 QTableWidgetItem("{}/{}".format(str(info.curDownloadEps), str(info.epsCount))))
        self.tableWidget.setItem(info.tableRow, 5, QTableWidgetItem(info.speedStr))
        self.tableWidget.setItem(info.tableRow, 6, QTableWidgetItem("{}/{}".format(str(info.curConvertCnt), str(info.convertCnt))))
        self.tableWidget.setItem(info.tableRow, 7, QTableWidgetItem("{}/{}".format(str(info.curConvertEps), str(info.convertEpsCnt))))
        self.tableWidget.setItem(info.tableRow, 8, QTableWidgetItem("{}".format(str(info.convertTick))))
        self.tableWidget.setItem(info.tableRow, 9, QTableWidgetItem(info.GetConvertStatusMsg()))
        return

    def RemoveRecord(self, bookId):
        task = self.downloadDict.get(bookId)
        if not task:
            return
        assert isinstance(task, DownloadItem)
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
        openDirAction = QAction(Str.GetStr(Str.OpenDir), self)
        openDirAction.triggered.connect(self.ClickOpenFilePath)

        pauseAction = QAction(Str.GetStr(Str.Pause), self)
        pauseAction.triggered.connect(self.ClickPause)

        removeAction = QAction(Str.GetStr(Str.DeleteRecord), self)
        removeAction.triggered.connect(self.DelRecording)

        removeFileAction = QAction(Str.GetStr(Str.DeleteRecordFile), self)
        removeFileAction.triggered.connect(self.DelRecordingAndFile)

        # self.openDirAction = QAction("打开目录", self)
        # self.openDirAction.triggered.connect(self.ClickOpenFilePath)

        selectEpsAction = QAction(Str.GetStr(Str.SelectEps), self)
        selectEpsAction.triggered.connect(self.ClickDownloadEps)

        startAction = QAction(Str.GetStr(Str.Start), self)
        startAction.triggered.connect(self.ClickStart)

        startConvertAction = QAction(Str.GetStr(Str.StartConvert), self)
        startConvertAction.triggered.connect(self.ClickConvertStart)

        pauseConvertAction = QAction(Str.GetStr(Str.PauseConvert), self)
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
                assert isinstance(task, DownloadItem)
                if task.status in [task.Pause, task.Error]:
                    menu.addAction(startAction)
                elif task.status in [task.Downloading, task.Waiting]:
                    menu.addAction(pauseAction)

                if task.convertStatus in [task.Converting, task.Waiting]:
                    menu.addAction(pauseConvertAction)
                elif task.convertStatus in [task.Pause, task.Error]:
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
        assert isinstance(task, DownloadItem)
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
            if task.status in [task.Success]:
                continue
            self.SetNewStatus(task, task.Pause)
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
            if task.convertStatus in [task.ConvertSuccess]:
                continue
            self.SetNewCovertStatus(task, task.Pause)
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
            QtOwner().OpenEpsInfo(task.bookId)

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
            if task.status not in [task.Pause, task.Error]:
                continue
            self.SetNewStatus(task, task.Waiting)

            if Setting.DownloadAuto.value:
                if task.convertStatus not in [task.Pause, task.Error]:
                    continue
                self.SetNewCovertStatus(task, task.Waiting)

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
            if task.convertStatus not in [task.Pause, task.Error]:
                continue
            self.SetNewCovertStatus(task, task.Waiting)

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
        QtOwner().OpenBookInfo(bookId)

    def StartAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status not in [task.Pause, task.Error]:
                continue
            self.SetNewStatus(task, task.Waiting)
            if Setting.DownloadAuto.value:
                if task.convertStatus not in [task.Pause, task.Error]:
                    continue
                self.SetNewCovertStatus(task, task.Waiting)

    def StopAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status in [task.Success]:
                continue
            self.SetNewStatus(task, task.Pause)

    def StartConvertAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.convertStatus not in [task.Pause, task.Error]:
                continue
            self.SetNewCovertStatus(task, task.Waiting)

    def StopConvertAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.convertStatus in [task.ConvertSuccess]:
                continue
            self.SetNewCovertStatus(task, task.Pause)

    def SetAutoConvert(self):
        Setting.DownloadAuto.SetValue(int(self.radioButton.isChecked()))

    def Sort(self, col):
        order = self.order.get(col, 1)
        if order == 1:
            self.tableWidget.sortItems(col, Qt.AscendingOrder)
            self.order[col] = 0
        else:
            self.tableWidget.sortItems(col, Qt.DescendingOrder)
            self.order[col] = 1
        self.UpdateTableRow()
