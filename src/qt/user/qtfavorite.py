import json
import time

from PySide2 import QtWidgets
import weakref

from PySide2.QtCore import QTimer

from src.index.book import BookMgr
from src.qt.user.qtfavorite_db import DbFavorite, QtFavoriteDb
from src.server import Server, req
from src.user.user import User
from src.util import Log
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

        self.bookList.InitBook(self.__class__.__name__, owner, self.LoadNextPage)

        self.sortList = ["dd", "da"]
        self.bookList.InstallDel()

        self.updateBookIds = []
        self.sortId = 1
        self.timer = QTimer(self, timeout=self.TimerOut)
        self.timer.setInterval(10)
        self.timer.start()
        self.dbMgr = QtFavoriteDb(self)
        self.reupdateBookIds = set()

    def close(self):
        self.timer.close()
        super(QtFavorite, self).close()

    def SwitchCurrent(self):
        self.RefreshDataFocus()

    def UpdatePageNum(self):
        maxFovorite = len(self.dbMgr.allFavoriteIds)
        self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
        self.pages.setText("{}/{}页".format(self.bookList.page, self.bookList.pages))
        self.nums.setText("收藏数：{}".format(maxFovorite))
        self.spinBox.setValue(self.bookList.page)
        self.spinBox.setMaximum(self.bookList.pages)
        self.bookList.UpdateState()

    def InitFavorite(self):
        self.dbMgr.LoadAllFavorite()
        self.UpdatePageNum()
        self.LoadPage(1)
        return

    def RefreshDataFocus(self):
        User().category.clear()
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        self.RefreshData()

    def DelCallBack(self, bookIds):
        self.owner().loadingForm.show()

        self.dealCount = len(bookIds)
        for bookId in bookIds:
            self.owner().qtTask.AddHttpTask(lambda x: User().AddAndDelFavorites(bookId, x), self.DelAndFavoritesBack, bookId)
            info = BookMgr().books.get(bookId)
            if info:
                info.isFavourite = False

        pass

    def DelAndFavoritesBack(self, msg, bookId):
        self.dealCount -= 1
        self.dbMgr.DelFavorite(bookId)
        if self.dealCount <= 0:
            self.owner().loadingForm.close()
            self.RefreshDataFocus()

    def AddFavorites(self, bookId):
        if bookId in self.dbMgr.allFavoriteIds:
            sortId = self.dbMgr.allFavoriteIds[bookId]
        else:
            self.dbMgr.maxSortId += 1
            sortId = self.dbMgr.maxSortId
        self._AddUpdateBookIds(sortId, bookId)

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData()

    def LoadPage(self, page):
        Log.Info("load favorite page:{}".format(page))
        self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.FavoritesReq(page, "da"), bakParam=x), self.UpdatePagesBack, page)
        # self.owner().loadingForm.show()

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self):
        sortId1 = self.comboBox.currentIndex()
        sortId2 = self.comboBox_2.currentIndex()
        bookList = self.dbMgr.Search(self.bookList.page, sortId1, sortId2)
        for info in bookList:
            self.bookList.AddBookItem(info)
        self.UpdatePageNum()

    def UpdatePagesBack(self, data, page):
        loadPage = 0
        try:
            data = json.loads(data)
            info = data.get("data", {}).get("comics", {})
            # total = info["total"]
            page = info["page"]
            pages = info["pages"]
            for bookInfo in info.get("docs", []):
                bookId = bookInfo.get("_id")
                self.reupdateBookIds.add(bookId)

                if bookId in self.dbMgr.allFavoriteIds:
                    continue
                else:
                    self.dbMgr.needUpdatefavorite.append(bookId)
            if pages > page:
                loadPage = page + 1
            self.msgLabel.setText("正在加载收藏分页{}/{}".format(page, pages))
        except Exception as es:
            Log.Error(es)
            loadPage = page
        finally:
            if loadPage > 0:
                self.LoadPage(loadPage)
            else:
                self.LoadPageComplete()

    ## 完成所有的收藏加载
    def LoadPageComplete(self):
        delBookIds = set(self.dbMgr.allFavoriteIds.keys()) - self.reupdateBookIds
        for bookId in delBookIds:
            self.dbMgr.DelFavorite(bookId)

        for bookId in self.dbMgr.needUpdatefavorite:
            if bookId in self.dbMgr.allFavoriteIds:
                sortId = self.dbMgr.allFavoriteIds[bookId]
            else:
                self.dbMgr.maxSortId += 1
                sortId = self.dbMgr.maxSortId
            self._AddUpdateBookIds(sortId, bookId)

        return

    def _AddUpdateBookIds(self, sortId, bookId):
        self.updateBookIds.append((sortId, bookId))
        if not self.timer.isActive():
            self.timer.start()
        return

    def TimerOut(self):
        if len(self.updateBookIds) <= 0:
            self.timer.stop()
            self.msgLabel.setText("更新完毕")
            return

        self.msgLabel.setText("正在更新收藏, 剩余数量 {}".format(len(self.updateBookIds)))
        (sortId, bookId) = self.updateBookIds.pop()
        self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookById(bookId, x), self.OpenBookBack, (sortId, bookId))
        pass

    def OpenBookBack(self, msg, v):
        (sortId, bookId) = v
        try:
            info = BookMgr().books.get(bookId)
            if msg == Status.Ok:
                bookInfo = DbFavorite()
                bookInfo.id = bookId
                bookInfo.lastUpdateTick = int(time.time())
                bookInfo.description = info.description.replace("'", "\"")
                bookInfo.created_at = info.created_at
                bookInfo.updated_at = info.updated_at
                if hasattr(info, "chineseTeam"):
                    bookInfo.chineseTeam = info.chineseTeam.replace("'", "\"")
                bookInfo.author = info.author.replace("'", "\"")
                bookInfo.finished = info.finished
                bookInfo.likesCount = info.likesCount
                bookInfo.pages = info.pagesCount
                bookInfo.title = info.title.replace("'", "\"")
                bookInfo.epsCount = info.epsCount
                bookInfo.tags = info.tags
                if bookInfo.tags:
                    bookInfo.tags = json.dumps(bookInfo.tags)
                bookInfo.categories = info.categories
                if bookInfo.categories:
                    bookInfo.categories = json.dumps(bookInfo.categories)
                bookInfo.path = info.thumb.get("path", "")
                bookInfo.fileServer = info.thumb.get("fileServer", "")
                bookInfo.originalName = info.thumb.get("originalName", "").replace("'", "\"")
                bookInfo.totalLikes = info.totalLikes
                bookInfo.totalViews = info.totalViews
                bookInfo.sortId = sortId
                self.dbMgr.UpdateFavorite(bookInfo)
                self.UpdatePageNum()
            elif msg == Status.UnderReviewBook:
                pass
            else:
                self._AddUpdateBookIds(sortId, bookId)
        except Exception as es:
            Log.Error(es)
            self._AddUpdateBookIds(sortId, bookId)

        # self.owner().loadingForm.close()
        # self.bookList.UpdateState()
        # if st == Status.Ok:
        #     pageNums = User().pages
        #     page = User().page
        #     self.nums.setText("收藏数：{}".format(str(User().total)))
        #     self.pages.setText("页：{}/{}".format(str(page), str(pageNums)))
        #     self.bookList.UpdatePage(page, pageNums)
        #     self.spinBox.setValue(page)
        #     self.spinBox.setMaximum(pageNums)
        #     for index, info in enumerate(User().category.get(self.bookList.page)):
        #         self.bookList.AddBookItem(info)





































