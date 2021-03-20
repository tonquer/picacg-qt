from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Qt, QRectF, QPointF, QSizeF, QEvent
from PySide2.QtGui import QColor, QPainter, QPixmap, QImage
from PySide2.QtWidgets import QFrame, QGraphicsPixmapItem, QGraphicsScene, QApplication

from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.util import Singleton


class QtImgMgr(Singleton):
    def __init__(self):
        self.obj = QtImg()

    def ShowImg(self, data):
        p = None
        if isinstance(data, bytes):
            p = QPixmap()
            p.loadFromData(data)
        elif isinstance(data, (QPixmap, QImage)):
            p = data
        else:
            return
        self.obj.ShowImg(p)


class QtImg(QtWidgets.QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.bookId = ""
        self.epsId = 0
        self.curIndex = 0
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.setWindowTitle("图片查看")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(402, 509)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.graphicsView.setFrameStyle(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                                         QPainter.SmoothPixmapTransform)
        self.graphicsView.setCacheMode(self.graphicsView.CacheBackground)
        self.graphicsView.setViewportUpdateMode(self.graphicsView.SmartViewportUpdate)

        self.graphicsItem = QGraphicsPixmapItem()
        self.graphicsItem.setFlags(QGraphicsPixmapItem.ItemIsFocusable |
                                   QGraphicsPixmapItem.ItemIsMovable)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.CopyPicture)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsScene.addItem(self.graphicsItem)
        self.graphicsView.setMinimumSize(10, 10)
        self.pixMap = QPixmap("加载中")
        self.graphicsItem.setPixmap(self.pixMap)
        # self.radioButton.setChecked(True)
        self.isStripModel = False

        # self.radioButton.installEventFilter(self)
        # self.radioButton_2.installEventFilter(self)
        self.graphicsView.installEventFilter(self)
        self.graphicsView.setWindowFlag(Qt.FramelessWindowHint)
        self.gridLayout.addWidget(self.graphicsView)

        self._delta = 0.1
        self.scaleCnt = 0

    def ShowImg(self, pixMap):
        self.scaleCnt = 0
        self.pixMap = QPixmap(pixMap)
        self.show()
        self.graphicsItem.setPixmap(self.pixMap)
        self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixMap.width(), self.pixMap.height())))
        self.ScalePicture()

    def ScalePicture(self):
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
        x_ratio = y_ratio = min(x_ratio, y_ratio)

        self.graphicsView.scale(x_ratio, y_ratio)
        # if self.readImg.isStripModel:
        #     height2 = self.pixMap.size().height() / 2
        #     height3 = self.graphicsView.size().height()/2
        #     height3 = height3/x_ratio
        #     p = self.graphicsItem.pos()
        #     self.graphicsItem.setPos(p.x(), p.y()+height2-height3)
        self.graphicsView.centerOn(rect.center())

        for _ in range(abs(self.scaleCnt)):
            if self.scaleCnt > 0:
                self.graphicsView.scale(1.1, 1.1)
            else:
                self.graphicsView.scale(1/1.1, 1/1.1)


    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.ScalePicture()

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress:
            return True
        else:
            return super(self.__class__, self).eventFilter(obj, ev)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def zoomIn(self):
        """放大"""
        self.zoom(1.1)

    def zoomOut(self):
        """缩小"""
        self.zoom(1/1.1)

    def zoom(self, factor):
        """缩放
        :param factor: 缩放的比例因子
        """
        _factor = self.graphicsView.transform().scale(
            factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if _factor < 0.07 or _factor > 100:
            # 防止过大过小
            return
        if factor >= 1:
            self.scaleCnt += 1
        else:
            self.scaleCnt -= 1
        self.graphicsView.scale(factor, factor)

    def CopyPicture(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.pixMap)
        QtBubbleLabel.ShowMsgEx(self, "复制成功")
        return
