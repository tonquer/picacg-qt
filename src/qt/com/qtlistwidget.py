import weakref

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QColor, QIntValidator,  QFont, QCursor
from PySide2.QtWidgets import QListWidget, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QAbstractSlider, \
    QScroller, QMenu, QApplication, QAbstractItemView

from conf import config
from src.qt.com.qtcomment import QtComment
from src.qt.com.qtimg import  QtImgMgr
from src.qt.util.qttask import QtTask
from src.util import ToolUtil
from src.util.status import Status


class QtIntLimit(QIntValidator):
    def __init__(self, bottom, top, parent):
        super(self.__class__, self).__init__(bottom, top, parent)

    def fixup(self, input: str) -> str:
        return str(self.top())


class ItemWidget(QWidget):
    def __init__(self, _id, title, index, info, param):
        super(ItemWidget, self).__init__()
        self.id = _id
        self.url = ""
        self.path = ""
        self.param = param
        self.setMaximumSize(220, 400)
        self.setMaximumSize(220, 400)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 0)
        # 图片label
        self.pictureData = None
        self.picIcon = QLabel(self)
        # self.picIcon.setCursor(Qt.PointingHandCursor)
        # self.picIcon.setScaledContents(True)
        self.picIcon.setMinimumSize(220, 320)
        self.picIcon.setMaximumSize(220, 320)
        self.picIcon.setToolTip(title)
        pic = QPixmap()
        self.picIcon.setPixmap(pic)
        layout.addWidget(self.picIcon)
        layout2 = QHBoxLayout()

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
        self.label.setMaximumSize(220, 50)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Microsoft YaHei",  12,   87))
        self.label.setWordWrap(True)
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
        if not data:
            return
        self.pictureData = data
        pic = QPixmap()
        pic.loadFromData(data)
        # maxW = self.picIcon.width()
        # maxH = self.picIcon.height()
        # picW = pic.width()
        # picH = pic.height()
        # if maxW / picW < maxH / picH:
        #     toW = maxW
        #     toH = (picH/(picW/maxW))
        # else:
        #     toH = maxH
        #     toW = (picW / (picH / maxH))
        newPic = pic.scaled(self.picIcon.width(), self.picIcon.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.picIcon.setPixmap(newPic)


    def GetTitle(self):
        return self.label.text()

    def GetId(self):
        return self.id


class QtBookList(QListWidget):
    def __init__(self, parent, name, owner):
        QListWidget.__init__(self, parent)
        self.page = 1
        self.pages = 1
        self.name = name
        self.verticalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        self.isLoadingPage = False
        self.LoadCallBack = None
        self.parentId = -1
        self.popMenu = None
        self.owner = weakref.ref(owner)

        QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def GetName(self):
        return self.name + "-QtBookList"

    def InitBook(self, callBack=None):
        self.resize(800, 600)
        self.setMinimumHeight(400)
        self.setFrameShape(self.NoFrame)  # 无边框
        self.setFlow(self.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.LoadCallBack = callBack

        self.popMenu = QMenu(self)
        action = self.popMenu.addAction("打开")
        action.triggered.connect(self.OpenBookInfoHandler)
        action = self.popMenu.addAction("查看封面")
        action.triggered.connect(self.OpenPicture)
        action = self.popMenu.addAction("重下封面")
        action.triggered.connect(self.ReDownloadPicture)
        action = self.popMenu.addAction("复制标题")
        action.triggered.connect(self.CopyHandler)
        action = self.popMenu.addAction("下载")
        action.triggered.connect(self.DownloadHandler)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.doubleClicked.connect(self.OpenBookInfo)
        self.customContextMenuRequested.connect(self.SelectMenu)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def InstallCategory(self):
        self.doubleClicked.disconnect(self.OpenBookInfo)
        self.popMenu = QMenu(self)
        action = self.popMenu.addAction("查看封面")
        action.triggered.connect(self.OpenPicture)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return

    def InstallDel(self):
        action = self.popMenu.addAction("刪除")
        action.triggered.connect(self.DelHandler)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def InitUser(self, callBack=None):
        self.setFrameShape(self.NoFrame)  # 无边框
        self.LoadCallBack = callBack
        self.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
        iwidget = ItemWidget(_id, title, str(index+1), info, param)
        iwidget.url = url
        iwidget.path = path
        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)
        iwidget.picIcon.setText("图片加载中...")
        if url and path and config.IsLoadingPicture:
            QtTask().AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True, self.GetName())
            pass

    def AddUserItem(self, commnetId, commentsCount, likesCount, content, name, createdTime, floor, url="", path="", originalName="", title="", level=1):
        index = self.count()
        iwidget = QtComment(self)
        iwidget.id = commnetId
        iwidget.commentLabel.setText(content)
        iwidget.nameLabel.setText(name)
        iwidget.numLabel.setText("({})".format(commentsCount))
        iwidget.starLabel.setText("({})".format(likesCount))
        iwidget.levelLabel.setText(" LV" + str(level) + " ")
        iwidget.titleLabel.setText(" " + title + " ")
        iwidget.url = url
        iwidget.path = path
        if createdTime:
            timeArray, day = ToolUtil.GetDateStr(createdTime)
            if day >= 1:
                iwidget.dateLabel.setText("{}天前".format(str(day)))
            else:
                strTime = "{}:{}:{}".format(timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)
                iwidget.dateLabel.setText("{}".format(strTime))

        iwidget.indexLabel.setText("{}楼".format(str(floor)))

        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)
        if url and config.IsLoadingPicture:
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

    def SelectMenu(self, pos):
        index = self.indexAt(pos)
        if index.isValid():
            self.popMenu.exec_(QCursor.pos())
        pass

    def DownloadHandler(self):
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            self.owner().epsInfoForm.OpenEpsInfo(widget.GetId())
        pass

    def OpenBookInfoHandler(self):
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            self.owner().bookInfoForm.OpenBook(widget.GetId())
            return

    def CopyHandler(self):
        selected = self.selectedItems()
        if not selected:
            return

        data = ''
        for item in selected:
            widget = self.itemWidget(item)
            data += widget.GetTitle() + str("\r\n")
        clipboard = QApplication.clipboard()
        data = data.strip("\r\n")
        clipboard.setText(data)
        pass

    def DelHandler(self):
        bookIds = set()
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            bookIds.add(widget.GetId())
        if not bookIds:
            return
        self.parent().DelCallBack(bookIds)

    def OpenBookInfo(self, modelIndex):
        index = modelIndex.row()
        item = self.item(index)
        if not item:
            return
        widget = self.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        self.owner().bookInfoForm.OpenBook(bookId)

    def OpenPicture(self):
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            QtImgMgr().ShowImg(widget.pictureData)
            return

    def ReDownloadPicture(self):
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            index = self.row(item)
            if widget.url and config.IsLoadingPicture:
                widget.picIcon.setPixmap(None)
                widget.picIcon.setText("图片加载中")
                QtTask().AddDownloadTask(widget.url, widget.path, None, self.LoadingPictureComplete, True, index, False,
                                         self.GetName())
                pass

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
