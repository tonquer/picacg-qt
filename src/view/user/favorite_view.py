import json

from PySide6 import QtWidgets

from config.setting import Setting
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
        self.bookList.LoadCallBack = self.LoadNextPage
        self.bookList.DelCallBack = self.DelCallBack
        self.resetCnt = 5
        self.sortIdCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.sortCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.sortKeyCombox.currentIndexChanged.connect(self.RefreshDataFocus)

        # TODO 判断是否使用本地
        self.isLocal = False
        self.SetLocal(False)
        self.someDownButton.clicked.connect(self.bookList.OpenBookDownloadAll)
        self.widget.hide()
        self.lineEdit.textChanged.connect(self.SearchTextChange)
        self.searchText = ""

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh or self.bookList.count() <= 0:
            self.RefreshDataFocus()

    def SearchTextChange(self, text):
        self.searchText = text
        sortId = self.sortIdCombox.currentIndex()
        sortKey = self.sortKeyCombox.currentIndex()
        sql = SqlServer.SearchFavorite(self.bookList.page, sortKey, sortId, self.searchText)
        self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, self.SearchTextChangeBack, self.searchText)

    def SearchTextChangeBack(self, bookList, bakKey):
        if bakKey == self.searchText:
            self.bookList.UpdatePage(1, 1)
            self.bookList.UpdateState()
            self.bookList.clear()
            for info in bookList:
                self.bookList.AddBookItemByBook(info, isShowHistory=True)
            self.UpdatePageNum()
            return

    def SetLocal(self, isLocal):
        self.isLocal = isLocal
        self.sortCombox.setVisible(not isLocal)
        self.sortIdCombox.setVisible(isLocal)
        self.sortKeyCombox.setVisible(isLocal)
        self.widget.setVisible(isLocal)
        return

    def UpdatePageNum(self):
        maxFovorite = len(self.allFavoriteIds)
        self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
        self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + Str.GetStr(Str.Page))
        self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(maxFovorite))
        self.spinBox.setValue(self.bookList.page)
        self.spinBox.setMaximum(self.bookList.pages)
        self.bookList.UpdateState()

    def InitFavorite(self):
        if not QtOwner().isUseDb:
            self.SetLocal(False)
            return
        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectFavorite, self.LoadAllFavoriteBack)
        return

    def LoadAllFavoriteBack(self, data):
        if not data and not QtOwner().isUseDb:
            return
        for _id, sordId in data:
            self.allFavoriteIds[_id] = sordId
        if self.allFavoriteIds:
            self.maxSortId = max(self.allFavoriteIds.values()) + 1
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
            if self.isLocal:
                sql = "delete from favorite where id='{}' and user='{}';".format(bookId, Setting.UserId.value)
                self.AddSqlTask("book", sql, SqlServer.TaskTypeSql)
            if bookId in self.allFavoriteIds:
                self.allFavoriteIds.pop(bookId)
            self.bookList.DelBookID(bookId)
            # self.RefreshDataFocus()

    def AddFavorites(self, bookId):
        if bookId in self.allFavoriteIds:
            sortId = self.allFavoriteIds[bookId]
        else:
            sortId = self.UpdateSortId(bookId)
        if self.isLocal:
            self.AddSqlTask("book", [(bookId, sortId)], SqlServer.TaskTypeUpdateFavorite)

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData()

    def LoadPage(self, page):
        if not User().userId:
            return
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
        sortId = self.sortIdCombox.currentIndex()
        sortKey = self.sortKeyCombox.currentIndex()
        if self.isLocal or QtOwner().isOfflineModel:
            sql = SqlServer.SearchFavorite(self.bookList.page, sortKey, sortId, self.searchText)
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, self.SearchLocalBack)
        else:
            sort = self.sortList[self.sortCombox.currentIndex()]
            self.AddHttpTask(req.FavoritesReq(self.bookList.page, sort), self.SearchBack, self.bookList.page)

    def SearchLocalBack(self, bookList):
        QtOwner().CloseLoading()
        for info in bookList:
            self.bookList.AddBookItemByBook(info, isShowHistory=True)
        self.UpdatePageNum()
        return

    def SearchBack(self, raw, page):
        QtOwner().CloseLoading()
        try:
            data = raw["data"]
            data = json.loads(data)
            info = data.get("data", {}).get("comics", {})
            total = info["total"]
            page = info["page"]
            pages = info["pages"]
            self.bookList.UpdateState()
            self.bookList.UpdatePage(page, pages)
            self.spinBox.setMaximum(pages)
            self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(total))
            for bookInfo in info.get("docs", []):
                bookId = bookInfo.get("_id")
                self.bookList.AddBookByDict(bookInfo)
        except Exception as es:
            Log.Error(es)

    def UpdatePagesBack(self, raw, page):
        loadPage = 0
        try:
            data = raw["data"]
            data = json.loads(data)
            info = data.get("data", {}).get("comics", {})
            total = info["total"]
            page = info["page"]
            pages = info["pages"]
            bookIds = []

            # 判断一下 如果数量相等，并且这一页的数据全有，则不再做更新数据
            isContinue = False
            updateDict = {}
            maxSortId = self.maxSortId
            for bookInfo in info.get("docs", []):
                bookId = bookInfo.get("_id")
                self.reupdateBookIds.add(bookId)
                maxSortId += 1
                updateDict[bookId] = maxSortId
                bookIds.append((bookId, maxSortId))
                if bookId not in self.allFavoriteIds:
                    isContinue = True

            #
            if page == 1 and isContinue == False and len(self.allFavoriteIds) == total:
                self.LoadPageComplete(False)
                return
            self.maxSortId = maxSortId
            self.allFavoriteIds.update(updateDict)
            self.AddSqlTask("book", bookIds, SqlServer.TaskTypeUpdateFavorite)
            if pages > page:
                loadPage = page + 1
            self.msgLabel.setText(Str.GetStr(Str.FavoriteLoading) + "{}/{}".format(page, pages))
        except Exception as es:
            Log.Error(es)
            loadPage = page
            self.resetCnt -= 1
        if self.resetCnt <= 0:
            self.msgLabel.setText(Str.GetStr(Str.Error))
            self.SetLocal(False)
        else:
            if loadPage > 0:
                self.LoadPage(loadPage)
            else:
                self.LoadPageComplete()

    def LoadPageComplete(self, isUpdate=True):
        self.SetLocal(True)
        self.msgLabel.setText(Str.GetStr(Str.Updated))
        if isUpdate:
            delBookIds = set(self.allFavoriteIds.keys()) - self.reupdateBookIds
            for bookId in delBookIds:
                self.allFavoriteIds.pop(bookId)
                sql = "delete from favorite where id='{}' and user='{}';".format(bookId, Setting.UserId.value)
                self.AddSqlTask("book", sql, SqlServer.TaskTypeSql)
