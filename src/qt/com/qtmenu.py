from PySide2.QtGui import QCursor, Qt
from PySide2.QtWidgets import QMenu, QApplication

from src.qt.qtmain import QtOwner


class QtBookListMenu(object):
    def __init__(self):
        self.popMenu = QMenu(self.bookList)
        action = self.popMenu.addAction("打开")
        action.triggered.connect(self.OpenBookInfoHandler)
        action = self.popMenu.addAction("复制标题")
        action.triggered.connect(self.CopyHandler)
        action = self.popMenu.addAction("刪除")
        action.triggered.connect(self.DelHandler)
        action = self.popMenu.addAction("下载")
        action.triggered.connect(self.DownloadHandler)

        self.bookList.setContextMenuPolicy(Qt.CustomContextMenu)

        self.bookList.doubleClicked.connect(self.OpenBookInfo)
        self.bookList.customContextMenuRequested.connect(self.SelectMenu)

    def SelectMenu(self, pos):
        index = self.bookList.indexAt(pos)
        if index.isValid():
            self.popMenu.exec_(QCursor.pos())
        pass

    def DownloadHandler(self):
        selected = self.bookList.selectedItems()
        for item in selected:
            widget = self.bookList.itemWidget(item)
            QtOwner().owner.epsInfoForm.OpenEpsInfo(widget.GetId())
        pass

    def OpenBookInfoHandler(self):
        selected = self.bookList.selectedItems()
        for item in selected:
            widget = self.bookList.itemWidget(item)
            QtOwner().owner.bookInfoForm.OpenBook(widget.GetId())
            return

    def CopyHandler(self):
        selected = self.bookList.selectedItems()
        if not selected:
            return

        data = ''
        for item in selected:
            widget = self.bookList.itemWidget(item)
            data += widget.GetTitle() + str("\r\n")
        clipboard = QApplication.clipboard()
        data = data.strip("\r\n")
        clipboard.setText(data)
        pass

    def DelHandler(self):
        bookIds = set()
        selected = self.bookList.selectedItems()
        for item in selected:
            widget = self.bookList.itemWidget(item)
            bookIds.add(widget.GetId())
        if not bookIds:
            return
        self.DelCallBack(bookIds)

    def OpenBookInfo(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList.item(index)
        if not item:
            return
        widget = self.bookList.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        QtOwner().owner.bookInfoForm.OpenBook(bookId)
