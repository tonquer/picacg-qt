import re

from PySide2 import QtWidgets
from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QPixmap, QIcon

from resources.resources import DataMgr
from src.qt.com.qtimg import QtImgMgr
from src.qt.qtmain import QtOwner
from src.util import Log
from ui.comment import Ui_Comment
from ui.user_info import Ui_UserInfo


class QtUserInfo(QtWidgets.QWidget, Ui_UserInfo):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        Ui_Comment.__init__(self)
        self.setupUi(self)
        self.linkId = ""
        self.id = ""
        self.url = ""
        self.path = ""
        self.picIcon.SetPicture(DataMgr.GetData("placeholder_avatar"))

        p = QPixmap()
        p.loadFromData(DataMgr.GetData("icon_comic"))
        self.starButton.setIcon(QIcon(p.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.starButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.pictureData = None
        self.headData = None
        self.picIcon.installEventFilter(self)
        self.commentLabel.setWordWrap(True)
        self.nameLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.titleLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.commentLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.picIcon.setCursor(Qt.PointingHandCursor)

    def SetLike(self, isLike=True):
        p = QPixmap()
        if isLike:
            p.loadFromData(DataMgr.GetData("icon_comment_liked"))
        else:
            p.loadFromData(DataMgr.GetData("icon_comment_like"))
        nums = re.findall("\d+", self.starButton.text())
        if nums:
            num = int(nums[0]) + 1 if isLike else int(nums[0]) - 1
            self.starButton.setText("({})".format(str(num)))
        self.starButton.setIcon(QIcon(p.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))

    def SetPicture(self, data):
        self.pictureData = data
        self.picIcon.SetPicture(self.pictureData, self.headData)

    def SetHeadData(self, data):
        self.headData = data
        self.picIcon.SetPicture(self.pictureData, self.headData)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if obj == self.picIcon:
                    if self.pictureData:
                        QtImgMgr().ShowImg(self.pictureData)
                elif obj == self.nameLabel:
                    QtOwner().owner.searchForm.SearchCreator(self.nameLabel.text())
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def OpenComment(self):
        try:
            if self.parent().parent().OpenBack:
                self.parent().parent().OpenBack(self.id)
        except Exception as es:
            Log.Error(es)
        return

    def AddLike(self):
        try:
            if self.parent().parent().LikeBack:
                self.parent().parent().LikeBack(self.id)
        except Exception as es:
            Log.Error(es)
        return
