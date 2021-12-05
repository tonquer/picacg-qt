from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtWidgets import QWidget

from config.setting import Setting
from interface.ui_comic_item import Ui_ComicItem
from tools.str import Str


class ComicItemWidget(QWidget, Ui_ComicItem):
    def __init__(self, isCategory=False):
        QWidget.__init__(self)
        Ui_ComicItem.__init__(self)
        self.setupUi(self)
        self.picData = None
        self.id = ""
        self.url = ""
        self.path = ""
        # TODO 如何自适应
        if not isCategory:
            rate = Setting.CoverSize.value
            baseW = 250
            baseH = 340
        else:
            rate = Setting.CategorySize.value
            baseW = 300
            baseH = 300

        width = baseW * rate / 100
        height = baseH * rate / 100

        self.picLabel.setFixedSize(width, height)
        # self.picLabel.setMinimumSize(300, 400)
        # self.picLabel.setMaximumSize(220, 308)

        # self.categoryLabel.setMinimumSize(210, 25)
        # self.categoryLabel.setMaximumSize(210, 150)

        self.starButton.setIcon(QIcon(":/png/icon/icon_bookmark_on.png"))
        self.starButton.setIconSize(QSize(20, 20))
        self.starButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.starButton.setMinimumHeight(24)
        self.timeLabel.setMinimumHeight(24)

        self.categoryLabel.setMaximumWidth(width-20)
        self.starButton.setMaximumWidth(width-20)
        self.timeLabel.setMaximumWidth(width-20)

        # self.nameLable.setMinimumSize(210, 25)
        # self.nameLable.setMaximumSize(210, 150)
        self.nameLable.setMaximumWidth(width-20)
        self.nameLable.adjustSize()
        self.nameLable.setWordWrap(True)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.nameLable.setFont(font)
        self.adjustSize()
        self.isWaifu2x = False
        self.isWaifu2xLoading = False

    def GetTitle(self):
        return self.nameLable.text()

    def SetPicture(self, data):
        self.picData = data
        pic = QPixmap()
        if data:
            pic.loadFromData(data)
        self.isWaifu2x = False
        self.isWaifu2xLoading = False
        radio = self.devicePixelRatio()
        pic.setDevicePixelRatio(radio)
        newPic = pic.scaled(self.picLabel.width() * radio, self.picLabel.height() * radio, Qt.KeepAspectRatio,
                            Qt.SmoothTransformation)
        self.picLabel.setPixmap(newPic)

    def SetWaifu2xData(self, data):
        pic = QPixmap()
        if not data:
            return
        self.isWaifu2x = True
        self.isWaifu2xLoading = False
        pic.loadFromData(data)
        radio = self.devicePixelRatio()
        pic.setDevicePixelRatio(radio)
        newPic = pic.scaled(self.picLabel.width()*radio, self.picLabel.height()*radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.picLabel.setPixmap(newPic)

    def SetPictureErr(self):
        self.picLabel.setText(Str.GetStr(Str.LoadingFail))