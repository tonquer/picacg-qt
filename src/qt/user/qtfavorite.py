import json
import time

from PySide2 import QtWidgets
from PySide2.QtCore import QTimer

from src.index.book import BookMgr
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req
from src.server.sql_server import SqlServer
from src.user.user import User
from src.util import Log
from src.util.tool import time_me
from ui.favorite import Ui_favorite


class QtFavorite(QtWidgets.QWidget, Ui_favorite, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_favorite.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)

        self.dealCount = 0
        self.dirty = False

        self.bookList.InitBook(self.LoadNextPage)

        self.sortList = ["dd", "da"]
        self.bookList.InstallDel()

        self.sortId = 1
        self.reupdateBookIds = set()
        self.allFavoriteIds = dict()
        self.maxSortId = 0

    def close(self):
        self.timer.close()
        super(QtFavorite, self).close()

    def SwitchCurrent(self):
        self.RefreshDataFocus()

    def UpdatePageNum(self):
        maxFovorite = len(self.allFavoriteIds)
        self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
        self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + self.tr("页"))
        self.nums.setText(self.tr("收藏数：") + "{}".format(maxFovorite))
        self.spinBox.setValue(self.bookList.page)
        self.spinBox.setMaximum(self.bookList.pages)
        self.bookList.UpdateState()

    def InitFavorite(self):
        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectFavorite, self.LoadAllFavoriteBack)
        return

    def LoadAllFavoriteBack(self, data):
        for _id in data:
            self.allFavoriteIds[_id] = 0
        self.UpdatePageNum()
        self.LoadPage(1)
        return

    def UpdateSortId(self, bookId):
        self.maxSortId += 1
        self.allFavoriteIds[bookId] = self.maxSortId
        return self.maxSortId

    def RefreshDataFocus(self):
        User().category.clear()
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        self.RefreshData()

    def DelCallBack(self, bookIds):
        QtOwner().owner.loadingForm.show()

        self.dealCount = len(bookIds)
        for bookId in bookIds:
            self.AddHttpTask(req.FavoritesAdd(bookId), self.DelAndFavoritesBack, bookId)
            info = BookMgr().books.get(bookId)
            if info:
                info.isFavourite = False

        pass

    def DelAndFavoritesBack(self, msg, bookId):
        self.dealCount -= 1
        sql = "delete from favorite where id='{}' and user='{}';".format(bookId, User().userId)
        self.AddSqlTask("book", sql, SqlServer.TaskTypeSql)
        if bookId in self.allFavoriteIds:
            self.allFavoriteIds.pop(bookId)
        if self.dealCount <= 0:
            QtOwner().owner.loadingForm.close()
            self.RefreshDataFocus()

    def AddFavorites(self, bookId):
        if bookId in self.allFavoriteIds:
            sortId = self.allFavoriteIds[bookId]
        else:
            sortId = self.UpdateSortId(bookId)
        self.AddSqlTask("book", [(bookId, sortId)], SqlServer.TaskTypeUpdateFavorite)

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData()

    def LoadPage(self, page):
        Log.Info("load favorite page:{}".format(page))
        self.AddHttpTask(req.FavoritesReq(page, "da"), self.UpdatePagesBack, page)
        # QtOwner().owner.loadingForm.show()

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self):
        QtOwner().owner.loadingForm.show()
        sortId1 = self.comboBox.currentIndex()
        sortId2 = self.comboBox_2.currentIndex()
        sql = SqlServer.SearchFavorite(self.bookList.page, sortId1, sortId2)
        self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, self.SeachBack)

    def SeachBack(self, bookList):
        QtOwner().owner.loadingForm.close()
        for info in bookList:
            self.bookList.AddBookItem(info, isShowHistory=True)
        self.UpdatePageNum()
        return

    def UpdatePagesBack(self, data, page):
        loadPage = 0
        try:
            data = json.loads(data)
            info = data.get("data", {}).get("comics", {})
            # total = info["total"]
            page = info["page"]
            pages = info["pages"]
            bookIds = []
            for bookInfo in info.get("docs", []):
                bookId = bookInfo.get("_id")
                self.reupdateBookIds.add(bookId)
                sortId = self.UpdateSortId(bookId)
                bookIds.append((bookId, sortId))
            self.AddSqlTask("book", bookIds, SqlServer.TaskTypeUpdateFavorite)
            if pages > page:
                loadPage = page + 1
            self.msgLabel.setText(self.tr("正在加载收藏分页") + "{}/{}".format(page, pages))
        except Exception as es:
            Log.Error(es)
            loadPage = page
        finally:
            if loadPage > 0:
                self.LoadPage(loadPage)
            else:
                self.LoadPageComplete()

    ## 完成所有的收藏加载
    @time_me
    def LoadPageComplete(self):
        self.msgLabel.setText(self.tr("更新完毕"))
        delBookIds = set(self.allFavoriteIds.keys()) - self.reupdateBookIds
        for bookId in delBookIds:
            self.allFavoriteIds.pop(bookId)
            sql = "delete from favorite where id='{}' and user='{}';".format(bookId, User().userId)
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSql)
















