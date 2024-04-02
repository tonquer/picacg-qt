
import json

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QListWidgetItem, QLabel, QApplication, QScroller, QListView

from config.setting import Setting
from interface.ui_game_info import Ui_GameInfo
from qt_owner import QtOwner
from server import req, Status, Log, ToolUtil, config
from task.qt_task import QtTaskBase
from tools.str import Str


class GameInfoView(QtWidgets.QWidget, Ui_GameInfo, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_GameInfo.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.gameId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.pictureData = None

        self.picture.installEventFilter(self)
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.description.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.description.adjustSize()
        self.title.adjustSize()

        self.epsListWidget.setFlow(QListView.TopToBottom)
        self.epsListWidget.setFrameShape(QListView.NoFrame)
        self.epsListWidget.setResizeMode(QListView.Adjust)
        # self.epsListWidget.doubleClicked.connect(self.OpenListPicture)
        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.epsListWidget, QScroller.LeftMouseButtonGesture)
        # self.epsListWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.epsListWidget.verticalScrollBar().setStyleSheet(QssDataMgr().GetData('qt_list_scrollbar'))
        # self.epsListWidget.verticalScrollBar().setSingleStep(30)
        self.androidLink = ""
        self.iosLink = ""
        self.description.adjustSize()
        self.listPictureInfo = {}
        self.lastClick = 0
        self.lastIndex = -1
        self.epsListWidget.itemClicked.connect(self.ShowPicture)

        self.commentButton.clicked.connect(self.OpenComment)

    def ShowPicture(self, item):
        index = self.epsListWidget.row(item)
        data = self.listPictureInfo.get(index)
        if not data:
            return
        QtOwner().OpenWaifu2xTool(data)

    def OpenComment(self):
        if self.gameId:
            QtOwner().OpenGameComment(self.gameId)

    def CopyIos(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.iosLink)
        QtOwner().ShowMsg(Str.GetStr(Str.CopyIos))
        return

    def CopyAndroid(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.androidLink)
        QtOwner().ShowMsg(Str.GetStr(Str.CopyAndroid))
        return

    # def OpenAutor(self):
    #     text = self.autor.text()
    #     self.owner().userForm.listWidget.setCurrentRow(0)
    #     self.owner().searchForm.searchEdit.setText(text)
    #     self.owner().searchForm.Search()
    #     return

    def Clear(self):
        self.ClearTask()
        self.epsListWidget.clear()
        self.listPictureInfo.clear()
        self.icon_1.setVisible(False)
        self.icon_2.setVisible(False)
        self.icon_3.setVisible(False)
        self.icon_4.setVisible(False)

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        if bookId:
            self.OpenBook(bookId)
        pass

    def OpenBook(self, gameId):
        self.gameId = gameId
        self.setFocus()

        self.Clear()
        self.show()
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetGameInfoReq(gameId), self.OpenBookBack)

    def OpenBookBack(self, raw):
        QtOwner().CloseLoading()
        try:
            st = raw["st"]
            if st == Status.Ok:
                data = json.loads(raw["data"])
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
                self.description.setPlainText(description)
                self.picture.setText(Str.GetStr(Str.LoadingPicture))
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
                self.updateTick.setText(dayStr + Str.GetStr(Str.Update))
                if config.IsLoadingPicture:
                    url = ToolUtil.GetRealUrl(fileServer, path)
                    path = ToolUtil.GetRealPath(self.gameId, "game/{}".format(self.gameId))
                    self.AddDownloadTask(url, path, completeCallBack=self.UpdatePicture)
                for index, pic in enumerate(data.get("data").get("game").get("screenshots", [])):
                    item = QListWidgetItem(self.epsListWidget)
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                    self.epsListWidget.setItemWidget(item, QLabel(Str.GetStr(Str.LoadingPicture)))
                    self.epsListWidget.addItem(item)
                    url = ToolUtil.GetRealUrl(pic.get("fileServer"), pic.get("path"))
                    path = ToolUtil.GetMd5RealPath(url, "game/{}".format(self.gameId))
                    self.AddDownloadTask(url, path, completeCallBack=self.UpdateListPicture, backParam=index)
            else:
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
        return

    def UpdatePicture(self, data, status):
        if status == Status.Ok:
            self.pictureData = data
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            radio = self.devicePixelRatio()
            pic.setDevicePixelRatio(radio)
            newPic = pic.scaled(self.picture.size()*radio, QtCore.Qt.KeepAspectRatio,  Qt.SmoothTransformation)
            self.picture.setPixmap(newPic)
            # self.picture.setScaledContents(True)
        else:
            self.picture.setText(Str.GetStr(status))
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
            pic.setDevicePixelRatio(self.devicePixelRatio())
            newPic = pic.scaled(QSize(self.width()-40, 300), QtCore.Qt.KeepAspectRatio,  Qt.SmoothTransformation)
            widget.setPixmap(newPic)

            item.setSizeHint(widget.sizeHint())
        else:
            widget.setText(Str.GetStr(status))
        return

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.pictureData:
                    QtOwner().OpenWaifu2xTool(self.pictureData)
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)