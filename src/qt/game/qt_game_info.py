
import json

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt, QSize, QEvent
from PySide2.QtGui import QFont, QPixmap
from PySide2.QtWidgets import QListWidgetItem, QLabel, QApplication, QHBoxLayout, QLineEdit, QPushButton, \
    QVBoxLayout, QScroller, QAbstractItemView

from conf import config
from qss.qss import QssDataMgr
from resources.resources import DataMgr
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtimg import QtImgMgr
from src.qt.com.qtloading import QtLoading
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log, ToolUtil
from src.util.status import Status
from ui.bookinfo import Ui_BookInfo
from ui.gameinfo import Ui_GameInfo
from ui.qtlistwidget import QtBookList


class QtGameInfo(QtWidgets.QWidget, Ui_GameInfo, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.loadingForm = QtLoading(self)
        self.gameId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.pictureData = None

        self.msgForm = QtBubbleLabel(self)
        self.picture.installEventFilter(self)
        self.title.setWordWrap(True)
        self.title.setContextMenuPolicy(Qt.CustomContextMenu)
        self.title.customContextMenuRequested.connect(self.CopyTitle)

        self.description.setContextMenuPolicy(Qt.CustomContextMenu)
        self.description.customContextMenuRequested.connect(self.CopyDescription)

        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignTop)

        self.description.adjustSize()
        self.title.adjustSize()

        self.epsListWidget.setFlow(self.epsListWidget.TopToBottom)
        self.epsListWidget.setFrameShape(self.epsListWidget.NoFrame)
        self.epsListWidget.setResizeMode(self.epsListWidget.Adjust)
        self.epsListWidget.doubleClicked.connect(self.OpenListPicture)
        QScroller.grabGesture(self.epsListWidget, QScroller.LeftMouseButtonGesture)
        self.epsListWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.epsListWidget.verticalScrollBar().setStyleSheet(QssDataMgr().GetData('qt_list_scrollbar'))
        self.epsListWidget.verticalScrollBar().setSingleStep(30)

        self.listWidget.InitUser(self.LoadNextPage)
        self.listWidget.doubleClicked.connect(self.OpenCommentInfo)

        self.childrenListWidget = QtBookList(None)
        self.childrenListWidget.InitUser(self.LoadChildrenNextPage)

        self.childrenWidget = QtWidgets.QWidget()
        self.androidLink = ""
        self.iosLink = ""
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

        self.commentButton.clicked.connect(self.SendComment)
        self.listPictureInfo = {}

        # self.epsListWidget.clicked.connect(self.OpenReadImg)
        p = QPixmap()
        p.loadFromData(DataMgr().GetData("icon_game_recommend"))
        self.icon_1.setPixmap(p)
        p = QPixmap()

        p.loadFromData(DataMgr().GetData("icon_adult"))
        self.icon_2.setPixmap(p)

        p = QPixmap()
        p.loadFromData(DataMgr().GetData("icon_game_android"))
        self.icon_3.setPixmap(p)

        p = QPixmap()
        p.loadFromData(DataMgr().GetData("icon_game_ios"))
        self.icon_4.setPixmap(p)
        self.icon_1.setScaledContents(True)
        self.icon_2.setScaledContents(True)
        self.icon_3.setScaledContents(True)
        self.icon_4.setScaledContents(True)
        ToolUtil.SetIcon(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.stackedWidget.currentIndex() == 1:
            self.stackedWidget.setCurrentIndex(0)
            a0.ignore()
        else:
            a0.accept()

    def CopyTitle(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.title.text())
        self.msgForm.ShowMsg("复制标题")
        return

    def CopyIos(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.iosLink)
        self.msgForm.ShowMsg("复制Ios下载地址")
        return

    def CopyAndroid(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.androidLink)
        self.msgForm.ShowMsg("复制Android下载地址")
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
        self.listPictureInfo.clear()
        self.ClearCommnetList()
        self.icon_1.setVisible(False)
        self.icon_2.setVisible(False)
        self.icon_3.setVisible(False)
        self.icon_4.setVisible(False)

    def CopyDescription(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.description.text())
        self.msgForm.ShowMsg("复制描述")
        return


    def OpenBook(self, gameId):
        self.gameId = gameId
        self.setWindowTitle(self.gameId)
        self.setFocus()

        self.Clear()
        self.show()
        self.loadingForm.show()
        self.AddHttpTask(req.GetGameInfoReq(gameId), self.OpenBookBack)

    def close(self):
        super(self.__class__, self).close()

    def OpenBookBack(self, data):
        self.loadingForm.close()
        self.listWidget.UpdatePage(1, 1)
        self.childrenListWidget.UpdatePage(1, 1)
        self.childrenListWidget.UpdateState()
        self.listWidget.UpdateState()
        try:

            data = json.loads(data)
            title = data.get("data").get("game").get("title")
            description = data.get("data").get("game").get("description")
            self.title.setText(title)
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.title.setFont(font)

            if data.get("data").get("game").get("suggest"):
                self.icon_1.setVisible(True)
            if data.get("data").get("game").get("adult"):
                self.icon_2.setVisible(True)
            if data.get("data").get("game").get("android"):
                self.icon_3.setVisible(True)
            if data.get("data").get("game").get("ios"):
                self.icon_4.setVisible(True)
            self.description.setText(description)
            self.picture.setText("图片加载中...")
            fileServer = data.get("data").get("game").get("icon").get("fileServer")
            path = data.get("data").get("game").get("icon").get("path")
            self.url = fileServer
            self.path = path

            androidLiks = data.get("data").get("game").get("androidLinks")
            if not androidLiks:
                self.androidButton.setEnabled(False)
            else:
                self.androidButton.setEnabled(True)
                self.androidLink = androidLiks[0]

            iosLinks = data.get("data").get("game").get("iosLinks")
            if not iosLinks:
                self.iosButton.setEnabled(False)
            else:
                self.iosButton.setEnabled(True)
                self.iosLink = androidLiks[0]

            dayStr = ToolUtil.GetUpdateStr(data.get("data").get("game").get("updated_at"))
            self.updateTick.setText(dayStr + "更新")
            if config.IsLoadingPicture:
                self.AddDownloadTask(fileServer, path, completeCallBack=self.UpdatePicture)
            self.AddHttpTask(req.GetGameCommentsReq(self.gameId), self.GetCommnetBack)
            for index, pic in enumerate(data.get("data").get("game").get("screenshots", [])):
                item = QListWidgetItem(self.epsListWidget)
                self.epsListWidget.setItemWidget(item, QLabel("图片加载中"))
                self.epsListWidget.addItem(item)
                self.AddDownloadTask(pic.get("fileServer"), pic.get("path"), completeCallBack=self.UpdateListPicture, backParam=index)
        except Exception as es:
            Log.Error(es)
        return

    def UpdatePicture(self, data, status):
        if status == Status.Ok:
            self.pictureData = data
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            newPic = pic.scaled(self.picture.size(), QtCore.Qt.KeepAspectRatio,  Qt.SmoothTransformation)
            self.picture.setPixmap(newPic)
            # self.picture.setScaledContents(True)
            self.update()
        else:
            self.picture.setText("图片加载失败")
        return

    def UpdateListPicture(self, data, status, backId):
        item = self.epsListWidget.item(backId)
        if not item:
            return
        widget = self.epsListWidget.itemWidget(item)
        if not widget:
            return

        if status == Status.Ok:
            # self.pictureData = data
            self.listPictureInfo[backId] = data
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            newPic = pic.scaled(QSize(self.width()-40, 300), QtCore.Qt.KeepAspectRatio,  Qt.SmoothTransformation)
            widget.setPixmap(newPic)

            item.setSizeHint(widget.sizeHint())
            self.epsListWidget.update()
        else:
            widget.setText("图片加载失败")
        return

    def OpenListPicture(self, modelIndex):
        index = modelIndex.row()
        item = self.listWidget.item(index)
        if not item:
            return
        data = self.listPictureInfo.get(index)
        if not data:
            return
        QtImgMgr().ShowImg(data)

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

    def LoadNextPage(self):
        self.loadingForm.show()
        self.AddHttpTask(req.GetGameCommentsReq(self.gameId, self.listWidget.page + 1), self.GetCommnetBack)
        return

    def SendComment(self):
        data = self.commentLine.text()
        if not data:
            return
        self.commentLine.setText("")
        self.loadingForm.show()
        self.AddHttpTask(req.SendGameCommentsReq(self.gameId, data), callBack=self.SendCommentBack)

    def SendCommentBack(self, msg):
        try:
            data = json.loads(msg)
            if data.get("code") == 200:
                self.ClearCommnetList()
                self.AddHttpTask(req.GetComments(self.gameId), self.GetCommnetBack)
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
