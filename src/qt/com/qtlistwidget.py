from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QColor, QIntValidator, QImage
from PySide2.QtWidgets import QListWidget, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QAbstractSlider, \
    QScroller, QGridLayout, QSpacerItem, QSizePolicy

from conf import config
from resources import resources
from src.qt.util.qttask import QtTask
from src.util import ToolUtil
from src.util.status import Status


class QtIntLimit(QIntValidator):
    def __init__(self, bottom, top, parent):
        super(self.__class__, self).__init__(bottom, top, parent)

    def fixup(self, input: str) -> str:
        return str(self.top())


class UserItemWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(UserItemWidget, self).__init__(*args, **kwargs)
        self.id = ""
        self.setMinimumSize(0, 180)
        self.setMaximumSize(16777215, 16777215)
        self.gridLayout = QGridLayout(self)
        hboxLayout = QHBoxLayout()
        self.gridLayout.addLayout(hboxLayout, 0, 0, 1, 1)


        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout2 = QHBoxLayout()

        self.indexLabel = QLabel("", self, styleSheet="color: #999999;")
        self.indexLabel.setMinimumSize(40, 0)
        self.indexLabel.setMaximumSize(40, 30)
        self.indexLabel.setAlignment(Qt.AlignLeft)

        self.timeLabel = QLabel("", self, styleSheet="color: #999999;")
        self.timeLabel.setMinimumSize(60, 0)
        self.timeLabel.setMaximumSize(60, 30)
        self.timeLabel.setAlignment(Qt.AlignRight)

        layout2.addWidget(self.indexLabel)
        layout2.addWidget(self.timeLabel)
        layout.addLayout(layout2)
        # layout.addWidget(self.timeLabel)

        # 图片label
        self.picIcon = QLabel(self)
        self.picIcon.setCursor(Qt.PointingHandCursor)
        self.picIcon.setScaledContents(True)
        self.picIcon.setMinimumSize(100, 100)
        self.picIcon.setMaximumSize(100, 100)
        pic = QPixmap()
        pic.loadFromData(resources.DataMgr.GetData("placeholder_avatar"))
        self.picIcon.setPixmap(pic)
        layout.addWidget(self.picIcon)

        self.label = QLabel("", self, styleSheet="color: #999999;")
        self.label.setMinimumSize(100, 0)
        self.label.setMaximumSize(100, 16777215)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        hboxLayout.addLayout(layout)

        layout3 = QVBoxLayout()
        self.commentLabel = QLabel(self)
        # self.commentLabel.setGeometry(QRect(328, 240, 329, 27 * 4))
        self.commentLabel.setWordWrap(True)
        layout3.addWidget(self.commentLabel)

        self.likeNum = QLabel(self)
        self.likeNum.setAlignment(Qt.AlignLeft)
        self.likeNum.setMaximumSize(16777215, 30)
        layout4 = QHBoxLayout()
        label = QLabel()
        label.setMaximumSize(30, 30)
        label.setCursor(Qt.PointingHandCursor)
        label.setScaledContents(True)
        data = resources.DataMgr.GetData("icon_comment_like")
        pixMap = QPixmap()
        pixMap.loadFromData(data)
        label.setPixmap(pixMap)

        layout4.addWidget(label)
        layout4.addWidget(self.likeNum)

        self.commentNum = QLabel(self)
        self.commentNum.setAlignment(Qt.AlignLeft)
        self.commentNum.setMaximumSize(16777215, 30)
        label = QLabel()
        label.setMaximumSize(40, 30)
        label.setCursor(Qt.PointingHandCursor)
        label.setScaledContents(True)
        data = resources.DataMgr.GetData("icon_comment_reply")
        pixMap = QPixmap()
        pixMap.loadFromData(data)
        label.setPixmap(pixMap)
        layout4.addWidget(label)
        layout4.addWidget(self.commentNum)
        space = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout4.addItem(space)
        layout3.addLayout(layout4)
        # self.commentLabel.setAlignment(Qt.AlignTop)
        hboxLayout.addLayout(layout3)

    def SetPicture(self, data):
        pic = QPixmap()
        pic.loadFromData(data)
        self.picIcon.setPixmap(pic)


