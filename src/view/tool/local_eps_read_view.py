import json
import os
from this import d

from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QAction, Qt, QDesktopServices
from PySide6.QtWidgets import QWidget, QMenu, QFileDialog
from natsort import natsorted

from interface.ui_index import Ui_Index
from interface.ui_local import Ui_Local
from interface.ui_local_eps import Ui_LocalEps
from qt_owner import QtOwner
from server import req, Log, User, Status
from task.qt_task import QtTaskBase
from task.task_local import LocalData
from tools.str import Str
from view.tool.local_read_db import LocalReadDb


class LocalEpsReadView(QWidget, Ui_LocalEps, QtTaskBase):
    ReloadHistory = Signal(int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Index.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        # self.tabWidget.setCurrentIndex(0)
        # self.toolButton.clicked.connect(self.AddBookByDir)
        # self.action3 = QAction(Str.GetStr(Str.ImportSimpleDir), self.toolMenu, triggered=self.CheckAction3)
        # self.action4 = QAction(Str.GetStr(Str.ImportChipDir), self.toolMenu, triggered=self.CheckAction4)

        self.bookList.isLocal = True
        # self.randomList.InitBook()

        # self.godList.InitBook()

        # self.magicList.InitBook()
        self.allBookInfos = {}
        self.isInit = False

        self.bookList.LoadingPicture = self.LoadingPicture
        self.bookList.ReDownloadPicture = self.LoadingPicture
        self.lastPath = ""

        self.setAcceptDrops(True)

        self.curSelectCategory = ""
        self.bookList.openMenu = True
        self.bookList.OpenDirHandler = self.OpenDirCallBack
        self.cacheBook = None

    def OpenDirCallBack(self, index):
        widget = self.bookList.indexWidget(index)
        if widget:
            info = self.allBookInfos.get(widget.id)
            if not info:
                return
            assert isinstance(info, LocalData)
            if info.isZipFile:
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(info.file)))
            else:
                QDesktopServices.openUrl(QUrl.fromLocalFile(info.file))

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        book = kwargs.get("book")
        if book:
            self.cacheBook = book
            self.InitData()
        return

    def InitData(self):
        assert isinstance(self.cacheBook, LocalData)
        self.cacheBook.eps = natsorted(self.cacheBook.eps, key=lambda a: a.title)
        return

    def LoadingPicture(self, index):
        if isinstance(index, int):
            item = self.bookList.item(index)
            widget = self.bookList.itemWidget(item)
        else:
            widget = self.bookList.indexWidget(index)
        bookId = widget.id
        if bookId not in self.allBookInfos:
            return
        v = self.allBookInfos[bookId]
        self.AddLocalTaskLoadPicture(v, -1, index, self.bookList.LoadingPictureComplete)

    def OpenLocalBook(self, bookId):
        if bookId not in self.allBookInfos:
            return
        QtOwner().OpenLocalReadView(v)
        return
