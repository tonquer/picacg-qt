import weakref

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, QProcess, QFile
from PySide6.QtGui import QPixmap, Qt, QIcon, QCursor, QFont
from PySide6.QtWidgets import QMenu, QApplication

from interface.ui_chat_room_msg import Ui_ChatRoomMsg
from qt_owner import QtOwner


class ChatMsgWidget(QtWidgets.QWidget, Ui_ChatRoomMsg):
    def __init__(self, chatRoom):
        super(self.__class__, self).__init__()
        Ui_ChatRoomMsg.__init__(self)
        self.setupUi(self)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlag(Qt.Dialog)
        self.resize(400, 100)
        self.setWindowTitle("PicACG")
        self.setWindowIcon(QIcon(":/png/icon/logo_round.png"))
        f = QFile(u":/png/icon/placeholder_avatar.png")
        f.open(QFile.ReadOnly)
        self.picLabel.SetPicture(f.readAll())
        f.close()

        # p = QPixmap()
        # p.loadFromData(DataMgr().GetData("placeholder_avatar"))
        self.commentLabel.installEventFilter(self)
        self.picLabel.installEventFilter(self)
        self.data = None
        self.picData = None
        self.audioData = None
        self.userId = ""
        # self.picLabel.setPixmap(p)
        self.picLabel.setCursor(Qt.PointingHandCursor)
        self.picLabel.setScaledContents(True)
        self.picLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.commentLabel.setWordWrap(True)
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.replayLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.commentLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # self.setStyleSheet("""
        #     background:transparent;
        #     border:2px solid red;
        # """)
        # self.widget.setStyleSheet(""".QWidget{
        #     border-image:url(:png/icon/skin_aio_friend_bubble_pressed.9.png) 50;
        #     border-top-width: 25px;
        #     border-right-width: 25px;
        #     border-bottom-width: 25px;
        #     border-left-width: 25px;
        #     }
        #     """)
        self.replayLabel.setWordWrap(True)
        # font = QFont("MicrosoftYaHei", 14, 100)
        # self.replayLabel.setFont(font)
        # self.commentLabel.setFont(font)
        # self.replayLabel.setStyleSheet("""
        #     border-image:url(:png/icon/skin_aio_friend_bubble_pressed.9.png) 50;
        #     border-top-width: 25px;
        #     border-right-width: 25px;
        #     border-bottom-width: 25px;
        #     border-left-width: 25px;
        #     """)
        # self.commentLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # self.name.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # p = QPixmap()
        # p.loadFromData(DataMgr().GetData("audio"))
        # self.toolButton.setIcon(QIcon(p))
        self.popMenu = QMenu(self)

        action = self.popMenu.addAction("回复")
        action.triggered.connect(self.Reply)

        action = self.popMenu.addAction("@")
        action.triggered.connect(self.At)

        action = self.popMenu.addAction("复制")
        action.triggered.connect(self.CopyHandler)

        action = self.popMenu.addAction("悄悄话")
        action.triggered.connect(self.AtPrivate)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenu)
        self.__chatRoom = weakref.ref(chatRoom)

    @property
    def chatRoom(self):
        if not self.__chatRoom:
            return None
        return self.__chatRoom()

    def setParent(self, parent):
        self.__chatRoom = None
        return super(self.__class__, self).setParent(parent)

    def SetPicture(self, data):
        self.picData = data
        self.picLabel.SetPicture(data)

    def SetHeadPicture(self, data):
        self.picLabel.SetPicture(self.picData, data)

    def SetPictureComment(self, data):
        pic = QPixmap()
        pic.loadFromData(data)
        pic.setDevicePixelRatio(self.devicePixelRatio())
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
                    QtOwner().OpenWaifu2xTool(self.picData)
                    return True
                elif self.data and obj == self.commentLabel:
                    QtOwner().OpenWaifu2xTool(self.data)
                    return True
                return False
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

    def AtPrivate(self):
        if self.chatRoom:
            self.chatRoom.SetAtPrivateLabel(self.nameLabel.text(), self.userId)
        return

    def OpenAudioPath(self):
        if self.audioData:
            process = QProcess()
            path = "explorer.exe /select,\"{}\"".format(self.audioData)
            process.startDetached(path)
        return