class ItemWidget(QWidget):
    def __init__(self, _id, title, index, info, param, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        self.id = _id
        self.param = param
        self.setMaximumSize(220, 300)
        self.setMaximumSize(220, 300)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 0)
        # 图片label
        self.picIcon = QLabel(self)
        self.picIcon.setCursor(Qt.PointingHandCursor)
        self.picIcon.setScaledContents(True)
        self.picIcon.setMinimumSize(220, 220)
        self.picIcon.setMaximumSize(220, 220)
        self.picIcon.setToolTip(title)
        pic = QPixmap()
        self.picIcon.setPixmap(pic)
        layout.addWidget(self.picIcon)
        layout2 = QHBoxLayout(self)

        self.indexLabel = QLabel(index, self, styleSheet="color: #999999;")
        self.indexLabel.setMinimumSize(40, 20)
        self.indexLabel.setMaximumSize(40, 40)
        self.indexLabel.setAlignment(Qt.AlignLeft)
        layout2.addWidget(self.indexLabel)

        self.infoLabel = QLabel(info, self, styleSheet="color: #999999;")
        self.infoLabel.setMinimumSize(160, 20)
        self.infoLabel.setMaximumSize(160, 40)
        self.infoLabel.setAlignment(Qt.AlignRight)
        layout2.addWidget(self.infoLabel)

        layout.addLayout(layout2)

        self.label = QLabel(title, self, styleSheet="color: #999999;")
        self.label.setMinimumSize(220, 20)
        self.label.setMaximumSize(220, 40)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        # if self.info:
        #     self.PaintInfo()

    # def PaintInfo(self):
    #     painter = QPainter(self.picIcon)
    #     rect = self.picIcon.rect()
    #     painter.save()
    #     fheight = self.picIcon.fontMetrics().height()
    #     # 底部矩形框背景渐变颜色
    #     bottomRectColor = QLinearGradient(
    #         rect.width() / 2, rect.height() - 24 - fheight,
    #         rect.width() / 2, rect.height())
    #
    #     bottomRectColor.setSpread(QGradient.PadSpread)
    #     bottomRectColor.setColorAt(0, QColor(255, 255, 255, 70))
    #     bottomRectColor.setColorAt(1, QColor(0, 0, 0, 50))
    #
    #     # 画半透明渐变矩形框
    #     painter.setPen(Qt.NoPen)
    #     painter.setBrush(QBrush(bottomRectColor))
    #     painter.drawRect(rect.x(), rect.height() - 24 -
    #                      fheight, rect.width(), 24 + fheight)
    #     painter.restore()
    #     # 距离底部一定高度画文字
    #     font = self.picIcon.font() or QFont()
    #     font.setPointSize(8)
    #     painter.setFont(font)
    #     painter.setPen(Qt.white)
    #     rect.setHeight(rect.height() - 12)  # 底部减去一定高度
    #     painter.drawText(rect, Qt.AlignHCenter |
    #                      Qt.AlignBottom, self.info)

    def SetPicture(self, data):
        pic = QPixmap()
        pic.loadFromData(data)
        self.picIcon.setPixmap(pic)

    def GetTitle(self):
        return self.label.text()

    def GetId(self):
        return self.id


class QtBookList(QListWidget):
    def __init__(self, parent, name):
        QListWidget.__init__(self, parent)
        self.page = 1
        self.pages = 1
        self.name = name
        self.verticalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        self.isLoadingPage = False
        self.LoadCallBack = None
        self.parentId = -1

    def GetName(self):
        return self.name + "-QtBookList"

    def InitBook(self, callBack=None):
        self.resize(800, 600)
        self.setFrameShape(self.NoFrame)  # 无边框
        self.setFlow(self.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.LoadCallBack = callBack

    def InitUser(self, callBack=None):
        self.setFrameShape(self.NoFrame)  # 无边框
        self.LoadCallBack = callBack

    def OnActionTriggered(self, action):
        if action != QAbstractSlider.SliderMove or self.isLoadingPage:
            return
        if self.page >= self.pages:
            return
        if self.verticalScrollBar().sliderPosition() == self.verticalScrollBar().maximum():
            self.isLoadingPage = True
            if self.LoadCallBack:
                self.LoadCallBack()

    def UpdatePage(self, page, pages):
        self.page = page
        self.pages = pages

    def UpdateState(self, isLoading=False):
        self.isLoadingPage = isLoading

    def AddBookItem(self, _id, title, info="", url="", path="", param="", originalName=""):
        index = self.count()
        iwidget = ItemWidget(_id, title, str(index+1), info, param, self)
        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)
        iwidget.picIcon.setText("图片加载中...")
        if url and path and config.IsLoadingPicture:
            QtTask().AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True, self.GetName())
            pass

    def AddUserItem(self, commnetId, commentsCount, likesCount, content, name, createdTime, floor, url="", path="", originalName=""):
        index = self.count()
        iwidget = UserItemWidget(self)
        iwidget.id = commnetId
        iwidget.commentLabel.setText(content)
        iwidget.label.setText(name)
        iwidget.commentNum.setText("({})".format(commentsCount))
        iwidget.likeNum.setText("({})".format(likesCount))
        timeArray, day = ToolUtil.GetDateStr(createdTime)
        if day >= 1:
            iwidget.timeLabel.setText("{}天前".format(str(day)))
        else:
            strTime = "{}:{}:{}".format(timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)
            iwidget.timeLabel.setText("{}".format(strTime))

        iwidget.indexLabel.setText("{}楼".format(str(floor)))

        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)
        if url and path and config.IsLoadingPicture:
            QtTask().AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True, self.GetName())
            pass

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPicture(data)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.picIcon.setText("图片加载失败")
        return

    def clear(self) -> None:
        QListWidget.clear(self)

        # 防止异步加载时，信息错乱
        QtTask().CancelTasks(self.GetName())


class QtCategoryList(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setViewMode(self.ListMode)
        self.setFlow(self.LeftToRight)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(self.ScrollPerItem)
        QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)
        self.setMaximumHeight(30)
        self.setFocusPolicy(Qt.NoFocus)

    def AddItem(self, name):
        item = QListWidgetItem(name)
        item.setTextAlignment(Qt.AlignCenter)
        # item.setBackground(QColor(87, 195, 194))
        item.setBackground(QColor(0, 0, 0, 0))
        item.setSizeHint(QSize(90, 30))
        item.setFlags(item.flags() & (~Qt.ItemIsSelectable))

        self.addItem(item)

    def ClickItem(self, item):
        if item.background().color() == QColor(0, 0, 0, 0):
            item.setBackground(QColor(87, 195, 194))
            return True
        else:
            item.setBackground(QColor(0, 0, 0, 0))
            return False

    def GetAllSelectItem(self):
        data = set()
        for i in range(self.count()):
            item = self.item(i)
            if item.background().color() == QColor(87, 195, 194):
                data.add(item.text())
        return data
