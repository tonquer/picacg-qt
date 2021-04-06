from PySide2 import QtWidgets
from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QPixmap

from resources.resources import DataMgr
from src.qt.com.qtimg import QtImgMgr
from ui.comment import Ui_Comment


class QtComment(QtWidgets.QWidget, Ui_Comment):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        Ui_Comment.__init__(self)
        self.setupUi(self)
        self.id = ""
        p = QPixmap()
        p.loadFromData(DataMgr.GetData("placeholder_avatar"))
        self.picIcon.setPixmap(p)
        self.picIcon.setCursor(Qt.PointingHandCursor)
        self.picIcon.setScaledContents(True)
        self.picIcon.setWordWrap(True)
        p = QPixmap()
        p.loadFromData(DataMgr.GetData("icon_comment_like"))
        q = QPixmap()
        q.loadFromData(DataMgr.GetData("icon_comment_reply"))
        self.pictureData = None
        self.starPic.setPixmap(p)
        self.starPic.setCursor(Qt.PointingHandCursor)
        self.starPic.setScaledContents(True)
        self.numPic.setPixmap(q)
        self.numPic.setCursor(Qt.PointingHandCursor)
        self.numPic.setScaledContents(True)
        self.picIcon.installEventFilter(self)
        self.commentLabel.setWordWrap(True)
        self.commentLabel.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        # self.nameLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def SetPicture(self, data):
        p = QPixmap()
        p.loadFromData(data)
        self.pictureData = data
        self.picIcon.setPixmap(p)

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