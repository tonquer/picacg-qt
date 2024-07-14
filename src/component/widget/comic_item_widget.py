from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QIcon, QFont, QFontMetrics, QImage
from PySide6.QtWidgets import QWidget

from config import config
from config.setting import Setting
from interface.ui_comic_item import Ui_ComicItem
from tools.str import Str


class ComicItemWidget(QWidget, Ui_ComicItem):
    PicLoad = Signal(int)

    def __init__(self, isCategory=False, isShiled=False):
        QWidget.__init__(self)
        Ui_ComicItem.__init__(self)
        self.setupUi(self)
        self.isShiled = isShiled
        self.picData = None
        self.id = ""
        self.title = ""
        self.picNum = 0
        self.category = ""

        self.index = 0
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

        icon2 = QIcon()
        icon2.addFile(u":/png/icon/new.svg", QSize(), QIcon.Normal, QIcon.Off)

        self.toolButton.setMinimumSize(QSize(0, 40))
        self.toolButton.setFocusPolicy(Qt.NoFocus)
        self.toolButton.setIcon(icon2)
        self.toolButton.setIconSize(QSize(32, 32))

        self.picLabel.setFixedSize(width, height)
        if self.isShiled:
            pic = QImage(":/png/icon/shiled.svg")
            radio = self.devicePixelRatio()
            pic.setDevicePixelRatio(radio)
            newPic = pic.scaled(self.picLabel.width() * radio, self.picLabel.height() * radio, Qt.KeepAspectRatio,
                                Qt.SmoothTransformation)
            newPic2 = QPixmap(newPic)
            self.picLabel.setPixmap(newPic2)

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
        self.isLoadPicture = False

    def SetTitle(self, title, fontColor):
        self.title = title
        if Setting.NotCategoryShow.value:
           self.categoryLabel.setVisible(False)

        if Setting.TitleLine.value == 0:
            self.nameLable.setVisible(False)
        elif Setting.TitleLine.value == 1:
            self.nameLable.setWordWrap(False)
            self.nameLable.setText(title + fontColor)
        elif Setting.TitleLine.value > 3:
            self.nameLable.setText(title+fontColor)
        else:
            title2 = self.ElidedLineText(fontColor)
            self.nameLable.setText(title2)

    def ElidedLineText(self, fontColor):
        line = Setting.TitleLine.value
        if line <= 0 :
            line = 2
        f = QFontMetrics(self.nameLable.font())
        if (line == 1):
            return f.elidedText(self.title + fontColor, Qt.ElideRight, self.nameLable.maximumWidth())

        strList = []
        start = 0
        isEnd = False
        for i in range(1, len(self.title)):
            if f.boundingRect(self.title[start:i]).width() >= self.nameLable.maximumWidth()-10:
                strList.append(self.title[start:i])
                if len(strList) >= line:
                    isEnd = True
                    break
                start = i

        if not isEnd:
            strList.append(self.title[start:])

        if not strList:
            strList.append(self.title)

        # strList[-1] = strList[-1] + fontColor

        hasElided = True
        endIndex = len(strList) - 1
        endString = strList[endIndex]
        if f.boundingRect(endString).width() < self.nameLable.maximumWidth() -10:
            strList[endIndex] += fontColor
            hasElided = False

        if (hasElided):
            if len(endString) > 8 :
                endString = endString[0:len(endString) - 8] + "..." + fontColor
                strList[endIndex] = endString
            else:
                strList[endIndex] += fontColor
        return "".join(strList)

    def GetTitle(self):
        return self.title

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

    def SetPictureErr(self, status):
        self.picLabel.setText(Str.GetStr(status))

    def paintEvent(self, event) -> None:
        if self.isShiled:
            return
        if self.url and not self.isLoadPicture and config.IsLoadingPicture:
            self.isLoadPicture = True
            self.PicLoad.emit(self.index)