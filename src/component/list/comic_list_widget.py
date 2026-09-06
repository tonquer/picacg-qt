from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QListWidgetItem, QMenu, QApplication, QListView, QMessageBox
from unicodedata import category

from component.list.base_list_widget import BaseListWidget
from component.widget.comic_item_widget import ComicItemWidget
from config import config
from config.setting import Setting
from qt_owner import QtOwner
from server.sql_server import DbBook
from tools.book import Book
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class ComicListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        self.setFrameShape(QListView.NoFrame)  # 无边框
        self.setFlow(QListView.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(QListView.Adjust)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.itemClicked.connect(self.SelectItem)
        self.isDelMenu = False
        self.isGame = False
        self.isLocal = False
        self.isLocalEps = False
        self.isMoveMenu = False
        self.openMenu = False
        self.isLocalFavorite = False
        self.isFavorite = False
        self.isHistory = False

        self.isOpen2 = False
        self.isCanBatch = True
        self.isOpenBatch = False

    def OpenBatch(self):
        self.isOpenBatch = True
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            assert isinstance(w, ComicItemWidget)
            w.SetSelect(False)
        return

    def CloseBatch(self):
        self.isOpenBatch = False
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            assert isinstance(w, ComicItemWidget)
            w.SetSelect(None)
        return

    def BatchAll(self):
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            assert isinstance(w, ComicItemWidget)
            if w.rawBook:
                if isinstance(w.rawBook.tags, list):
                    tags = ",".join(w.rawBook.tags)
                else:
                    tags = w.rawBook.tags

                if isinstance(w.rawBook.categories, list):
                    category = ",".join(w.rawBook.categories)
                else:
                    category = w.rawBook.categories
                if QtOwner().IsInFilter(category, tags, w.rawBook.title):
                    isFilter = True
                else:
                    isFilter = False
            else:
                isFilter = False
            if not isFilter:
                w.SetSelect(True)
        return

    def GetAllSelectNum(self):
        num = 0
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            if w and w.isSelect:
                num += 1
        return num

    def SelectMenuBook(self, pos):
        index = self.indexAt(pos)
        widget = self.indexWidget(index)
        if index.isValid() and widget:
            assert isinstance(widget, ComicItemWidget)
            popMenu = QMenu(self)
            if not self.isOpenBatch:
                if not self.isLocal:
                    action = popMenu.addAction(Str.GetStr(Str.Open))
                    action.triggered.connect(partial(self.OpenBookInfoHandler, index))
                    nas = QMenu(Str.GetStr(Str.NetNas))
                    nasDict = QtOwner().owner.nasView.nasDict
                    if not nasDict:
                        action = nas.addAction(Str.GetStr(Str.CvSpace))
                        action.setEnabled(False)
                    else:
                        for k, v in nasDict.items():
                            action = nas.addAction(v.showTitle)
                            if QtOwner().nasView.IsInUpload(k, widget.id):
                                action.setEnabled(False)
                            action.triggered.connect(partial(self.NasUploadHandler, k, index))
                    popMenu.addMenu(nas)

                cover = QMenu(Str.GetStr(Str.Cover))
                action = cover.addAction(Str.GetStr(Str.LookCover))
                action.triggered.connect(partial(self.OpenPicture, index))
                action = cover.addAction(Str.GetStr(Str.ReDownloadCover))
                action.triggered.connect(partial(self.ReDownloadPicture, index))
                if config.CanWaifu2x and widget.picData:
                    if not widget.isWaifu2x:
                        action = cover.addAction(Str.GetStr(Str.Waifu2xConvert))
                        action.triggered.connect(partial(self.Waifu2xPicture, index))
                        if widget.isWaifu2xLoading or not config.CanWaifu2x:
                            action.setEnabled(False)
                    else:
                        action = cover.addAction(Str.GetStr(Str.DelWaifu2xConvert))
                        action.triggered.connect(partial(self.CancleWaifu2xPicture, index))
                popMenu.addMenu(cover)

                action = popMenu.addAction(Str.GetStr(Str.CopyTitle))
                action.triggered.connect(partial(self.CopyHandler, index))

                if not self.isLocal and not self.isGame:
                    action = popMenu.addAction(Str.GetStr(Str.Download))
                    action.triggered.connect(partial(self.DownloadHandler, index))

                if self.isDelMenu and not self.isLocalFavorite and not self.isLocal:
                    action = popMenu.addAction(Str.GetStr(Str.Delete))
                    action.triggered.connect(partial(self.DelHandler, index))
                if self.isMoveMenu and not self.isLocalFavorite and not self.isLocal:
                    action = popMenu.addAction(Str.GetStr(Str.Move))
                    action.triggered.connect(partial(self.MoveHandler, index))
                if self.openMenu:
                    action = popMenu.addAction(Str.GetStr(Str.OpenDir))
                    action.triggered.connect(partial(self.OpenDirHandler, index))

                if not self.isFavorite and not self.isLocalFavorite and not self.isLocal and not self.isGame and not self.isHistory:
                    if QtOwner().localFavoriteView.IsHave(widget.id):
                        action = popMenu.addAction(Str.GetStr(Str.DelLocalFavorite))
                        action.triggered.connect(partial(self.DelFavoriteHandler, index))
                    else:
                        action = popMenu.addAction(Str.GetStr(Str.LocalFavorite))
                        action.triggered.connect(partial(self.LocalFavoriteHandler, index))

                if self.isCanBatch and not self.isGame:
                    action = popMenu.addAction(Str.GetStr(Str.BatchModel))
                    action.triggered.connect(self.OpenBatch)
            else:
                num = self.GetAllSelectNum()
                if num > 0:
                    action = popMenu.addAction(Str.GetStr(Str.SelectAll)+ f"({num})")
                else:
                    action = popMenu.addAction(Str.GetStr(Str.SelectAll))
                action.triggered.connect(self.BatchAll)

                if not self.isLocal and not self.isGame and not self.isHistory:
                    nas = QMenu(Str.GetStr(Str.NetNas))
                    nasDict = QtOwner().owner.nasView.nasDict
                    if not nasDict:
                        action = nas.addAction(Str.GetStr(Str.CvSpace))
                        action.setEnabled(False)
                    else:
                        for k, v in nasDict.items():
                            action = nas.addAction(v.showTitle)
                            if QtOwner().nasView.IsInUpload(k, widget.id):
                                action.setEnabled(False)
                            action.triggered.connect(partial(self.BatchNasUploadHandler, k))
                    popMenu.addMenu(nas)

                    if not self.isGame and not self.isHistory:
                        action = popMenu.addAction(Str.GetStr(Str.DownloadAll))
                        action.triggered.connect(self.OpenBookDownloadAll)

                if self.isDelMenu :
                    action = popMenu.addAction(Str.GetStr(Str.BatchDelete))
                    action.triggered.connect(self.BatchDelHandler)
                if self.isMoveMenu:
                    action = popMenu.addAction(Str.GetStr(Str.BatchMove))
                    action.triggered.connect(self.BatchMoveHandler)
                if not self.isLocalFavorite and not self.isLocal and not self.isGame and not self.isHistory:
                    action = popMenu.addAction(Str.GetStr(Str.BatchLocalFavorite))
                    action.triggered.connect(self.BatchLocalFavoriteHandler)

                action = popMenu.addAction(Str.GetStr(Str.CloseBatchModel))
                action.triggered.connect(self.CloseBatch)
            popMenu.exec_(QCursor.pos())
        return

    def AddBookByDict(self, v):
        if self.isGame:
            _id = v.get("_id")
            title = v.get("title")
            categories = v.get("categories", [])
            if "thumb" in v:
                url = v.get("thumb", {}).get("fileServer")
                path = v.get("thumb", {}).get("path")
            elif "icon" in v:
                url = v.get("icon", {}).get("fileServer")
                path = v.get("icon", {}).get("path")
            else:
                url = ""
                path = ""
            categoryStr = "，".join(categories)
            likesCount = str(v.get("totalLikes", ""))
            finished = v.get("finished")
            pagesCount = v.get("pagesCount")
            isShiled = QtOwner().IsInFilter(categoryStr, "", title)
            self.AddBookItem(_id, title, categoryStr, url, path, likesCount, "", pagesCount, finished, isShiled=isShiled)
        else:
            book = Book()
            ToolUtil.ParseFromData(book, v)
            self.AddBookItemByBook(book, False)

    def AddBookByLocal(self, v, category=""):
        from task.task_local import LocalData
        assert isinstance(v, LocalData)
        index = self.count()
        widget = ComicItemWidget()
        widget.setFocusPolicy(Qt.NoFocus)
        widget.id = v.id
        title = v.title
        widget.index = index
        widget.title = v.title
        widget.picNum = v.picCnt
        widget.url = v.file
        if len(v.eps) > 0:
            fontColor = "<font color=#d5577c>{}</font>".format("(" + str(len(v.eps)) + "E)")
        else:
            fontColor = "<font color=#d5577c>{}</font>".format("(" + str(v.picCnt) + "P)")
        if v.lastReadTime:
            categories = "{} {}".format(ToolUtil.GetUpdateStrByTick(v.lastReadTime), Str.GetStr(Str.Looked))

            widget.timeLabel.setText(categories)
        else:
            widget.timeLabel.setVisible(False)
            widget.starButton.setVisible(False)

        widget.categoryLabel.setVisible(False)
        if category:
            widget.categoryLabel.setText(category)
            widget.categoryLabel.setVisible(True)

        widget.toolButton.setVisible(False)
        # widget.nameLable.setText(title)
        widget.SetTitle(title,fontColor)

        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        widget.PicLoad.connect(self.LoadingPicture)

    def AddBookItemByBook(self, v, isShowHistory=False):
        assert isinstance(v, Book)
        title = v.title
        if v.thumb:
            url = v.thumb.get("fileServer")
            path = v.thumb.get("path")
        else:
            url = ""
            path = ""
        _id = v.id
        finished = v.finished
        pagesCount = str(v.pagesCount)
        likesCount = str(v.totalLikes) if v.totalLikes else ""
        if isinstance(v.categories, list):
            categories  = "，".join(v.categories)
        elif isinstance(v.categories, str):
            categories = v.categories
        else:
            categories = ""

        updated_at = v.updated_at
        isShowToolButton = False
        if isShowHistory:
            info = QtOwner().owner.historyView.GetHistory(_id)
            if info:
                if v.epsCount-1 > info.epsId:
                    isShowToolButton = True
                categories = Str.GetStr(Str.LastLook) + str(info.epsId + 1) + Str.GetStr(Str.Chapter) + "/" + str(v.epsCount) + Str.GetStr(Str.Chapter)
        if isinstance(v.tags, list):
            tags = ",".join(v.tags)
        elif isinstance(v.tags, str):
            tags = v.tags
        else:
            tags = ""
        isShiled = QtOwner().IsInFilter(categories, tags, title)
        self.AddBookItem(_id, title, categories, url, path, likesCount, updated_at, pagesCount, finished, isShowToolButton=isShowToolButton, isShiled=isShiled, tags=tags, rawBook=v)

    def AddBookItemByDbBook(self, v, isShowHistory=False, isShowToolButton=False):
        title = v.title
        url = v.fileServer
        path = v.path
        _id = v.id
        finished = v.finished
        pagesCount = v.pages
        likesCount = str(v.likesCount) if v.likesCount else ""
        updated_at = v.updated_at
        categories = v.categories
        updated_at = v.updated_at
        if isShowHistory:
            info = QtOwner().owner.historyView.GetHistory(_id)
            if info:
                if v.epsCount-1 > info.epsId:
                    isShowToolButton = True

                categories = Str.GetStr(Str.LastLook) + str(info.epsId + 1) + Str.GetStr(Str.Chapter) + "/" + str(v.epsCount) + Str.GetStr(Str.Chapter)
        if hasattr(v, "tags") and isinstance(v.tags, list):
            tags = ",".join(v.tags)
        elif hasattr(v, "tags") and isinstance(v.tags, str):
            tags = v.tags
        else:
            tags = ""
        isShiled = QtOwner().IsInFilter(categories, tags, title)
        self.AddBookItem(_id, title, categories, url, path, likesCount, updated_at, pagesCount, finished, isShowToolButton=isShowToolButton, isShiled=isShiled, tags=tags, rawBook=v)

    def AddBookItemByHistory(self, v):
        _id = v.bookId
        title = v.name
        path = v.path
        url = v.url
        categories = "{} {}".format(ToolUtil.GetUpdateStrByTick(v.tick), Str.GetStr(Str.Looked))
        self.AddBookItem(_id, title, categories, url, path)

    def AddBookItem(self, _id, title, categoryStr="", url="", path="", likesCount="", updated_at="", pagesCount="", finished="", isShowToolButton=False, isShiled=False, tags="", rawBook=None):
        index = self.count()
        widget = ComicItemWidget(isShiled=isShiled)
        widget.setFocusPolicy(Qt.NoFocus)
        widget.id = _id
        widget.title = title
        widget.picNum = pagesCount
        widget.category = categoryStr
        widget.tags = tags
        widget.rawBook = rawBook

        widget.url = ToolUtil.GetRealUrl(url, path)
        if self.isGame:
            widget.path = ToolUtil.GetRealPath(_id, "game/cover")
        else:
            widget.path = ToolUtil.GetRealPath(_id, "cover")

        widget.index = index
        if not isShowToolButton:
            widget.toolButton.hide()
        widget.categoryLabel.setText(categoryStr)
        if updated_at:
            dayStr = ToolUtil.GetUpdateStr(updated_at)
            updateStr = dayStr + Str.GetStr(Str.Update)
            widget.timeLabel.setText(updateStr)
            widget.timeLabel.setVisible(True)
        else:
            widget.timeLabel.setVisible(False)

        if likesCount:
            widget.starButton.setText(str(likesCount))
            widget.starButton.setVisible(True)
        else:
            widget.starButton.setVisible(False)
        fontColor = ""
        if pagesCount:
            fontColor += "<font color=#d5577c>{}</font>".format("("+str(pagesCount)+"P)")
        # if finished:
        #     fontColor += "<font color=#d5577c>{}</font>".format("({})".format(Str.GetStr(Str.ComicFinished)))

        # widget.nameLable.setText(title)

        widget.SetTitle(title,fontColor)
        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        if not isShiled:
            widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        widget.PicLoad.connect(self.LoadingPicture)
        # if url and config.IsLoadingPicture:
        #     self.AddDownloadTask(url, path, completeCallBack=self.LoadingPictureComplete, backParam=index)
        #     pass

    def DelBookID(self, bookID):
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            if w.id == bookID:
                item.setHidden(True)
                break

    def LoadingPicture(self, index):
        item = self.item(index)
        widget = self.itemWidget(item)
        assert isinstance(widget, ComicItemWidget)
        self.AddDownloadTask(widget.url, widget.path, completeCallBack=self.LoadingPictureComplete, backParam=index)

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            assert isinstance(widget, ComicItemWidget)
            widget.SetPicture(data)
            if Setting.CoverIsOpenWaifu.value:
                item = self.item(index)
                indexModel = self.indexFromItem(item)
                self.Waifu2xPicture(indexModel, True)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            assert isinstance(widget, ComicItemWidget)
            widget.SetPictureErr(status)
        return

    def SelectItem(self, item):
        if not self.isOpenBatch:
            assert isinstance(item, QListWidgetItem)
            widget = self.itemWidget(item)
            assert isinstance(widget, ComicItemWidget)
            if widget.isShiled:
                QtOwner().ShowError(Str.GetStr(Str.Hidden))
                return
            if self.isGame:
                QtOwner().OpenGameInfo(widget.id)
            elif self.isLocalEps:
                QtOwner().OpenLocalEpsBook(widget.id)
            elif self.isLocal:
                QtOwner().OpenLocalBook(widget.id)
            else:
                if self.isOpen2:
                    QtOwner().OpenBookInfo2(widget.id)
                else:
                    QtOwner().OpenBookInfo(widget.id)
        else:
            assert isinstance(item, QListWidgetItem)
            widget = self.itemWidget(item)
            assert isinstance(widget, ComicItemWidget)
            widget.SwitchSelect()
        return

    def OpenBookInfoHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            if self.isOpen2:
                QtOwner().OpenBookInfo2(widget.id)
            else:
                QtOwner().OpenBookInfo(widget.id)
            return

    def OpenPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            QtOwner().OpenWaifu2xTool(widget.picData)
            return

    def ReDownloadPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            if widget.url and config.IsLoadingPicture:
                widget.SetPicture("")
                item = self.itemFromIndex(index)
                count = self.row(item)
                widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
                self.AddDownloadTask(widget.url, widget.path, completeCallBack=self.LoadingPictureComplete, backParam=count, isReload=True)
                pass

    def Waifu2xPicture(self, index, isIfSize=False):
        widget = self.indexWidget(index)
        assert isinstance(widget, ComicItemWidget)
        if widget and widget.picData:
            w, h, mat,_ = ToolUtil.GetPictureSize(widget.picData)
            if max(w, h) <= Setting.CoverMaxNum.value or not isIfSize:
                model = ToolUtil.GetModelByIndex(Setting.CoverLookModelName.value, Setting.CoverLookScale.value, mat)
                widget.isWaifu2xLoading = True
                if self.isLocal:
                    self.AddConvertTask(widget.path, widget.picData, model, self.Waifu2xPictureBack, index, noSaveCache=True)
                else:
                    self.AddConvertTask(widget.path, widget.picData, model, self.Waifu2xPictureBack, index)

    def CancleWaifu2xPicture(self, index):
        widget = self.indexWidget(index)
        assert isinstance(widget, ComicItemWidget)
        if widget.isWaifu2x and widget.picData:
            widget.SetPicture(widget.picData)

    def Waifu2xPictureBack(self, data, waifuId, index, tick):
        widget = self.indexWidget(index)
        if data and widget:
            assert isinstance(widget, ComicItemWidget)
            widget.SetWaifu2xData(data)
        return

    def CopyHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            data = widget.GetTitle() + str("\r\n")
            clipboard = QApplication.clipboard()
            data = data.strip("\r\n")
            clipboard.setText(data)
        pass

    def BatchMoveHandler(self):
        allIds = []
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            assert isinstance(w, ComicItemWidget)
            if w.isSelect and not item.isHidden():
                allIds.append(w.id)

        if allIds and hasattr(self, "BatchMoveCallBack"):
            self.BatchMoveCallBack(allIds)

    def MoveHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            self.MoveCallBack(widget.id)

    def OpenBookDownloadAll(self):
        allBooks = []
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            assert isinstance(w, ComicItemWidget)
            if w.isSelect and w.rawBook and not item.isHidden():
                allBooks.append(w.rawBook)
        QtOwner().OpenDownloadAll(allBooks)

    def BatchDelHandler(self):
        allIds = []
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            assert isinstance(w, ComicItemWidget)
            if w.isSelect and not item.isHidden():
                allIds.append(w.id)

        if allIds:
            isShow = QMessageBox.information(self, Str.GetStr(Str.BatchDelete), Str.GetStr(Str.BatchDeleteNotice),
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if isShow != QtWidgets.QMessageBox.Yes:
                return

        if allIds and hasattr(self, "BatchDelCallBack"):
            self.BatchDelCallBack(allIds)

    def DelFavoriteHandler(self, index):
        widget = self.indexWidget(index)
        if widget and widget.id:
            QtOwner().localFavoriteView.DelFavorites(widget.id)
            QtOwner().ShowMsg(Str.GetStr(Str.DelFavoriteSuc))

    def LocalFavoriteHandler(self, index):
        widget = self.indexWidget(index)
        if widget and widget.rawBook:
            QtOwner().localFavoriteView.AddFavorites(widget.rawBook)
            QtOwner().OpenLocalFavoriteFold(widget.id)

    def BatchLocalFavoriteHandler(self):
        allBooks = []
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            assert isinstance(w, ComicItemWidget)
            if w.isSelect and w.rawBook and not item.isHidden():
                allBooks.append(w.rawBook)

        if allBooks:
            allIds = []
            for book in allBooks:
                QtOwner().localFavoriteView.AddFavorites(book)
                allIds.append(book.id)
            QtOwner().OpenLocalFavoriteFold(allIds)


    def DelHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            self.DelCallBack(widget.id)

    def DelCallBack(self, cfgId):
        return

    def MoveCallBack(self, cfgId):
        return

    def DownloadHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            QtOwner().OpenEpsInfo(widget.id)
        pass

    def BatchNasUploadHandler(self, nasId):
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            assert isinstance(w, ComicItemWidget)
            if w.isSelect and w.rawBook and not item.isHidden():
                QtOwner().nasView.AddNasUploadCacheByBook(nasId, w.rawBook)
        pass

    def NasUploadHandler(self, nasId, index):
        widget = self.indexWidget(index)
        if widget and widget.rawBook:
            QtOwner().nasView.AddNasUploadCacheByBook(nasId, widget.rawBook)
        pass
    
    def OpenDirHandler(self, index):
        return

