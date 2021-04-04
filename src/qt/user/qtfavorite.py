from PySide2 import QtWidgets
import weakref

from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QMenu, QApplication
from PySide2.QtCore import Qt

from src.index.book import BookMgr
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

        self.bookList = QtBookList(self, self.__class__.__name__, owner)
        self.bookList.InitBook(self.LoadNextPage)
        self.gridLayout_3.addWidget(self.bookList)

        self.lineEdit.setValidator(QtIntLimit(1, 1, self))
        self.sortList = ["dd", "da"]
        self.bookList.InstallDel()

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

    def DelCallBack(self, bookIds):
        self.owner().loadingForm.show()

        self.dealCount = len(bookIds)
        for bookId in bookIds:
            self.owner().qtTask.AddHttpTask(lambda x: User().AddAndDelFavorites(bookId, x), self.DelAndFavoritesBack)
            info = BookMgr().books.get(bookId)
            if info:
                info.isFavourite = False

        pass

    def DelAndFavoritesBack(self, msg):
        self.dealCount -= 1
        if self.dealCount <= 0:
            self.owner().loadingForm.close()
            self.RefreshDataFocus()

    def LoadNextPage(self):
        self.LoadPage(self.bookList.page+1)

    def LoadPage(self, page):
        sortKey = self.sortList[self.comboBox.currentIndex()]
        self.owner().qtTask.AddHttpTask(lambda x: User().UpdateFavorites(page, sortKey, x), self.UpdatePagesBack)
        self.owner().loadingForm.show()

    def JumpPage(self):
        page = int(self.lineEdit.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.LoadPage(page)

