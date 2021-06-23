from PySide2 import QtWidgets
from PySide2.QtCore import QEvent, QProcess
from PySide2.QtGui import QPixmap, Qt, QIcon, QCursor
from PySide2.QtWidgets import QMenu, QApplication

from resources.resources import DataMgr
from src.qt.com.qtimg import QtImgMgr
from ui.chatrootmsg import Ui_ChatRoomMsg


class QtChatRoomMsg(QtWidgets.QWidget, Ui_ChatRoomMsg):
    def __init__(self, chatRoom):
        super(self.__class__, self).__init__()
        Ui_ChatRoomMsg.__init__(self)
        self.setupUi(self)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlag(Qt.Dialog)
        self.resize(400, 100)

        p = QPixmap()
        p.loadFromData(DataMgr().GetData("placeholder_avatar"))
        self.commentLabel.installEventFilter(self)
        self.picLabel.installEventFilter(self)
        self.data = None
        self.picData = None
        self.audioData = None
        self.picLabel.setPixmap(p)
        self.picLabel.setCursor(Qt.PointingHandCursor)
        self.picLabel.setScaledContents(True)
        self.picLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.commentLabel.setWordWrap(True)
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
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
        self.replayLabel.setStyleSheet("""
            border-image:url(resources/skin_aio_friend_bubble_pressed.9.png) 50;
            border-top-width: 20px;
            border-right-width: 20px;
            border-bottom-width: 10px;
            border-left-width: 20px;
            """)
        # self.commentLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # self.name.setTextInteractionFlags(Qt.TextSelectableByMouse)
        p = QPixmap()
        p.loadFromData(DataMgr().GetData("audio"))
        self.toolButton.setIcon(QIcon(p))
        self.popMenu = QMenu(self)

        action = self.popMenu.addAction("回复")
        action.triggered.connect(self.Reply)

        action = self.popMenu.addAction("@")
        action.triggered.connect(self.At)

        action = self.popMenu.addAction("复制")
        action.triggered.connect(self.CopyHandler)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenu)
        self.chatRoom = chatRoom

    def setParent(self, parent):
        self.chatRoom = None
        return super(self.__class__, self).setParent(parent)

    def SetPicture(self, data):
        self.picData = data
        self.picLabel.SetPicture(data)

    def SetHeadPicture(self, data):
        self.picLabel.SetPicture(self.picData, data)

    def SetPictureComment(self, data):
        pic = QPixmap()
        pic.loadFromData(data)
        self.data = data
        newPic = pic.scaled(500, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # print(newPic.height(), newPic.width())
        self.commentLabel.setCursor(Qt.PointingHandCursor)
        self.commentLabel.setScaledContents(True)
        self.commentLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.commentLabel.setPixmap(newPic)
        self.commentLabel.setMinimumSize(newPic.width(), newPic.height())
        self.commentLabel.setMaximumSize(newPic.width(), newPic.height())

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.picData and (obj == self.picLabel):
                    QtImgMgr().ShowImg(self.picData)
                elif self.data and obj == self.commentLabel:
                    QtImgMgr().ShowImg(self.data)
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

    def Reply(self):
        if self.chatRoom:
            self.chatRoom.SetReplyLabel(self.nameLabel.text(), self.commentLabel.text())
        return

    def At(self):
        if self.chatRoom:
            self.chatRoom.SetAtLabel(self.nameLabel.text())
        return

    def OpenAudioPath(self):
        if self.audioData:
            process = QProcess()
            path = "explorer.exe /select,\"{}\"".format(self.audioData)
            process.startDetached(path)
        return
