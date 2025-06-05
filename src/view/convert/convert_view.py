import os
import shutil
import time

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer, QUrl, QSize
from PySide6.QtGui import QCursor, QDesktopServices, QAction, QIcon
from PySide6.QtWidgets import QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem

from config import config
from config.setting import Setting
from interface.ui_convert import Ui_Convert
from interface.ui_download import Ui_Download
from qt_owner import QtOwner
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr, Book
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil
from view.convert.convert_status import ConvertStatus


class ConvertView(QtWidgets.QWidget, Ui_Convert, ConvertStatus):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Convert.__init__(self)
        ConvertStatus.__init__(self)
        self.setupUi(self)

        # self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tableWidget.setColumnCount(9)
        # # self.tableWidget.setHorizontalHeaderLabels(HorizontalHeaderLabels)
        # self.timer = QTimer(self.tableWidget)
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.TimeOutHandler)
        #
        # # self.settings = QSettings('download.ini', QSettings.IniFormat)
        # # self.InitSetting()
        #
        # self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)
        #
        # self.tableWidget.doubleClicked.connect(self.OpenBookInfo)
        #
        # self.tableWidget.horizontalHeader().sectionClicked.connect(self.Sort)
        # self.order = {}
        # # datas = self.db.LoadDownload(self)
        # self.tableWidget.setColumnHidden(0, True)
        # # for task in datas.values():
        # #     self.downloadDict[task.bookId] = task
        # #     if not task.epsIds:
        # #         Log.Warn("not fond task, epsIds, bookId:{}, title:{}".format(task.bookId, task.title))
        # #         continue
        # #     rowCont = self.tableWidget.rowCount()
        # #     task.tableRow = rowCont
        # #     self.tableWidget.insertRow(rowCont)
        # #     self.UpdateTableItem(task)
        #
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # # self.tableWidget.horizontalHeader().setMinimumSectionSize(120)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # # self.tableWidget.setColumnWidth(0, 40)
        # print(self.width())
        # self.tableWidget.setColumnWidth(1, 300)

    def Close(self):
        self.timer.stop()

    def Init(self):
        self.timer.start()

    def GetDownloadEpsInfo(self, bookId, epsId):
        info = self.GetDownloadInfo(bookId)
        if not info:
            return False
        return info.epsInfo.get(epsId)

    def GetDownloadInfo(self, bookId):
        return self.downloadDict.get(bookId)

    def IsDownloadEpsId(self, bookId, epsId):
        info = self.GetDownloadInfo(bookId)
        if not info:
            return False
        return epsId in info.epsIds

    def GetDownloadEpsId(self, bookId):
        if bookId not in self.downloadDict:
            return []
        return self.downloadDict[bookId].epsIds

    # def GetDownloadCompleteEpsId(self, bookId):
    #     if bookId not in self.downloadDict:
    #         return []
    #     return self.downloadDict[bookId].GetDownloadCompleteEpsId()

    def GetDownloadWaifu2xFilePath(self, bookId, epsId, index):
        if bookId not in self.downloadDict:
            return ""
        task = self.downloadDict[bookId]
        if epsId not in task.epsInfo:
            return ""
        epsTitle = task.epsInfo[epsId].epsTitle
        convertPath = os.path.join(task.convertPath, ToolUtil.GetCanSaveName(epsTitle))
        return os.path.join(convertPath, "{:04}.{}".format(index + 1, "jpg"))

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

        localTime = time.localtime(info.tick)

        strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        self.tableWidget.setItem(info.tableRow, 0, QTableWidgetItem(info.bookId))
        self.tableWidget.setItem(info.tableRow, 1, QTableWidgetItem(strTime))
        item = QTableWidgetItem(info.title)
        item.setToolTip(info.title)
        self.tableWidget.setItem(info.tableRow, 2, item)

        self.tableWidget.setItem(info.tableRow, 6, QTableWidgetItem(info.GetStatusMsg()))

        self.tableWidget.setItem(info.tableRow, 3, QTableWidgetItem("{}/{}".format(str(info.curDownloadPic), str(info.maxDownloadPic))))
        bookInfo = BookMgr().GetBook(info.bookId)

        item2 = QTableWidgetItem("{}/{}".format(str(info.curDownloadEps), str(info.epsCount)))
        if isinstance(bookInfo, Book):
            if len(info.epsIds) < bookInfo.epsCount:
                icon2 = QIcon()
                icon2.addFile(u":/png/icon/new.svg", QSize(), QIcon.Normal, QIcon.Off)
                item2.setIcon(icon2)
        self.tableWidget.setItem(info.tableRow, 4, item2)
        self.tableWidget.setItem(info.tableRow, 5, QTableWidgetItem(info.speedStr))
        self.tableWidget.setItem(info.tableRow, 7, QTableWidgetItem("{}/{}".format(str(info.curConvertCnt), str(info.convertCnt))))
        self.tableWidget.setItem(info.tableRow, 8, QTableWidgetItem("{}/{}".format(str(info.curConvertEps), str(info.convertEpsCnt))))
        self.tableWidget.setItem(info.tableRow, 9, QTableWidgetItem("{}".format(str(info.convertTick))))
        self.tableWidget.setItem(info.tableRow, 10, QTableWidgetItem(info.GetConvertStatusMsg()))
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
                if task.status in [task.Pause, task.Error, task.SpaceEps]:
                    menu.addAction(startAction)
                elif task.status in [task.Downloading, task.Waiting]:
                    menu.addAction(pauseAction)

                if task.convertStatus in [task.Converting, task.Waiting]:
                    menu.addAction(pauseConvertAction)
                elif task.convertStatus in [task.Pause, task.Error, task.SpaceEps]:
                    menu.addAction(startConvertAction)
            else:
                menu = QMenu(self.tableWidget)
                menu.addAction(startAction)
                menu.addAction(pauseAction)
                menu.addAction(startConvertAction)
                menu.addAction(pauseConvertAction)

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
            if task.status not in [task.Pause, task.Error, task.SpaceEps]:
                continue
            self.SetNewStatus(task, task.Waiting)

            if Setting.DownloadAuto.value:
                if task.convertStatus not in [task.Pause, task.Error, task.SpaceEps]:
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
            if task.convertStatus not in [task.Pause, task.Error, task.SpaceEps]:
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
            if task.status not in [task.Pause, task.Error, task.SpaceEps]:
                continue
            self.SetNewStatus(task, task.Waiting)
            if Setting.DownloadAuto.value:
                if task.convertStatus not in [task.Pause, task.Error, task.SpaceEps]:
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
            if task.convertStatus not in [task.Pause, task.Error, task.SpaceEps]:
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