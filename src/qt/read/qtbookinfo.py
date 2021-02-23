import json
import weakref

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QRect, Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QListWidget, QListWidgetItem, QLabel, QApplication

from conf import config
from src.index.book import BookMgr
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtlistwidget import QtBookList, QtCategoryList
from src.qt.com.qtloading import QtLoading
from src.server import req, Log, Server, ToolUtil
from src.user.user import User
from src.util.status import Status
from ui.bookinfo import Ui_BookInfo


class QtBookInfo(QtWidgets.QWidget, Ui_BookInfo):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.loadingForm = QtLoading(self)
        self.bookId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1

        self.msgForm = QtBubbleLabel(self)

        self.title.setGeometry(QRect(328, 240, 329, 27 * 4))
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignTop)
        self.title.setContextMenuPolicy(Qt.CustomContextMenu)
        self.title.customContextMenuRequested.connect(self.CopyTitle)

        # self.autor.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.autor.customContextMenuRequested.connect(self.OpenAutor)

        layouy = self.horizontalLayout_4
        self.autorList = QtCategoryList(self)
        layouy.addWidget(QLabel("作者："))
        layouy.addWidget(self.autorList)
        self.autorList.itemClicked.connect(self.ClickTagsItem)

        self.description.setContextMenuPolicy(Qt.CustomContextMenu)
        self.description.customContextMenuRequested.connect(self.CopyDescription)

        self.description.setGeometry(QRect(328, 240, 329, 27 * 4))
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignTop)

        # self.categories.setGeometry(QRect(328, 240, 329, 27 * 4))
        # self.categories.setWordWrap(True)
        # self.categories.setAlignment(Qt.AlignTop)

        layouy = self.horizontalLayout_6
        self.categoriesList = QtCategoryList(self)
        layouy.addWidget(QLabel("分类："))
        layouy.addWidget(self.categoriesList)
        self.categoriesList.itemClicked.connect(self.ClickCategoriesItem)

        # self.tags.setGeometry(QRect(328, 240, 329, 27 * 4))
        # self.tags.setWordWrap(True)
        # self.tags.setAlignment(Qt.AlignTop)

        layouy = self.horizontalLayout_7
        self.tagsList = QtCategoryList(self)
        layouy.addWidget(QLabel("Tags："))
        layouy.addWidget(self.tagsList)
        self.tagsList.itemClicked.connect(self.ClickTagsItem)

        self.epsListWidget = QListWidget(self)
        self.epsListWidget.setFlow(self.epsListWidget.LeftToRight)
        self.epsListWidget.setWrapping(True)
        self.epsListWidget.setFrameShape(self.epsListWidget.NoFrame)
        self.epsListWidget.setResizeMode(self.epsListWidget.Adjust)

        self.epsLayout.addWidget(self.epsListWidget)

        self.listWidget = QtBookList(self, self.__class__.__name__)
        self.listWidget.InitUser(self.LoadNextPage)

        self.commentLayout.addWidget(self.listWidget)

        # self.stackedWidget.addWidget(self.qtReadImg)
        self.epsListWidget.clicked.connect(self.OpenReadImg)

        self.closeFlag = self.__class__.__name__ + "-close"         # 切换book时，取消加载

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.stackedWidget.currentIndex() == 1:
            self.stackedWidget.setCurrentIndex(0)
            self.owner().qtReadImg.AddHistory()
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
        self.owner().qtTask.CancelTasks(self.closeFlag)
        self.epsListWidget.clear()
        self.listWidget.clear()

    def CopyDescription(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.description.text())
        self.msgForm.ShowMsg("复制描述")
        return

    def OpenBook(self, bookId):
        self.bookId = bookId
        self.setWindowTitle(self.bookId)
        if self.bookId in self.owner().downloadForm.downloadDict:
            self.download.setEnabled(False)
        else:
            self.download.setEnabled(True)

        self.Clear()
        self.show()
        self.loadingForm.show()
        self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookById(bookId, x), self.OpenBookBack)

    def close(self):
        super(self.__class__, self).close()

    def OpenBookBack(self, msg):
        self.loadingForm.close()
        self.listWidget.UpdatePage(1, 1)
        self.listWidget.UpdateState()
        self.categoriesList.clear()
        self.tagsList.clear()
        self.autorList.clear()
        info = BookMgr().books.get(self.bookId)
        if msg == Status.Ok and info:
            # self.autor.setText(info.author)
            self.autorList.AddItem(info.author)
            self.title.setText(info.title)
            self.bookName = info.title
            self.description.setText(info.description)
            self.isFinished.setText("完本" if info.finished else "未完本")
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
            timeArray, day = ToolUtil.GetDateStr(info.updated_at)
            self.updateTick.setText(str(day) + "天前更新")
            if config.IsLoadingPicture:

                self.owner().qtTask.AddDownloadTask(fileServer, path, completeCallBack=self.UpdatePicture, cleanFlag=self.closeFlag)
            self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.GetComments(self.bookId), bakParam=x),
                                            self.GetCommnetBack, cleanFlag=self.closeFlag)

            self.owner().qtTask.AddHttpTask(lambda x: BookMgr().AddBookEpsInfo(self.bookId, x), self.GetEpsBack, cleanFlag=self.closeFlag)
            self.startRead.setEnabled(False)
        else:
            # QtWidgets.QMessageBox.information(self, '加载失败', msg, QtWidgets.QMessageBox.Yes)
            self.msgForm.ShowError(msg)
            self.hide()
        return

    def UpdatePicture(self, data, status):
        if status == Status.Ok:
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            pic.scaled(self.picture.size(), QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pic)
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
                page = int(comments.get("page", 1))
                pages = int(comments.get("pages", 1))
                limit = int(comments.get("limit", 1))
                self.listWidget.UpdatePage(page, pages)
                total = comments.get("total", 0)
                self.tabWidget.setTabText(1, "评论({})".format(str(total)))

                for index, info in enumerate(comments.get("docs")):
                    floor = total - ((page - 1) * limit + index)
                    content = info.get("content")
                    name = info.get("_user", {}).get("name")
                    avatar = info.get("_user", {}).get("avatar", {})
                    createdTime = info.get("created_at")
                    commentsCount = info.get("commentsCount")
                    self.listWidget.AddUserItem(content, name, createdTime, floor, avatar.get("fileServer"),
                                 avatar.get("path"), avatar.get("originalName"))
            return
        except Exception as es:
            import sys
            cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
            e = sys.exc_info()[1]
            Log.Error(cur_tb, e)

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
        downloadIds = self.owner().downloadForm.GetDownloadCompleteEpsId(self.bookId)
        for index, epsInfo in enumerate(info.eps):
            label = QLabel(epsInfo.title)
            label.setContentsMargins(20, 10, 20, 10)
            item = QListWidgetItem(self.epsListWidget)
            if index in downloadIds:
                item.setBackground(QColor(18, 161, 130))
            else:
                item.setBackground(QColor(0,0,0,0))
            item.setSizeHint(label.sizeHint())
            self.epsListWidget.setItemWidget(item, label)
        self.tabWidget.setTabText(0, "章节({})".format(str(len(info.eps))))
        return

    def AddDownload(self):
        self.owner().epsInfoForm.OpenEpsInfo(self.bookId)
        # if self.owner().downloadForm.AddDownload(self.bookId):
        #     QtBubbleLabel.ShowMsgEx(self, "添加下载成功")
        # else:
        #     QtBubbleLabel.ShowMsgEx(self, "已在下载列表")
        # self.download.setEnabled(False)

    def AddFavority(self):
        User().AddAndDelFavorites(self.bookId)
        QtBubbleLabel.ShowMsgEx(self, "添加收藏成功")
        self.favorites.setEnabled(False)

    def LoadNextPage(self):
        self.loadingForm.show()
        self.owner().qtTask.AddHttpTask(
            lambda x: Server().Send(req.GetComments(self.bookId, self.listWidget.page + 1), bakParam=x),
            self.GetCommnetBack, cleanFlag=self.closeFlag)
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
        self.owner().qtReadImg.OpenPage(self.bookId, index, name)
        # self.stackedWidget.setCurrentIndex(1)

    def StartRead(self):
        if self.lastEpsId >= 0:
            self.OpenReadIndex(self.lastEpsId)
        else:
            self.OpenReadIndex(0)
        return

    def LoadHistory(self):
        info = self.owner().historyForm.GetHistory(self.bookId)
        if not info:
            self.startRead.setText("观看第{}章".format(str(1)))
            return
        if self.lastEpsId == info.epsId:
            self.startRead.setText("观看第{}章".format(str(self.lastEpsId + 1)))
            return

        if self.lastEpsId >= 0:
            item = self.epsListWidget.item(self.lastEpsId)
            if item:
                downloadIds = self.owner().downloadForm.GetDownloadCompleteEpsId(self.bookId)
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
        self.startRead.setText("观看第{}章".format(str(self.lastEpsId+1)))

    def ClickCategoriesItem(self, item):
        text = item.text()
        self.owner().userForm.listWidget.setCurrentRow(0)
        self.owner().searchForm.searchEdit.setText("")
        self.owner().searchForm.OpenSearchCategories(text)
        return

    def ClickTagsItem(self, item):
        text = item.text()
        self.owner().userForm.listWidget.setCurrentRow(0)
        self.owner().searchForm.searchEdit.setText(text)
        self.owner().searchForm.Search()
        return