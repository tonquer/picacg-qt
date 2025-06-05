import time

from PySide6.QtCore import Qt, QEvent, QPoint, Signal, QRect, QFile
from PySide6.QtGui import QPainter, QFont, QPixmap, QFontMetrics, QWheelEvent, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QGraphicsView, QFrame, QGraphicsItem, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsProxyWidget, QScroller, QAbstractSlider, QApplication

from component.label.msg_label import MsgLabel
from component.scroll.read_scroll import ReadScroll
from component.scroll.smooth_scroll import SmoothScroll
from config import config
from qt_owner import QtOwner
from config.setting import Setting
from tools.log import Log
from tools.str import Str
from view.read.read_enum import ReadMode, QtFileData
from view.read.read_opengl import ReadOpenGL
from view.read.read_pool import QtReadImgPoolManager
from view.read.read_qgraphics_proxy_widget import ReadQGraphicsProxyWidget


class ReadGraphicsView(QGraphicsView, SmoothScroll):
    changeLastPage = Signal(int)
    changeNextPage = Signal(int)
    changePage = Signal(int, int)
    changeScale = Signal(int)

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        SmoothScroll.__init__(self)

        self.vScrollBar = ReadScroll(parent)
        self.vScrollBar.setOrientation(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(self.vScrollBar)


        # self.animation.finished.connect(self.Finished)

        self.hScrollBar = ReadScroll(parent)
        self.hScrollBar.setOrientation(Qt.Orientation.Horizontal)
        self.setHorizontalScrollBar(self.hScrollBar)

        # self.horizontalScrollBar().valueChanged.connect(self.HValueChange)
        self.changeLastPage.connect(self.ChangeLastPage)
        self.changeNextPage.connect(self.ChangeNextPage)
        self.changePage.connect(self.ChangePage)
        self.changeScale.connect(self.ChangeScale)

        # self.setInteractive(False)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setFrameStyle(QFrame.NoFrame)
        self.setObjectName("graphicsView")
        # self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        # self.graphicsView.setCursor(Qt.OpenHandCursor)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setCacheMode(QGraphicsView.CacheBackground)
        # self.setCacheMode(QGraphicsView.CacheNone)
        if Setting.IsOpenOpenGL.value:
            self.openGl = ReadOpenGL()
            f = QSurfaceFormat()
            # f.setVersion(4, 3)
            a = f.version()
            f.setSamples(4)
            # f.setSwapInterval(0)
            self.openGl.setFormat(f)
            self.setViewport(self.openGl)
            Log.Info("open opengl, ver:{}".format(a))

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

        # self.graphicsGroup = QGraphicsItemGroup()
        # self.graphicsGroup.setFlag(QGraphicsItem.ItemIsFocusable)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.setScene(self.graphicsScene)
        # self.graphicsScene.addItem(self.graphicsGroup)
        self.graphicsItem1 = ReadQGraphicsProxyWidget()
        self.graphicsItem2 = ReadQGraphicsProxyWidget()
        # self.graphicsItem1.setFlag(QGraphicsItem.ItemIsFocusable)
        # self.graphicsItem2.setFlag(QGraphicsItem.ItemIsFocusable)

        self.setMinimumSize(10, 10)
        self.graphicsScene.installEventFilter(self)
        # self.installEventFilter(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.testItem = QGraphicsPixmapItem()
        self.allItems = []
        self.allItemsState = {}
        self.allItemsScale = {}

        self.itemWight = {}
        self.labelSize = {}
        self.initReadMode = None
        # QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)
        # properties = QScroller.scroller(self).scrollerProperties()
        # properties.setScrollMetric(QScrollerProperties.FrameRate, QScrollerProperties.Fps60)
        # properties.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor, 0.3)
        # properties.setScrollMetric(QScrollerProperties.OvershootDragDistanceFactor, 0.5)
        # properties.setScrollMetric(QScrollerProperties.OvershootScrollTime, 0.2)
        # properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 1)
        # properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 2)
        # properties.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.3)
        # QScroller.scroller(self).setScrollerProperties(properties)

        self.labelSize = {}  # index: value
        # self.oldValue = 0
        self.resetImg = False
        # QScroller.scroller(self).stateChanged.connect(self.StateChanged)

        # self.verticalScrollBar().actionTriggered.connect(self.OnActionTriggered)

        # self.horizontalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        self.verticalScrollBar()
        self.startPos = QPoint()
        self.labelWaifu2xState = {}
        # self.setSceneRect(-self.width()//2, -self.height()//2, self.width(), self.height())
        QtOwner().owner.WindowsSizeChange.connect(self.ResetSize)
        self.isLastPageMode = False   # 是否切换到上一页


    @property
    def readImg(self):
        return self.parent().readImg

    @property
    def frame(self):
        return self.parent()

    @property
    def maxPic(self):
        return self.parent().readImg.maxPic

    @property
    def qtTool(self):
        return self.parent().readImg.qtTool

    @property
    def curIndex(self):
        return self.readImg.curIndex

    @property
    def scaleCnt(self):
        return self.readImg.frame.scaleCnt

    def radioWidth(self):
        return int(self.devicePixelRatioF() * self.width())

    def radioWidthF(self):
        return self.devicePixelRatioF() * self.width()

    def radioHeight(self):
        return int(self.devicePixelRatioF() * self.height())

    def radioHeightF(self):
        return self.devicePixelRatioF() * self.height()

    # def HValueChange(self, v):
    #     print("hv:" +str(v) +", max:"+str(self.horizontalScrollBar().maximum())+"scene:"+str(self.width()) + " pic"+str(self.graphicsItem1.pixmap().width()))

    # def Finished(self):
    #     QtOwner().readForm.frame.scrollArea.OnValueChange(self.value())

    def wheelEvent(self, e: QWheelEvent):
        if (QApplication.keyboardModifiers() == Qt.ControlModifier):
            if self.frame.scaleCnt <= -20:
                return

            if e.angleDelta().y() < 0:
                v = 100+(self.frame.scaleCnt - 1)*10
                self.qtTool.ScalePicture2(v)
                # self.Scale(1/1.1)
            #     self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() - 10)
            else:
                v = 100 + (self.frame.scaleCnt + 1) * 10
                self.qtTool.ScalePicture2(v)
                # self.frame.scaleCnt += 1
                # self.Scale(1.1)
            #     self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() + 10)
            # print("scale:{}".format(self.frame.scaleCnt))
            return

        if not ReadMode.isScroll(self.parent().qtTool.stripModel):
            if e.angleDelta().y() < 0:
                if abs(self.verticalScrollBar().value() - self.verticalScrollBar().maximum()) <= 5:
                    self.parent().qtTool.NextPage()
                    return
            else:
                if self.verticalScrollBar().value() <= 5:
                    self.parent().qtTool.LastPage()
                    return
        if e.angleDelta().y() < 0:
            value = int(self.qtTool.scrollSpeed.value())
        else:
            value = - int(self.qtTool.scrollSpeed.value())

        if ReadMode.isUpDown(self.initReadMode):
            self.vScrollBar.scrollValue(value)
        else:
            self.hScrollBar.scrollValue(value)

    def Scale(self, ratio):
        oldValue = self.GetScrollBar().value()
        self.GetScrollBar().SaveLastPosition()
        # self.GetScrollBar().SetChangeState(True)
        # oldValue = self.verticalScrollBar().value()
        # subPos = self.GetSubPos(oldValue)

        self.scale(ratio, ratio)
        self.ScaleResetVer()
        newValue = self.GetScrollBar().value()
        print("scale, oldv:{}, newV:{}, newV2:{}".format(oldValue, newValue, oldValue*ratio))
        
        # for k, v in self.labelSize.items():
            # self.labelSize[k] *= ratio
        self.ResetLabelSize(self.qtTool.maxPic)

        # if self.qtTool.stripModel == ReadMode.UpDown:
        #     curPos = self.labelSize.get(self.curIndex, 0)
        #     self.verticalScrollBar().ForceSetValue2(curPos + subPos*ratio, ratio > 1)
        # elif ReadMode.isScroll(self.qtTool.stripModel):
        #     self.horizontalScrollBar().ForceSetValue2(oldValue * ratio, ratio > 1)

        # self.GetScrollBar().SetChangeState(False)
        # self.ResetMaxNum(notChange=True)
        self.GetScrollBar().SaveLastPositionEnd()

    def GetSubPos(self, oldV):
        if self.initReadMode != ReadMode.UpDown:
            return 0
        oldIndex = self.curIndex
        oldMinV = self.labelSize.get(oldIndex, 0)
        subV = (oldV - oldMinV)
        return subV

    def ScaleReset(self, oldScaleCnt):
        # self.GetScaleCntRatio()
        self.frame.scaleCnt = 0
        oldV = self.GetScrollBar().value()
        # subPos = self.GetSubPos(oldV)
        self.GetScrollBar().SaveLastPosition()
        
        self.resetTransform()
        # newV = self.verticalScrollBar().value()
        #  需要重新计算原始的位置
        # if oldScaleCnt > 0:
        #     isBig = True
        # else:
        #     isBig = False
        # # self.GetScrollBar().SetChangeState(True)
        # if oldScaleCnt != 0:
        #     for i in range(abs(oldScaleCnt)):
        #         if oldScaleCnt > 0:
        #             ratio = 1.1
        #         else:
        #             ratio = 0.9
        #         # if ReadMode.isScroll(self.qtTool.stripModel):
        #             # self.horizontalScrollBar().ForceSetValue2(self.horizontalScrollBar().value() * ratio, ratio>1)
        # newV2 = self.verticalScrollBar().value()
        # print(oldV, newV, newV2)
        # if oldScaleCnt != 0:
        #     for i in range(abs(oldScaleCnt)):
        #         if oldScaleCnt > 0:
        #             self.scale(0.9, 0.9)
        #         else:
        #             self.scale(1.1, 1.1)

        self.ResetLabelSize(self.qtTool.maxPic)
        # if self.qtTool.stripModel == ReadMode.UpDown:
            # oldMinV = self.labelSize.get(self.curIndex, 0)
            # self.verticalScrollBar().ForceSetValue2(oldMinV+subPos, isBig)
        # self.GetScrollBar().SetChangeState(False)
        self.GetScrollBar().SaveLastPositionEnd()

    def ResetSize(self):
        self.qtTool.ChangeReadMode2(self.readImg.stripModel.value)

    def ScaleResetVer(self):
        if not ReadMode.isScroll(self.initReadMode) or self.initReadMode == ReadMode.UpDown:
            if self.scaleCnt != 0:
                self.horizontalScrollBar().ForceSetValue((self.horizontalScrollBar().maximum() / 2))
            else:
                self.horizontalScrollBar().ForceSetValue(0)
        else:
            if self.scaleCnt != 0:
                self.verticalScrollBar().ForceSetValue((self.verticalScrollBar().maximum() / 2))
            else:
                self.verticalScrollBar().ForceSetValue(0)

    def SetLabel(self, label, i):
        text = str(i + 1)
        font = QFont()
        font.setPointSize(64)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)
        label.setText(text)

    # 滑动切换上一页
    def ScrollNextPage(self):
        self.qtTool.NextPage()
        return

    # 滑动切换下一页
    def ScrollLastPage(self):
        self.qtTool.LastPage()
        return

    def ScrollValue(self, value):
        # if self.parent().qtTool.stripModel not in [ReadMode.LeftRight, ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
        #     if value > 0:
        #         if abs(self.verticalScrollBar().value() - self.verticalScrollBar().maximum()) <= 5:
        #             self.parent().qtTool.NextPage()
        #             return
        #     else:
        #         if self.verticalScrollBar().value() <= 5:
        #             self.parent().qtTool.LastPage()
        #             return

        if self.initReadMode in [ReadMode.UpDown, ReadMode.LeftRight, ReadMode.RightLeftDouble2, ReadMode.Samewight,
                                 ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            if self.initReadMode == ReadMode.Samewight and self.vScrollBar.value() >= self.vScrollBar.maximum():
                self.ScrollNextPage()
            else:
                self.vScrollBar.scrollValue(value)
            # QScroller.scroller(self).scrollTo(QPoint(0, self.verticalScrollBar().value() + value), 500)
        else:
            self.hScrollBar.scrollValue(value)
            # QScroller.scroller(self).scrollTo(QPoint(self.horizontalScrollBar().value() + value, 0), 500)
        return

    def eventFilter(self, obj, ev) -> bool:
        # print(obj, ev.type())
        if obj == self.graphicsScene:
            if ev.type() == QEvent.KeyPress:
                return True
            elif ev.type() == QEvent.KeyRelease:
                if not self.frame.helpLabel.isHidden():
                    self.frame.helpLabel.hide()
                    return True
                if ev.key() == Qt.Key_Down:
                    self.ScrollValue(self.height() / 2)
                elif ev.key() == Qt.Key_Up:
                    self.ScrollValue(-self.height() / 2)
                elif ev.key() == Qt.Key_Left:
                    self.ScrollLastPage()
                elif ev.key() == Qt.Key_Right:
                    self.ScrollNextPage()
                elif ev.key() == Qt.Key_Escape:
                    self.qtTool.ReturnPage()
                elif ev.key() == Qt.Key_F5:
                    self.qtTool.SwitchScrollAndTurn()
                elif ev.key() == Qt.Key_F10:
                    self.readImg.ChangeDoublePage()
                elif ev.key() == Qt.Key_F11:
                    self.qtTool.FullScreen()
                elif ev.key() == Qt.Key_F2:
                    self.qtTool.curWaifu2x.click()

                elif ev.key() == Qt.Key_F4:
                    self.readImg.CopyLastFile()
                elif ev.key() == Qt.Key_F3:
                    self.readImg.CopyFile()
                elif ev.key() == Qt.Key_F1:
                    self.readImg.CopyPicture()

                elif ev.key() == Qt.Key_F12:
                    self.readImg.ShowAndCloseTool()
                elif ev.key() == Qt.Key_Space:
                    self.ScrollValue(self.height())
                elif ev.modifiers() == Qt.ShiftModifier and ev.key() == Qt.Key_Left:
                    self.qtTool.OpenLastEps()
                elif ev.modifiers() == Qt.ShiftModifier and ev.key() == Qt.Key_Right:
                    self.qtTool.OpenNextEps()
                elif ev.key() == Qt.Key_Plus or ev.key() == Qt.Key_Equal:
                    self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() + 10)
                elif ev.key() == Qt.Key_Minus:
                    self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() - 10)
                return True
            elif ev.type() == QEvent.GraphicsSceneMousePress:
                if ev.button() == Qt.MouseButton.LeftButton:
                    self.startPos = ev.screenPos()
            elif ev.type() == QEvent.GraphicsSceneMouseRelease:
                if not self.frame.helpLabel.isHidden():
                    self.frame.helpLabel.hide()
                    return True
                self.qtTool.CloseScrollAndTurn()
                if ev.button() == Qt.MouseButton.LeftButton:
                    if not self.frame.helpLabel.isHidden():
                        self.frame.helpLabel.hide()
                        return True
                    endPos = ev.screenPos()
                    subPos = (endPos - self.startPos)
                    if abs(subPos.x()) <= 20:
                        curPos = endPos - QtOwner().owner.pos()

                        # print(curPos, endPos, QtOwner().owner.pos(), self.width(), self.height())
                        if curPos.x() <= self.width() // 3:
                            if curPos.y() <= self.height() // 2:
                                self.readImg.ShowAndCloseTool()
                            else:
                                self.ScrollLastPage()
                        elif curPos.x() <= self.width() // 3 * 2:
                            if curPos.y() <= self.height() // 2:
                                self.ScrollValue(-self.height() / 2)
                            else:
                                self.ScrollValue(self.height() / 2)
                        else:
                            if curPos.y() <= self.height() // 2:
                                self.readImg.ShowAndCloseTool()
                            else:
                                self.ScrollNextPage()
        return False

    # def StateChanged(self, state):
    #     if state == QScroller.State.Inactive:
    #         self.OnValueChange(self.GetScrollBar().value())
        # return print(state)

    def GetScrollBar(self):
        if self.initReadMode == ReadMode.UpDown:
            return self.verticalScrollBar()
        else:
            return self.horizontalScrollBar()

    def GetOtherScrollBar(self):
        if self.initReadMode == ReadMode.UpDown:
            return self.horizontalScrollBar()
        else:
            return self.verticalScrollBar()

    # def OnActionTriggered(self, action):
    #     if action != QAbstractSlider.SliderMove:
    #         return
    #     self.OnValueChange(self.GetScrollBar().value())

    def InitAllQLabel(self, maxNum, curIndex):
        if not maxNum:
            return
        self.verticalScrollBar().ForceSetValue(0)
        # self.horizontalScrollBar().setValue(0)
        # self.oldValue = 0
        self.qtTool.CloseScrollAndTurn()
        # if self.initReadMode and self.readImg.stripModel != self.initReadMode:
        if self.initReadMode:
            for proxy in self.allItems:
                self.graphicsScene.removeItem(proxy)

            for item in [self.graphicsItem1, self.graphicsItem2]:
                self.graphicsScene.removeItem(item)

        # self.initReadMode = ReadMode.UpDown
        self.initReadMode = self.readImg.stripModel
        # TODO make PixMap
        # for label in [self.label1, self.label2]:
        #     self.SetLabel(label, 1)
        for item in self.allItems:
            if isinstance(item, QGraphicsProxyWidget):
                QtReadImgPoolManager().AddProxyItem(item)
            else:
                QtReadImgPoolManager().AddPixMapItem(item)

        self.allItems = []

        if ReadMode.isScroll(self.initReadMode):

            for i in range(0, maxNum):
                t1 = time.time()
                proxy = QtReadImgPoolManager().GetProxyItem()
                label = proxy.widget()

                self.SetLabel(label, i)
                # print(time.time() - t1)
                self.allItems.append(proxy)

                self.graphicsScene.addItem(proxy)
                label.resize(self.width(), self.height())
                label.setMinimumSize(self.width(), self.height())
                label.setMaximumSize(self.width(), self.height())

            self.ResetLabelSize(maxNum)
            for index, proxy in enumerate(self.allItems):
                value = self.labelSize.get(index)
                if self.initReadMode == ReadMode.UpDown:
                    proxy.setPos(0, value/self.devicePixelRatioF())
                else:
                    proxy.setPos(value/self.devicePixelRatioF(), 0)

            value = self.labelSize.get(curIndex)
            # self.oldValue = value
            self.GetScrollBar().ForceSetValue(value)
            # print(value)
            # print(self.labelSize)
        elif self.initReadMode in [ReadMode.LeftRight, ReadMode.Samewight]:

            self.graphicsItem1.setPos(0, 0)
            self.graphicsScene.addItem(self.graphicsItem1)
            # self.horizontalScrollBar().setMaximum(self.width())
        elif ReadMode.isDouble(self.initReadMode):
            self.graphicsItem1.setPos(0, 0)
            self.graphicsItem2.setPos(self.width() // 2, 0)
            self.graphicsScene.addItem(self.graphicsItem1)
            self.graphicsScene.addItem(self.graphicsItem2)
            self.horizontalScrollBar().setMaximum(self.width())
        self.ResetMaxNum()
        return

    def ResetMaxNum(self, addHeight=0, notChange=False):
        maxNum = self.maxPic
        if maxNum <= 0:
            return
        if self.initReadMode == ReadMode.RightLeftScroll:
            maxSize = max(self.width(), self.labelSize.get(-1, 0) - self.width()) + 50

            oldV = self.GetScrollBar().value()
            self.graphicsScene.setSceneRect(0, 0, maxSize, self.height())
            self.GetScrollBar().setMaximum(maxSize)
        elif self.initReadMode in [ReadMode.LeftRightScroll]:
            maxSize = max(self.width(), self.labelSize.get(maxNum, 0) - self.width()) + 50

            oldV = self.GetScrollBar().value()
            self.graphicsScene.setSceneRect(0, 0, maxSize, self.height())
            self.GetScrollBar().setMaximum(maxSize)
        elif self.initReadMode in [ReadMode.UpDown]:
            maxSize = max(self.height(), self.labelSize.get(maxNum, 0) - self.height()) + 50
            oldV = self.GetScrollBar().value()
            self.graphicsScene.setSceneRect(0, 0, self.width(), maxSize)
            self.GetScrollBar().setMaximum(maxSize)
        else:
            self.graphicsScene.setSceneRect(0, 0, self.width(), max(self.height(),
                                                                    self.graphicsItem1.pixmap().height() // self.graphicsItem1.pixmap().devicePixelRatio()))
            pictureHeight = self.graphicsItem1.pixmap().height() // self.graphicsItem1.pixmap().devicePixelRatio()
            pictureWight= self.graphicsItem1.pixmap().width() // self.graphicsItem1.pixmap().devicePixelRatio()
            self.verticalScrollBar().setMaximum(max(0, pictureHeight - self.height()))
            # if self.scaleCnt > 0:
            #     self.horizontalScrollBar().setMaximum(max(0, self.width()*0.1*self.scaleCnt))
            # else:
            #     self.horizontalScrollBar().setMaximum(0)
        self.ScaleResetVer()

    def ResetLabelSize(self, size):
        # 重新计算每个图片的位置
        if ReadMode.isScroll(self.initReadMode):
            if not self.allItems:
                return
            height = 0
            if self.initReadMode != ReadMode.RightLeftScroll:
                labelIndex = list(range(0, size))
                labelIndex.append(size)
            else:
                labelIndex = list(range(size - 1, -1, -1))
                labelIndex.append(-1)
            if labelIndex:
                for lenSize, i in enumerate(labelIndex):
                    # self.labelSize[i] = height * self.GetScaleCntRatio()
                    self.labelSize[i] = height
                    if lenSize == len(labelIndex) - 1:
                        continue

                    proxy = self.allItems[i]
                    if self.initReadMode == ReadMode.UpDown:
                        if isinstance(proxy, QGraphicsProxyWidget):
                            height += proxy.widget().height()
                        else:
                            height += proxy.pixmap().height() // proxy.pixmap().devicePixelRatio()
                    else:
                        if isinstance(proxy, QGraphicsProxyWidget):
                            height += proxy.widget().width()
                        else:
                            height += proxy.pixmap().width() // proxy.pixmap().devicePixelRatio()

        self.ResetMaxNum(notChange=True)

    def GetLabel(self, index):
        if self.qtTool.stripModel in [ReadMode.LeftRight, ReadMode.Samewight]:
            return self.graphicsItem1
        elif self.qtTool.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftDouble2]:
            if index == self.readImg.curIndex:
                return self.graphicsItem2
            else:
                return self.graphicsItem1
        elif self.qtTool.stripModel == ReadMode.LeftRightDouble:
            if index == self.readImg.curIndex:
                return self.graphicsItem1
            else:
                return self.graphicsItem2
        elif ReadMode.isScroll(self.qtTool.stripModel):
            return self.allItems[index]

    def MakePixItem(self, index):
        if index >= self.maxPic:
            text = "End"
        else:
            text = str(index + 1)
        font = QFont()
        font.setPointSize(64)
        fm = QFontMetrics(font)
        p = QPixmap(self.radioWidth(), self.radioHeight())
        p.setDevicePixelRatio(self.devicePixelRatio())
        rect = QRect(self.width() // 2, self.height() // 2 - fm.height() // 2, self.width() // 2,
                     self.height() // 2 + fm.height() // 2)
        p.fill(Qt.transparent)
        painter = QPainter(p)
        painter.setFont(font)
        if Setting.ThemeIndex.autoValue == 1:
            painter.setPen(Qt.white)
        else:
            painter.setPen(Qt.black)
        painter.drawText(rect, text)
        return p

    def PixmapToLabel(self, index):
        if ReadMode.isScroll(self.initReadMode):
            proxy = self.GetLabel(index)
            if isinstance(proxy, QGraphicsPixmapItem):
                oldPox = proxy.pos()
                self.graphicsScene.removeItem(proxy)
                newProxy = QtReadImgPoolManager().GetProxyItem()
                if not isinstance(newProxy, QGraphicsProxyWidget):
                    raise
                label = newProxy.widget()
                # label.setPixmap(QPixmap())
                text = str(index + 1)
                font = QFont()
                font.setPointSize(64)
                label.setAlignment(Qt.AlignCenter)
                label.setFont(font)
                label.setText(text)
                label.resize(proxy.pixmap().width() // proxy.pixmap().devicePixelRatio(),
                             proxy.pixmap().height() // proxy.pixmap().devicePixelRatio())
                newProxy.widget().setMinimumSize(proxy.pixmap().width() // proxy.pixmap().devicePixelRatio(),
                                                 proxy.pixmap().height() // proxy.pixmap().devicePixelRatio())
                newProxy.widget().setMaximumSize(proxy.pixmap().width() // proxy.pixmap().devicePixelRatio(),
                                                 proxy.pixmap().height() // proxy.pixmap().devicePixelRatio())
                newProxy.setPos(oldPox)
                # print(index, newProxy.widget().width(), newProxy.widget().height())
                self.graphicsScene.addItem(newProxy)
                self.allItems[index] = newProxy
                # if proxy:
                #     del proxy
                QtReadImgPoolManager().AddPixMapItem(proxy)

    def LabelToPixmap(self, index):
        proxy = self.GetLabel(index)
        if ReadMode.isScroll(self.initReadMode):
            if isinstance(proxy, QGraphicsProxyWidget):
                oldHeight, oldWidth = proxy.widget().height(), proxy.widget().width()
                oldPox = proxy.pos()
                self.graphicsScene.removeItem(proxy)
                newProxy = QtReadImgPoolManager().GetPixMapItem()

                assert isinstance(newProxy, QGraphicsPixmapItem)
                newProxy.setPos(oldPox)
                self.graphicsScene.addItem(newProxy)
                self.allItems[index] = newProxy
                QtReadImgPoolManager().AddProxyItem(proxy)
                return oldHeight, oldWidth
            else:
                return proxy.pixmap().height() // proxy.pixmap().devicePixelRatio(), proxy.pixmap().width() // proxy.pixmap().devicePixelRatio()
        elif (self.initReadMode == ReadMode.RightLeftDouble and index == self.readImg.curIndex) or (
                self.initReadMode == ReadMode.RightLeftDouble2 and index == self.readImg.curIndex) or (
                self.initReadMode == ReadMode.LeftRightDouble and index != self.readImg.curIndex):
            self.graphicsItem2.pixmap().height(), self.graphicsItem2.pixmap().width()
        return self.graphicsItem1.pixmap().height(), self.graphicsItem1.pixmap().width()

    def ClearPixItem(self):
        self.allItemsState.clear()
        self.allItemsScale.clear()
        self.ClearOtherPictureShow([])
        # self.SetPixIem(self.readImg.curIndex, None)
        # if self.readImg.curIndex + 1 < self.readImg.maxPic:
        #     self.SetPixIem(self.readImg.curIndex + 1, None)
        return

    def IsAlreadLoad(self, index, waifu2x):
        if waifu2x:
            state = 2
        else:
            state = 1
        if self.allItemsState.get(index) == state and self.allItemsScale.get(index) == self.scaleCnt and ReadMode.isScroll(self.readImg.stripModel):
            return True
        return False

    def SetPixIem(self, index, data, isWaifu2x=False):
        if not self.allItems and ReadMode.isScroll(self.readImg.stripModel):
            return
        notPic = False
        if not data:
            notPic = True
            # self.labelWaifu2xState[index] = isWaifu2x
            if ReadMode.isScroll(self.initReadMode):
                self.PixmapToLabel(index)
                self.allItemsState[index] = 0
                self.allItemsScale[index] = 0
                return
            else:
                data = self.MakePixItem(index)

        # else:
            # data.setDevicePixelRatio(self.devicePixelRatio())

        oldHeight, oldWidth = self.LabelToPixmap(index)
        label = self.GetLabel(index)
        # if ReadMode.isScroll(self.readImg.stripModel):
            # TODO，优化
            # waifu2x = self.labelWaifu2xState.get(index, False)
            # if label.pixmap() and waifu2x == isWaifu2x and not self.resetImg:
            #     return
        # self.labelWaifu2xState[index] = isWaifu2x
        oldPos = label.pos()
        radio = data.devicePixelRatio()

        # 非滚动模式，需要进行缩放
        # if not ReadMode.isScroll(self.initReadMode):
        #     toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, self.scaleCnt, self.width(), self.height(), False)
        #     data2 = QPixmap(data)
        #     newData = data2.scaled(toW * radio, toH * radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # else:
        #     newData = data

        toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, self.scaleCnt, self.width(), self.height(), False)
        data2 = QPixmap(data)
        newData = data2.scaled(toW * radio, toH * radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        pos = QtFileData.GetReadToPos(self.qtTool.stripModel, self.width(), self.height(), newData.width() / radio,
                                      newData.height() // radio, index, self.readImg.curIndex, oldPos)
        # print(index, pos, radio, newData.size(), self.size())
        label.setPos(pos)
        # print("set index, {}".format(index))
        label.setPixmap(newData)
        self.allItemsScale[index] = self.scaleCnt
        if not notPic:
            if isWaifu2x:
                self.allItemsState[index] = 2
            else:
                self.allItemsState[index] = 1
        else:
            self.allItemsState[index] = 0

        self.GetScrollBar().SaveLastPosition()
        if self.initReadMode == ReadMode.UpDown:
            self.UpdateOtherHeight(index, oldHeight, label.pixmap().height() // radio)
        else:
            self.UpdateOtherHeight(index, oldWidth, label.pixmap().width() // radio)
        self.GetScrollBar().SaveLastPositionEnd()

    def SetGifData(self, index, data, p2, isWaifu2x=False):
        label = self.GetLabel(index)
        # self.labelWaifu2xState[index] = isWaifu2x
        oldPos = label.pos()
        radio = p2.devicePixelRatio()

        toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, self.scaleCnt, self.width(), self.height(), False)
        newData = p2.scaled(toW * radio, toH * radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        pos = QtFileData.GetReadToPos(self.qtTool.stripModel, self.width(), self.height(), newData.width()/radio ,
                                      newData.height()//radio , index, self.readImg.curIndex, oldPos)
        # print(index, pos, radio, newData.size(), self.size())
        label.setPos(pos)
        label.SetGifData(data, newData.width(), newData.height())
        self.graphicsScene.setSceneRect(0, 0, self.width(), max(self.height(),
                                                                self.graphicsItem1.height() // self.graphicsItem1.devicePixelRatio()))
        if not ReadMode.isScroll(self.initReadMode):
            pictureHeight = self.graphicsItem1.height() // self.graphicsItem1.devicePixelRatio()
        else:
            pictureHeight = self.graphicsItem1.height() // self.graphicsItem1.devicePixelRatio() * self.devicePixelRatioF()
        self.verticalScrollBar().setMaximum(max(0, pictureHeight - self.height()))

    # def UpdateAllPixIem(self):
    #     if not self.allItems and ReadMode.isScroll(self.readImg.stripModel):
    #         return
    #     if ReadMode.isScroll(self.readImg.stripModel):
    #         for i in range(self.readImg.curIndex, config.PreLook+1):
    #             self.UpdatePixIem(i)
    #         return
    #     elif ReadMode.isDouble(self.readImg.stripModel):
    #         self.UpdatePixIem(self.readImg.curIndex)
    #         self.UpdatePixIem(self.readImg.curIndex+1)
    #     else:
    #         self.UpdatePixIem(self.readImg.curIndex)
    #     return

    # def UpdatePixIem(self, index, isWaifu2x=False):
    #     if not self.allItems and ReadMode.isScroll(self.readImg.stripModel):
    #         return
    #     oldHeight, oldWidth = self.LabelToPixmap(index)
    #     label = self.GetLabel(index)
    #     # if ReadMode.isScroll(self.readImg.stripModel):
    #         # TODO，优化
    #         # waifu2x = self.labelWaifu2xState.get(index, False)
    #         # if label.pixmap() and waifu2x == isWaifu2x and not self.resetImg:
    #             # return
    #     # self.labelWaifu2xState[index] = isWaifu2x
    #     oldPos = label.pos()
    #     # toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, self.scaleCnt, self.width(), self.height())
    #     # newData = data.scaled(toW * radio, toH * radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #     radio = self.devicePixelRatio()
    #     newData = label.pixmap()
    #     pos = QtFileData.GetReadToPos(self.qtTool.stripModel, self.width(), self.height(), newData.width() / radio,
    #                                   newData.height() // radio, index, self.readImg.curIndex, oldPos)
    #     # print(index, pos, radio, newData.size(), self.size())
    #     label.setPos(pos)
    #     if self.initReadMode == ReadMode.UpDown:
    #         self.UpdateOtherHeight(index, oldHeight, label.pixmap().height() // radio)
    #     else:
    #         self.UpdateOtherHeight(index, oldWidth, label.pixmap().width() // radio)

    # def GetScaleCntRatio(self):
    #     return (pow(1.1, self.scaleCnt) if self.scaleCnt >= 0 else pow(0.9, abs(self.scaleCnt)))

    def UpdateOtherHeight(self, index, oldHeight, height):
        # 修改了图片导致label长宽变化，重新计算
        # addHeight = (height - oldHeight)
        # addHeight2 = (height - oldHeight) * (pow(1.1, self.scaleCnt) if self.scaleCnt >= 0 else pow(0.9, abs(self.scaleCnt)))
        # addHeight2 = (height - oldHeight)
        # if addHeight == 0:
        #     return

        oldValue = self.GetScrollBar().value()
        needAddHeight = 0
        if self.initReadMode == ReadMode.RightLeftScroll:
            indexList = list(range(index - 1, -1, -1))
            indexList.append(-1)
            # TODO 需要重新定位
            curPixcurSize = self.labelSize.get(index)
            # if curPixcurSize <= oldValue:
            #     needAddHeight = addHeight
                # self.GetScrollBar().ResetAniValueByAdd(oldValue, addHeight2)
                # self.oldValue = self.GetScrollBar().value()

        elif self.initReadMode in [ReadMode.LeftRightScroll, ReadMode.UpDown]:
            indexList = list(range(index + 1, self.readImg.maxPic))
            indexList.append(self.readImg.maxPic)
            # if index < self.readImg.curIndex:
            #     needAddHeight = addHeight
            curPixcurSize = self.labelSize.get(index)
            # TODO 需要重新定位
            # if curPixcurSize < oldValue:
            #     needAddHeight = addHeight
                # self.GetScrollBar().ResetAniValueByAdd(oldValue, addHeight2)
                # self.oldValue = self.GetScrollBar().value()

        else:
            self.ResetMaxNum()
            if self.initReadMode in [ReadMode.Samewight, ReadMode.LeftRight] and self.isLastPageMode:
                self.verticalScrollBar().ForceSetValue(self.verticalScrollBar().maximum())
            return
        # print("sub value, {}, {}, {}".format(index, addHeight, needAddHeight))

        self.ResetLabelSize(self.qtTool.maxPic)
        # for lenSize, i in enumerate(indexList):

            # self.labelSize[i] += addHeight2
            # if lenSize == len(indexList) - 1:
            #     continue
        for i in range(0, self.maxPic):
            proxy = self.allItems[i]
            oldPos = proxy.pos()
            if self.initReadMode == ReadMode.UpDown:
                y = self.labelSize.get(i, 0)
                if isinstance(proxy, QGraphicsPixmapItem):
                    radio = proxy.pixmap().devicePixelRatio()
                    proxy.setPos(max(0, self.width() // 2 - proxy.pixmap().width() // radio // 2), y)
                else:
                    proxy.setPos(oldPos.x(), y)
            else:
                x = self.labelSize.get(i, 0)
                if isinstance(proxy, QGraphicsPixmapItem):
                    radio = proxy.pixmap().devicePixelRatio()
                    proxy.setPos(x, max(0, self.height() // 2 - proxy.pixmap().height() // radio // 2))
                else:
                    proxy.setPos(x, oldPos.y())

        self.ResetMaxNum(needAddHeight)
        return

    def ResetScrollValue(self, index):
        if ReadMode.isScroll(self.initReadMode):
            value = self.labelSize.get(index)
            self.GetScrollBar().ForceSetValue(value)

    # 上一页
    def ChangeLastPage(self, index):
        # TODO 取消其他图片的显示, 节约内存占用
        if ReadMode.isScroll(self.initReadMode):
            self.ClearOtherPictureShow(range(self.curIndex, self.curIndex + config.PreLook))
            # if index + config.PreLoading < self.maxPic:
            #     self.SetPixIem(index + config.PreLoading, None)
        elif ReadMode.isDouble(self.initReadMode):
            self.SetPixIem(index - 1, None)
        self.isLastPageMode = True
        self.ReloadImg()
        return

    # 下一页
    def ChangeNextPage(self, index):
        # TODO 取消其他图片的显示, 节约内存占用
        if ReadMode.isScroll(self.initReadMode):
            # if index - 1 >= 0:
            #     self.SetPixIem(index - 1, None)
            self.ClearOtherPictureShow(range(self.curIndex, self.curIndex + config.PreLook))
        elif ReadMode.isDouble(self.initReadMode):
            self.SetPixIem(index + 1, None)
        self.isLastPageMode = False
        self.ReloadImg()
        return

    # 跳页
    def ChangePage(self, oldIndex, index):

        # TODO 取消其他图片的显示, 节约内存占用
        if ReadMode.isScroll(self.initReadMode):
            self.ClearOtherPictureShow(range(oldIndex + 1, min(oldIndex + config.PreLoading, self.maxPic)))
            value = self.labelSize.get(index)
            self.GetScrollBar().ForceSetValue(value)
        self.isLastPageMode = False
        self.ReloadImg()
        return

    def ClearOtherPictureShow(self, saveIndex):
        if ReadMode.isScroll(self.initReadMode):
            indexSet = set(saveIndex)
            for i, state in self.allItemsState.items():
                if i in indexSet:
                    continue
                if state > 0 and i < self.maxPic:
                    self.SetPixIem(i, None)
            # self.SetPixIem(oldIndex, None)
            # for newIndex in range(oldIndex + 1, min(oldIndex + config.PreLoading, self.maxPic)):
            #     self.SetPixIem(newIndex, None)
            # value = self.labelSize.get(index)
            # self.GetScrollBar().ForceSetValue(value)

    # 缩放
    def ChangeScale(self, scale=1):
        print("change scale, mode={}, scale={}, change:={}".format(self.initReadMode, self.frame.scaleCnt, scale))
        self.readImg.ShowImgAll()
        return
        if not ReadMode.isScroll(self.initReadMode):
            # 非滚动模式，通过QPixmap进行缩放
            self.readImg.ShowImgAll()
            return

        if self.scaleCnt == 0:
            return

        for i in range(abs(scale)):
            if scale > 0:
                self.Scale(1.1)
            else:
                self.Scale(0.9)
        # self.setSceneRect(-self.width()//2, -self.height()//2, self.width(), self.height())
        # self.resetImg = True
        # self.ReloadImg()
        # self.UpdateAllPixIem()
        # for index, v in self.readImg.pictureData.items():
        #     assert isinstance(v, QtFileData)
        #     if v.cacheImageScale != self.scaleCnt and v.data:
        #         self.readImg.CheckToQImage(index, v, False)
        #     if v.cacheWaifu2xImageScale != self.scaleCnt and v.waifuData:
        #         self.readImg.CheckToQImage(index, v, True)
        # self.resetImg = False

        return

    # 
    def ReloadImg(self):
        if self.initReadMode in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble2, ReadMode.RightLeftDouble,
                                 ReadMode.LeftRight, ReadMode.Samewight]:
            self.verticalScrollBar().ForceSetValue(0)
        # self.UpdateAllPixIem()
        self.readImg.CheckClearProcess()
        self.readImg.ShowImgAll()
        # self.readImg.CheckLoadPicture()