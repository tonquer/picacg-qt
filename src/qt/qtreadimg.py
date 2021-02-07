import weakref

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QEvent
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QApplication, QFrame, QVBoxLayout, QLabel

from conf import config
from src.index.book import BookMgr
from src.qt.qtbubblelabel import QtBubbleLabel
from src.qt.qtloading import QtLoading
from src.qt.qttask import QtTask
from src.util.status import Status
from ui.readimg import Ui_ReadImg


class QtImgTool(QtWidgets.QWidget, Ui_ReadImg):
    def __init__(self, parent, *args, **kwargs):
        super(QtImgTool, self).__init__(*args, **kwargs)
        Ui_ReadImg.__init__(self)
        self.setupUi(self)
        self.resize(100, 300)
        self.parent = weakref.ref(parent)
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 16)
        layout.addWidget(QLabel("test"))
        self.pushButton.setText("未开放")
        self.radioButton.installEventFilter(self)
        self.radioButton_2.installEventFilter(self)

    @property
    def graphicsItem(self):
        return self.parent().graphicsItem

    @property
    def curIndex(self):
        return self.parent().curIndex

    @curIndex.setter
    def curIndex(self, value):
        self.parent().curIndex = value

    @property
    def maxPic(self):
        return self.parent().maxPic

    @property
    def isStripModel(self):
        return self.parent().isStripModel

    @isStripModel.setter
    def isStripModel(self, value):
        self.parent().isStripModel = value

    def Show(self, size):
        self.show()

    def Close(self, size):
        self.show()

    @property
    def qtTool(self):
        return self.parent().qtTool

    @property
    def scaleCnt(self):
        return self.parent().scaleCnt

    @scaleCnt.setter
    def scaleCnt(self, value):
        self.parent().scaleCnt = value

    def NextPage(self):
        if self.curIndex >= self.maxPic-1:
            QtBubbleLabel.ShowMsgEx(self.parent(), "已经最后一页")
            return
        self.curIndex += 1
        self.parent().ShowImg()
        return

    def LastPage(self):
        if self.curIndex <= 0:
            QtBubbleLabel.ShowMsgEx(self.parent(), "已经是第一页")
            return
        self.curIndex -= 1
        self.parent().ShowImg()
        return

    def SwitchPicture(self):
        if self.radioButton.isChecked():
            self.isStripModel = False
        else:
            self.isStripModel = True
        self.graphicsItem.setPos(0, 0)
        self.scaleCnt = 0
        self.parent().ScalePicture()

    def ReturnPage(self):
        self.parent().hide()
        self.hide()
        self.parent().owner().bookInfoForm.show()
        self.parent().AddHistory()
        self.parent().owner().bookInfoForm.LoadHistory()
        return

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress:
            return True
        else:
            return super(self.__class__, self).eventFilter(obj, ev)

