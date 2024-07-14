from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import QItemSelectionModel, Qt, QEvent
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView, QMenu

from interface.ui_download_all import Ui_DownloadAll
from qt_owner import QtOwner
from server import req, Status
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.str import Str
from view.download.download_all_item import DownloadAllItem


class DownloadAllView(QtWidgets.QWidget, Ui_DownloadAll, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_DownloadAll.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        # self.buttonGroup = QtWidgets.QButtonGroup(self)
        # self.buttonGroup.addButton(self.selectIp1)
        # self.selectIp1.setChecked(True)
        self.task = {}
        self.waitTask = []
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.doubleClicked.connect(self.OpenBookInfo)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tableWidget.setColumnWidth(4, 300)
        # self.tableWidget.installEventFilter(self)
        self.selectAllButton.clicked.connect(self.SelectAll)
        self.chipButton.clicked.connect(self.SelectAllChip)
        self.downButton.clicked.connect(self.StartDownload)
        self.isAll = True
        self.isAllChip = True
        self.uploadButton.clicked.connect(self.ShowMenu)
        self.selectNasId = ""

    def SelectAll(self):
        self.isAll = not self.isAll
        for v in self.task.values():
            v.isAll = self.isAll
            self.UpdateTableItem(v)
        return

    def SelectAllChip(self):
        self.isAllChip = not self.isAllChip
        for v in self.task.values():
            v.isAllChip = self.isAllChip
            self.UpdateTableItem(v)
        return

    def StartDownload(self):
        self.selectNasId = ""
        self.StartDownload2()

    def StartDownload2(self):
        if not self.task:
            return
        for v in self.task.values():
            isFind = False
            item = self.tableWidget.item(v.tableRow, 0)
            v.isAll = item.checkState() == Qt.Checked
            item2 = self.tableWidget.item(v.tableRow, 1)
            v.isAllChip = item2.checkState() == Qt.Checked

            if item.checkState() == Qt.Unchecked:
                continue
            for v2 in self.waitTask:
                if v2.bookId == v.bookId:
                    isFind = True
                    break
            if isFind:
                continue
            self.waitTask.append(v)
        self.InitBooks([])
        self.StartGetEpsData()
        return

    def SwitchCurrent(self, **kwargs):
        books = kwargs.get("books")
        if books is None:
            return
        self.InitBooks(books)

    def InitBooks(self, books):
        # self.tableWidget.clear()
        for i in range(self.tableWidget.rowCount(), 0, -1):
            self.tableWidget.removeRow(i-1)

        self.task.clear()
        for task in books:
            if QtOwner().IsInFilter(task.category, "", task.title):
                task.isAll = False
                task.isAllChip = False
            self.task[task.bookId] = task
            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            self.tableWidget.insertRow(rowCont)
            self.UpdateTableItem(task)

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
        bookId = ""
        for v in self.task.values():
            if v.tableRow == row:
                bookId = v.bookId
        if not bookId:
            return
        QtOwner().OpenBookInfo(bookId)

    def UpdateTableItem(self, info):
        assert isinstance(info, DownloadAllItem)

        item = QTableWidgetItem()

        if info.isAll:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.tableWidget.setItem(info.tableRow, 0, item)

        item = QTableWidgetItem()
        if info.isAllChip:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.tableWidget.setItem(info.tableRow, 1, item)
        item = QTableWidgetItem(str(info.pages))
        self.tableWidget.setItem(info.tableRow, 2, item)
        item = QTableWidgetItem(info.category)
        self.tableWidget.setItem(info.tableRow, 3, item)
        item = QTableWidgetItem(info.title)
        self.tableWidget.setItem(info.tableRow, 4, item)
        return

    def StartGetEpsData(self):
        if not self.waitTask:
            self.msgLabel.setText("")
            return
        self.msgLabel.setText("{}个任务等待处理".format(str(len(self.waitTask))))
        v = self.waitTask.pop(len(self.waitTask)-1)
        assert isinstance(v, DownloadAllItem)
        if v.isAllChip:
            info = BookMgr().GetBook(v.bookId)
            if info and info.epsCount > 0:
                downloadIds = list(range(info.epsCount))
                if self.selectNasId:
                    QtOwner().nasView.AddNasUploadCache(self.selectNasId, v.bookId)
                else:
                    QtOwner().downloadView.AddDownload(v.bookId, downloadIds)
                self.StartGetEpsData()
            else:
                self.AddSqlTask("book", v.bookId, SqlServer.TaskTypeCacheBook, callBack=self.SendLocalBack, backParam=v)
        else:
            if self.selectNasId:
                QtOwner().nasView.AddNasUploadCache(self.selectNasId, v.bookId)
            else:
                QtOwner().downloadView.AddDownload(v.bookId, [0])
            self.StartGetEpsData()

    def SendLocalBack(self, books, v):
        if not QtOwner().isOfflineModel:
            self.AddHttpTask(req.GetComicsBookReq(v.bookId), self.OpenBookBack, backParam=v)
        else:
            self.OpenBookBack({"st": Status.Ok}, v)

    def OpenBookBack(self, raw, v):
        info = BookMgr().GetBook(v.bookId)
        if info and info.epsCount > 0:
            downloadIds = list(range(info.epsCount))
            if self.selectNasId:
                QtOwner().nasView.AddNasUploadCache(self.selectNasId, v.bookId)
            else:
                QtOwner().downloadView.AddDownload(v.bookId, downloadIds)
        self.StartGetEpsData()

    def ShowMenu(self):
        toolMenu = QMenu(self.uploadButton)
        toolMenu.clear()
        nasDict = QtOwner().owner.nasView.nasDict
        action = toolMenu.addAction(Str.GetStr(Str.NetNas))
        action.setEnabled(False)

        if not nasDict:
            action = toolMenu.addAction(Str.GetStr(Str.CvSpace))
            action.setEnabled(False)
        else:
            for k, v in nasDict.items():
                action = toolMenu.addAction(v.showTitle)
                self.selectNasId = k
                action.triggered.connect(partial(self.StartUpload, k))
        toolMenu.exec(QCursor().pos())

    def StartUpload(self, nasId):
        self.selectNasId = nasId
        self.StartDownload2()