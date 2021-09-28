import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QSizeF, QRectF, QEvent, QPoint, QSize, QRect, QAbstractAnimation, QEasingCurve, \
    QPropertyAnimation
from PySide2.QtGui import QPainter, QColor, QPixmap, QFont, QFontMetrics, QPen, QBrush
from PySide2.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QFrame, QGraphicsItemGroup, QGraphicsItem, \
    QAbstractSlider, QAbstractItemView, QScroller, QLabel, QScrollArea, QScrollBar, QWidget, QVBoxLayout, \
    QScrollerProperties, QHBoxLayout, QGridLayout

from conf import config
from resources.resources import DataMgr
from src.qt.com.DWaterProgress import DWaterProgress
from src.qt.com.qt_git_label import QtGifLabel
from src.qt.com.qtmsg import QtMsgLabel
from src.qt.read.qtreadimg_scroll import ReadScrollArea
from src.qt.read.qtreadimg_tool import QtImgTool
from src.util.tool import time_me


class QtImgFrame(QFrame):
    def __init__(self, readImg):
        QFrame.__init__(self, readImg)
        self._readImg = weakref.ref(readImg)
        self.resize(readImg.width(), readImg.height())
        self.scrollArea = ReadScrollArea(self)
        self.qtTool = QtImgTool(self)
        self.qtTool.hide()
        self.helpLabel = QLabel(self)
        self.helpPixMap = QPixmap()
        self.helpLabel.installEventFilter(self)
        self.scaleCnt = 0
        self.startPos = QPoint()
        self.endPos = QPoint()
        self.process = DWaterProgress(self)
        self.waifu2xProcess = QtGifLabel(self)
        self.waifu2xProcess.setVisible(False)

        self.waifu2xProcess.Init(DataMgr.GetData("loading_gif"))
        self.downloadSize = 1
        self.downloadMaxSize = 1
        self.oldValue = 0
        self.baseValue = 0


    @property
    def readImg(self):
        return self._readImg()

    # def OnValueChange(self, value):
    #     self.UpdateScrollBar(value)
    #     return

    def InitHelp(self):

        self.resize(self.parent().width(), self.parent().height())
        label = self.helpLabel
        font = QFont()
        font.setPointSize(64)
        fm = QFontMetrics(font)
        label.resize(self.width(), self.height())
        p = QPixmap(self.width(), self.height())
        p.fill(Qt.transparent)
        painter = QPainter(p)
        # painter.setFont(font)
        # painter.drawText(rect, text)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.setBrush(QBrush(QColor(218, 84, 124, 100)))
        painter.drawRect(QRect(0, self.height() // 2, self.width() // 3, self.height() // 2))
        painter.drawRect(QRect(self.width() // 3 * 2, self.height() // 2, self.width() // 3, self.height() // 2))

        painter.drawRect(QRect(self.width() // 3 * 1, 0, self.width() // 3, self.height() // 2))
        painter.drawRect(QRect(self.width() // 3 * 1, self.height() // 2, self.width() // 3, self.height() // 2))

        painter.setBrush(QBrush(QColor(51, 200, 255, 100)))
        painter.drawRect(QRect(0, 0, self.width()//4, self.height() // 2))
        painter.drawRect(QRect(0, 0, self.width()//3*4, self.height() // 2))

        painter.setFont(font)
        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            nextPage = self.tr("上一页")
            lastPage = self.tr("下一页")
        else:
            lastPage = self.tr("上一页")
            nextPage = self.tr("下一页")
        # print(self.height(), self.width())
        painter.drawText(QRect(0, self.height() // 4 * 3, self.width() // 3, self.height() // 2), lastPage)
        painter.drawText(QRect(self.width() // 3 * 2, self.height() // 4 * 3, self.width() // 3, self.height() // 2),
                         nextPage)
        painter.drawText(QRect(0, self.height() // 4 * 1, self.width(), self.height()), self.tr("菜单"))
        painter.drawText(QRect(self.width()*2 // 3, self.height() // 4 * 1, self.width(), self.height()), self.tr("菜单"))

        if self.qtTool.stripModel in [ReadMode.UpDown, ReadMode.LeftRight]:
            painter.drawText(QRect(self.width() // 3, self.height() // 4 * 1, self.width(), self.height()), self.tr("上滑"))
            painter.drawText(QRect(self.width() // 3, self.height() // 4 * 3, self.width(), self.height()), self.tr("下滑"))
        self.helpPixMap = p
        label.setPixmap(p)
        label.setVisible(True)
        # p = QPixmap()
        # p.loadFromData(DataMgr().GetData("icon_picacg"))
        # label.setPixmap(p)
        return

    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.ScaleFrame()

    def ScaleFrame(self):
        size = self.size()
        w = size.width()
        h = size.height()
        self.scrollArea.setGeometry(0, 0, w, h)
        h2 = min(800, h)
        self.qtTool.setGeometry(w - 220, 0, 220, h2)

        # w = max((w - 150)//2, 0)
        # h = max((h - 150)//2, 0)
        self.process.setGeometry(w-150, h-150, 150, 150)
        self.waifu2xProcess.setGeometry(w-150, h-150, 150, 150)
        self.scrollArea.ResetLabelSize(self.qtTool.maxPic)
        return

    def UpdateProcessBar(self, info):
        if info:
            self.downloadSize = info.downloadSize
            self.downloadMaxSize = max(1, info.size)
            value = int((self.downloadSize / self.downloadMaxSize) * 100)
            # print(value)
            self.process.setValue(value)
        else:
            self.downloadSize = 0
            self.downloadMaxSize = 1
            self.process.setValue(0)

    def eventFilter(self, obj, ev) -> bool:
        # print(obj, ev.type())
        if obj == self.helpLabel:
            if ev.type() == QEvent.MouseButtonPress:
                if not self.helpLabel.isHidden():
                    self.helpLabel.hide()
                    return True
        return False