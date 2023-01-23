import time

from PySide6.QtCore import Qt, QEvent, QPoint, Signal, QRect, QFile
from PySide6.QtGui import QPainter, QFont, QPixmap, QFontMetrics, QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QFrame, QGraphicsItem, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsProxyWidget, QScroller, QAbstractSlider, QApplication, QLabel

from component.label.msg_label import MsgLabel
from component.scroll.read_scroll import ReadScroll
from component.scroll.smooth_scroll import SmoothScroll
from config import config
from qt_owner import QtOwner
from config.setting import Setting
from tools.str import Str
from view.read.read_enum import ReadMode, QtFileData
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

        self.vScrollBar = ReadScroll()
        self.vScrollBar.setOrientation(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(self.vScrollBar)

        # self.animation.finished.connect(self.Finished)

        self.hScrollBar = ReadScroll()
        self.hScrollBar.setOrientation(Qt.Orientation.Horizontal)
        self.setHorizontalScrollBar(self.hScrollBar)

        self.changeLastPage.connect(self.ChangeLastPage)
        self.changeNextPage.connect(self.ChangeNextPage)
        self.changePage.connect(self.ChangePage)
        self.changeScale.connect(self.ChangeScale)

        # self.setInteractive(False)
        self.setTransformationAnchor(self.NoAnchor)
        self.setResizeAnchor(self.NoAnchor)
        self.setDragMode(self.NoDrag)
        self.setFrameStyle(QFrame.NoFrame)
        self.setObjectName("graphicsView")
        # self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        # self.graphicsView.setCursor(Qt.OpenHandCursor)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setCacheMode(QGraphicsView.CacheBackground)
        # self.setCacheMode(QGraphicsView.CacheNone)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

        # self.graphicsGroup = QGraphicsItemGroup()
        # self.graphicsGroup.setFlag(QGraphicsItem.ItemIsFocusable)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.setScene(self.graphicsScene)
        # self.graphicsScene.addItem(self.graphicsGroup)
        self.graphicsItem1 = ReadQGraphicsProxyWidget()
        self.graphicsItem1.setWidget(QLabel())
        self.graphicsItem2 = ReadQGraphicsProxyWidget()
        self.graphicsItem2.setWidget(QLabel())
        # self.graphicsItem1.setFlag(QGraphicsItem.ItemIsFocusable)
        # self.graphicsItem2.setFlag(QGraphicsItem.ItemIsFocusable)

        self.setMinimumSize(10, 10)
        self.graphicsScene.installEventFilter(self)
        # self.installEventFilter(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.testItem = QGraphicsPixmapItem()
        self.allItems = []
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
        self.oldValue = 0
        self.resetImg = False
        # QScroller.scroller(self).stateChanged.connect(self.StateChanged)

        self.verticalScrollBar().actionTriggered.connect(self.OnActionTriggered)

        self.horizontalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        self.verticalScrollBar()
        self.startPos = QPoint()
        self.labelWaifu2xState = {}
        # self.setSceneRect(-self.width()//2, -self.height()//2, self.width(), self.height())
        QtOwner().owner.WindowsSizeChange.connect(self.ChangeScale)

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

    # def Finished(self):
    #     QtOwner().readForm.frame.scrollArea.OnValueChange(self.value())

    def wheelEvent(self, e):
        if (QApplication.keyboardModifiers() == Qt.ControlModifier):
            if e.angleDelta().y() < 0:
                self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() - 10)
            else:
                self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() + 10)
            return

        from view.read.read_view import ReadMode
        if self.parent().qtTool.stripModel not in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if e.angleDelta().y() < 0:
                if abs(self.verticalScrollBar().value() - self.verticalScrollBar().maximum()) <= 5:
                    self.parent().qtTool.NextPage()
                    return
            else:
                if self.verticalScrollBar().value() <= 5:
                    self.parent().qtTool.LastPage()
                    return

        return SmoothScroll.wheelEvent(self, e)

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

        if self.initReadMode in [ReadMode.UpDown, ReadMode.LeftRight, ReadMode.RightLeftDouble2,
                                 ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            self.vScrollBar.Scroll(value, 100)
            # QScroller.scroller(self).scrollTo(QPoint(0, self.verticalScrollBar().value() + value), 500)
        else:
            self.hScrollBar.Scroll(value, 100)
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

    def StateChanged(self, state):
        if state == QScroller.State.Inactive:
            self.OnValueChange(self.GetScrollBar().value())
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

    def OnActionTriggered(self, action):
        if action != QAbstractSlider.SliderMove:
            return
        self.OnValueChange(self.GetScrollBar().value())

    def OnValueChange(self, value):
        addValue = value - self.oldValue
        # self.UpdateScrollBar(value)
        self.oldValue = value

        if self.initReadMode not in [ReadMode.LeftRightScroll, ReadMode.RightLeftScroll, ReadMode.UpDown]:
            return

        curPictureSize = self.labelSize.get(self.readImg.curIndex)
        nextPictureSize = self.labelSize.get(self.readImg.curIndex + 1, 0)
        if self.initReadMode == ReadMode.RightLeftScroll:
            while True:
                newValue = value + self.width()
                ## 切换上一图片
                if addValue > 0 and value >= nextPictureSize:
                    if self.readImg.curIndex <= 0:
                        QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastPage))
                        return
                    self.readImg.curIndex -= 1
                    # print(self.readImg.curIndex)
                    self.changeLastPage.emit(self.readImg.curIndex)

                ## 切换下一图片
                elif addValue < 0 and newValue < curPictureSize:
                    if self.readImg.curIndex >= self.readImg.maxPic - 1:
                        QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextPage))
                        return
                    self.readImg.curIndex += 1
                    # print(self.readImg.curIndex)
                    self.changeNextPage.emit(self.readImg.curIndex)
                else:
                    break
                curPictureSize = self.labelSize.get(self.readImg.curIndex)
                nextPictureSize = self.labelSize.get(self.readImg.curIndex + 1, 0)
        else:
            while True:
                ## 切换上一图片
                if addValue < 0 and value < curPictureSize:
                    if self.readImg.curIndex <= 0:
                        QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastPage))
                        return
                    self.readImg.curIndex -= 1
                    self.changeLastPage.emit(self.readImg.curIndex)

                ## 切换下一图片
                elif addValue > 0 and value >= nextPictureSize:
                    if self.readImg.curIndex >= self.readImg.maxPic - 1:
                        QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextPage))
                        return
                    self.readImg.curIndex += 1
                    self.changeNextPage.emit(self.readImg.curIndex)
                else:
                    break

                curPictureSize = self.labelSize.get(self.readImg.curIndex)
                nextPictureSize = self.labelSize.get(self.readImg.curIndex + 1, 0)
        return

    def InitAllQLabel(self, maxNum, curIndex):
        if not maxNum:
            return
        self.verticalScrollBar().setValue(0)
        self.horizontalScrollBar().setValue(0)
        self.oldValue = 0
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

        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:

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
                    proxy.setPos(0, value)
                else:
                    proxy.setPos(value, 0)

            value = self.labelSize.get(curIndex)
            self.oldValue = value
            self.GetScrollBar().setValue(value)
            # print(value)
            # print(self.labelSize)
        elif self.initReadMode in [ReadMode.LeftRight]:

            self.graphicsItem1.setPos(0, 0)
            self.graphicsScene.addItem(self.graphicsItem1)
            self.horizontalScrollBar().setMaximum(self.width())
        elif ReadMode.isDouble(self.initReadMode):
            self.graphicsItem1.setPos(0, 0)
            self.graphicsItem2.setPos(self.width() // 2, 0)
            self.graphicsScene.addItem(self.graphicsItem1)
            self.graphicsScene.addItem(self.graphicsItem2)
            self.horizontalScrollBar().setMaximum(self.width())
        self.ResetMaxNum()
        return

    def ResetMaxNum(self):
        maxNum = self.maxPic
        if maxNum <= 0:
            return
        if self.initReadMode == ReadMode.RightLeftScroll:
            maxSize = max(self.width(), self.labelSize.get(-1, 0) - self.width()) + 50

            self.graphicsScene.setSceneRect(0, 0, maxSize, self.height())
            self.GetScrollBar().setMaximum(maxSize)
            self.GetOtherScrollBar().setMaximum(0)
        elif self.initReadMode in [ReadMode.LeftRightScroll]:
            maxSize = max(self.width(), self.labelSize.get(maxNum, 0) - self.width()) + 50

            self.graphicsScene.setSceneRect(0, 0, maxSize, self.height())
            self.GetScrollBar().setMaximum(maxSize)
            self.GetOtherScrollBar().setMaximum(0)
        elif self.initReadMode in [ReadMode.UpDown]:
            maxSize = max(self.height(), self.labelSize.get(maxNum, 0) - self.height()) + 50
            self.graphicsScene.setSceneRect(0, 0, self.width(), maxSize)
            self.GetScrollBar().setMaximum(maxSize)
            self.GetOtherScrollBar().setMaximum(0)
        else:
            self.graphicsScene.setSceneRect(0, 0, self.width(), max(self.height(),
                                                                    self.graphicsItem1.pixmap().height() // self.graphicsItem1.pixmap().devicePixelRatio()))
            self.verticalScrollBar().setMaximum(max(0,
                                                    self.graphicsItem1.pixmap().height() // self.graphicsItem1.pixmap().devicePixelRatio() - self.height()))
            self.horizontalScrollBar().setMaximum(0)

    def ResetLabelSize(self, size):
        # 重新计算每个图片的位置
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            height = 0
            if self.initReadMode != ReadMode.RightLeftScroll:
                labelIndex = list(range(0, size))
                labelIndex.append(size)
            else:
                labelIndex = list(range(size - 1, -1, -1))
                labelIndex.append(-1)
            if labelIndex:
                for lenSize, i in enumerate(labelIndex):
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

        self.ResetMaxNum()

    def GetLabel(self, index):
        if self.qtTool.stripModel == ReadMode.LeftRight:
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
        elif self.qtTool.stripModel in [ReadMode.LeftRightScroll, ReadMode.UpDown, ReadMode.RightLeftScroll]:
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
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
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
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            return proxy.height(), proxy.width()
        elif (self.initReadMode == ReadMode.RightLeftDouble and index == self.readImg.curIndex) or (
                        self.initReadMode == ReadMode.RightLeftDouble2 and index == self.readImg.curIndex) or (
                             self.initReadMode == ReadMode.LeftRightDouble and index != self.readImg.curIndex):
            self.graphicsItem2.pixmap().height(), self.graphicsItem2.pixmap().width()
        return self.graphicsItem1.pixmap().height(), self.graphicsItem1.pixmap().width()

    def ClearPixItem(self):
        self.SetPixIem(self.readImg.curIndex, None)
        if self.readImg.curIndex + 1 < self.readImg.maxPic:
            self.SetPixIem(self.readImg.curIndex + 1, None)
        return

    def SetGifData(self, index, data, width, height):
        if not self.allItems and self.readImg.stripModel in [ReadMode.UpDown, ReadMode.LeftRightScroll, ReadMode.RightLeftScroll]:
            return
        if not data:
            return
        label = self.GetLabel(index)

        oldPos = label.pos()
        toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, self.scaleCnt, self.width(), self.height())

        scale = min(toW / width, toH / height)
        label.setScale(scale)
        label.SetGifData(data, width, height)

        pos = QtFileData.GetReadToPos(self.qtTool.stripModel, self.width(), self.height(), label.width()*scale, label.height()*scale, index, self.readImg.curIndex, oldPos)
        label.setPos(pos)
        return

    def SetPixIem(self, index, data, isWaifu2x=False):
        if not self.allItems and self.readImg.stripModel in [ReadMode.UpDown, ReadMode.LeftRightScroll,
                                                             ReadMode.RightLeftScroll]:
            return
        if not data:
            self.labelWaifu2xState[index] = isWaifu2x
            if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
                self.PixmapToLabel(index)
                return
            else:
                data = self.MakePixItem(index)
        else:
            data.setDevicePixelRatio(self.devicePixelRatio())

        oldHeight, oldWidth = self.LabelToPixmap(index)
        label = self.GetLabel(index)
        if self.readImg.stripModel in [ReadMode.UpDown, ReadMode.LeftRightScroll, ReadMode.RightLeftScroll]:
            # TODO，优化
            waifu2x = self.labelWaifu2xState.get(index, False)
            if label.pixmap() and waifu2x == isWaifu2x and not self.resetImg:
                return
        self.labelWaifu2xState[index] = isWaifu2x
        oldPos = label.pos()
        radio = data.devicePixelRatio()
        toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, self.scaleCnt, self.width(), self.height())
        newData = data.scaled(toW * radio, toH * radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pos = QtFileData.GetReadToPos(self.qtTool.stripModel, self.width(), self.height(), newData.width() / radio,
                                      newData.height() // radio, index, self.readImg.curIndex, oldPos)
        # print(index, pos, radio, newData.size(), self.size())
        label.setPos(pos)
        label.setPixmap(newData)
        # print("pos:{}, pos:{} {} {}".format(pos, self.graphicsItem1.pos(), self.graphicsItem1.widget().devicePixelRatioF(), self.graphicsItem1.widget().size()))
        if self.initReadMode == ReadMode.UpDown:
            self.UpdateOtherHeight(index, oldHeight, label.pixmap().height() // radio)
        else:
            self.UpdateOtherHeight(index, oldWidth, label.pixmap().width() // radio)

    def UpdateOtherHeight(self, index, oldHeight, height):
        # 修改了图片导致label长宽变化，重新计算
        addHeight = height - oldHeight
        if addHeight == 0:
            return

        oldValue = self.GetScrollBar().value()

        if self.initReadMode == ReadMode.RightLeftScroll:
            indexList = list(range(index - 1, -1, -1))
            indexList.append(-1)
            # TODO 需要重新定位
            curPixcurSize = self.labelSize.get(index)
            if curPixcurSize <= oldValue:
                self.GetScrollBar().setValue(oldValue + addHeight)
                self.oldValue = self.GetScrollBar().value()

        elif self.initReadMode in [ReadMode.LeftRightScroll, ReadMode.UpDown]:
            indexList = list(range(index + 1, self.readImg.maxPic))
            indexList.append(self.readImg.maxPic)
            curPixcurSize = self.labelSize.get(index)
            # TODO 需要重新定位
            if curPixcurSize <= oldValue:
                self.GetScrollBar().setValue(oldValue + addHeight)
                self.oldValue = self.GetScrollBar().value()

        else:
            self.ResetMaxNum()
            return

        for lenSize, i in enumerate(indexList):

            self.labelSize[i] += addHeight
            if lenSize == len(indexList) - 1:
                continue

            proxy = self.allItems[i]
            oldPos = proxy.pos()
            if self.initReadMode == ReadMode.UpDown:
                if isinstance(proxy, QGraphicsPixmapItem):
                    radio = proxy.pixmap().devicePixelRatio()
                    proxy.setPos(max(0, self.width() // 2 - proxy.pixmap().width() // radio // 2),
                                 oldPos.y() + addHeight)
                else:
                    proxy.setPos(oldPos.x(), oldPos.y() + addHeight)
            else:
                if isinstance(proxy, QGraphicsPixmapItem):
                    radio = proxy.pixmap().devicePixelRatio()
                    proxy.setPos(oldPos.x() + addHeight,
                                 max(0, self.height() // 2 - proxy.pixmap().height() // radio // 2))
                else:
                    proxy.setPos(oldPos.x() + addHeight, oldPos.y())

        self.ResetMaxNum()
        return

    def ResetScrollValue(self, index):
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            value = self.labelSize.get(index)
            self.GetScrollBar().setValue(value)

    def ChangeLastPage(self, index):
        # TODO 取消其他图片的显示, 节约内存占用
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if index + config.PreLoading < self.maxPic:
                self.SetPixIem(index + config.PreLoading, None)
        elif ReadMode.isDouble(self.initReadMode):
            self.SetPixIem(index - 1, None)
        self.ReloadImg()
        return

    def ChangeNextPage(self, index):
        # TODO 取消其他图片的显示, 节约内存占用
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if index - 1 >= 0:
                self.SetPixIem(index - 1, None)
        elif ReadMode.isDouble(self.initReadMode):
            self.SetPixIem(index + 1, None)

        self.ReloadImg()
        return

    def ChangePage(self, oldIndex, index):

        # TODO 取消其他图片的显示, 节约内存占用
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            self.SetPixIem(oldIndex, None)
            for newIndex in range(oldIndex + 1, min(oldIndex + config.PreLoading, self.maxPic)):
                self.SetPixIem(newIndex, None)
            value = self.labelSize.get(index)
            self.GetScrollBar().setValue(value)

        self.ReloadImg()
        return

    def ChangeScale(self, scale=1):
        # self.setSceneRect(-self.width()//2, -self.height()//2, self.width(), self.height())
        self.resetImg = True
        self.ReloadImg()
        self.resetImg = False
        return

    def ReloadImg(self):
        if self.initReadMode in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble2, ReadMode.RightLeftDouble,
                                 ReadMode.LeftRight]:
            self.verticalScrollBar().setValue(0)

        self.readImg.ShowImg()
        self.readImg.ShowOtherPage()
        self.readImg.CheckLoadPicture()