class QtReadImg(QtWidgets.QWidget):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        self.owner = weakref.ref(owner)
        self.resize(800, 800)
        self.loadingForm = QtLoading(self)
        self.bookId = ""
        self.epsId = 0
        self.resetCnt = config.ResetCnt
        self.curIndex = 0

        self.pictureData = {}
        self.maxPic = 0

        self.curPreLoadIndex = 0
        self.maxPreLoad = 10

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.qtTool = QtImgTool(self)

        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.graphicsView.setFrameStyle(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")

        self.gridLayout.addWidget(self.graphicsView)
        self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.graphicsView.setResizeAnchor(self.graphicsView.AnchorViewCenter)
        self.graphicsView.setTransformationAnchor(self.graphicsView.AnchorViewCenter)

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
        self.customContextMenuRequested.connect(self.ShowAndCloseTool)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsScene.addItem(self.graphicsItem)
        rect = QApplication.instance().desktop().availableGeometry(self)
        self.graphicsView.setMinimumSize(10, 10)
        self.pixMap = QPixmap("加载中")
        self.graphicsItem.setPixmap(self.pixMap)
        self.scaleCnt = 0

        self.isStripModel = False

        self.graphicsView.installEventFilter(self)
        # self.resize(1200, 1080)
        self.closeFlag = self.__class__.__name__   # 防止切换时异步加载图片错位

    def closeEvent(self, a0) -> None:
        self.ReturnPage()
        self.owner().bookInfoForm.show()
        self.qtTool.hide()
        a0.accept()

    def OpenPage(self, bookId, epsId, name):
        self.bookId = bookId
        self.epsId = epsId
        self.pictureData.clear()
        self.maxPic = 0
        self.curIndex = 0
        self.curPreLoadIndex = 0
        self.scaleCnt = 0
        self.graphicsItem.setPos(0, 0)

        # historyInfo = self.owner().historyForm.GetHistory(bookId)
        # if historyInfo and historyInfo.epsId == epsId:
        #     self.curIndex = historyInfo.picIndex
        # else:
        #     self.AddHistory()
        # self.AddHistory()

        QtTask().CancelTasks(self.closeFlag)
        self.loadingForm.show()
        self.StartLoadPicUrl()
        self.setWindowTitle(name)
        self.show()

    def ReturnPage(self):
        self.AddHistory()
        self.owner().bookInfoForm.LoadHistory()
        return

    def RevertPicture(self):
        self.graphicsItem.setPos(0, 0)
        self.scaleCnt = 0
        self.ScalePicture()

    def StartLoadPicUrl(self):
        QtTask().AddHttpTask(lambda x: BookMgr().AddBookEpsPicInfo(self.bookId, self.epsId+1, x),
                                        self.StartLoadPicUrlBack,
                                        self.bookId, cleanFlag=self.closeFlag)

    def CheckLoadPicture(self):
        i = 0
        for i in range(self.curIndex, self.curIndex + self.maxPreLoad):
            if i >= self.maxPic:
                continue
            if i < self.curPreLoadIndex:
                continue
            if i not in self.pictureData:
                bookInfo = BookMgr().books.get(self.bookId)
                epsInfo = bookInfo.eps[self.epsId]
                picInfo = epsInfo.pics[i]
                QtTask().AddDownloadTask(picInfo.fileServer, picInfo.path,
                                                    completeCallBack=self.CompleteDownloadPic, backParam=i,
                                                    isSaveCache=True, cleanFlag=self.closeFlag)
        self.curPreLoadIndex = max(i, self.curPreLoadIndex)
        pass

    def StartLoadPicUrlBack(self, msg, bookId):
        if msg != Status.Ok:
            self.StartLoadPicUrl()
        else:
            bookInfo = BookMgr().books.get(self.bookId)
            epsInfo = bookInfo.eps[self.epsId]
            self.maxPic = len(epsInfo.pics)
            self.CheckLoadPicture()
        return

    def CompleteDownloadPic(self, data, st, index):
        self.loadingForm.close()
        if st != Status.Ok:
            bookInfo = BookMgr().books.get(self.bookId)
            epsInfo = bookInfo.eps[self.epsId]
            picInfo = epsInfo.pics[index]
            QtTask().AddDownloadTask(picInfo.fileServer, picInfo.path,
                                                completeCallBack=self.CompleteDownloadPic, backParam=index,
                                                isSaveCache=True, cleanFlag=self.closeFlag)
        else:
            self.pictureData[index] = data
            if index == self.curIndex:
                self.ShowImg()
            return

    def ShowImg(self):
        self.qtTool.epsLabel.setText("页：{}/{}".format(self.curIndex+1, self.maxPic))
        self.qtTool.epsLabel.setAlignment(Qt.AlignCenter)
        data = self.pictureData.get(self.curIndex)
        if not data:
            a = QPixmap("加载失败")
            QtBubbleLabel.ShowMsgEx(self, "正在努力加载中")
            self.graphicsItem.setPixmap(a)
            return False
        else:
            self.pixMap = QPixmap()
            self.pixMap.loadFromData(data)
            self.graphicsItem.setPixmap(self.pixMap)
            self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixMap.width(), self.pixMap.height())))
            self.ScalePicture()

            self.CheckLoadPicture()
            return True

    def ScalePicture(self):
        if self.isStripModel:
            self.graphicsItem.setPos(0, 0)
        rect = QRectF(self.graphicsItem.pos(), QSizeF(
                self.pixMap.size()))
        flags = Qt.KeepAspectRatio
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
        if not self.isStripModel:
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        else:
            x_ratio = y_ratio = max(x_ratio, y_ratio)
            # self.graphicsItem.setPos(p.x(), p.y()+height3)
            # self.graphicsView.move(p.x(), p.y()+height2)
            # self.graphicsView.move(p.x(), p.y()+height3)

        self.graphicsView.scale(x_ratio, y_ratio)
        if self.isStripModel:
            height2 = self.pixMap.size().height() / 2
            height3 = self.graphicsView.size().height()/2
            # height4 = self.graphicsView.geometry().height()/2
            # height5 = self.graphicsView.frameGeometry().height()/2
            height3 = height3/x_ratio
            # pos = height2
            p = self.graphicsItem.pos()
            # self.graphicsItem.setPos(0, 0)
            self.graphicsItem.setPos(p.x(), p.y()+height2-height3)

        self.graphicsView.centerOn(rect.center())
        for _ in range(abs(self.scaleCnt)):
            if self.scaleCnt > 0:
                self.graphicsView.scale(1.1, 1.1)
            else:
                self.graphicsView.scale(1/1.1, 1/1.1)

    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.ScalePicture()
        self.MoveTool()

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

    def keyReleaseEvent(self, ev):
        if ev.key() == Qt.Key_Left:
            self.qtTool.LastPage()
            return
        elif ev.key() == Qt.Key_Right:
            self.qtTool.NextPage()
            return
        elif ev.key() == Qt.Key_Escape:
            self.qtTool.ReturnPage()
            return
        elif ev.key() == Qt.Key_Up:
            point = self.graphicsItem.pos()
            self.graphicsItem.setPos(point.x(), point.y()+50)
            return
        elif ev.key() == Qt.Key_Down:
            point = self.graphicsItem.pos()
            self.graphicsItem.setPos(point.x(), point.y()-50)
            return
        super(self.__class__, self).keyReleaseEvent(ev)

    def AddHistory(self):
        bookName = self.owner().bookInfoForm.bookName
        url = self.owner().bookInfoForm.url
        path = self.owner().bookInfoForm.path
        self.owner().historyForm.AddHistory(self.bookId, bookName, self.epsId, self.curIndex, url, path)
        return

    def ShowAndCloseTool(self):
        if self.qtTool.isHidden():
            self.MoveTool()
            self.qtTool.show()
        else:
            self.qtTool.hide()

    def MoveTool(self):
        size1 = self.geometry()
        # size2 = self.graphicsView.pos()
        h = self.width()
        self.qtTool.move(size1.x() + h - 100, size1.y())