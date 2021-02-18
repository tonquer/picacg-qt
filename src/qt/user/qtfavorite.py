from PyQt5 import QtWidgets
import weakref

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QApplication
from PyQt5.QtCore import Qt

from src.qt.com.qtlistwidget import QtBookList, QtIntLimit
from src.user.user import User
from src.util.status import Status
from ui.favorite import Ui_favorite


class QtFavorite(QtWidgets.QWidget, Ui_favorite):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_favorite.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)

        self.dealCount = 0
        self.dirty = False

        self.bookList = QtBookList(self, self.__class__.__name__)
        self.bookList.InitBook(self.LoadNextPage)
        self.gridLayout_3.addWidget(self.bookList)
        self.bookList.doubleClicked.connect(self.OpenBookInfo)
        self.bookList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bookList.customContextMenuRequested.connect(self.SelectMenu)

        self.popMenu = QMenu(self.bookList)
        action = self.popMenu.addAction("打开")
        action.triggered.connect(self.OpenBookInfoHandler)
        action = self.popMenu.addAction("复制")
        action.triggered.connect(self.CopyHandler)
        action = self.popMenu.addAction("刪除")
        action.triggered.connect(self.DelHandler)
        action = self.popMenu.addAction("下载")
        action.triggered.connect(self.DownloadHandler)

        self.lineEdit.setValidator(QtIntLimit(1, 1, self))

    def SwitchCurrent(self):
        self.RefreshDataFocus()

    def RefreshDataFocus(self):
        User().category.clear()
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self):
        if not User().category.get(self.bookList.page):
            self.LoadPage(self.bookList.page)
        else:
            self.UpdatePagesBack(Status.Ok)

    def UpdatePagesBack(self, st):
        self.owner().loadingForm.close()
        self.bookList.UpdateState()
        if st == Status.Ok:
            pageNums = User().pages
            page = User().page
            self.nums.setText("收藏数：{}".format(str(User().total)))
            self.pages.setText("页：{}/{}".format(str(page), str(pageNums)))
            self.bookList.UpdatePage(page, pageNums)
            self.lineEdit.setValidator(QtIntLimit(1, pageNums, self))
            for index, info in enumerate(User().category.get(self.bookList.page)):
                url = info.thumb.get("fileServer")
                path = info.thumb.get("path")
                originalName = info.thumb.get("originalName")
                data = "完本," if info.finished else ""
                data += "{}E/{}P".format(str(info.epsCount), str(info.pagesCount))
                self.bookList.AddBookItem(info.id, info.title, data, url, path, originalName)

    def SelectMenu(self, pos):
        index = self.bookList.indexAt(pos)
        if index.isValid():
            self.popMenu.exec_(QCursor.pos())
        pass

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
        self.DelAndFavorites(bookIds)

    def DelAndFavorites(self, bookIds):
        self.owner().loadingForm.show()

        self.dealCount = len(bookIds)
        for bookId in bookIds:
            self.owner().qtTask.AddHttpTask(lambda x: User().AddAndDelFavorites(bookId, x), self.DelAndFavoritesBack)
        pass

    def DelAndFavoritesBack(self, msg):
        self.dealCount -= 1
        if self.dealCount <= 0:
            self.owner().loadingForm.close()
            self.RefreshDataFocus()

    def DownloadHandler(self):
        selected = self.bookList.selectedItems()
        for item in selected:
            widget = self.bookList.itemWidget(item)
            self.owner().epsInfoForm.OpenEpsInfo(widget.GetId())
        pass

    def OpenBookInfoHandler(self):
        selected = self.bookList.selectedItems()
        for item in selected:
            widget = self.bookList.itemWidget(item)
            self.owner().bookInfoForm.OpenBook(widget.GetId())
            return

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
        self.owner().bookInfoForm.OpenBook(bookId)

    def LoadNextPage(self):
        self.LoadPage(self.bookList.page+1)

    def LoadPage(self, page):
        self.owner().qtTask.AddHttpTask(lambda x: User().UpdateFavorites(page, x), self.UpdatePagesBack)
        self.owner().loadingForm.show()

    def JumpPage(self):
        page = int(self.lineEdit.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.LoadPage(page)

