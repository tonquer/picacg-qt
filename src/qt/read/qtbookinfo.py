import json

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt, QSize, QEvent
from PySide2.QtGui import QColor, QFont
from PySide2.QtWidgets import QListWidgetItem, QLabel, QApplication, QHBoxLayout, QLineEdit, QPushButton, \
    QVBoxLayout

from conf import config
from src.index.book import BookMgr
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtimg import QtImgMgr
from src.qt.com.qtloading import QtLoading
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log, ToolUtil
from src.util.status import Status
from ui.bookinfo import Ui_BookInfo
from ui.qtlistwidget import QtBookList


class QtBookInfo(QtWidgets.QWidget, Ui_BookInfo, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.loadingForm = QtLoading(self)
        self.bookId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.pictureData = None

        self.msgForm = QtBubbleLabel(self)
        self.picture.installEventFilter(self)
        # self.title.setGeometry(QRect(328, 240, 329, 27 * 4))
        self.title.setWordWrap(True)
        # self.title.setAlignment(Qt.AlignLeft)
        self.title.setContextMenuPolicy(Qt.CustomContextMenu)
        self.title.customContextMenuRequested.connect(self.CopyTitle)

        # self.autor.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.autor.customContextMenuRequested.connect(self.OpenAutor)

        self.autorList.itemClicked.connect(self.ClickTagsItem)

        self.description.setContextMenuPolicy(Qt.CustomContextMenu)
        self.description.customContextMenuRequested.connect(self.CopyDescription)

        # self.description.setGeometry(QRect(328, 240, 329, 27 * 4))
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignTop)

        self.description.adjustSize()
        self.title.adjustSize()

        # self.categories.setGeometry(QRect(328, 240, 329, 27 * 4))
        # self.categories.setWordWrap(True)
        # self.categories.setAlignment(Qt.AlignTop)

        self.categoriesList.itemClicked.connect(self.ClickCategoriesItem)

        # self.tags.setGeometry(QRect(328, 240, 329, 27 * 4))
        # self.tags.setWordWrap(True)
        # self.tags.setAlignment(Qt.AlignTop)

        self.tagsList.itemClicked.connect(self.ClickTagsItem)

        self.epsListWidget.setFlow(self.epsListWidget.LeftToRight)
        self.epsListWidget.setWrapping(True)
        self.epsListWidget.setFrameShape(self.epsListWidget.NoFrame)
        self.epsListWidget.setResizeMode(self.epsListWidget.Adjust)

        self.listWidget.InitUser(self.LoadNextPage)
        self.listWidget.doubleClicked.connect(self.OpenCommentInfo)

        self.childrenListWidget = QtBookList(None)
        self.childrenListWidget.InitUser(self.LoadChildrenNextPage)

        self.childrenWidget = QtWidgets.QWidget()
        layout = QHBoxLayout(self.childrenWidget)

        label = QLabel()
        label.setMinimumWidth(100)
        layout.addWidget(label)
        layout3 = QVBoxLayout()

        layout2 = QHBoxLayout()
        self.commentLine2 = QLineEdit()
        self.commentButton2 = QPushButton("回复")
        self.commentButton2.clicked.connect(self.SendCommentChildren)
        layout2.addWidget(self.commentLine2)
        layout2.addWidget(self.commentButton2)
        layout3.addLayout(layout2)
        layout3.addWidget(self.childrenListWidget)
        layout.addLayout(layout3)

        # self.commentLayout.addWidget(self.listWidget)
        # layout = QHBoxLayout()
        # self.commentLine = QLineEdit()
        # layout.addWidget(self.commentLine)
        # self.commentButton = QPushButton("发送评论")
        # layout.addWidget(self.commentButton)
        # self.commentLayout.addLayout(layout, 1, 0)
        self.commentButton.clicked.connect(self.SendComment)

        # self.stackedWidget.addWidget(self.qtReadImg)
        self.epsListWidget.clicked.connect(self.OpenReadImg)

        # self.title.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # self.description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        ToolUtil.SetIcon(self)


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.stackedWidget.currentIndex() == 1:
            self.stackedWidget.setCurrentIndex(0)
            QtOwner().owner.qtReadImg.AddHistory()
            self.LoadHistory()
            a0.ignore()
        else:
            a0.accept()

    def CopyTitle(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.title.text())
        self.msgForm.ShowMsg("复制标题")
        return

    # def OpenAutor(self):
    #     text = self.autor.text()
    #     self.owner().userForm.listWidget.setCurrentRow(0)
    #     self.owner().searchForm.searchEdit.setText(text)
    #     self.owner().searchForm.Search()
    #     return

    def Clear(self):
        self.stackedWidget.setCurrentIndex(0)
        self.ClearTask()
        self.epsListWidget.clear()
        self.ClearCommnetList()

    def CopyDescription(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.description.text())
        self.msgForm.ShowMsg("复制描述")
        return

    def OpenBook(self, bookId):
        self.bookId = bookId
        self.setWindowTitle(self.bookId)
        self.setFocus()
        # if self.bookId in self.owner().downloadForm.downloadDict:
        #     self.download.setEnabled(False)
        # else:
        #     self.download.setEnabled(True)

        self.Clear()
        self.show()
        self.loadingForm.show()
        self.AddHttpTask(req.GetComicsBookReq(bookId), self.OpenBookBack)

    def close(self):
        super(self.__class__, self).close()

    def OpenBookBack(self, msg):
        self.loadingForm.close()
        self.listWidget.UpdatePage(1, 1)
        self.childrenListWidget.UpdatePage(1, 1)
        self.childrenListWidget.UpdateState()
        self.listWidget.UpdateState()
        self.categoriesList.clear()
        self.tagsList.clear()
        self.autorList.clear()
        info = BookMgr().books.get(self.bookId)
        if msg == Status.Ok and info:
            # self.autor.setText(info.author)
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

            self.bookName = info.title
            self.description.setText(info.description)
            # self.isFinished.setText("完本" if info.finished else "未完本")

            for name in info.categories:
                self.categoriesList.AddItem(name)
            # self.categories.setText(','.join(info.categories))
            # self.tags.setText(','.join(info.tags))
            for name in info.tags:
                self.tagsList.AddItem(name)
            self.likes.setText(str(info.totalLikes))
            self.views.setText(str(info.totalViews))

            if info.isFavourite:
                self.favorites.setEnabled(False)
            else:
                self.favorites.setEnabled(True)
            self.picture.setText("图片加载中...")
            fileServer = info.thumb.get("fileServer")
            path = info.thumb.get("path")
            name = info.thumb.get("originalName")
            self.url = fileServer
            self.path = path
            dayStr = ToolUtil.GetUpdateStr(info.updated_at)
            self.updateTick.setText(str(dayStr) + "更新")
            if config.IsLoadingPicture:

                self.AddDownloadTask(fileServer, path, completeCallBack=self.UpdatePicture)
            self.AddHttpTask(req.GetComments(self.bookId), self.GetCommnetBack)

            self.AddHttpTask(req.GetComicsBookEpsReq(self.bookId), self.GetEpsBack)
            self.startRead.setEnabled(False)
        else:
            # QtWidgets.QMessageBox.information(self, '加载失败', msg, QtWidgets.QMessageBox.Yes)
            self.msgForm.ShowError(msg)
            self.hide()
        return

    def UpdatePicture(self, data, status):
        if status == Status.Ok:
            self.pictureData = data
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            newPic = pic.scaled(self.picture.size(), QtCore.Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.picture.setPixmap(newPic)
            # self.picture.setScaledContents(True)
            self.update()
        else:
            self.picture.setText("图片加载失败")
        return

    # 加载评论
    def GetCommnetBack(self, data):
        try:
            self.loadingForm.close()
            self.listWidget.UpdateState()
            msg = json.loads(data)
            if msg.get("code") == 200:
                comments = msg.get("data", {}).get("comments", {})
                topComments = msg.get("data", {}).get("topComments", [])
                page = int(comments.get("page", 1))
                pages = int(comments.get("pages", 1))
                limit = int(comments.get("limit", 1))
                self.listWidget.UpdatePage(page, pages)
                total = comments.get("total", 0)
                self.tabWidget.setTabText(1, "评论({})".format(str(total)))
                if page == 1:
                    for index, info in enumerate(topComments):
                        floor = "置顶"
                        self.listWidget.AddUserItem(info, floor)

                for index, info in enumerate(comments.get("docs")):
                    floor = total - ((page - 1) * limit + index)
                    self.listWidget.AddUserItem(info, floor)
            return
        except Exception as es:
            Log.Error(es)

    def GetEpsBack(self, st):
        if st == Status.Ok:
            self.UpdateEpsData()
            self.lastEpsId = -1
            self.LoadHistory()
            return
        return

    def UpdateEpsData(self):
        self.epsListWidget.clear()
        info = BookMgr().books.get(self.bookId)
        if not info:
            return
        self.startRead.setEnabled(True)
        downloadIds = QtOwner().owner.downloadForm.GetDownloadCompleteEpsId(self.bookId)
        for index, epsInfo in enumerate(info.eps):
            label = QLabel(epsInfo.title)
            label.setAlignment(Qt.AlignCenter)
            # label.setWordWrap(True)
            # label.setContentsMargins(20, 10, 20, 10)
            item = QListWidgetItem(self.epsListWidget)
            if index in downloadIds:
                item.setBackground(QColor(18, 161, 130))
            else:
                item.setBackground(QColor(0,0,0,0))
            item.setSizeHint(label.sizeHint() + QSize(20, 20))
            item.setToolTip(epsInfo.title)
            self.epsListWidget.setItemWidget(item, label)
        self.tabWidget.setTabText(0, "章节({})".format(str(len(info.eps))))
        return

    def AddDownload(self):
        QtOwner().owner.epsInfoForm.OpenEpsInfo(self.bookId)
        # if self.owner().downloadForm.AddDownload(self.bookId):
        #     QtBubbleLabel.ShowMsgEx(self, "添加下载成功")
        # else:
        #     QtBubbleLabel.ShowMsgEx(self, "已在下载列表")
        # self.download.setEnabled(False)

    def AddFavority(self):
        self.AddHttpTask(req.FavoritesAdd(self.bookId))
        QtBubbleLabel.ShowMsgEx(self, "添加收藏成功")
        QtOwner().owner.favoriteForm.AddFavorites(self.bookId)
        self.favorites.setEnabled(False)

    def LoadNextPage(self):
        self.loadingForm.show()
        self.AddHttpTask(req.GetComments(self.bookId, self.listWidget.page + 1), self.GetCommnetBack)
        return

    def OpenReadImg(self, modelIndex):
        index = modelIndex.row()
        self.OpenReadIndex(index)

    def OpenReadIndex(self, index):
        item = self.epsListWidget.item(index)
        if not item:
            return
        widget = self.epsListWidget.itemWidget(item)
        if not widget:
            return
        name = widget.text()
        self.hide()
        QtOwner().owner.qtReadImg.OpenPage(self.bookId, index, name)
        # self.stackedWidget.setCurrentIndex(1)

    def StartRead(self):
        if self.lastEpsId >= 0:
            self.OpenReadIndex(self.lastEpsId)
        else:
            self.OpenReadIndex(0)
        return

    def LoadHistory(self):
        info = QtOwner().owner.historyForm.GetHistory(self.bookId)
        if not info:
            self.startRead.setText("观看第{}章".format(str(1)))
            return
        if self.lastEpsId == info.epsId:
            self.startRead.setText("上次看到第{}章".format(str(self.lastEpsId + 1)))
            return

        if self.lastEpsId >= 0:
            item = self.epsListWidget.item(self.lastEpsId)
            if item:
                downloadIds = QtOwner().owner.downloadForm.GetDownloadCompleteEpsId(self.bookId)
                if self.lastEpsId in downloadIds:
                    item.setBackground(QColor(18, 161, 130))
                else:
                    item.setBackground(QColor(0,0,0,0))

        item = self.epsListWidget.item(info.epsId)
        if not item:
            return
        item.setBackground(QColor(238, 162, 164))
        self.epsListWidget.update()
        self.lastEpsId = info.epsId
        self.startRead.setText("上次看到第{}章".format(str(self.lastEpsId+1)))

    def ClickCategoriesItem(self, item):
        text = item.text()
        QtOwner().owner.userForm.toolButton1.click()
        QtOwner().owner.searchForm.searchEdit.setText("")
        QtOwner().owner.searchForm.OpenSearchCategories(text)
        return

    def ClickTagsItem(self, item):
        text = item.text()
        QtOwner().owner.searchForm.Search2(text)
        return

    def SendComment(self):
        data = self.commentLine.text()
        if not data:
            return
        self.commentLine.setText("")
        self.loadingForm.show()
        self.AddHttpTask(req.SendComment(self.bookId, data), callBack=self.SendCommentBack)

    def SendCommentBack(self, msg):
        try:
            data = json.loads(msg)
            if data.get("code") == 200:
                self.ClearCommnetList()
                self.AddHttpTask(req.GetComments(self.bookId), self.GetCommnetBack)
            else:
                self.loadingForm.close()
                QtBubbleLabel.ShowErrorEx(self, data.get("message", "错误"))
            self.commentLine.setText("")
        except Exception as es:
            self.loadingForm.close()
            Log.Error(es)

    def OpenCommentInfo(self, modelIndex):
        index = modelIndex.row()
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return

        self.childrenListWidget.clear()
        self.childrenListWidget.UpdatePage(1, 1)
        self.childrenListWidget.UpdateState()
        if self.childrenListWidget.parentId == index:
            # self.childrenWidget.hide()
            self.childrenWidget.setParent(None)
            widget.gridLayout.removeWidget(self.childrenWidget)
            self.childrenListWidget.parentId = -1
            item.setSizeHint(widget.sizeHint())
            return
        if self.childrenListWidget.parentId >= 0:
            item2 = self.listWidget.item(self.childrenListWidget.parentId)
            widget2 = self.listWidget.itemWidget(item2)
            self.childrenWidget.setParent(None)
            widget2.gridLayout.removeWidget(self.childrenWidget)
            self.childrenListWidget.parentId = -1
            item2.setSizeHint(widget2.sizeHint())

        self.loadingForm.show()
        self.AddHttpTask(req.GetCommentsChildrenReq(widget.id), self.LoadCommentInfoBack, backParam=index)

    def LoadCommentInfoBack(self, msg, index):
        try:
            self.loadingForm.close()
            item = self.listWidget.item(index)
            if not item:
                return
            widget = self.listWidget.itemWidget(item)
            if not widget:
                return
            self.childrenListWidget.UpdateState()
            data = json.loads(msg)
            self.childrenListWidget.parentId = index
            widget.gridLayout.addWidget(self.childrenWidget, 1, 0, 1, 1)
            if data.get("code") == 200:
                comments = data.get("data", {}).get("comments", {})
                page = int(comments.get("page", 1))
                total = int(comments.get("total", 1))
                pages = int(comments.get("pages", 1))
                limit = int(comments.get("limit", 1))
                self.childrenListWidget.UpdatePage(page, pages)
                for index, info in enumerate(comments.get("docs")):
                    floor = total - ((page - 1) * limit + index)
                    self.childrenListWidget.AddUserItem(info, floor)

                pass
            self.listWidget.scrollToItem(item, self.listWidget.ScrollHint.PositionAtTop)
            size = self.listWidget.size()
            item.setSizeHint(size)
        except Exception as es:
            Log.Error(es)

    def SendCommentChildren(self):
        data = self.commentLine2.text()
        if not data:
            return
        index = self.childrenListWidget.parentId
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.commentLine2.setText("")
        commentId = widget.id
        self.loadingForm.show()
        self.childrenListWidget.clear()
        self.AddHttpTask(req.SendCommentChildrenReq(commentId, data), callBack=self.SendCommentChildrenBack, backParam=index)

    def SendCommentChildrenBack(self, msg, index):
        try:
            item = self.listWidget.item(index)
            if not item:
                self.loadingForm.close()
                return
            widget = self.listWidget.itemWidget(item)
            if not widget:
                self.loadingForm.close()
                return

            data = json.loads(msg)
            if data.get("code") == 200:
                self.AddHttpTask(req.GetCommentsChildrenReq(widget.id), self.LoadCommentInfoBack, backParam=index)
            else:
                self.loadingForm.close()
                QtBubbleLabel.ShowErrorEx(self, data.get("message", "错误"))
            self.commentLine.setText("")
        except Exception as es:
            self.loadingForm.close()
            Log.Error(es)

    def LoadChildrenNextPage(self):
        index = self.childrenListWidget.parentId
        item = self.listWidget.item(index)
        if not item:
            return
        widget = self.listWidget.itemWidget(item)
        if not widget:
            return
        self.loadingForm.show()
        self.AddHttpTask(req.GetCommentsChildrenReq(widget.id, self.childrenListWidget.page + 1), self.LoadCommentInfoBack, backParam=index)
        return

    def ClearCommnetList(self):
        if self.childrenListWidget.parentId >= 0:
            item2 = self.listWidget.item(self.childrenListWidget.parentId)
            widget2 = self.listWidget.itemWidget(item2)
            self.childrenWidget.setParent(None)
            widget2.gridLayout.removeWidget(self.childrenWidget)
            self.childrenListWidget.parentId = -1
            item2.setSizeHint(widget2.sizeHint())
        self.childrenListWidget.clear()
        self.listWidget.clear()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.pictureData:
                    QtImgMgr().ShowImg(self.pictureData)
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
