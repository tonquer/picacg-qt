from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtWidgets import QWidget

from interface.ui_comic_item import Ui_ComicItem
from tools.str import Str


class ComicItemWidget(QWidget, Ui_ComicItem):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_ComicItem.__init__(self)
        self.setupUi(self)
        self.picData = None
        self.id = ""
        self.url = ""
        self.path = ""
        # TODO 如何自适应
        self.picLabel.setFixedSize(300, 400)
        # self.picLabel.setMinimumSize(300, 400)
        # self.picLabel.setMaximumSize(220, 308)

        # self.categoryLabel.setMinimumSize(210, 25)
        # self.categoryLabel.setMaximumSize(210, 150)

        self.starButton.setIcon(QIcon(":/png/icon/icon_bookmark_on.png"))
        self.starButton.setIconSize(QSize(20, 20))
        self.starButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.starButton.setMinimumHeight(24)
        self.timeLabel.setMinimumHeight(24)

        self.starButton.setMaximumWidth(280)
        self.timeLabel.setMaximumWidth(280)

        # self.nameLable.setMinimumSize(210, 25)
        # self.nameLable.setMaximumSize(210, 150)
        self.nameLable.setMaximumWidth(280)
        self.nameLable.adjustSize()
        self.nameLable.setWordWrap(True)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.nameLable.setFont(font)
        self.adjustSize()

    def GetTitle(self):
        return self.nameLable.text()

    def SetPicture(self, data):
        self.picData = data
        pic = QPixmap()
        if data:
            pic.loadFromData(data)
        newPic = pic.scaled(self.picLabel.width(), self.picLabel.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.picLabel.setPixmap(newPic)

    def SetPictureErr(self):
        self.picLabel.setText(Str.GetStr(Str.LoadingFail))