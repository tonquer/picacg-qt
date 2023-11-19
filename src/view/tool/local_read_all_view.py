import time

from PySide6 import QtWidgets
from PySide6.QtGui import Qt, QAction, QCursor
from PySide6.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView, QMenu

from interface.ui_local_all import Ui_LocalAll
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from task.task_local import LocalData
from tools.book import BookMgr
from tools.str import Str
from view.download.download_all_item import DownloadAllItem


class LocalReadAllView(QtWidgets.QWidget, Ui_LocalAll, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LocalAll.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.task = {}
        self.waitTask = []

        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)
        self.tableWidget.setColumnWidth(1, 300)
        # self.tableWidget.installEventFilter(self)
        self.selectAllButton.clicked.connect(self.SelectAll)
        self.downButton.clicked.connect(self.StartDel)
        self.isAll = False

    @property
    def bookInfos(self):
        return QtOwner().localReadView.allBookInfos

    def SelectAll(self):
        self.isAll = not self.isAll

        rowCont = self.tableWidget.rowCount()
        for i in range(0, rowCont):
            item = QTableWidgetItem()
            if self.isAll:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.tableWidget.setItem(i, 0, item)
        return

    def StartDel(self):
        QtOwner().ShowLoading()
        rowCont = self.tableWidget.rowCount()
        delBookIds = []
        for i in range(0, rowCont):
            item = self.tableWidget.item(i, 0)
            check = item.checkState()
            id = self.tableWidget.item(i, 6).text()
            if check == Qt.Checked:
                delBookIds.append(id)
        QtOwner().localReadView.DelLocalReadAll(delBookIds)
        self.InitBooks()
        QtOwner().CloseLoading()
        return

    def SwitchCurrent(self, **kwargs):
        self.InitBooks()

    def InitBooks(self):
        # self.tableWidget.clear()
        for i in range(self.tableWidget.rowCount(), 0, -1):
            self.tableWidget.removeRow(i-1)

        for task in self.bookInfos.values():
            rowCont = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCont)
            self.UpdateTableItem(rowCont, task)

    def UpdateTableItem(self, row, info):
        assert isinstance(info, LocalData)

        item = QTableWidgetItem()
        item.setCheckState(Qt.Unchecked)
        self.tableWidget.setItem(row, 0, item)

        item = QTableWidgetItem(str(info.sumPicCnt))
        self.tableWidget.setItem(row, 3, item)

        item = QTableWidgetItem(info.category)
        self.tableWidget.setItem(row, 2, item)

        item = QTableWidgetItem(info.title)
        self.tableWidget.setItem(row, 1, item)

        localTime = time.localtime(info.addTime)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        item = QTableWidgetItem(strTime)
        self.tableWidget.setItem(row, 4, item)

        localTime = time.localtime(info.lastReadTime)
        if info.lastReadTime:
            strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        else:
            strTime = ""
        item = QTableWidgetItem(strTime)
        self.tableWidget.setItem(row, 5, item)

        item = QTableWidgetItem(info.id)
        self.tableWidget.setItem(row, 6, item)
        return

    # 右键菜单
    def SelectMenu(self, pos):
        index = self.tableWidget.indexAt(pos)
        openDirAction = QAction(Str.GetStr(Str.SelectAll), self)
        openDirAction.triggered.connect(self.SelectItems)

        pauseAction = QAction(Str.GetStr(Str.NotSelectAll), self)
        pauseAction.triggered.connect(self.NotSelectItems)
        if index.isValid():
            menu = QMenu(self.tableWidget)
            menu.addAction(openDirAction)
            menu.addAction(pauseAction)
            menu.exec_(QCursor.pos())

    def UpdateCheck(self, i, check):
        item = QTableWidgetItem()
        item.setCheckState(check)
        self.tableWidget.setItem(i, 0, item)

    def SelectItems(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for i in selectRows:
            self.UpdateCheck(i, Qt.Checked)
        return

    def NotSelectItems(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for i in selectRows:
            self.UpdateCheck(i, Qt.Unchecked)
        return