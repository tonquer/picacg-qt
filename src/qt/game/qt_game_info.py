
import json

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt, QSize, QEvent
from PySide2.QtGui import QFont, QPixmap
from PySide2.QtWidgets import QListWidgetItem, QLabel, QApplication, QScroller, QAbstractItemView

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


class QtGameInfo(QtWidgets.QWidget, Ui_GameInfo, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.loadingForm = QtLoading(self)
        self.commentWidget.InitReq(req.GetGameCommentsReq, req.SendGameCommentsReq, req.GameCommentsLikeReq)
        self.tabWidget.setCurrentIndex(0)
        self.gameId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.pictureData = None

        self.msgForm = QtBubbleLabel(self)
        self.picture.installEventFilter(self)
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.description.setTextInteractionFlags(Qt.TextBrowserInteraction)
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
        self.androidLink = ""
        self.iosLink = ""

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
        self.commentWidget.ClearCommnetList()
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
            self.commentWidget.bookId = self.gameId
            self.commentWidget.LoadComment()
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
        item = self.epsListWidget.item(index)
        if not item:
            return
        data = self.listPictureInfo.get(index)
        if not data:
            return
        QtImgMgr().ShowImg(data)

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
