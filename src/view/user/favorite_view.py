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
        self.bookList.isFavorite = True
        self.bookList.isDelMenu = True
        self.bookList.LoadCallBack = self.LoadNextPage
        self.bookList.DelCallBack = self.DelCallBack
        self.bookList.BatchDelCallBack = self.BatchDelCallBack
        self.resetCnt = 5
        self.sortCombox.currentIndexChanged.connect(self.RefreshDataFocus)

        # self.someDownButton.clicked.connect(self.bookList.OpenBookDownloadAll)
        self.searchText = ""

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh or self.bookList.count() <= 0:
            self.RefreshDataFocus()

    # def SearchTextChangeBack(self, bookList, bakKey):
    #     if bakKey == self.searchText:
    #         self.bookList.UpdatePage(1, 1)
    #         self.bookList.UpdateState()
    #         self.bookList.clear()
    #         for info in bookList:
    #             self.bookList.AddBookItemByBook(info, isShowHistory=True)
    #         self.UpdatePageNum()
    #         return

    def UpdatePageNum(self):
        # maxFovorite = len(self.allFavoriteIds)
        # self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
        self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + Str.GetStr(Str.Page))
        # self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(maxFovorite))
        self.spinBox.setValue(self.bookList.page)
        self.spinBox.setMaximum(self.bookList.pages)
        self.bookList.UpdateState()

    def InitFavorite(self):
        # self.SetLocal(False)
        # if not QtOwner().canUseDb:
        #     self.SetLocal(False)
        #     return
        # self.AddSqlTask("book", "", SqlServer.TaskTypeSelectFavorite, self.LoadAllFavoriteBack)
        return

    # def LoadAllFavoriteBack(self, data):
    #     if not data and not QtOwner().isUseDb:
    #         return
    #     for _id, sordId in data:
    #         self.allFavoriteIds[_id] = sordId
    #     if self.allFavoriteIds:
    #         self.maxSortId = max(self.allFavoriteIds.values()) + 1
    #     self.UpdatePageNum()
    #     self.LoadPage(1)
    #     return

    # def UpdateSortId(self, bookId):
    #     self.maxSortId += 1
    #     self.allFavoriteIds[bookId] = self.maxSortId
    #     return self.maxSortId

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

    def BatchDelCallBack(self, bookIds):
        QtOwner().ShowLoading()
        for bookId in bookIds:
            self.AddHttpTask(req.FavoritesAdd(bookId), self.DelAndFavoritesBack, bookId)

    def DelAndFavoritesBack(self, raw, bookId):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            info = BookMgr().books.get(bookId)
            if info:
                info.isFavourite = False
            # if bookId in self.allFavoriteIds:
            #     self.allFavoriteIds.pop(bookId)
            self.bookList.DelBookID(bookId)
            # self.RefreshDataFocus()

    def AddFavorites(self, bookId):
        pass
        # if bookId in self.allFavoriteIds:
        #     sortId = self.allFavoriteIds[bookId]
        # else:
        #     sortId = self.UpdateSortId(bookId)

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData()

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self):
        QtOwner().ShowLoading()
        sort = self.sortList[self.sortCombox.currentIndex()]
        self.AddHttpTask(req.FavoritesReq(self.bookList.page, sort), self.SearchBack, self.bookList.page)

    # def SearchLocalBack(self, bookList):
    #     QtOwner().CloseLoading()
    #     for info in bookList:
    #         self.bookList.AddBookItemByBook(info, isShowHistory=True)
    #     self.UpdatePageNum()
    #     return

    def SearchBack(self, raw, page):
        QtOwner().CloseLoading()
        try:
            st = raw.get("st")
            if st == Str.Ok:
                data = raw["data"]
                data = json.loads(data)
                info = data.get("data", {}).get("comics", {})
                total = info["total"]
                page = info["page"]
                pages = info["pages"]
                self.bookList.UpdateState()
                self.bookList.UpdatePage(page, pages)
                self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(total))
                for bookInfo in info.get("docs", []):
                    bookId = bookInfo.get("_id")
                    self.bookList.AddBookByDict(bookInfo)
                self.UpdatePageNum()
            else:
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
