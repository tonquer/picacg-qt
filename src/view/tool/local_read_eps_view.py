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
from task.qt_task import QtTaskBase
from task.task_local import LocalData
from tools.str import Str
from view.tool.local_read_db import LocalReadDb


class LocalReadEpsView(QWidget, Ui_LocalEps, QtTaskBase):
    ReloadHistory = Signal(int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Index.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.bookId = ""
        self.cacheBook = None
        self.bookIdToIndex = {}
        self.bookList.isLocal = True
        self.bookList.isLocalEps = True
        self.bookList.LoadingPicture = self.LoadingPicture
        self.bookList.ReDownloadPicture = self.LoadingPicture
        self.showWaifu2x.clicked.connect(self.Init)

    @property
    def localReadView(self):
        return QtOwner().localReadView

    def Init(self):
        book = self.localReadView.allBookInfos.get(self.bookId)
        if not book:
            return
        self.name.setText(book.title)
        self.bookIdToIndex.clear()
        self.cacheBook = book
        assert isinstance(book, LocalData)
        self.bookList.clear()
        for i, v in enumerate(book.eps):
            assert isinstance(v, LocalData)
            self.bookIdToIndex[v.id] = i
            categroup = []
            if v.isWaifu2x:
                categroup.append("waifu2x")
            else:
                if self.showWaifu2x.isChecked():
                    continue

            if v.isZipFile:
                categroup.append("zip")
            self.bookList.AddBookByLocal(v, "".join(categroup))
        pass

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        if not bookId:
            return
        # if bookId == self.bookId:
        #     return
        self.bookId = bookId
        self.Init()
        return

    def LoadingPicture(self, index):
        if isinstance(index, int):
            item = self.bookList.item(index)
            widget = self.bookList.itemWidget(item)
        else:
            widget = self.bookList.indexWidget(index)

        bookId = widget.id
        if bookId not in self.bookIdToIndex:
            return
        i = self.bookIdToIndex.get(bookId)
        v = self.cacheBook.eps[i]
        self.AddLocalTaskLoadPicture(v, -1, index, self.bookList.LoadingPictureComplete)

    def OpenLocalBook(self, bookId):
        if bookId not in self.bookIdToIndex:
            return
        newV = LocalData()
        newV.id = self.cacheBook.id
        newV.CopyData(self.cacheBook)
        newV.eps = []
        eps = 0
        i = 0
        for v in self.cacheBook.eps:
            assert isinstance(v, LocalData)
            if v.id == bookId:
                eps = i
            if not v.isWaifu2x:
                if self.showWaifu2x.isChecked():
                    continue
            i += 1
            newV.eps.append(v)
        QtOwner().OpenLocalReadView(newV, eps)
