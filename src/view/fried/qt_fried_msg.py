import json

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent
from PySide6.QtGui import QPixmap, Qt, QIcon, QCursor
from PySide6.QtWidgets import QMenu, QApplication

from interface.ui_fried_msg import Ui_FriedMsg
from qt_owner import QtOwner
from server import req, Log, Status
from server.server import Server
from task.qt_task import QtTaskBase
from tools.str import Str


class QtFriedMsg(QtWidgets.QWidget, Ui_FriedMsg, QtTaskBase):
    def __init__(self, chatRoom):
        super(self.__class__, self).__init__()
        Ui_FriedMsg.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.id = ""
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlag(Qt.Dialog)
        self.resize(400, 100)

        # self.commentLabel.installEventFilter(self)
        self.picLabel.installEventFilter(self)
        self.replayLabel.installEventFilter(self)
        self.data = None
        self.picData = None
        self.headData = None
        self.picLabel.setPixmap(QPixmap(u":/png/icon/placeholder_avatar.png"))
        # self.picLabel.setCursor(Qt.PointingHandCursor)
        # self.picLabel.setScaledContents(True)
        # self.picLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.commentLabel.setWordWrap(True)
        # self.setStyleSheet("""
        #     background:transparent;
        #     border:2px solid red;
        # """)
        self.widget.setStyleSheet(""".QWidget{
            border-image:url(resources/skin_aio_friend_bubble_pressed.9.png) 50;
            border-top-width: 10px;
            border-right-width: 10px;
            border-bottom-width: 10px;
            border-left-width: 10px;
            }
            """)
        self.replayLabel.setWordWrap(True)
        # self.replayLabel.setStyleSheet("""
        #     border-image:url(resources/skin_aio_friend_bubble_pressed.9.png) 50;
        #     border-top-width: 20px;
        #     border-right-width: 20px;
        #     border-bottom-width: 10px;
        #     border-left-width: 20px;
        #     """)
        # self.commentLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # self.name.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.popMenu = QMenu(self)

        action = self.popMenu.addAction(self.tr("复制"))
        action.triggered.connect(self.CopyHandler)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenu)
        self.chatRoom = chatRoom
        self.likeButton.setIcon(QIcon(":/png/icon/icon_comment_like"))
        self.commentButton.setIcon(QIcon(":/png/icon/icon_comment_like"))
        self.likeButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.listWidget.setVisible(False)
        self.page = 1
        self.limit = 20

    def setParent(self, parent):
        self.chatRoom = None
        return super(self.__class__, self).setParent(parent)

    def SetPicture(self, data):
        self.picData = data
        self.picLabel.SetPicture(self.picData, self.headData)

    def SetHeadPicture(self, data):
        self.headData = data
        self.picLabel.SetPicture(self.picData, self.headData)

    def SetPictureComment(self, data):
        pic = QPixmap()
        pic.loadFromData(data)
        self.data = data
        # newPic = pic.scaled(500, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # print(newPic.height(), newPic.width())
        self.replayLabel.setCursor(Qt.PointingHandCursor)
        self.replayLabel.setScaledContents(True)
        self.replayLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.replayLabel.setMinimumSize(500, 400)
        self.replayLabel.setMaximumSize(500, 400)
        self.replayLabel.SetGifData(data, 500, 400)
        self.replayLabel.setVisible(True)
        self.listWidget.setVisible(False)
        # self.listWidget.InitUser(self.LoadNextPage)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.picData and (obj == self.picLabel):
                    QtOwner().OpenWaifu2xTool(self.picData)
                elif self.data and obj == self.replayLabel:
                    QtOwner().OpenWaifu2xTool(self.data)
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def SelectMenu(self, pos):
        self.popMenu.exec_(QCursor.pos())
        pass

    def CopyHandler(self):
        if self.commentLabel.text():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.commentLabel.text())
        return

    def Clear(self):
        self.listWidget.clear()

    def OpenAudioPath(self):
        return

    def OpenComment(self):
        if not self.listWidget.isVisible():
            QtOwner().ShowLoading()
            self.AddHttpTask(req.AppCommentInfoReq(self.id, Server().token), self.LoadBack)
        else:
            self.listWidget.setVisible(False)
        return

    def LoadBack(self, data):
        QtOwner().CloseLoading()
        errMsg = ""
        try:
            data = json.loads(data.get("data"))
            self.listWidget.UpdateState()
            errMsg = data.get("error", {}).get("message", "")
            self.limit = int(data.get('data').get("limit", 1))
            total = int(data.get('data').get("total", 1))
            pages = total//self.limit+1
            self.listWidget.UpdatePage(self.page, pages)
            for index, v in enumerate(data.get('data').get("comments")):
                floor = total - ((self.listWidget.page - 1) * self.limit + index)
                self.listWidget.AddUserItem(v, floor, True)

            self.listWidget.setVisible(True)
            self.page = self.listWidget.page
        except Exception as es:
            self.page = self.listWidget.page
            Log.Error(es)
            QtOwner().ShowError(Str.GetStr(Status.UnKnowError) + errMsg)
        return

    def LoadNextPage(self):
        self.page += 1
        QtOwner().CloseLoading()
        self.AddHttpTask(req.AppCommentInfoReq(self.id, Server().token, (self.page - 1)*self.limit), self.LoadBack)
        return
