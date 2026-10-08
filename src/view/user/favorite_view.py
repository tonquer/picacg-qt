import json

from PySide6 import QtWidgets

from config.setting import Setting
from interface.ui_favorite import Ui_Favorite
from qt_owner import QtOwner
from server import req, User, Log
from server.book_query import BookQuery, SORT_FIELDS, FAVORITE_SORT_FIELDS
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.status import Status
from tools.str import Str
from tools.page_result import PageResult, PageRequest


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
        self.isLocal = False
        self.isLocal = Setting.IsOpenLocalFavorite.value

        self.sortIdCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.sortKeyCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.lineEdit.textChanged.connect(self.SearchTextChange)
        self.localWidget.SetState(self.isLocal)
        self.localWidget.Switch.connect(self.SwitchLocalButton)

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh or self.bookList.count() <= 0:
            self.RefreshDataFocus()

    def SearchTextChange(self, text):
        self.searchText = text
        self.bookList.clear()
        self.RefreshData()

    # def SearchTextChangeBack(self, bookList, bakKey):
    #     if bakKey == self.searchText:
    #         self.bookList.UpdatePage(1, 1)
    #         self.bookList.UpdateState()
    #         self.bookList.clear()
    #         for info in bookList:
    #             self.bookList.AddBookItemByBook(info, isShowHistory=True)
    #         self.UpdatePageNum()
    #         return

    def SwitchLocalButton(self, isLocal):
        Setting.IsOpenLocalFavorite.SetValue(isLocal)
        self.SetLocal(Setting.IsOpenLocalFavorite.value)
        if isLocal:
            self.InitFavorite()

    def SetLocal(self, isLocal):
        self.isLocal = isLocal
        self.sortCombox.setVisible(not isLocal)
        self.sortIdCombox.setVisible(isLocal)
        self.sortKeyCombox.setVisible(isLocal)
        self.widget.setVisible(isLocal)
        return

    def UpdatePageNum(self):
        # maxFovorite = len(self.allFavoriteIds)
        # self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
        self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + Str.GetStr(Str.Page))
        # self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(maxFovorite))
        self.spinBox.setMaximum(self.bookList.pages)
        self.spinBox.setValue(self.bookList.page)
        self.bookList.UpdateState()

    def InitFavorite(self):
        if not QtOwner().canUseDb:
            self.SetLocal(False)
            self.localWidget.setVisible(False)
            return
        if not Setting.IsOpenLocalFavorite.value:
            self.SetLocal(False)
            return

        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectFavorite, self.LoadAllFavoriteBack)
        return

    def LoadAllFavoriteBack(self, data):
        if not data and not QtOwner().canUseDb:
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
        if self.bookList.page >= self.bookList.pages:
            self.bookList.UpdateState()
            return
        self.RefreshData(self.bookList.page + 1)

    def LoadPage(self, page):
        if not Setting.UserId.value:
            return
        Log.Info("load favorite page:{}".format(page))
        self.SetTipText(Str.GetStr(Str.Update)+f":{page}")
        self.AddHttpTask(req.FavoritesReq(page, "da"), self.UpdatePagesBack, page)
        # QtOwner().ShowLoading()

    def SetTipText(self, str):
        self.msgLabel.setStyleSheet("background-color:transparent;color:{}".format("#d71345"))
        self.msgLabel.setText(str)

    def JumpPage(self):
        page = self.spinBox.value()
        if self.bookList.isLoadingPage or not 1 <= page <= self.bookList.pages:
            return
        self.RefreshData(page, replace=True)

    def RefreshData(self, page=1, replace=False):
        QtOwner().ShowLoading()
        if self.isLocal :
            query = self.BuildBookQuery()
            self.AddSqlTask("book", (query, PageRequest(page)), SqlServer.TaskTypeSelectBookPage,
                            self.ReceiveLocalPage, (page, self.searchText))
        else:
            sort = self.sortList[self.sortCombox.currentIndex()]
            self.AddHttpTask(req.FavoritesReq(self.bookList.page, sort), self.SearchBack, (self.bookList.page, replace))

    def BuildBookQuery(self):
        text = self.lineEdit.text()
        enabled = {"title": True, "author": True,
                   "description": True, "tags":True,
                   "categories": True, "creator": True}
        fields = tuple(field for field, selected in enabled.items() if selected)
        return BookQuery(text=text, fields=fields,
                         sort_field=FAVORITE_SORT_FIELDS[self.sortKeyCombox.currentIndex()],
                         descending=self.sortIdCombox.currentIndex() == 0, link_favorite_user=Setting.UserId.value)

    def ReceiveLocalPage(self, result, v):
        requestedPage, bakKey = v
        if bakKey == self.searchText:
            if result is None:
                self.SetPageLoading(False)
                QtOwner().CloseLoading()
                QtOwner().ShowError(Str.GetStr(Str.Error))
                return
            if result.page != requestedPage:
                self.bookList.clear()
            self.ApplyPageResult(result)

    def ApplyPageResult(self, result):
        QtOwner().CloseLoading()
        self.bookList.UpdatePage(result.page, result.pages)
        self.SetPageLoading(True)
        self.spinBox.setMaximum(result.pages)
        self.spinBox.setValue(result.page)
        self.pages.setText(self.bookList.GetPageStr())
        try:
            for item in result.items:
                self.bookList.AddBookItemByDbBook(item, isShowHistory=True)
        finally:
            self.SetPageLoading(False)

    def SetPageLoading(self, loading):
        self.bookList.UpdateState(loading)
        self.spinBox.setEnabled(not loading)
        self.jumpButton.setEnabled(not loading)

    # def SearchLocalBack(self, bookList):
    #     QtOwner().CloseLoading()
    #     for info in bookList:
    #         self.bookList.AddBookItemByBook(info, isShowHistory=True)
    #     self.UpdatePageNum()
    #     return

    def SearchBack(self, raw, pending):
        QtOwner().CloseLoading()
        try:
            st = raw.get("st")
            if st == Str.Ok:
                data = raw["data"]
                data = json.loads(data)
                info = data.get("data", {}).get("comics", {})
                result = PageResult.from_remote(info)
                if pending[1]:
                    self.bookList.clear()
                self.bookList.UpdatePage(result.page, result.pages)
                self.bookList.UpdateState(True)
                self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(result.total))
                for bookInfo in result.items:
                    self.bookList.AddBookByDict(bookInfo)
                self.UpdatePageNum()
            else:
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
        finally:
            self.bookList.UpdateState()
            self.spinBox.setEnabled(True)
            self.jumpButton.setEnabled(True)

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
            self.SetTipText(Str.GetStr(Str.FavoriteLoading) + "{}/{}".format(page, pages))
        except Exception as es:
            Log.Error(es)
            loadPage = page
            self.resetCnt -= 1
        if self.resetCnt <= 0:
            self.SetTipText(Str.GetStr(Str.Error))
            self.SetLocal(False)
        else:
            if loadPage > 0:
                self.LoadPage(loadPage)
            else:
                self.LoadPageComplete()

    def LoadPageComplete(self, isUpdate=True):
        self.SetLocal(True)
        self.SetTipText(Str.GetStr(Str.Updated))
        if isUpdate:
            delBookIds = set(self.allFavoriteIds.keys()) - self.reupdateBookIds
            for bookId in delBookIds:
                self.allFavoriteIds.pop(bookId)
                sql = "delete from favorite where id='{}' and user='{}';".format(bookId, Setting.UserId.value)
                self.AddSqlTask("book", sql, SqlServer.TaskTypeSql)