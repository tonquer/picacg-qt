import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QSizeF, QRectF, QEvent, QPoint
from PySide2.QtGui import QPainter, QColor, QPixmap
from PySide2.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QFrame

from src.qt.read.qtreadimg_tool import QtImgTool


class QtImgFrame(QFrame):
    def __init__(self, readImg):
        QFrame.__init__(self)
        self._readImg = weakref.ref(readImg)
        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.graphicsView.setTransformationAnchor(self.graphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(self.graphicsView.AnchorUnderMouse)
        self.graphicsView.setFrameStyle(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.qtTool = QtImgTool(self)
        self.qtTool.hide()
        self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        # self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.graphicsView.setResizeAnchor(self.graphicsView.AnchorViewCenter)
        self.graphicsView.setTransformationAnchor(self.graphicsView.AnchorViewCenter)

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.SmoothPixmapTransform)
        self.graphicsView.setCacheMode(self.graphicsView.CacheBackground)
        self.graphicsView.setViewportUpdateMode(self.graphicsView.SmartViewportUpdate)

        self.graphicsItem = QGraphicsPixmapItem()
        self.graphicsItem.setFlags(QGraphicsPixmapItem.ItemIsFocusable)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsItem.setTransformationMode(Qt.SmoothTransformation)

        self.graphicsScene.addItem(self.graphicsItem)

        self.graphicsView.setMinimumSize(10, 10)

        self.graphicsScene.installEventFilter(self)
        # self.graphicsView.installEventFilter(self)
        # self.graphicsItem.installSceneEventFilter(self.graphicsItem)

        self.graphicsView.setWindowFlag(Qt.FramelessWindowHint)
        self.pixMap = QPixmap()
        self.scaleCnt = 0
        self.startPos = QPoint()
        self.endPos = QPoint()

    @property
    def readImg(self):
        return self._readImg()

    def eventFilter(self, obj, ev):
        # print(obj, ev)
        if obj == self.graphicsScene:
            if ev.type() == QEvent.GraphicsSceneMousePress:
                # print(ev, ev.button())
                self.startPos = ev.screenPos()
                return ev.ignore()
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

                return ev.ignore()
        return super(self.__class__, self).eventFilter(obj, ev)

    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.ScaleFrame()
        self.ScalePicture()

    def ScaleFrame(self):
        size = self.size()
        w = size.width()
        h = size.height()
        self.graphicsView.setGeometry(0, 0, w, h)

        h = min(700, h)
        self.qtTool.setGeometry(w - 220, 0, 220, h)
        return

    def ScalePicture(self):
        if self.readImg.isStripModel:
            self.graphicsItem.setPos(0, 0)
        rect = QRectF(self.graphicsItem.pos(), QSizeF(
                self.pixMap.size()))
        unity = self.graphicsView.transform().mapRect(QRectF(0, 0, 1, 1))
        width = unity.width()
        height = unity.height()
        if width <= 0 or height <= 0:
            return
        self.graphicsView.scale(1 / width, 1 / height)
        viewRect = self.graphicsView.viewport().rect()
        sceneRect = self.graphicsView.transform().mapRect(rect)
        if sceneRect.width() <= 0 or sceneRect.height() <= 0:
            return
        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()
        if not self.readImg.isStripModel:
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        else:
            x_ratio = y_ratio = max(x_ratio, y_ratio)

        self.graphicsView.scale(x_ratio, y_ratio)
        if self.readImg.isStripModel:
            height2 = self.pixMap.size().height() / 2
            height3 = self.graphicsView.size().height()/2
            height3 = height3/x_ratio
            p = self.graphicsItem.pos()
            self.graphicsItem.setPos(p.x(), p.y()+height2-height3)

        self.graphicsView.centerOn(rect.center())
        for _ in range(abs(self.scaleCnt)):
            if self.scaleCnt > 0:
                self.graphicsView.scale(1.1, 1.1)
            else:
                self.graphicsView.scale(1/1.1, 1/1.1)

