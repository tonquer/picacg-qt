import time

from PySide6.QtCore import Qt, QEvent, QPoint, Signal, QRect
from PySide6.QtGui import QPainter, QFont, QPixmap, QFontMetrics
from PySide6.QtWidgets import QGraphicsView, QFrame, QGraphicsItem, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsProxyWidget, QScroller, QAbstractSlider

from component.label.msg_label import MsgLabel
from component.scroll.read_scroll import ReadScroll
from component.scroll.smooth_scroll import SmoothScroll
from config import config
from qt_owner import QtOwner
from view.read.read_enum import ReadMode
from view.read.read_pool import QtReadImgPoolManager


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
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setResizeAnchor(self.AnchorUnderMouse)
        self.setFrameStyle(QFrame.NoFrame)
        self.setObjectName("graphicsView")
        # self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        # self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.setResizeAnchor(self.AnchorViewCenter)
        self.setTransformationAnchor(self.AnchorViewCenter)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

        # self.graphicsGroup = QGraphicsItemGroup()
        # self.graphicsGroup.setFlag(QGraphicsItem.ItemIsFocusable)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.setScene(self.graphicsScene)
        # self.graphicsScene.addItem(self.graphicsGroup)
        self.graphicsItem1 = QGraphicsPixmapItem()
        self.graphicsItem2 = QGraphicsPixmapItem()
        self.graphicsItem1.setFlag(QGraphicsItem.ItemIsFocusable)
        self.graphicsItem2.setFlag(QGraphicsItem.ItemIsFocusable)

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
        self.startPos = QPoint()
        self.labelWaifu2xState = {}
        # self.setSceneRect(-self.width()//2, -self.height()//2, self.width(), self.height())

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

    # def Finished(self):
    #     QtOwner().readForm.frame.scrollArea.OnValueChange(self.value())

    def wheelEvent(self, e):
        from view.read.read_view import ReadMode
        if self.parent().qtTool.stripModel not in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if e.angleDelta().y() < 0:
                self.parent().qtTool.NextPage()
            else:
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
        if self.initReadMode in [ReadMode.UpDown, ReadMode.LeftRight]:
            QScroller.scroller(self).scrollTo(QPoint(0, self.verticalScrollBar().value() + value), 500)
        else:
            QScroller.scroller(self).scrollTo(QPoint(self.horizontalScrollBar().value() + value, 0), 500)
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
                    self.ScrollValue(self.height()/2)
                elif ev.key() == Qt.Key_Up:
                    self.ScrollValue(-self.height() / 2)
                elif ev.key() == Qt.Key_Left:
                    self.ScrollLastPage()
                elif ev.key() == Qt.Key_Right:
                    self.ScrollNextPage()
                elif ev.key() == Qt.Key_Escape:
                    self.qtTool.ReturnPage()
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
                                self.ScrollValue(-self.height()/2)
                            else:
                                self.ScrollValue(self.height()/2)
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
        nextPictureSize = self.labelSize.get(self.readImg.curIndex+1, 0)
        if self.initReadMode == ReadMode.RightLeftScroll:
            while True:
                newValue = value + self.width()
                ## 切换上一图片
                if addValue > 0 and value >= nextPictureSize:
                    if self.readImg.curIndex <= 0:
                        MsgLabel().ShowMsgEx(self.readImg, self.tr("已经到第一页"))
                        return
                    self.readImg.curIndex -= 1
                    # print(self.readImg.curIndex)
                    self.changeLastPage.emit(self.readImg.curIndex)

                ## 切换下一图片
                elif addValue < 0 and newValue < curPictureSize:
                    if self.readImg.curIndex >= self.readImg.maxPic - 1:
                        MsgLabel().ShowMsgEx(self.readImg, self.tr("已经到最后一页"))
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
                        MsgLabel().ShowMsgEx(self.readImg, self.tr("已经到第一页"))
                        return
                    self.readImg.curIndex -= 1
                    self.changeLastPage.emit(self.readImg.curIndex)

                ## 切换下一图片
                elif addValue > 0 and value >= nextPictureSize:
                    if self.readImg.curIndex >= self.readImg.maxPic - 1:
                        MsgLabel().ShowMsgEx(self.readImg, self.tr("已经到最后一页"))
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
            print(value)
            print(self.labelSize)
        elif self.initReadMode in [ReadMode.LeftRight]:

            self.graphicsItem1.setPos(0, 0)
            self.graphicsScene.addItem(self.graphicsItem1)
            self.horizontalScrollBar().setMaximum(self.width())
        elif self.initReadMode in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            self.graphicsItem1.setPos(0, 0)
            self.graphicsItem2.setPos(self.width()//2, 0)
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
            self.graphicsScene.setSceneRect(0, 0, self.labelSize.get(0), self.height())
            self.GetScrollBar().setMaximum(self.labelSize.get(0))
            self.GetOtherScrollBar().setMaximum(0)
        elif self.initReadMode in [ReadMode.LeftRightScroll]:
            self.graphicsScene.setSceneRect(0, 0, self.labelSize.get(maxNum - 1), self.height())
            self.GetScrollBar().setMaximum(self.labelSize.get(maxNum - 1, 0))
            self.GetOtherScrollBar().setMaximum(0)
        elif self.initReadMode in [ReadMode.UpDown]:
            self.graphicsScene.setSceneRect(0, 0, self.width(), self.labelSize.get(maxNum - 1))
            self.GetScrollBar().setMaximum(self.labelSize.get(maxNum - 1, 0))
            self.GetOtherScrollBar().setMaximum(0)
        else:
            self.graphicsScene.setSceneRect(0, 0, self.width(), max(self.height(), self.graphicsItem1.pixmap().height()))
            self.verticalScrollBar().setMaximum(max(0, self.graphicsItem1.pixmap().height()- self.height()))
            self.horizontalScrollBar().setMaximum(0)

    def ResetLabelSize(self, size):
        # 重新计算每个图片的位置
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            height = 0
            if self.initReadMode != ReadMode.RightLeftScroll:
                labelIndex = list(range(0, size))
            else:
                labelIndex = list(range(size - 1, -1, -1))
            for i in labelIndex:
                proxy = self.allItems[i]
                self.labelSize[i] = height
                if self.initReadMode == ReadMode.UpDown:
                    if isinstance(proxy, QGraphicsProxyWidget):
                        height += proxy.widget().height()
                    else:
                        height += proxy.pixmap().height()
                else:
                    if isinstance(proxy, QGraphicsProxyWidget):
                        height += proxy.widget().width()
                    else:
                        height += proxy.pixmap().width()

        self.ResetMaxNum()

    def GetLabel(self, index):
        if self.qtTool.stripModel == ReadMode.LeftRight:
            return self.graphicsItem1
        elif self.qtTool.stripModel == ReadMode.RightLeftDouble:
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
            text = str(index+1)
        font = QFont()
        font.setPointSize(64)
        fm = QFontMetrics(font)
        p = QPixmap(self.width(), self.height())
        rect = QRect(self.width()//2, self.height()//2 - fm.height()//2, self.width()//2, self.height()//2+fm.height()//2)
        p.fill(Qt.transparent)
        painter = QPainter(p)
        painter.setFont(font)
        if config.ThemeText == "flatblack":
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
                text = str(index+1)
                font = QFont()
                font.setPointSize(64)
                label.setAlignment(Qt.AlignCenter)
                label.setFont(font)
                label.setText(text)
                label.resize(proxy.pixmap().width(), proxy.pixmap().height())
                newProxy.widget().setMinimumSize(proxy.pixmap().width(), proxy.pixmap().height())
                newProxy.widget().setMaximumSize(proxy.pixmap().width(), proxy.pixmap().height())
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
                return proxy.pixmap().height(), proxy.pixmap().width()
        elif (self.initReadMode == ReadMode.RightLeftDouble and index == self.readImg.curIndex) or (self.initReadMode == ReadMode.LeftRightDouble and index != self.readImg.curIndex):
            self.graphicsItem2.pixmap().height(), self.graphicsItem2.pixmap().width()
        return self.graphicsItem1.pixmap().height(), self.graphicsItem1.pixmap().width()

    def SetPixIem(self, index, data, isWaifu2x=False):
        if not self.allItems and self.readImg.stripModel in [ReadMode.UpDown, ReadMode.LeftRightScroll, ReadMode.RightLeftScroll]:
            return
        if not data:
            self.labelWaifu2xState[index] = isWaifu2x
            if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
                self.PixmapToLabel(index)
                return
            else:
                data = self.MakePixItem(index)

        oldHeight, oldWidth = self.LabelToPixmap(index)
        label = self.GetLabel(index)
        if self.readImg.stripModel in [ReadMode.UpDown, ReadMode.LeftRightScroll, ReadMode.RightLeftScroll]:
            # TODO，优化
            waifu2x = self.labelWaifu2xState.get(index, False)
            if label.pixmap() and waifu2x == isWaifu2x and not self.resetImg:
                return
        self.labelWaifu2xState[index] = isWaifu2x
        oldPos = label.pos()

        if self.qtTool.stripModel == ReadMode.LeftRight:
            scale = (1 + self.scaleCnt * 0.1)
            wight = min(self.width(), int(self.width() * scale))
            height = self.height() * scale
            newData = data.scaled(wight, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPos(self.width()//2 - newData.width()//2, max(0, self.height()//2-newData.height()//2))
        elif self.qtTool.stripModel in [ReadMode.RightLeftDouble]:
            scale = (1 + self.scaleCnt * 0.1)
            newData = data.scaled(min(self.width()//2, int(self.width()//2*scale)), self.height()*scale,
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if index == self.readImg.curIndex:
                label.setPos(self.width()//2, self.height()//2 - newData.height()//2)
            else:
                label.setPos(self.width()//2-newData.width(), self.height()//2 - newData.height()//2)
        elif self.qtTool.stripModel in [ReadMode.LeftRightDouble]:
            scale = (1 + self.scaleCnt * 0.1)
            newData = data.scaled(min(self.width()//2, int(self.width()//2*scale)), self.height()*scale,
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if index != self.readImg.curIndex:
                label.setPos(self.width()//2, self.height()//2 - newData.height()//2)
            else:
                label.setPos(self.width()//2-newData.width(), self.height()//2 - newData.height()//2)
        elif self.qtTool.stripModel in [ReadMode.LeftRightScroll]:
            scale = (1 + self.scaleCnt * 0.1)
            newData = data.scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPos(oldPos.x(), max(0, self.height() // 2 - newData.height() // 2))

        elif self.qtTool.stripModel in [ReadMode.RightLeftScroll]:
            scale = (1 + self.scaleCnt * 0.1)
            newData = data.scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPos(oldPos.x(), max(0, self.height() // 2 - newData.height() // 2))

        elif self.qtTool.stripModel in [ReadMode.UpDown]:
            scale = (0.5 + self.scaleCnt * 0.1)
            minWidth = min(self.width(), self.width() * scale)
            minHeight = self.height() * scale * 10
            newData = data.scaled(minWidth, minHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPos(self.width()//2 - newData.width()//2, oldPos.y())

        label.setPixmap(newData)

        if self.initReadMode == ReadMode.UpDown:
            self.UpdateOtherHeight(index, oldHeight, label.pixmap().height())
        else:
            self.UpdateOtherHeight(index, oldWidth, label.pixmap().width())

    def UpdateOtherHeight(self, index, oldHeight, height):
        # 修改了图片导致label长宽变化，重新计算
        addHeight = height - oldHeight
        if addHeight == 0:
            return

        oldValue = self.GetScrollBar().value()

        if self.initReadMode == ReadMode.RightLeftScroll:
            indexList = list(range(index-1, -1, -1))
            # TODO 需要重新定位
            curPixcurSize = self.labelSize.get(index)
            if curPixcurSize <= oldValue:
                self.GetScrollBar().setValue(oldValue + addHeight)
                self.oldValue = self.GetScrollBar().value()

        elif self.initReadMode in [ReadMode.LeftRightScroll, ReadMode.UpDown]:
            indexList = list(range(index+1, self.readImg.maxPic))

            curPixcurSize = self.labelSize.get(index)
            # TODO 需要重新定位
            if curPixcurSize <= oldValue:
                self.GetScrollBar().setValue(oldValue + addHeight)
                self.oldValue = self.GetScrollBar().value()

        else:
            self.ResetMaxNum()
            return

        for i in indexList:
            proxy = self.allItems[i]
            oldPos = proxy.pos()
            if self.initReadMode == ReadMode.UpDown:
                if isinstance(proxy, QGraphicsPixmapItem):
                    proxy.setPos(max(0, self.width()//2 - proxy.pixmap().width()//2), oldPos.y() + addHeight)
                else:
                    proxy.setPos(oldPos.x(), oldPos.y() + addHeight)
            else:
                if isinstance(proxy, QGraphicsPixmapItem):
                    proxy.setPos(oldPos.x() + addHeight, max(0, self.height()//2 - proxy.pixmap().height()//2))
                else:
                    proxy.setPos(oldPos.x() + addHeight, oldPos.y())
            self.labelSize[i] += addHeight

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
                self.SetPixIem(index+config.PreLoading, None)
        elif self.initReadMode in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            self.SetPixIem(index - 1, None)
        self.ReloadImg()
        return

    def ChangeNextPage(self, index):
        # TODO 取消其他图片的显示, 节约内存占用
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if index - 1 >= 0:
                self.SetPixIem(index-1, None)
        elif self.initReadMode in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            self.SetPixIem(index + 1, None)

        self.ReloadImg()
        return

    def ChangePage(self, oldIndex, index):

        # TODO 取消其他图片的显示, 节约内存占用
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            self.SetPixIem(oldIndex, None)
            for newIndex in range(oldIndex+1, min(oldIndex+config.PreLoading, self.maxPic)):
                self.SetPixIem(newIndex, None)
            value = self.labelSize.get(index)
            self.GetScrollBar().setValue(value)

        self.ReloadImg()
        return

    def ChangeScale(self, scale):
        # self.setSceneRect(-self.width()//2, -self.height()//2, self.width(), self.height())
        self.resetImg = True
        self.ReloadImg()
        self.resetImg = False
        return

    def ReloadImg(self):
        self.readImg.ShowImg()
        self.readImg.ShowOtherPage()
        self.readImg.CheckLoadPicture()