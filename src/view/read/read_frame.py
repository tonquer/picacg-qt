import weakref

from PySide6.QtCore import Qt, QEvent, QPoint, QRect, QFile
from PySide6.QtGui import QPainter, QColor, QPixmap, QFont, QFontMetrics, QPen, QBrush
from PySide6.QtWidgets import QFrame, QLabel

from component.label.gif_label import GifLabel
from component.progress_bar.dwater_progress_bar import DWaterProgress
from tools.str import Str
from view.read.read_enum import ReadMode
from view.read.read_graphics import ReadGraphicsView
from view.read.read_tool import ReadTool


class ReadFrame(QFrame):
    def __init__(self, readImg):
        QFrame.__init__(self, readImg)
        self._readImg = weakref.ref(readImg)
        self.resize(readImg.width(), readImg.height())
        # self.scrollArea = ReadScrollArea(self)
        self.scrollArea = ReadGraphicsView(self)
        self.qtTool = ReadTool(self)
        self.qtTool.hide()
        self.helpLabel = QLabel(self)
        self.helpPixMap = QPixmap()
        self.helpLabel.installEventFilter(self)
        self.scaleCnt = 0
        self.startPos = QPoint()
        self.endPos = QPoint()
        self.process = DWaterProgress(self)
        self.process.hide()

        self.process2 = DWaterProgress(self)
        self.process2.hide()

        self.waifu2xProcess = GifLabel(self)
        self.waifu2xProcess.setVisible(False)
        f = QFile(":/png/icon/loading_gif.webp")
        f.open(QFile.ReadOnly)
        self.waifu2xProcess.Init(f.readAll())

        self.waifu2xProcess2 = GifLabel(self)
        self.waifu2xProcess2.setVisible(False)
        f = QFile(":/png/icon/loading_gif.webp")
        f.open(QFile.ReadOnly)
        self.waifu2xProcess2.Init(f.readAll())

        f.close()
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
        # fm = QFontMetrics(font)
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
        if self.qtTool.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            nextPage = Str.GetStr(Str.LastPage)
            lastPage = Str.GetStr(Str.NextPage)
        else:
            lastPage = Str.GetStr(Str.LastPage)
            nextPage = Str.GetStr(Str.NextPage)
        # print(self.height(), self.width())
        painter.drawText(QRect(0, self.height() // 4 * 3, self.width() // 3, self.height() // 2), lastPage)
        painter.drawText(QRect(self.width() // 3 * 2, self.height() // 4 * 3, self.width() // 3, self.height() // 2),
                         nextPage)
        painter.drawText(QRect(0, self.height() // 4 * 1, self.width(), self.height()),Str.GetStr(Str.Menu))
        painter.drawText(QRect(self.width()*2 // 3, self.height() // 4 * 1, self.width(), self.height()), Str.GetStr(Str.Menu))

        if self.qtTool.stripModel in [ReadMode.UpDown, ReadMode.LeftRight, ReadMode.Samewight]:
            painter.drawText(QRect(self.width() // 3, self.height() // 4 * 1, self.width(), self.height()), Str.GetStr(Str.LastScroll))
            painter.drawText(QRect(self.width() // 3, self.height() // 4 * 3, self.width(), self.height()), Str.GetStr(Str.NextScroll))
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
        # h2 = min(800, h)
        # self.qtTool.adjustSize()
        self.qtTool.setGeometry(w - 400, 0, 400, h)

        # w = max((w - 150)//2, 0)
        # h = max((h - 150)//2, 0)
        self.process.setGeometry(w-150, h-150, 150, 150)
        self.process2.setGeometry(w//2-150, h-150, 150, 150)
        self.waifu2xProcess.setGeometry(w-150, h-150, 150, 150)
        self.waifu2xProcess2.setGeometry(w//2-150, h-150, 150, 150)
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

    def UpdateProcessBar2(self, info):
        if info:
            self.downloadSize = info.downloadSize
            self.downloadMaxSize = max(1, info.size)
            value = int((self.downloadSize / self.downloadMaxSize) * 100)
            # print(value)
            self.process2.setValue(value)
        else:
            self.downloadSize = 0
            self.downloadMaxSize = 1
            self.process2.setValue(0)

    def eventFilter(self, obj, ev) -> bool:
        # print(obj, ev.type())
        if obj == self.helpLabel:
            if ev.type() == QEvent.MouseButtonPress:
                if not self.helpLabel.isHidden():
                    self.helpLabel.hide()
                    return True
        return False
