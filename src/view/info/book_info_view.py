from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QSize, QEvent, Signal
from PySide6.QtGui import QColor, QFont, QPixmap, QIcon
from PySide6.QtWidgets import QListWidgetItem, QLabel

from config.setting import Setting
from interface.ui_book_info import Ui_BookInfo
from qt_owner import QtOwner
from server import req, ToolUtil, config, Status
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr
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
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.autorList.itemClicked.connect(self.ClickAutorItem)
        self.idLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.description.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.starButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.starButton.setIconSize(QSize(50, 50))
        self.downloadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.downloadButton.setIconSize(QSize(50, 50))
        self.favoriteButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.favoriteButton.setIconSize(QSize(50, 50))
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commentButton.setIconSize(QSize(50, 50))
        self.description.adjustSize()
        self.title.adjustSize()

        self.categoriesList.itemClicked.connect(self.ClickCategoriesItem)

        self.tagsList.itemClicked.connect(self.ClickTagsItem)

        self.epsListWidget.setFlow(self.epsListWidget.LeftToRight)
        self.epsListWidget.setWrapping(True)
        self.epsListWidget.setFrameShape(self.epsListWidget.NoFrame)
        self.epsListWidget.setResizeMode(self.epsListWidget.Adjust)

        self.epsListWidget.clicked.connect(self.OpenReadImg)

        # QScroller.grabGesture(self.epsListWidget, QScroller.LeftMouseButtonGesture)
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
        self.ReloadHistory.connect(self.LoadHistory)

    def UpdateFavoriteIcon(self):
        p = QPixmap()
        if self.isFavorite:
            self.favoriteButton.setIcon(QIcon(":/png/icon/icon_like.png"))
        else:
            self.favoriteButton.setIcon(QIcon(":/png/icon/icon_like_off.png"))

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
        self.setFocus()
        self.Clear()
        self.show()
        QtOwner().ShowLoading()
        self.OpenLocalBack()

    def OpenComment(self):
        if self.bookId:
            QtOwner().OpenComment(self.bookId)

    def OpenLocalBack(self):
        self.AddSqlTask("book", self.bookId, SqlServer.TaskTypeCacheBook, callBack=self.SendLocalBack)

    def SendLocalBack(self, books):
        self.AddHttpTask(req.GetComicsBookReq(self.bookId), self.OpenBookBack)

    def OpenBookBack(self, raw):
        QtOwner().CloseLoading()
        self.categoriesList.clear()
        self.tagsList.clear()
        self.autorList.clear()
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
                self.tagsList.AddItem(name)
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
                self.AddDownloadTask(url, self.path, completeCallBack=self.UpdatePicture, isReload=True)

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
                w, h, mat = ToolUtil.GetPictureSize(self.pictureData)
                if max(w, h) <= Setting.CoverMaxNum.value:
                    model = ToolUtil.GetModelByIndex(Setting.CoverLookNoise.value, Setting.CoverLookScale.value, Setting.CoverLookModel.value, mat)
                    self.AddConvertTask(self.path, self.pictureData, model, self.Waifu2xPictureBack)
        else:
            self.picture.setText(Str.GetStr(Str.LoadingFail))
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
        return

    def UpdateEpsData(self):
        self.epsListWidget.clear()
        info = BookMgr().books.get(self.bookId)
        if not info:
            return
        self.startRead.setEnabled(True)
        # downloadIds = QtOwner().owner.downloadForm.GetDownloadCompleteEpsId(self.bookId)
        for index, epsInfo in enumerate(info.eps):
            label = QLabel(str(index + 1) + "-" + epsInfo.title)
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

    def OpenReadImg(self, modelIndex):
        index = modelIndex.row()
        self.OpenReadIndex(index)

    def OpenReadIndex(self, index, pageIndex=-1):
        item = self.epsListWidget.item(index)
        if not item:
            return
        widget = self.epsListWidget.itemWidget(item)
        if not widget:
            return
        name = widget.text()
        QtOwner().OpenReadView(self.bookId, index, name, pageIndex=pageIndex)
        # self.stackedWidget.setCurrentIndex(1)

    def StartRead(self):
        if self.lastEpsId >= 0:
            self.OpenReadIndex(self.lastEpsId, self.lastIndex)
        else:
            self.OpenReadIndex(0)
        return

    def LoadHistory(self):
        info = QtOwner().historyView.GetHistory(self.bookId)
        if not info:
            self.startRead.setText(Str.GetStr(Str.LookFirst))
            return
        if self.lastEpsId == info.epsId:
            self.lastIndex = info.picIndex
            self.startRead.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))
            return

        # if self.lastEpsId >= 0:
        #     item = self.epsListWidget.item(self.lastEpsId)
        #     if item:
        #         downloadIds = QtOwner().downloadView.GetDownloadCompleteEpsId(self.bookId)
        #         if self.lastEpsId in downloadIds:
        #             item.setBackground(QColor(18, 161, 130))
        #         else:
        #             item.setBackground(QColor(0, 0, 0, 0))

        item = self.epsListWidget.item(info.epsId)
        if not item:
            return
        item.setBackground(QColor(238, 162, 164))
        self.lastEpsId = info.epsId
        self.lastIndex = info.picIndex
        self.startRead.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))

    def ClickCategoriesItem(self, item):
        text = item.text()
        # QtOwner().owner.searchForm.SearchCategories(text)
        QtOwner().OpenSearchByCategory2(text)
        return

    def ClickAutorItem(self, item):
        text = item.text()
        # QtOwner().owner.searchForm.SearchAutor(text)
        QtOwner().OpenSearch2(text, True, False, False, False, False, True, False)
        return

    def ClickTagsItem(self, item):
        text = item.text()
        # QtOwner().owner.searchForm.SearchTags(text)
        QtOwner().OpenSearch2(text, True, False, False, False, True, False, False)
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
