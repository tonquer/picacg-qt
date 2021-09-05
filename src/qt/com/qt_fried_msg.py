import json

from PySide2 import QtWidgets
from PySide2.QtCore import QEvent
from PySide2.QtGui import QPixmap, Qt, QIcon, QCursor
from PySide2.QtWidgets import QMenu, QApplication

from resources.resources import DataMgr
from src.qt.com.qtimg import QtImgMgr
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import Server, req, Log, Status
from ui.chatrootmsg import Ui_ChatRoomMsg
from ui.fried_msg import Ui_FriedMsg


class QtFriedMsg(QtWidgets.QWidget, Ui_FriedMsg, QtTaskBase):
    def __init__(self, chatRoom):
        super(self.__class__, self).__init__()
        Ui_ChatRoomMsg.__init__(self)
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
        self.picLabel.SetPicture(DataMgr().GetData("placeholder_avatar"))
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
        p = QPixmap()
        p.loadFromData(DataMgr.GetData("icon_comment_like"))
        q = QPixmap()
        q.loadFromData(DataMgr.GetData("icon_comment_reply"))
        self.likeButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.likeButton.setIcon(QIcon(p))
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commentButton.setIcon(QIcon(q))
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
        newPic = pic.scaled(500, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # print(newPic.height(), newPic.width())
        self.replayLabel.setCursor(Qt.PointingHandCursor)
        self.replayLabel.setScaledContents(True)
        self.replayLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.replayLabel.setPixmap(newPic)
        self.replayLabel.setMinimumSize(newPic.width(), newPic.height())
        self.replayLabel.setMaximumSize(newPic.width(), newPic.height())
        self.replayLabel.setVisible(True)
        self.listWidget.setVisible(False)
        self.listWidget.InitUser(self.LoadNextPage)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.picData and (obj == self.picLabel):
                    QtImgMgr().ShowImg(self.picData)
                elif self.data and obj == self.replayLabel:
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

    def Clear(self):
        self.listWidget.clear()

    def OpenAudioPath(self):
        return

    def OpenComment(self):
        if not self.listWidget.isVisible():
            QtOwner().owner.loadingForm.show()
            self.AddHttpTask(req.AppCommentInfoReq(self.id, Server().token), self.LoadBack)
        else:
            self.listWidget.setVisible(False)
        return

    def LoadBack(self, data):
        QtOwner().owner.loadingForm.close()
        errMsg = ""
        try:
            data = json.loads(data)
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
            QtOwner().owner.msgForm.ShowMsg(QtOwner().owner.GetStatusStr(Status.UnKnowError) + errMsg)
        return

    def LoadNextPage(self):
        self.page += 1
        QtOwner().owner.loadingForm.show()
        self.AddHttpTask(req.AppCommentInfoReq(self.id, Server().token, (self.page - 1)*self.limit), self.LoadBack)
        return