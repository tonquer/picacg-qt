import json
import os
import shutil
from functools import partial

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QSize, QEvent, Signal
from PySide6.QtGui import QColor, QFont, QPixmap, QIcon, QCursor
from PySide6.QtWidgets import QListWidgetItem, QLabel, QApplication, QScroller, QPushButton, QButtonGroup, QMessageBox, \
    QListView, QWidget, QMenu

from component.layout.flow_layout import FlowLayout
from config.setting import Setting
from interface.ui_book_info import Ui_BookInfo
from interface.ui_book_right import Ui_BookRight
from qt_owner import QtOwner
from server import req, ToolUtil, config, Status, Log
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr, Book, BookEps
from tools.str import Str


class BookInfoView(QtWidgets.QWidget, Ui_BookInfo, QtTaskBase):
    ReloadHistory = Signal()

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.lastIndex = 0
        self.pictureData = None
        self.isFavorite = False
        self.isLike = False
        self.picture.installEventFilter(self)

        self.starButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.starButton.setIconSize(QSize(50, 50))
        self.downloadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.downloadButton.setIconSize(QSize(50, 50))
        self.favoriteButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.favoriteButton.setIconSize(QSize(50, 50))
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commentButton.setIconSize(QSize(50, 50))

        # self.tagsList.clicked.connect(self.ClickTagsItem)
        # self.tagsList.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tagsList.customContextMenuRequested.connect(self.CopyClickTagsItem)

        self.epsListWidget.setFlow(QListView.LeftToRight)
        self.epsListWidget.setWrapping(True)
        self.epsListWidget.setFrameShape(QListView.NoFrame)
        self.epsListWidget.setResizeMode(QListView.Adjust)

        self.epsListWidget.clicked.connect(self.OpenReadImg)

        self.listWidget.setFlow(QListView.LeftToRight)
        self.listWidget.setWrapping(True)
        self.listWidget.setFrameShape(QListView.NoFrame)
        self.listWidget.setResizeMode(QListView.Adjust)

        self.listWidget.clicked.connect(self.OpenReadImg2)

        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.epsListWidget, QScroller.LeftMouseButtonGesture)
        # self.epsListWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.epsListWidget.verticalScrollBar().setStyleSheet(QssDataMgr().GetData('qt_list_scrollbar'))
        # self.epsListWidget.verticalScrollBar().setSingleStep(30)
        self.user_name.setCursor(Qt.PointingHandCursor)
        self.user_icon.setCursor(Qt.PointingHandCursor)
        self.user_name.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.user_icon.radius = 50
        self.userIconData = None
        self.user_name.installEventFilter(self)
        self.user_icon.installEventFilter(self)

        self.commentButton.clicked.connect(self.OpenComment)
        # self.epsListWidget.verticalScrollBar().rangeChanged.connect(self.ChageMaxNum)
        self.epsListWidget.setMinimumHeight(300)

        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.autorList.clicked.connect(self.ClickAutorItem)
        self.autorList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.autorList.customContextMenuRequested.connect(self.CopyClickAutorItem)

        self.idLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.description.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.description.adjustSize()
        self.title.adjustSize()

        self.categoriesList.clicked.connect(self.ClickCategoriesItem)
        self.categoriesList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.categoriesList.customContextMenuRequested.connect(self.CopyClickCategoriesItem)

        self.ReloadHistory.connect(self.LoadHistory)

        self.pageBox.currentIndexChanged.connect(self.UpdateEpsPageData)
        self.tabWidget.currentChanged.connect(self.SwitchPage)
        self.commandLinkButton.clicked.connect(self.OpenRecommend)
        self.readOffline.clicked.connect(self.StartRead2)
        self.flowLayout = FlowLayout(self.tagList)
        self.uploadButton.clicked.connect(self.ShowMenu)

    def UpdateFavoriteIcon(self):
        p = QPixmap()
        if self.isFavorite:
            self.favoriteButton.setIcon(QIcon(":/png/icon/icon_like.png"))
        else:
            self.favoriteButton.setIcon(QIcon(":/png/icon/icon_like_off.png"))

        path = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), "book/{}".format(self.bookId))
        waifuPath = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), "waifu2x/book/{}".format(self.bookId))
        if os.path.isdir(path) or os.path.isdir(waifuPath):
            self.clearButton.setIcon(QIcon(":/png/icon/clear_on.png"))
        else:
            self.clearButton.setIcon(QIcon(":/png/icon/clear_off.png"))

    def UpdateLikeIcon(self):
        p = QPixmap()
        if not self.isLike:
            self.starButton.setIcon(QIcon(":/png/icon/icon_bookmark_off.png"))
        else:
            self.starButton.setIcon(QIcon(":/png/icon/icon_bookmark_on.png"))

    def Clear(self):
        self.ClearTask()
        self.epsListWidget.clear()

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        if bookId:
            self.OpenBook(bookId)

        pass

    def OpenBook(self, bookId):
        self.bookId = bookId
        if QtOwner().isOfflineModel:
            self.tabWidget.setCurrentIndex(1)
        else:
            self.tabWidget.setCurrentIndex(0)
        self.setFocus()
        self.Clear()
        self.show()
        QtOwner().ShowLoading()
        self.OpenLocalBack()

    def OpenRecommend(self):
        QtOwner().OpenRecomment(self.bookId)

    def SwitchPage(self, page):
        pass

    def OpenComment(self):
        if self.bookId:
            QtOwner().OpenComment(self.bookId)

    def OpenLocalBack(self):
        self.AddSqlTask("book", self.bookId, SqlServer.TaskTypeCacheBook, callBack=self.SendLocalBack)

    def SendLocalBack(self, books):
        if not QtOwner().isOfflineModel:
            self.AddHttpTask(req.GetComicsBookReq(self.bookId), self.OpenBookBack)
        else:
            self.OpenBookBack({"st": Status.Ok})
        self.UpdateDownloadEps()
        self.LoadHistory()

    def UpdateDownloadEps(self):
        info = QtOwner().downloadView.GetDownloadInfo(self.bookId)
        self.listWidget.clear()
        if info:
            from view.download.download_item import DownloadItem
            from view.download.download_item import DownloadEpsItem
            assert isinstance(info, DownloadItem)
            # downloadIds = QtOwner().owner.downloadForm.GetDownloadCompleteEpsId(self.bookId)
            maxEpsId = max(info.epsIds)
            for i in range(0, maxEpsId+1):
                epsInfo = info.epsInfo.get(i)

                item = QListWidgetItem(self.listWidget)
                if not epsInfo:
                    label = QLabel(str(i + 1) + "-" + "未下载")
                    item.setToolTip("未下载")
                else:
                    assert isinstance(epsInfo, DownloadEpsItem)
                    label = QLabel(str(i + 1) + "-" + epsInfo.epsTitle)
                    item.setToolTip(epsInfo.epsTitle)

                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("color: rgb(196, 95, 125);")
                font = QFont()
                font.setPointSize(12)
                font.setBold(True)
                label.setFont(font)
                # label.setWordWrap(True)
                # label.setContentsMargins(20, 10, 20, 10)
                # if index in downloadIds:
                #     item.setBackground(QColor(18, 161, 130))
                # else:
                #     item.setBackground(QColor(0, 0, 0, 0))
                item.setSizeHint(label.sizeHint() + QSize(20, 20))
                self.listWidget.setItemWidget(item, label)
        return

    def ClearTags(self):
        while 1:
            child = self.flowLayout.takeAt(0)
            if not child:
                break
            if child.widget():
                child.widget().setParent(None)
            del child
        return

    def AddTags(self, name):
        box = QPushButton(name)
        # box.setMinimumWidth(160)
        # self.allBox[text] = box
        box.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        box.customContextMenuRequested.connect(self.CopyClickTagsItem)
        box.clicked.connect(self.ClickTagsItem)
        self.flowLayout.addWidget(box)
        return

    def OpenBookBack(self, raw):
        QtOwner().CloseLoading()
        self.categoriesList.clear()
        self.autorList.clear()
        self.ClearTags()
        info = BookMgr().books.get(self.bookId)
        st = raw["st"]
        if info:
            self.autorList.AddItem(info.author)
            if hasattr(info, "chineseTeam"):
                self.autorList.AddItem(info.chineseTeam)
            title = info.title
            if info.pagesCount:
                title += "<font color=#d5577c>{}</font>".format("(" + str(info.pagesCount) + "P)")
            if info.finished:
                title += "<font color=#d5577c>{}</font>".format("(完)")
            self.title.setText(title)
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.title.setFont(font)
            self.idLabel.setText(info.id)

            self.bookName = info.title
            self.description.setPlainText(info.description)

            for name in info.categories:
                self.categoriesList.AddItem(name)
            for name in info.tags:
                self.AddTags(name)
            self.starButton.setText(str(info.totalLikes))
            self.views.setText(str(info.totalViews))
            self.commentButton.setText(str(getattr(info, "commentsCount", 0)))
            self.isFavorite = info.isFavourite
            self.isLike = info.isLiked
            self.UpdateFavoriteIcon()
            self.UpdateLikeIcon()
            self.picture.setText(Str.GetStr(Str.LoadingPicture))
            fileServer = info.thumb.get("fileServer")
            path = info.thumb.get("path")
            name = info.thumb.get("originalName")
            self.url = fileServer
            dayStr = ToolUtil.GetUpdateStr(info.updated_at)
            self.updateTick.setText(str(dayStr) + Str.GetStr(Str.Updated))
            if config.IsLoadingPicture:
                url = ToolUtil.GetRealUrl(fileServer, path)
                self.path = ToolUtil.GetRealPath(self.bookId, "cover")
                if QtOwner().isOfflineModel:
                    self.AddDownloadTask(url, self.path, completeCallBack=self.UpdatePicture)
                else:
                    self.AddDownloadTask(url, self.path, completeCallBack=self.UpdatePicture, isReload=True)
            if not QtOwner().isOfflineModel:
                self.AddHttpTask(req.GetComicsBookEpsReq(self.bookId), self.GetEpsBack)
            self.startRead.setEnabled(False)
            if hasattr(info, "_creator"):
                creator = info._creator
                self.user_name.setText(creator.get("name"))
                url2 = creator.get("avatar", {}).get("fileServer")
                path2 = creator.get("avatar", {}).get("path")
                if url2:
                    url2 = ToolUtil.GetRealUrl(url2, path2)
                    path2 = ToolUtil.GetMd5RealPath(url2, "user")
                    self.AddDownloadTask(url2, path2, completeCallBack=self.LoadingPictureComplete)
        else:
            # QtWidgets.QMessageBox.information(self, '加载失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(Str.GetStr(st))

        # if st == Status.UnderReviewBook:
        #     QtOwner().ShowError(Str.GetStr(st))

        return

    def LoadingPictureComplete(self, data, status):
        if status == Status.Ok:
            self.userIconData = data
            self.user_icon.SetPicture(data)

    def UpdatePicture(self, data, status):
        if status == Status.Ok:
            self.pictureData = data
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            radio = self.devicePixelRatio()
            pic.setDevicePixelRatio(radio)
            newPic = pic.scaled(self.picture.size()*radio, QtCore.Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.picture.setPixmap(newPic)
            # self.picture.setScaledContents(True)
            if Setting.CoverIsOpenWaifu.value:
                w, h, mat,_ = ToolUtil.GetPictureSize(self.pictureData)
                if max(w, h) <= Setting.CoverMaxNum.value:
                    model = ToolUtil.GetModelByIndex(Setting.CoverLookNoise.value, Setting.CoverLookScale.value, Setting.CoverLookModel.value, mat)
                    self.AddConvertTask(self.path, self.pictureData, model, self.Waifu2xPictureBack)
        else:
            self.picture.setText(Str.GetStr(status))
        return

    def Waifu2xPictureBack(self, data, waifuId, index, tick):
        if data:
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            radio = self.devicePixelRatio()
            pic.setDevicePixelRatio(radio)
            newPic = pic.scaled(self.picture.size()*radio, QtCore.Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.picture.setPixmap(newPic)
        return

    def GetEpsBack(self, raw):
        st = raw["st"]
        if st == Status.Ok:
            self.UpdateEpsData()
            self.lastEpsId = -1
            self.LoadHistory()
            return
        else:
            QtOwner().ShowError(Str.GetStr(Str.ChapterLoadFail) + ", {}".format(Str.GetStr(st)))
            # # 从下载中导入章节
            # info = QtOwner().downloadView.downloadDict.get(self.bookId)
            # if info:
            #     from view.download.download_item import DownloadItem, DownloadEpsItem
            #     from tools.book import BookEps
            #     assert isinstance(info, DownloadItem)
            #     for v in info.epsInfo:
            #         assert isinstance(v, DownloadEpsItem)
            #         epsInfo = BookEps()
            #         epsInfo.maxPics = v.picCnt
            #         epsInfo.title = v.epsTitle
            #         epsInfo.id = v.epsId
            #         info.epsDict[epsInfo.id] = epsInfo
        return

    def UpdateEpsData(self):
        self.epsListWidget.clear()
        info = BookMgr().books.get(self.bookId)
        if not info:
            return
        assert isinstance(info, Book)
        self.pageBox.clear()

        texts = []
        for i in range(0, info.maxLoadEps):
            start = info.epsCount - i*info.epsLimit*1
            end = max(1, info.epsCount - (i+1)*info.epsLimit + 1)
            texts.append("{}-{}".format(start, end))

        self.pageBox.addItems(texts)

        if info.epsCount == 1:
            self.pageLabel.setVisible(False)
            self.pageBox.setVisible(False)
        else:
            self.pageLabel.setVisible(False)
            self.pageBox.setVisible(True)

    def UpdateEpsPageData(self, index):
        info = BookMgr().books.get(self.bookId)
        if not info:
            return
        if index < 0:
            return
        assert isinstance(info, Book)
        if index + 1 in info.curLoadEps:
            self.UpdateEpsPageDataBack({"st": Status.Ok}, index)
        else:
            QtOwner().ShowLoading()
            self.startRead.setEnabled(False)
            self.AddHttpTask(req.GetComicsBookEpsReq(info.id, index+1), self.UpdateEpsPageDataBack, index)

    def UpdateEpsPageDataBack(self, raw, index):
        QtOwner().CloseLoading()
        self.epsListWidget.clear()
        self.startRead.setEnabled(True)
        st = raw["st"]
        if st == Status.Ok:
            # downloadIds = QtOwner().owner.downloadForm.GetDownloadCompleteEpsId(self.bookId)
            info = BookMgr().books.get(self.bookId)
            if not info:
                return
            assert isinstance(info, Book)

            for i in range(0, info.epsLimit):

                epsId = (info.epsCount - index*info.epsLimit) - 1-i
                epsInfo = info.epsDict.get(epsId)
                if not epsInfo:
                    return
                label = QLabel(str(epsId + 1) + "-" + epsInfo.title)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("color: rgb(196, 95, 125);")
                font = QFont()
                font.setPointSize(12)
                font.setBold(True)
                label.setFont(font)
                # label.setWordWrap(True)
                # label.setContentsMargins(20, 10, 20, 10)
                item = QListWidgetItem(self.epsListWidget)
                # if index in downloadIds:
                #     item.setBackground(QColor(18, 161, 130))
                # else:
                #     item.setBackground(QColor(0, 0, 0, 0))
                item.setSizeHint(label.sizeHint() + QSize(20, 20))
                item.setToolTip(epsInfo.title)
                self.epsListWidget.setItemWidget(item, label)
        else:
            QtOwner().ShowError(Str.GetStr(Str.ChapterLoadFail) + ", {}".format(Str.GetStr(st)))
        return

    # def ChageMaxNum(self):
    #     maxHeight = self.epsListWidget.verticalScrollBar().maximum()
    #     print(maxHeight)
    #     self.epsListWidget.setMinimumHeight(maxHeight)

    def AddDownload(self):
        QtOwner().OpenEpsInfo(self.bookId)
        return

    def AddBookLike(self):
        self.AddHttpTask(req.BookLikeReq(self.bookId))
        self.isLike = not self.isLike
        if self.isLike:
            self.starButton.setText(str(int(self.starButton.text()) + 1))
        else:
            self.starButton.setText(str(int(self.starButton.text()) - 1))
        self.UpdateLikeIcon()

    def AddFavorite(self):
        self.AddHttpTask(req.FavoritesAdd(self.bookId))
        self.isFavorite = not self.isFavorite
        self.UpdateFavoriteIcon()
        if self.isFavorite:
            QtOwner().ShowMsg(Str.GetStr(Str.AddFavoriteSuc))
            QtOwner().favoriteView.AddFavorites(self.bookId)
        else:
            QtOwner().favoriteView.DelAndFavoritesBack({"st": Status.Ok}, self.bookId)

    def ClearCache(self):
        path = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir),
                            "book/{}".format(self.bookId))
        waifuPath = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir),
                                 "waifu2x/book/{}".format(self.bookId))
        isClear = QMessageBox.information(self, '清除缓存', "是否清除本书所有缓存\n{}\n{}".format(path, waifuPath), QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if isClear == QtWidgets.QMessageBox.Yes:
            if not Setting.SavePath.value:
                return
            path = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir),
                                "book/{}".format(self.bookId))
            waifuPath = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir),
                                     "waifu2x/book/{}".format(self.bookId))
            if os.path.isdir(path):
                shutil.rmtree(path, True)
            if os.path.isdir(waifuPath):
                shutil.rmtree(waifuPath, True)
        self.UpdateFavoriteIcon()


    def OpenReadImg(self, modelIndex):
        index = modelIndex.row()
        item = self.epsListWidget.item(index)
        if not item:
            return
        book = BookMgr().GetBook(self.bookId)
        if not book:
            return
        assert isinstance(book, Book)
        loadIndex = self.pageBox.currentIndex()
        epsId = (book.epsCount - loadIndex*book.epsLimit) - index - 1
        self.OpenReadIndex(epsId)

    def OpenReadImg2(self, modelIndex):
        index = modelIndex.row()
        item = self.listWidget.item(index)
        if not item:
            return
        book = BookMgr().GetBook(self.bookId)
        if not book:
            return
        assert isinstance(book, Book)
        if not QtOwner().downloadView.IsDownloadEpsId(self.bookId, index):
            QtOwner().ShowError(Str.GetStr(Str.NotDownload))
            return
        self.OpenReadIndex(index, isOffline=True)

    def OpenReadIndex(self, epsId, pageIndex=-1, isOffline=False):
        QtOwner().OpenReadView(self.bookId, epsId, pageIndex=pageIndex, isOffline=isOffline)
        # self.stackedWidget.setCurrentIndex(1)

    def StartRead(self):
        if self.lastEpsId >= 0:
            self.OpenReadIndex(self.lastEpsId, self.lastIndex)
        else:
            self.OpenReadIndex(0)
        return

    def StartRead2(self):
        if self.lastEpsId >= 0:
            if not QtOwner().downloadView.IsDownloadEpsId(self.bookId, self.lastEpsId):
                QtOwner().ShowError(Str.GetStr(Str.NotDownload))
                return
            self.OpenReadIndex(self.lastEpsId, self.lastIndex, isOffline=True)
        else:
            if not QtOwner().downloadView.IsDownloadEpsId(self.bookId, 0):
                QtOwner().ShowError(Str.GetStr(Str.NotDownload))
                return
            self.OpenReadIndex(0, isOffline=True)
        return

    def LoadHistory(self):
        info = QtOwner().historyView.GetHistory(self.bookId)
        if not info:
            self.lastEpsId = -1
            self.lastIndex = 0
            self.startRead.setText(Str.GetStr(Str.LookFirst))
            return
        if self.lastEpsId == info.epsId:
            self.lastIndex = info.picIndex
            self.startRead.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))
            self.readOffline.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))
            return

        # if self.lastEpsId >= 0:
        #     item = self.epsListWidget.item(self.lastEpsId)
        #     if item:
        #         downloadIds = QtOwner().downloadView.GetDownloadCompleteEpsId(self.bookId)
        #         if self.lastEpsId in downloadIds:
        #             item.setBackground(QColor(18, 161, 130))
        #         else:
        #             item.setBackground(QColor(0, 0, 0, 0))

        # item = self.epsListWidget.item(info.epsId)
        # if not item:
        #     return
        # item.setBackground(QColor(238, 162, 164))
        self.lastEpsId = info.epsId
        self.lastIndex = info.picIndex
        self.startRead.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))
        self.readOffline.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))

    def ClickCategoriesItem(self, modelIndex):
        index = modelIndex.row()
        item = self.categoriesList.item(index)
        if not item:
            return
        widget = self.categoriesList.itemWidget(item)
        text = widget.text()
        # QtOwner().owner.searchForm.SearchCategories(text)
        QtOwner().OpenSearchByCategory2(text)
        return

    def ClickAutorItem(self, modelIndex):
        index = modelIndex.row()
        item = self.autorList.item(index)
        if not item:
            return
        widget = self.autorList.itemWidget(item)
        text = widget.text()
        # QtOwner().owner.searchForm.SearchAutor(text)
        QtOwner().OpenSearch2(text, True, False, False, False, False, True, False)
        return
    #

    def ClickTagsItem(self):
        text = self.sender().text()
        # QtOwner().owner.searchForm.SearchTags(text)
        QtOwner().OpenSearch2(text, True, False, False, False, True, False, False)
        return

    def CopyClickTagsItem(self):
        text = self.sender().text()
        QtOwner().CopyText(text)

    def CopyClickCategoriesItem(self, pos):
        index = self.categoriesList.indexAt(pos)
        item = self.categoriesList.itemFromIndex(index)
        if item:
            widget = self.categoriesList.itemWidget(item)
            text = widget.text()
            QtOwner().CopyText(text)

    def CopyClickAutorItem(self, pos):
        index = self.autorList.indexAt(pos)
        item = self.autorList.itemFromIndex(index)
        if index.isValid() and item:
            widget = self.autorList.itemWidget(item)
            text = widget.text()
            QtOwner().CopyText(text)

    def ShowMenu(self):
        if not self.bookName:
            return
        if not self.bookId:
            return
        toolMenu = QMenu(self.uploadButton)
        toolMenu.clear()
        title = self.bookName
        if not title:
            return
        nasDict = QtOwner().owner.nasView.nasDict
        action = toolMenu.addAction(Str.GetStr(Str.NetNas))
        action.setEnabled(False)

        if not nasDict:
            action = toolMenu.addAction(Str.GetStr(Str.CvSpace))
            action.setEnabled(False)
        else:
            for k, v in nasDict.items():
                action = toolMenu.addAction(v.showTitle)
                if QtOwner().nasView.IsInUpload(k, self.bookId):
                    action.setEnabled(False)
                action.triggered.connect(partial(self.NasUploadHandler, k, self.bookId))
        toolMenu.exec(QCursor().pos())

    def NasUploadHandler(self, nasId, bookId):
        QtOwner().nasView.AddNasUpload(nasId, bookId)
        return
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if obj == self.picture:
                    if self.pictureData:
                        QtOwner().OpenWaifu2xTool(self.pictureData)
                elif obj == self.user_icon:
                    if self.userIconData:
                        QtOwner().OpenWaifu2xTool(self.userIconData)
                elif obj == self.user_name:
                    QtOwner().OpenSearchByCreate(self.user_name.text())
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def keyPressEvent(self, ev):
        key = ev.key()
        if Qt.Key_Escape == key:
            self.close()
        return super(self.__class__, self).keyPressEvent(ev)
