from PySide2 import QtWidgets
from PySide2.QtCore import QEvent
from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWebSockets import QWebSocket

from src.qt.com.qtimg import QtImgMgr
from src.util import Log
from ui.chatrootmsg import Ui_ChatRoomMsg


class QtChatRoomMsg(QtWidgets.QWidget, Ui_ChatRoomMsg):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_ChatRoomMsg.__init__(self)
        self.setupUi(self)
        p = QPixmap("resources/placeholder_avatar.png")
        self.commentLabel.installEventFilter(self)
        self.picLabel.installEventFilter(self)
        self.picLabel.setPixmap(p)
        self.picLabel.setCursor(Qt.PointingHandCursor)
        self.picLabel.setScaledContents(True)
        self.commentLabel.setWordWrap(True)
        self.widget.setStyleSheet(""".QWidget{
            border-image:url(resources/skin_aio_friend_bubble_pressed.9.png) 50;
            border-top-width: 20px;
            border-right-width: 20px;
            border-bottom-width: 10px;
            border-left-width: 20px;}
            """)
        self.replayLabel.setWordWrap(True)
        self.replayLabel.setStyleSheet("""
            border-image:url(resources/skin_aio_friend_bubble_pressed.9.png) 50;
            border-top-width: 20px;
            border-right-width: 20px;
            border-bottom-width: 10px;
            border-left-width: 20px;
            """)

    def SetPicture(self, data):
        pic = QPixmap()
        pic.loadFromData(data)
        self.picLabel.setPixmap(pic)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if obj.pixmap() and not obj.text():
                    QtImgMgr().ShowImg(obj.pixmap())
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)
