import json

from PySide6 import QtWidgets

from interface.ui_favorite import Ui_Favorite
from qt_owner import QtOwner
from server import req, User, Log
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.status import Status
from tools.str import Str


class FavoriteView(QtWidgets.QWidget, Ui_Favorite, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Favorite.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)

        self.dealCount = 0
        self.dirty = False

        # self.bookList.InitBook(self.LoadNextPage)

        self.sortList = ["dd", "da"]
        # self.bookList.InstallDel()

        self.sortId = 1
        self.reupdateBookIds = set()
        self.allFavoriteIds = dict()
        self.maxSortId = 0
        self.bookList.isDelMenu = True
        self.bookList.DelCallBack = self.DelCallBack
        self.resetCnt = 5

    def close(self):
        self.timer.close()
        super(self.__class__, self).close()

    def SwitchCurrent(self, **kwargs):
        self.RefreshDataFocus()

    def UpdatePageNum(self):
        maxFovorite = len(self.allFavoriteIds)
        self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
        self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + Str.GetStr(Str.Page))
        self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(maxFovorite))
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

    def DelCallBack(self, bookId):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.FavoritesAdd(bookId), self.DelAndFavoritesBack, bookId)
        pass

    def DelAndFavoritesBack(self, raw, bookId):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            info = BookMgr().books.get(bookId)
            if info:
                info.isFavourite = False
            sql = "delete from favorite where id='{}' and user='{}';".format(bookId, User().userId)
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSql)
            if bookId in self.allFavoriteIds:
                self.allFavoriteIds.pop(bookId)
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
        # QtOwner().ShowLoading()

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self):
        QtOwner().ShowLoading()
        sortId1 = self.comboBox.currentIndex()
        sortId2 = self.comboBox_2.currentIndex()
        sql = SqlServer.SearchFavorite(self.bookList.page, sortId1, sortId2)
        self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, self.SeachBack)

    def SeachBack(self, bookList):
        QtOwner().CloseLoading()
        for info in bookList:
            self.bookList.AddBookItemByBook(info, isShowHistory=True)
        self.UpdatePageNum()
        return

    def UpdatePagesBack(self, raw, page):
        loadPage = 0
        try:
            data = raw["data"]
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
            self.msgLabel.setText(Str.GetStr(Str.FavoriteLoading) + "{}/{}".format(page, pages))
        except Exception as es:
            Log.Error(es)
            loadPage = page
            self.resetCnt -= 1
        finally:
            if self.resetCnt <= 0:
                self.msgLabel.setText(Str.GetStr(Str.Error))
            else:
                if loadPage > 0:
                    self.LoadPage(loadPage)
                else:
                    self.LoadPageComplete()

    def LoadPageComplete(self):
        self.msgLabel.setText(Str.GetStr(Str.Updated))
        delBookIds = set(self.allFavoriteIds.keys()) - self.reupdateBookIds
        for bookId in delBookIds:
            self.allFavoriteIds.pop(bookId)
            sql = "delete from favorite where id='{}' and user='{}';".format(bookId, User().userId)
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSql)
