import weakref

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, QProcess, QFile
from PySide6.QtGui import QPixmap, Qt, QIcon, QCursor, QFont
from PySide6.QtWidgets import QMenu, QApplication

from interface.ui_chat_new_room_msg import Ui_ChatNewRoomMsg
from qt_owner import QtOwner


class ChatNewMsgWidget(QtWidgets.QWidget, Ui_ChatNewRoomMsg):
    def __init__(self, chatRoom):
        super(self.__class__, self).__init__()
        Ui_ChatNewRoomMsg.__init__(self)
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
        self.pic2Label.installEventFilter(self)
        self.replyPic.installEventFilter(self)
        self.picLabel.installEventFilter(self)
        self.data = None
        self.replyData = None
        self.picData = None
        self.audioData = None
        self.rawMsg = {}

        self.userId = ""
        # self.picLabel.setPixmap(p)
        self.picLabel.setCursor(Qt.PointingHandCursor)
        self.picLabel.setScaledContents(True)
        self.picLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.commentLabel.setWordWrap(True)
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

        # action = self.popMenu.addAction("悄悄话")
        # action.triggered.connect(self.AtPrivate)

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
        self.pic2Label.setCursor(Qt.PointingHandCursor)
        self.pic2Label.setScaledContents(True)
        self.pic2Label.setAttribute(Qt.WA_TranslucentBackground)
        self.pic2Label.setPixmap(newPic)
        self.pic2Label.setMinimumSize(newPic.width(), newPic.height())
        self.pic2Label.setMaximumSize(newPic.width(), newPic.height())

    def SetPictureDefault(self):
        f = QFile(u":/png/icon/icon_question_error.png")
        f.open(QFile.ReadOnly)
        pic = QPixmap()
        pic.loadFromData(f.readAll())
        f.close()
        pic.setDevicePixelRatio(self.devicePixelRatio())
        newPic = pic.scaled(500, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # print(newPic.height(), newPic.width())
        self.pic2Label.setCursor(Qt.PointingHandCursor)
        self.pic2Label.setScaledContents(True)
        self.pic2Label.setAttribute(Qt.WA_TranslucentBackground)
        self.pic2Label.setPixmap(newPic)
        self.pic2Label.setMinimumSize(newPic.width(), newPic.height())
        self.pic2Label.setMaximumSize(newPic.width(), newPic.height())

    def SetReplyPictureComment(self, data):
        pic = QPixmap()
        pic.loadFromData(data)
        pic.setDevicePixelRatio(self.devicePixelRatio())
        self.replyData = data
        newPic = pic.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # print(newPic.height(), newPic.width())
        self.replyPic.setCursor(Qt.PointingHandCursor)
        self.replyPic.setScaledContents(True)
        self.replyPic.setAttribute(Qt.WA_TranslucentBackground)
        self.replyPic.setPixmap(newPic)
        self.replyPic.setMinimumSize(newPic.width(), newPic.height())
        self.replyPic.setMaximumSize(newPic.width(), newPic.height())

    def SetReplyPictureDefault(self):
        f = QFile(u":/png/icon/icon_question_error.png")
        f.open(QFile.ReadOnly)
        pic = QPixmap()
        pic.loadFromData(f.readAll())
        f.close()
        pic.setDevicePixelRatio(self.devicePixelRatio())
        newPic = pic.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # print(newPic.height(), newPic.width())
        self.replyPic.setCursor(Qt.PointingHandCursor)
        self.replyPic.setScaledContents(True)
        self.replyPic.setAttribute(Qt.WA_TranslucentBackground)
        self.replyPic.setPixmap(newPic)
        self.replyPic.setMinimumSize(newPic.width(), newPic.height())
        self.replyPic.setMaximumSize(newPic.width(), newPic.height())

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.picData and (obj == self.picLabel):
                    QtOwner().OpenWaifu2xTool(self.picData)
                    return True
                elif self.data and obj == self.pic2Label:
                    QtOwner().OpenWaifu2xTool(self.data)
                    return True
                elif self.replyData and obj == self.replyPic:
                    QtOwner().OpenWaifu2xTool(self.replyData)
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
            self.chatRoom.SetReplyLabel(self)
        return

    def At(self):
        if self.chatRoom:
            self.chatRoom.SetAtLabel(self)
        return

    # def AtPrivate(self):
    #     if self.chatRoom:
    #         self.chatRoom.SetAtPrivateLabel(self.nameLabel.text(), self)
    #     return

    def OpenAudioPath(self):
        if self.audioData:
            process = QProcess()
            path = "explorer.exe /select,\"{}\"".format(self.audioData)
            process.startDetached(path)
        return
