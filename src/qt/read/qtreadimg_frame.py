import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QSizeF, QRectF, QEvent, QPoint, QSize, QRect
from PySide2.QtGui import QPainter, QColor, QPixmap, QFont, QFontMetrics
from PySide2.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QFrame, QGraphicsItemGroup, QGraphicsItem, \
    QAbstractSlider, QAbstractItemView, QScroller

from resources.resources import DataMgr
from src.qt.com.DWaterProgress import DWaterProgress
from src.qt.com.qt_git_label import QtGifLabel
from src.qt.com.qt_scroll import QtComGraphicsView
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.read.qtreadimg_tool import QtImgTool
from src.util.tool import time_me


class QtImgFrame(QFrame):
    def __init__(self, readImg):
        QFrame.__init__(self)
        self._readImg = weakref.ref(readImg)
        self.graphicsView = QtComGraphicsView(self)
        self.graphicsView.setTransformationAnchor(self.graphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(self.graphicsView.AnchorUnderMouse)
        self.graphicsView.setFrameStyle(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.qtTool = QtImgTool(self)
        self.qtTool.hide()
        # self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        # self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.graphicsView.setResizeAnchor(self.graphicsView.AnchorViewCenter)
        self.graphicsView.setTransformationAnchor(self.graphicsView.AnchorViewCenter)

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.SmoothPixmapTransform)
        self.graphicsView.setCacheMode(self.graphicsView.CacheBackground)
        self.graphicsView.setViewportUpdateMode(self.graphicsView.SmartViewportUpdate)

        self.graphicsItem1 = QGraphicsPixmapItem()
        self.graphicsItem1.setFlags(QGraphicsPixmapItem.ItemIsFocusable)

        self.graphicsItem2 = QGraphicsPixmapItem()
        self.graphicsItem2.setFlags(QGraphicsPixmapItem.ItemIsFocusable)

        self.graphicsItem3 = QGraphicsPixmapItem()
        self.graphicsItem3.setFlags(QGraphicsPixmapItem.ItemIsFocusable)

        self.graphicsGroup = QGraphicsItemGroup()
        self.graphicsGroup.setFlag(QGraphicsItem.ItemIsFocusable)
        self.graphicsGroup.addToGroup(self.graphicsItem1)
        self.graphicsGroup.addToGroup(self.graphicsItem2)
        self.graphicsGroup.addToGroup(self.graphicsItem3)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsScene.addItem(self.graphicsGroup)

        self.graphicsView.setMinimumSize(10, 10)

        self.graphicsScene.installEventFilter(self)
        # self.graphicsView.installEventFilter(self)
        # self.graphicsItem.installSceneEventFilter(self.graphicsItem)

        self.graphicsView.setWindowFlag(Qt.FramelessWindowHint)
        self.pixMapList = []
        self.graphicsItemList = [self.graphicsItem1, self.graphicsItem2, self.graphicsItem3]

        self.scaleCnt = 2
        self.startPos = QPoint()
        self.endPos = QPoint()
        self.process = DWaterProgress(self)
        self.waifu2xProcess = QtGifLabel(self)
        self.waifu2xProcess.setVisible(False)

        self.waifu2xProcess.Init(DataMgr.GetData("loading_gif"))
        self.downloadSize = 1
        self.downloadMaxSize = 1
        self.oldValue = -1
        # QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)
        self.graphicsView.verticalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        # self.graphicsView.verticalScrollBar().setSingleStep(100)
        # self.graphicsView.verticalScrollBar().setPageStep(100)
        self.graphicsView.setSceneRect(0, 0, self.width(), self.height())
        self.graphicsView.verticalScrollBar().valueChanged.connect(self.OnValueChange)

    @property
    def readImg(self):
        return self._readImg()

    def OnValueChange(self, value):
        # print(value)
        return

    def eventFilter(self, obj, ev):
        # print(obj, ev)
        if obj == self.graphicsScene:
            if ev.type() == QEvent.GraphicsSceneMousePress:
                # print(ev, ev.button())
                self.startPos = ev.screenPos()
                return False
            elif ev.type() == QEvent.KeyPress:
                if ev.key() == Qt.Key_Down:
                    point = self.graphicsGroup.pos()
                    # if point.y() > 0:
                    #     return True
                    # self.UpdatePos(point, -200)
                    self.graphicsView.verticalScrollBar().setValue(self.graphicsView.verticalScrollBar().value()+100)
                    self.UpdateScrollBar(self.graphicsView.verticalScrollBar().value())
                elif ev.key() == Qt.Key_Up:
                    point = self.graphicsGroup.pos()
                    # if point.y() < 0:
                    #     return True
                    # self.UpdatePos(point, 200)
                    self.graphicsView.verticalScrollBar().setValue(self.graphicsView.verticalScrollBar().value()-100)
                    self.UpdateScrollBar(self.graphicsView.verticalScrollBar().value())
                return True
            elif ev.type() == QEvent.GraphicsSceneMouseRelease:
                # print(ev, self.width(), self.height(), self.readImg.pos())
                self.endPos = ev.screenPos()
                subPos = (self.endPos - self.startPos)

                if ev.button() == Qt.MouseButton.LeftButton:
                    if abs(subPos.x()) >= 50:
                        if subPos.x() < 0:
                            self.qtTool.NextPage()
                        elif subPos.y() > 0:
                            self.qtTool.LastPage()
                    elif abs(subPos.x()) <= 20:
                        curPos = self.endPos - self.readImg.pos()
                        if curPos.y() <= self.height() / 2:
                            self.readImg.ShowAndCloseTool()
                        else:
                            if curPos.x() >= self.width()/3*2:
                                self.qtTool.NextPage()
                            elif curPos.x() <= self.width()/3:
                                self.qtTool.LastPage()

                return False
        return super(self.__class__, self).eventFilter(obj, ev)

    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.ScaleFrame()
        self.ScalePicture()

    def OnActionTriggered(self, action):
        if action != QAbstractSlider.SliderMove:
            return
        value = self.graphicsView.verticalScrollBar().value()
        # print(value)

        self.UpdateScrollBar(value)

    def UpdateScrollBar(self, value):
        self.UpdatePos(value-self.oldValue)
        self.ResetScrollBar()
        self.graphicsView.verticalScrollBar().setSingleStep(60)
        self.graphicsView.verticalScrollBar().setPageStep(60)
        self.oldValue = value

    def ScaleFrame(self):
        size = self.size()
        w = size.width()
        h = size.height()
        self.graphicsView.setGeometry(0, 0, w, h)

        h2 = min(700, h)
        self.qtTool.setGeometry(w - 220, 0, 220, h2)

        # w = max((w - 150)//2, 0)
        # h = max((h - 150)//2, 0)
        self.process.setGeometry(w-150, h-150, 150, 150)
        self.waifu2xProcess.setGeometry(w-150, h-150, 150, 150)
        return

    def ScalePicture(self):
        self.graphicsView.setSceneRect(0, 0, self.width(), self.height())
        if not self.pixMapList:
            return
        self.ScaleGraphicsItem()

        self.ResetScrollBar()
        self.graphicsView.verticalScrollBar().setSingleStep(60)
        self.graphicsView.verticalScrollBar().setPageStep(60)

    def ResetScrollBar(self):
        width1 = self.graphicsItem1.pixmap().size().width()
        width2 = self.graphicsItem2.pixmap().size().width()
        width3 = self.graphicsItem3.pixmap().size().width()
        self.graphicsView.verticalScrollBar().setMinimum(-100)
        self.graphicsView.verticalScrollBar().setMaximum(width1 + width2 + 100)

    def MakePixItem(self, index):
        text = str(index+1)
        font = QFont()
        font.setPointSize(64)
        fm = QFontMetrics(font)

        p = QPixmap(self.width()//2, self.height()//2)
        rect = QRect(self.width()//4-fm.width(text)//2, self.height()//4 - fm.height()//2, self.width()//2+fm.width(text)//2, self.height()//4+fm.height()//2)
        p.fill(Qt.transparent)
        painter = QPainter(p)
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(rect, text)
        return p

    def SetPixIem(self, index, data):
        if not self.qtTool.isStripModel and index > 0:
            self.pixMapList[index] = QPixmap()
            self.graphicsItemList[index].setPixmap(None)
        else:
            if not data and self.readImg.curIndex+index < self.readImg.maxPic:
                data = self.MakePixItem(self.readImg.curIndex+index)
                self.pixMapList[index] = data
            else:

                self.pixMapList[index] = data
            scale = (1 + self.scaleCnt * 0.1)
            self.graphicsItemList[index].setPixmap(data.scaled(min(self.width(), self.width()*scale), self.height()*scale, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            height1 = self.graphicsItem1.pixmap().size().height()
            width1 = self.graphicsItem1.pixmap().size().width()
            width2 = self.graphicsItem2.pixmap().size().width()
            width3 = self.graphicsItem3.pixmap().size().width()
            height2 = self.graphicsItem2.pixmap().size().height()
            self.graphicsItem1.setPos((self.width() - width1) / 2, 0)
            self.graphicsItem2.setPos((self.width() - width2) / 2, 0 + height1)
            self.graphicsItem3.setPos((self.width() - width3) / 2, 0 + height1 + height2)
        # self.ScaleGraphicsItem()

    def ScaleGraphicsItem(self):
        scale = (1+self.scaleCnt*0.1)
        self.graphicsItem1.setPixmap(self.pixMapList[0].scaled(min(self.width(), self.width()*scale), self.height()*scale, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.graphicsItem2.setPixmap(self.pixMapList[1].scaled(min(self.width(), self.width()*scale), self.height()*scale, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.graphicsItem3.setPixmap(self.pixMapList[2].scaled(min(self.width(), self.width()*scale), self.height()*scale, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        height1 = self.graphicsItem1.pixmap().size().height()
        width1 = self.graphicsItem1.pixmap().size().width()
        width2 = self.graphicsItem2.pixmap().size().width()
        width3 = self.graphicsItem3.pixmap().size().width()
        height2 = self.graphicsItem2.pixmap().size().height()
        # print(self.width()-width1, height1, self.pixMapList[0].height(), self.graphicsItem1.pixmap().width(), self.pixMapList[0].width())
        self.graphicsItem1.setPos((self.width()-width1)/2, 0)
        self.graphicsItem2.setPos((self.width()-width2)/2, 0+height1)
        self.graphicsItem3.setPos((self.width()-width3)/2, 0+height1 + height2)

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

    def InitPixMap(self):
        pixMap1 = QPixmap()
        pixMap2 = QPixmap()
        pixMap3 = QPixmap()
        self.pixMapList = []
        self.pixMapList.append(pixMap1)
        self.pixMapList.append(pixMap2)
        self.pixMapList.append(pixMap3)
        self.graphicsGroup.setPos(0, 0)

    def UpdatePixMap(self):
        if not self.pixMapList:
            return
        self.ScaleGraphicsItem()
        return

    def UpdatePos(self, value):
        # scale = (1+self.scaleCnt*0.1)
        if not self.qtTool.isStripModel:
            return

        if value >= 0 and self.readImg.curIndex >= self.readImg.maxPic - 1:
            QtBubbleLabel().ShowMsgEx(self.readImg, "已经到最后一页")
            return

        height = self.graphicsItem1.pixmap().size().height()
        ## 切换上一图片
        if value < 0 and self.graphicsView.verticalScrollBar().value() < 0:
            if self.readImg.curIndex <= 0:
                return
            self.readImg.curIndex -= 1
            subValue = self.graphicsView.verticalScrollBar().value()
            self.readImg.ShowImg()
            self.readImg.ShowOtherPage()
            height = self.graphicsItem1.pixmap().size().height()
            subValue += height
            self.graphicsView.verticalScrollBar().setValue(subValue)
            pass

        ## 切换下一图片
        elif value > 0 and self.graphicsItem1.pixmap().size().height() > 0 and self.graphicsView.verticalScrollBar().value() > height:
            if self.readImg.curIndex >= self.readImg.maxPic - 1:
                return
            self.readImg.curIndex += 1
            subValue = self.graphicsView.verticalScrollBar().value() -height
            self.readImg.ShowImg()
            self.readImg.ShowOtherPage()
            # print(subValue)
            self.graphicsView.verticalScrollBar().setValue(subValue)
