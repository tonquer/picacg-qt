import weakref

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QApplication

from conf import config
from src.index.book import BookMgr
from src.qt.qttask import QtTask
from src.util.status import Status
from ui.readimg import Ui_ReadImg


class QtReadImg(QtWidgets.QWidget, Ui_ReadImg):
    def __init__(self, parent, owner):
        super(self.__class__, self).__init__(parent)
        Ui_ReadImg.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.bookId = ""
        self.epsId = 0
        self.resetCnt = config.ResetCnt
        self.curIndex = 0

        self.pictureData = {}
        self.maxPic = 0

        self.curPreLoadIndex = 0
        self.maxPreLoad = 10

        self.graphicsView.setBackgroundBrush(QColor(Qt.white))
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
        self.graphicsScene.addItem(self.graphicsItem)
        rect = QApplication.instance().desktop().availableGeometry(self)
        self.graphicsView.setMinimumSize(10, 10)
        self.pixMap = QPixmap("加载中")
        self.graphicsItem.setPixmap(self.pixMap)

        # self.resize(1200, 1080)
        self.closeFlag = self.__class__.__name__   # 防止切换时异步加载图片错位

    def OpenPage(self, bookId, epsId, name):
        self.bookId = bookId
        self.epsId = epsId
        self.pictureData.clear()
        self.maxPic = 0
        self.curIndex = 0
        self.curPreLoadIndex = 0
        historyInfo = self.owner().historyForm.GetHistory(bookId)
        if historyInfo and historyInfo.epsId == epsId:
            self.curIndex = historyInfo.picIndex
        else:
            self.AddHistory()

        QtTask().CancelTasks(self.closeFlag)
        self.owner().bookInfoForm.loadingForm.show()
        self.StartLoadPicUrl()
        self.setWindowTitle(name)

    def NextPage(self):
        if self.curIndex >= self.maxPic-1:
            return
        self.curIndex += 1
        self.ShowImg()
        self.CheckLoadPicture()
        return

    def LastPage(self):
        if self.curIndex <= 0:
            return
        self.curIndex -= 1
        self.ShowImg()
        self.CheckLoadPicture()
        return

    def ReturnPage(self):
        a = self.parent()
        a.setCurrentIndex(0)
        self.AddHistory()
        self.owner().bookInfoForm.LoadHistory()
        return

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
                QtTask().AddDownloadTask(picInfo.fileServer, picInfo.path, picInfo.originalName,
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
        self.owner().bookInfoForm.loadingForm.close()
        if st != Status.Ok:
            bookInfo = BookMgr().books.get(self.bookId)
            epsInfo = bookInfo.eps[self.epsId]
            picInfo = epsInfo.pics[index]
            QtTask().AddDownloadTask(picInfo.fileServer, picInfo.path, picInfo.originalName,
                                                completeCallBack=self.CompleteDownloadPic, backParam=index,
                                                isSaveCache=True, cleanFlag=self.closeFlag)
        else:
            self.pictureData[index] = data
            if index == self.curIndex:
                self.ShowImg()
            return

    def ShowImg(self):
        self.epsLabel.setText("页：{}/{}".format(self.curIndex+1, self.maxPic))
        self.epsLabel.setAlignment(Qt.AlignCenter)
        data = self.pictureData.get(self.curIndex)
        if not data:
            a = QPixmap("加载失败")
            self.graphicsItem.setPixmap(a)
            return False
        else:
            self.pixMap = QPixmap()
            self.pixMap.loadFromData(data)
            self.graphicsItem.setPixmap(self.pixMap)
            self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixMap.width(), self.pixMap.height())))
            self.ScalePicture()
            return True

    def ScalePicture(self):
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
        if flags == Qt.KeepAspectRatio:
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        elif flags == Qt.KeepAspectRatioByExpanding:
            x_ratio = y_ratio = max(x_ratio, y_ratio)
        self.graphicsView.scale(x_ratio, y_ratio)
        self.graphicsView.centerOn(rect.center())

    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.ScalePicture()

    def keyReleaseEvent(self, ev):
        if ev.key() == Qt.Key_Left:
            self.LastPage()
            return
        elif ev.key() == Qt.Key_Right:
            self.NextPage()
            return
        elif ev.key() == Qt.Key_Escape:
            self.ReturnPage()
            return
        super(self.__class__, self).keyReleaseEvent(ev)

    def AddHistory(self):
        bookName = self.owner().bookInfoForm.bookName
        url = self.owner().bookInfoForm.url
        path = self.owner().bookInfoForm.path
        self.owner().historyForm.AddHistory(self.bookId, bookName, self.epsId, self.curIndex, url, path)
        return
