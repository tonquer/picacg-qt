import json

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

from interface.ui_local_favorite import Ui_LocalFavorite
from qt_owner import QtOwner
from server import req, Log
from server.sql_server import SqlServer
from server.book_query import FavoriteQuery, FAVORITE_SORT_FIELDS
from task.qt_task import QtTaskBase
from tools.book import Book
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil
from tools.pagination import FAVORITE_PAGE_SIZE
from tools.page_result import PageRequest, PageResult
from view.user.local_favorite_db import LocalFavoriteDb


class LocalFavoriteView(QtWidgets.QWidget, Ui_LocalFavorite, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LocalFavorite.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)

        self.dealCount = 0
        self.dirty = False

        # self.bookList.InitBook(self.LoadNextPage)

        self.sortList = ["dd", "da"]
        # self.bookList.InstallDel()

        self.sortId = 1
        self.reupdateBookIds = set()
        self.maxSortId = 0
        self.bookList.isDelMenu = True
        self.bookList.isMoveMenu = True
        self.bookList.isCanBatch = True

        self.bookList.isLocalFavorite = True
        self.bookList.LoadCallBack = self.LoadNextPage
        self.bookList.DelCallBack = self.DelCallBack
        self.bookList.MoveCallBack = self.MoveCallBack

        self.bookList.BatchDelCallBack = self.BatchDelCallBack
        self.bookList.BatchMoveCallBack = self.BatchMoveCallBack

        self.resetCnt = 5
        self.sortIdCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.sortKeyCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.lastMoveBookIds = []
        # TODO 判断是否使用本地
        # self.widget.hide()
        self.lineEdit.textChanged.connect(self.SearchTextChange)
        self.searchText = ""
        self._snapshot = None
        self._snapshotKey = None
        self.db = LocalFavoriteDb()
        bookList = self.db.QueryFavorites(FavoriteQuery())
        self.allBookIds = set([v.id for v in bookList])
        # self.allDownButton.clicked.connect(self.OpenSomeBook)
        self.importButton.clicked.connect(self.ImportFavorite)
        self.loadPage = 1
        self.maxPage = 1
        self.loadFidNum = 0
        self.loadFid = []
        self.folderDict = self.db.LoadFold()
        self.fidBookList = self.db.LoadBookFold()
        self.folderBox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.updateEpsIds = []
        self.updateFailIds = []
        self.updateTick = 0
        self.updateEpsIndex = 0

    def GetFidByName(self, name):
        for k, v in self.folderDict.items():
            if v == name:
                return k
        return 0

    # def OpenSomeBook(self):
    #     name = self.folderBox.currentText()
    #     fid = self.GetFidByName(name)
    #     if fid > 0:
    #         books = list(self.fidBookList.get(fid, []))
    #     else:
    #         books = list(self.allBookIds)
    #     QtOwner().OpenSomeDownload(books)
    #     return

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh or self.bookList.count() <= 0:
            self.InitFolder()
            self.RefreshDataFocus()

    def ImportFavorite(self):
        isShow = QMessageBox.information(self, Str.GetStr(Str.ImportFavorite), Str.GetStr(Str.ImportFavoriteNotice), QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if isShow != QtWidgets.QMessageBox.Yes:
            return
        self.SetEnable(False)
        QtOwner().ShowLoading()
        self.loadPage = 1
        self.maxPage = 1
        self.loadFidNum = 0
        self.loadFid = []

        self.AddHttpTask(req.FavoritesReq(self.loadPage, "da"), self.ImportFavoriteBack, self.loadPage)
        return

    def ImportFavoriteBack(self, raw, v):
        page = v
        try:
            st = raw["st"]
            if st == Status.Ok:
                data = raw["data"]
                data = json.loads(data)
                info = data.get("data", {}).get("comics", {})
                total = info["total"]
                # page = info["page"]
                pages = info["pages"]
                for bookInfo in info.get("docs", []):
                    info = Book()
                    ToolUtil.ParseFromData(info, bookInfo)
                    self.AddFavoritesAndFidName(info)
                if page == 1:
                    self.maxPage = pages
                self.SetTipText(f"{Str.GetStr(Str.ImportFavorite)}:{page}/{self.maxPage}")

            else:
                QtOwner().CloseLoading()
                QtOwner().CheckShowMsg(raw)
        except Exception as es:
            Log.Error(es)
        finally:
            self.ImportNextFidFavorite()

    def ImportNextFidFavorite(self):
        if self.loadPage >= self.maxPage:
            QtOwner().CloseLoading()
            QtOwner().ShowMsg(Str.GetStr(Str.Ok))
            self.SetEnable(True)
            self.SetTipText("")
            self.RefreshData()
            return
        else:
            self.loadPage += 1
            self.AddHttpTask(req.FavoritesReq(self.loadPage, "da"), self.ImportFavoriteBack, self.loadPage)

    def SearchTextChange(self, text):
        self.searchText = text
        self.RefreshDataFocus()

    def UpdateSortAvailability(self):
        canUseDb = QtOwner().canUseDb
        for index in (3, 4):
            self.sortKeyCombox.model().item(index).setEnabled(canUseDb)
        if not canUseDb and self.sortKeyCombox.currentIndex() in (3, 4):
            blocked = self.sortKeyCombox.blockSignals(True)
            self.sortKeyCombox.setCurrentIndex(0)
            self.sortKeyCombox.blockSignals(blocked)

    def SetPageLoading(self, loading):
        self.bookList.UpdateState(loading)
        self.spinBox.setEnabled(not loading)
        self.jumpButton.setEnabled(not loading)

    def LoadBookList(self, page=None, replace=False):
        self.UpdateSortAvailability()
        page = self.bookList.page if page is None else page
        self.SetPageLoading(True)
        sortId = self.sortIdCombox.currentIndex()
        sortKey = self.sortKeyCombox.currentIndex()
        name = self.folderBox.currentText()
        fid = self.GetFidByName(name)
        criteria = FavoriteQuery(text=self.searchText, folder_id=fid,
                                 sort_field=FAVORITE_SORT_FIELDS[sortKey], descending=sortId == 0)
        key = (criteria, QtOwner().canUseDb)
        if self._snapshot is not None and key == self._snapshotKey:
            self.LoadSnapshotPage(page, replace)
            return
        books = self.db.QueryFavorites(criteria)
        # sortKey==0为收藏时间，其他只有book里才有最新的数据
        if sortKey > 0 and books and QtOwner().canUseDb:
            sql = SqlServer.GetBookMetrics([book.id for book in books])
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, self.ReceiveSortMetrics,
                            (books, key, page, replace))
            return
        self._snapshot = books
        self._snapshotKey = key
        self.LoadSnapshotPage(page, replace)

    def ReceiveSortMetrics(self, metrics, pending):
        books, key, page, replace = pending
        if not isinstance(metrics, list):
            self.SetPageLoading(False)
            QtOwner().CloseLoading()
            return
        criteria = key[0]
        field = criteria.sort_field
        values = {book.id: getattr(book, field) for book in metrics}
        known = [book for book in books if values.get(book.id) is not None]
        missing = [book for book in books if values.get(book.id) is None]
        known.sort(key=lambda book: book.id)
        known.sort(key=lambda book: values[book.id], reverse=criteria.descending)
        missing.sort(key=lambda book: book.id)
        self._snapshot = known + missing
        self._snapshotKey = key
        self.LoadSnapshotPage(page, replace)

    def LoadSnapshotPage(self, page, replace):
        request = PageRequest(page, FAVORITE_PAGE_SIZE).clamp(len(self._snapshot))
        books = self._snapshot[request.offset:request.offset + request.page_size]
        result = PageResult.from_total(books, request, len(self._snapshot))
        pending = (result, replace)
        if QtOwner().canUseDb and books:
            sql = SqlServer.GetBookByIds([book.id for book in books])
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, self.SearchLocalBack, pending)
        else:
            self.SearchLocalBack(books, pending)

    def SearchLocalBack(self, bookList, pending):
        QtOwner().CloseLoading()
        result, replace = pending
        if replace:
            self.bookList.clear()
        bookDict = {book.id: book for book in bookList} if isinstance(bookList, list) else {}
        for info in result.items:
            self.bookList.AddBookItemByDbBook(bookDict.get(info.id, info), isShowHistory=True)
        self.bookList.UpdatePage(result.page, result.pages)
        self.UpdatePageNum(result)
        self.SetPageLoading(False)
        return

    def UpdatePageNum(self, result):
        self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + Str.GetStr(Str.Page))
        self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(result.total))
        self.spinBox.setMaximum(self.bookList.pages)
        self.spinBox.setValue(self.bookList.page)
        self.bookList.UpdateState()

    def RefreshDataFocus(self):
        self._snapshot = None
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        self.RefreshData()

    def DelCallBack(self, bookId):
        self.DelFavorites(bookId)
        self.RefreshData()
        pass

    def BatchDelCallBack(self, bookIds):
        for bookId in bookIds:
            self.DelFavorites(bookId)
        self.RefreshData()
        pass

    def IsHave(self, bookId):
        return str(bookId) in self.allBookIds

    def AddFavorites(self, bookInfo):
        self.db.AddBookToDB(bookInfo)
        self.allBookIds.add(str(bookInfo.id))
        self._snapshot = None
        QtOwner().ShowMsg(Str.GetStr(Str.AddFavoriteSuc))

    def AddFavoritesAndFidName(self, bookInfo):
        self.db.AddBookToDB(bookInfo)
        self.allBookIds.add(str(bookInfo.id))
        self._snapshot = None
        # fid = self.GetFidByName(fidName)
        # self.db.AddBookFavoriteFid(str(bookInfo.baseInfo.id), fid)
        self.fidBookList = self.db.LoadBookFold()

    def DelFavorites(self, bookId):
        self.db.DelFavoriteDB(bookId)
        self.allBookIds.discard(str(bookId))
        self._snapshot = None
        self.fidBookList = self.db.LoadBookFold()

    def AddFidByName(self, name):
        if not name:
            return False
        fid = 0
        for k, v in self.folderDict.items():
            if v == name:
                fid = k
                break
        if (fid > 0):
            return False
        isSuc = self.db.AddFavoriteFid(name)
        self.folderDict = self.db.LoadFold()
        self.fidBookList = self.db.LoadBookFold()
        self.InitFolder()
        return isSuc

    def DelFidByName(self, name):
        fid = 0
        for k, v in self.folderDict.items():
            if v == name:
                fid = k
                break
        if not fid:
            return False
        isSuc = self.db.DelFavoriteFid(fid)
        self.folderDict = self.db.LoadFold()
        self.fidBookList = self.db.LoadBookFold()
        self.InitFolder()
        return isSuc

    def UpdateBookFid(self, bookList, fids):
        for bookId in bookList:
            self.db.UpdateBookFavoriteFid(bookId, fids)
        self.folderDict = self.db.LoadFold()
        self.fidBookList = self.db.LoadBookFold()
        self._snapshot = None
        return True

    def LoadNextPage(self):
        if self.bookList.page >= self.bookList.pages:
            self.SetPageLoading(False)
            return
        self.LoadBookList(self.bookList.page + 1)

    def JumpPage(self):
        page = self.spinBox.value()
        if self.bookList.isLoadingPage or not 1 <= page <= self.bookList.pages:
            return
        self.LoadBookList(page, replace=True)

    def RefreshData(self):
        QtOwner().ShowLoading()
        self.LoadBookList(replace=True)

    def InitFolder(self):
        self.ClearFolder()
        items = list(self.folderDict.values())
        self.folderBox.addItems(items)
        return

    def ClearFolder(self):
        self.folderBox.currentIndexChanged.disconnect()
        self.folderBox.clear()
        self.folderBox.addItem(Str.GetStr(Str.All))
        self.folderBox.setCurrentIndex(0)
        self.folderBox.currentIndexChanged.connect(self.RefreshDataFocus)
        return

    def MoveCallBack(self, bookId):
        self.lastMoveBookIds = [bookId]
        QtOwner().OpenLocalFavoriteFold(bookId, self.MoveOkBack, self.FoldChangeBack)
        return

    def BatchMoveCallBack(self, bookIds):
        self.lastMoveBookIds = bookIds[:]
        QtOwner().OpenLocalFavoriteFold(bookIds, self.MoveOkBack, self.FoldChangeBack)
        return

    def MoveOkBack(self):
        ## 如果检查移动的不在,则hidden book
        # self.RefreshDataFocus()
        self._snapshot = None
        self.RefreshData()
        QtOwner().ShowMsg(Str.GetStr(Str.Ok))
        return

    def FoldChangeBack(self):
        # self.RefreshDataFocus()
        return

    def SetTipText(self, str):
        self.tipText.setStyleSheet("background-color:transparent;color:{}".format("#d71345"))
        self.tipText.setText(str)

    def SetEnable(self, enable):
        self.importButton.setEnabled(enable)
        # self.allDownButton.setEnabled(enable)
        self.sortIdCombox.setEnabled(enable)
        self.sortKeyCombox.setEnabled(enable)
        self.folderBox.setEnabled(enable)


