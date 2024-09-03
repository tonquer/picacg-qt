import os
import shutil
import time
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QCursor, QDesktopServices, QAction
from PySide6.QtWidgets import QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem, QListWidgetItem, QMessageBox

from component.widget.nas_item_widget import NasItemWidget
from config import config
from config.setting import Setting
from interface.ui_download import Ui_Download
from interface.ui_nas import Ui_Nas
from qt_owner import QtOwner
from server import req
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil
from view.nas.nas_add_view import NasAddView
from view.nas.nas_db import NasDb
from view.nas.nas_item import NasInfoItem, NasUploadItem
from view.nas.nas_status import NasStatus


class NasView(QtWidgets.QWidget, Ui_Nas, NasStatus):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Nas.__init__(self)
        NasStatus.__init__(self)
        self.setupUi(self)

        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)
        # self.tableWidget.setColumnCount(11)
        # self.tableWidget.setHorizontalHeaderLabels(HorizontalHeaderLabels)
        self.timer = QTimer(self.tableWidget)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.TimeOutHandler)

        # self.settings = QSettings('download.ini', QSettings.IniFormat)
        # self.InitSetting()

        # self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)
        self.tableWidget.doubleClicked.connect(self.OpenBookInfo)
        # self.tableWidget.horizontalHeader().sectionClicked.connect(self.Sort)
        self.order = {}
        self.db = NasDb()
        datas = self.db.LoadNasInfo(self)
        self.nasDict = datas

        datas = self.db.LoadUpload(self)
        for task in datas.values():
            self.downloadDict[task.key] = task
            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            self.tableWidget.insertRow(rowCont)
            if task.status != task.Success:
                task.status = task.Pause
            self.UpdateTableItem(task)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.horizontalHeader().setMinimumSectionSize(120)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # self.tableWidget.setColumnWidth(0, 40)
        print(self.width())
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 300)
        self.addButton.clicked.connect(self.OpenAddView)
        self.isInt = False

    def retranslateUi(self, Nas):
        themId = Setting.ThemeIndex.autoValue
        if themId != 1:
            qss = """
                .QListWidgetItem
                {
                    background-color: rgb(253, 253, 253);

                    border:2px solid rgb(234,234,234);
                    border-radius:5px
                }        
                """
        else:
            qss = """
                .QListWidgetItem
                {
                    background-color: rgb(50, 50, 50);

                    border:2px solid rgb(35,35,35);
                    border-radius:5px
                }        
                """
        self.listWidget.setStyleSheet(qss)
        Ui_Nas.retranslateUi(self, self)

    def SwitchCurrent(self, **kwargs):
        if not self.isInt:
            self.LoadData()
            self.isInt = True

        self.LoadNasInfo()
        self.tabWidget.setCurrentIndex(0)
        self.CheckSuc()
        pass

    def CheckSuc(self):
        for task in self.downloadDict.values():
            if task.status != task.Success:
                continue
            if task.completeNum < task.maxDownloadPic:
                self.SetNewStatus(task, task.Waiting)

    def LoadData(self):
        for task in self.downloadDict.values():
            self.UpdateTableItem(task)

    def OpenAddView(self):
        if not self.nasDict:
            maxId = 1001
        else:
            maxId = max(self.nasDict.keys()) + 1
        view = NasAddView(QtOwner().owner, maxId)
        view.SaveLogin.connect(self.AddNasInfo)

        view.show()

    def OpenNasInfo(self, nasId):
        nasInfo = self.nasDict.get(nasId)
        if not nasInfo:
            return
        view = NasAddView(QtOwner().owner, nasId)
        view.Init(nasInfo)
        view.SaveLogin.connect(self.AddNasInfo)
        view.show()
        pass

    def DelNasInfo(self, nasId):
        if nasId not in self.nasDict:
            return
        nasInfo = self.nasDict[nasId]
        isClear = QMessageBox.information(self, '删除网络存储', "是否删除网络存储， {}".format(nasInfo.title), QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if isClear != QtWidgets.QMessageBox.Yes:
            return

        self.nasDict.pop(nasId)
        self.db.DelNasDB(nasId)
        QtOwner().ShowMsg(Str.GetStr(Str.Ok))

        self.LoadNasInfo()
        pass

    def AddNasInfo(self, nasInfo):
        self.db.AddNasDB(nasInfo)
        self.nasDict[nasInfo.nasId] = nasInfo
        self.LoadNasInfo()
        return

    def LoadNasInfo(self):
        self.listWidget.clear()
        allList = self.nasDict.values()
        for v in sorted(list(allList), key=lambda v:v.nasId, reverse=True):
            self.AddNasInfoItem(v)
        return

    def UpdateTableItem(self, info):
        assert isinstance(info, NasUploadItem)
        localTime = time.localtime(info.tick)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

        self.tableWidget.setItem(info.tableRow, 0, QTableWidgetItem(info.key))
        self.tableWidget.setItem(info.tableRow, 1, QTableWidgetItem(strTime))
        item = QTableWidgetItem(info.title)
        item.setToolTip(info.title)
        self.tableWidget.setItem(info.tableRow, 2, item)
        self.tableWidget.setItem(info.tableRow, 3, QTableWidgetItem(info.nasTitle))
        self.tableWidget.setItem(info.tableRow, 4,
                                 QTableWidgetItem("{}/{}".format(str(info.completeNum), str(info.maxDownloadPic))))

        self.tableWidget.setItem(info.tableRow, 5, QTableWidgetItem(Str.GetStr(info.status)))
        self.tableWidget.setItem(info.tableRow, 6, QTableWidgetItem(info.GetStatusMsg()))
        return

    def IsInUpload(self, nasId, bookId):
        key = "{}-{}".format(nasId, bookId)
        return key in self.downloadDict

    def AddNasInfoItem(self, v):
        assert isinstance(v, NasInfoItem)
        index = self.listWidget.count()
        widget = NasItemWidget()
        widget.title.setText(v.title)
        widget.address.setText(v.address + ":" + str(v.port))
        widget.waifu2x.setEnabled(bool(v.is_waifu2x))
        widget.user.setText(v.user)
        widget.editButton.clicked.connect(partial(self.OpenNasInfo, v.nasId))
        widget.delButton.clicked.connect(partial(self.DelNasInfo, v.nasId))
        item = QListWidgetItem(self.listWidget)
        # item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())

        self.listWidget.setItemWidget(item, widget)

    def AddNasUpload(self, nasId, bookId):
        bookId = str(bookId)
        QtOwner().ShowLoading()
        self.AddSqlTask("book", bookId, SqlServer.TaskTypeCacheBook, callBack=self.SendLocalBack, backParam=(nasId, bookId))

        # self.AddHttpTask(req.GetComicsBookReq(bookId), self.OpenEpsInfoBack, (nasId, bookId))
        # self.AddNasUploadCache(nasId, bookId)
        return True

    def SendLocalBack(self, books, v):
        nasId, bookId = v
        self.AddNasUploadCache(nasId, bookId)

    def AddNasUpload2(self, title, nasId, bookId, isShowMsg=True):
        bookId = str(bookId)
        key = "{}-{}".format(nasId, bookId)
        if key not in self.downloadDict:
            task = NasUploadItem()
            task.bookId = bookId
            task.nasId = nasId
            task.title = title

            self.downloadDict[key] = task
            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            self.tableWidget.insertRow(rowCont)
            self.SetNewStatus(task, task.Waiting)
            isShowMsg and QtOwner().ShowError(Str.GetStr(Str.CvAddUpload))
        else:
            task = self.downloadDict.get(key)
            if task.status == task.Success:
                self.SetNewStatus(task, task.Waiting)

        return

    def AddNasUploadCache(self, nasId, bookId):
        bookId = str(bookId)
        nasInfo = self.nasDict.get(nasId)
        QtOwner().CloseLoading()
        info = BookMgr().GetBook(bookId)
        if not info or not nasInfo:
            QtOwner().ShowError(Str.GetStr(Str.NotFoundBook))
            return
        if info.epsCount <= 0:
            QtOwner().ShowError(Str.GetStr(Str.SpaceEps))
            return
        epsIds = list(range(info.epsCount))
        QtOwner().downloadView.AddDownload(bookId, epsIds, nasInfo.is_waifu2x)
        self.AddNasUpload2(info.title, nasId, bookId, True)

    # def OpenEpsInfoBack(self, raw, v):
    #     QtOwner().CloseLoading()
    #     nasId, bookId = v
    #     nasInfo = self.nasDict.get(nasId)
    #     QtOwner().CloseLoading()
    #     self.listWidget.clear()
    #     st = raw["st"]
    #     if st == Status.Ok:
    #         info = BookMgr().GetBook(bookId)
    #         if not info:
    #             QtOwner().ShowError(Str.GetStr(Str.Error))
    #             return
    #         if not info.pageInfo.epsInfo:
    #             QtOwner().ShowError(Str.GetStr(Str.SpaceEps))
    #             return
    #         epsIds = list(info.pageInfo.epsInfo.keys())
    #         QtOwner().downloadView.AddDownload(bookId, epsIds, nasInfo.is_waifu2x)
    #         self.AddNasUpload2(info.baseInfo.title, nasId, bookId)
    #     else:
    #         QtOwner().ShowError(Str.GetStr(st))
    #     return

    # 右键菜单
    def SelectMenu(self, pos):
        index = self.tableWidget.indexAt(pos)
        pauseAction = QAction(Str.GetStr(Str.Pause), self)
        pauseAction.triggered.connect(self.ClickPause)

        removeAction = QAction(Str.GetStr(Str.DeleteRecord), self)
        removeAction.triggered.connect(self.DelRecording)

        startAction = QAction(Str.GetStr(Str.Start), self)
        startAction.triggered.connect(self.ClickStart)

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
                key = self.tableWidget.item(row, col).text()
                title = self.tableWidget.item(row, 2).text()
                task = self.downloadDict.get(key)
                if not task:
                    return

                menu = QMenu(self.tableWidget)

                assert isinstance(task, NasUploadItem)
                if task.status in [task.Success, task.Pause, task.Error]:
                    menu.addAction(startAction)
                elif task.status in [task.Uploading, task.Waiting, task.WaitWaifu2x]:
                    menu.addAction(pauseAction)

            else:
                menu = QMenu(self.tableWidget)
                menu.addAction(startAction)
                menu.addAction(pauseAction)

            menu.addAction(removeAction)
            menu.exec_(QCursor.pos())
        pass

    def ClickStart(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            key = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(key)
            if not task:
                continue
            if task.status not in [task.Success, task.Pause, task.Error]:
                continue
            self.SetNewStatus(task, task.Waiting)

    def ClickPause(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            key = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(key)
            if not task:
                continue
            if task.status in [task.Success]:
                continue
            self.SetNewStatus(task, task.Pause)
        return

    def DelRecording(self):
        isClear = QMessageBox.information(self, '删除记录', "是否删除记录", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if isClear != QtWidgets.QMessageBox.Yes:
            return
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in sorted(selectRows, reverse=True):
            col = 0
            key = self.tableWidget.item(row, col).text()
            self.RemoveRecord(key)
        self.UpdateTableRow()

    def UpdateTableRow(self):
        count = self.tableWidget.rowCount()
        for i in range(count):
            key = self.tableWidget.item(i, 0).text()
            info = self.downloadDict.get(key)
            if info:
                info.tableRow = i

    def RemoveRecord(self, key):
        task = self.downloadDict.get(key)
        if not task:
            return
        assert isinstance(task, NasUploadItem)
        if task in self.downloadingList:
            self.downloadingList.remove(task)
        if task in self.downloadList:
            self.downloadList.remove(task)
        self.downloadDict.pop(key)
        self.tableWidget.removeRow(task.tableRow)
        self.db.DelUploadDB(task.nasId, task.bookId)

    def Close(self):
        self.timer.stop()

    def Init(self):
        self.timer.start()

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
        key = self.tableWidget.item(row, col).text()
        info = self.downloadDict.get(key)
        if not info:
            return
        QtOwner().OpenBookInfo(info.bookId)