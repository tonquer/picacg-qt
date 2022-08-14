import re

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QIcon

from config import config
from interface.ui_comment_item import Ui_CommentItem
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str


class CommentItemWidget(QtWidgets.QWidget, Ui_CommentItem):
    PicLoad = Signal(int)

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        Ui_CommentItem.__init__(self)
        self.setupUi(self)
        self.linkId = ""
        self.id = ""
        self.url = ""
        self.path = ""
        self.character = ""
        self.index = 0
        self.isGame = False

        self.picIcon.setCursor(Qt.PointingHandCursor)
        self.picIcon.setScaledContents(True)
        self.picIcon.setWordWrap(True)
        self.picIcon.setPixmap(QPixmap(":/png/icon/placeholder_avatar"))
        self.starButton.setIcon(QIcon(":/png/icon/icon_comment_like"))
        self.starButton.setIconSize(QSize(30, 30))

        self.starButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commentButton.setIcon(QIcon(":/png/icon/icon_comment_reply"))
        self.commentButton.setIconSize(QSize(30, 30))
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.pictureData = None
        self.headData = None
        self.picIcon.installEventFilter(self)
        self.commentLabel.setWordWrap(True)
        self.nameLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.titleLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.commentLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        # self.nameLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.linkLabel.setWordWrap(True)
        self.linkLabel.setVisible(False)
        self.linkLabel.installEventFilter(self)
        self.starButton.setCursor(Qt.PointingHandCursor)
        # self.nameLabel.setCursor(Qt.PointingHandCursor)
        self.commentButton.setCursor(Qt.PointingHandCursor)
        self.killButton.setVisible(False)
        # q = QPixmap()
        # q.loadFromData(DataMgr.GetData("icon_comment_reply"))
        # self.killButton.setIcon(QIcon(p.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.killButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.killButton.setCursor(Qt.PointingHandCursor)
        self.isLoadPicture = False

    def SetLike(self, isLike=True):
        p = QPixmap()
        if isLike:
            p.load(":/png/icon/icon_comment_liked.png")
        else:
            p.load(":/png/icon/icon_comment_like.png")
        nums = re.findall("\d+", self.starButton.text())
        if nums:
            num = int(nums[0]) + 1 if isLike else int(nums[0]) - 1
            self.starButton.setText("({})".format(str(num)))
        self.starButton.setIcon(QIcon(p.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.starButton.setChecked(isLike)

    def SetPicture(self, data):
        self.pictureData = data
        self.picIcon.SetPicture(self.pictureData, self.headData)

    def SetPictureErr(self, status):
        self.picIcon.setText(Str.GetStr(status))

    def SetHeadData(self, data):
        self.headData = data
        self.picIcon.SetPicture(self.pictureData, self.headData)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if obj == self.picIcon:
                    if self.pictureData:
                        QtOwner().OpenWaifu2xTool(self.pictureData)
                elif obj == self.linkLabel and self.linkId:
                    if self.isGame:
                        QtOwner().OpenGameInfo(self.linkId)
                    else:
                        QtOwner().OpenBookInfo(self.linkId)
                elif obj == self.nameLabel:
                    QtOwner().OpenSearchByCreate(self.nameLabel.text())
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def OpenComment(self):
        QtOwner().OpenSubComment(self.id, self)

    def KillComment(self):
        try:
            if self.parent().parent().KillBack:
                self.parent().parent().KillBack(self.id)
        except Exception as es:
            Log.Error(es)
        return

    def paintEvent(self, event) -> None:
        if self.url and not self.isLoadPicture and config.IsLoadingPicture:
            self.isLoadPicture = True
            self.PicLoad.emit(self.index)