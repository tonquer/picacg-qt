import json
import time

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

from config.setting import Setting
from interface.ui_local_favorite import Ui_LocalFavorite
from qt_owner import QtOwner
from server import req, Log, config
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr, Book
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil
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
        self.db = LocalFavoriteDb()
        bookList = self.db.SearchFavorite(-1, 0, 0, 0, "")
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
        self.bookList.clear()
        self.LoadBookList()

    def LoadBookList(self):
        sortId = self.sortIdCombox.currentIndex()
        sortKey = self.sortKeyCombox.currentIndex()
        name = self.folderBox.currentText()
        fid = self.GetFidByName(name)
        bookList = self.db.SearchFavorite(self.bookList.page, sortKey, sortId, fid, self.searchText)
        page = self.bookList.page
        if QtOwner().canUseDb:
            bookIds = [v.id for v in bookList]
            sql, _, _ = SqlServer.Search2(
                self.searchText, True, True, True, True, False,
                True, [], -1, sortKey - 1, sortId, False, bookIds)
            
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, callBack=self.SearchLocalBack, backParam=bookList)
        else:
            self.SearchLocalBack(bookList, bookList)

    def SearchLocalBack(self, bookList, oldBookList):
        QtOwner().CloseLoading()
        sortKey = self.sortKeyCombox.currentIndex()
        self.bookList.UpdateState()
        ## 如果sortKey == 0, 按oldBookList排序，否则按bookList排序
        if sortKey == 0:
            bookDict = {}
            for v in bookList:
                bookDict[v.id] = v
            for info in oldBookList:
                info2 = bookDict.get(info.id)
                if info2:
                    self.bookList.AddBookItemByDbBook(info2, isShowHistory=True)
                else:
                    self.bookList.AddBookItemByDbBook(info, isShowHistory=True)
        else:
            for info in bookList:
                self.bookList.AddBookItemByDbBook(info, isShowHistory=True)
        self.UpdatePageNum()
        return

    def UpdatePageNum(self):
        maxFovorite = len(self.allBookIds)
        self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
        self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + Str.GetStr(Str.Page))
        self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(maxFovorite))
        self.spinBox.setValue(self.bookList.page)
        self.spinBox.setMaximum(self.bookList.pages)
        self.bookList.UpdateState()

    def RefreshDataFocus(self):
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        self.RefreshData()

    def DelCallBack(self, bookId):
        self.DelFavorites(bookId)
        self.bookList.DelBookID(bookId)
        # self.RefreshDataFocus()
        pass

    def BatchDelCallBack(self, bookIds):
        for bookId in bookIds:
            self.DelFavorites(bookId)
            self.bookList.DelBookID(bookId)
        # self.RefreshDataFocus()
        pass

    def IsHave(self, bookId):
        return str(bookId) in self.allBookIds

    def AddFavorites(self, bookInfo):
        self.db.AddBookToDB(bookInfo)
        self.allBookIds.add(str(bookInfo.id))
        QtOwner().ShowMsg(Str.GetStr(Str.AddFavoriteSuc))

    def AddFavoritesAndFidName(self, bookInfo):
        self.db.AddBookToDB(bookInfo)
        self.allBookIds.add(str(bookInfo.id))
        # fid = self.GetFidByName(fidName)
        # self.db.AddBookFavoriteFid(str(bookInfo.baseInfo.id), fid)
        self.fidBookList = self.db.LoadBookFold()

    def DelFavorites(self, bookId):
        self.db.DelFavoriteDB(bookId)
        self.allBookIds.discard(str(bookId))
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
        return True

    def LoadNextPage(self):
        self.bookList.page += 1
        self.LoadBookList()

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self):
        QtOwner().ShowLoading()
        self.SearchTextChange(self.searchText)

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
        bookIds = self.lastMoveBookIds
        name = self.folderBox.currentText()
        fid = self.GetFidByName(name)

        for bookId in bookIds:
            if fid > 0:
                isHave = bookId in self.fidBookList.get(fid, [])
                if not isHave:
                    self.bookList.DelBookID(bookId)
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


