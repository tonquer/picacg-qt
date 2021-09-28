from PySide2.QtCore import Qt, QPoint, QEvent, Signal
from PySide2.QtGui import QFont, QKeyEvent
from PySide2.QtWidgets import QWidget, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout, QScroller, QScrollerProperties, \
    QScrollArea, QLabel, QAbstractSlider

from src.qt.com.qt_scroll import QtScroll
from src.util import Log


class ReadScrollArea(QScrollArea, QtScroll):
    changeLastPage = Signal(int)
    changeNextPage = Signal(int)
    changePage = Signal(int, int)
    changeScale = Signal(int)

    def __init__(self, parent=None):
        QScrollArea.__init__(self, parent)
        QtScroll.__init__(self)
        self.changeLastPage.connect(self.ChangeLastPage)
        self.changeNextPage.connect(self.ChangeNextPage)
        self.changePage.connect(self.ChangePage)
        self.changeScale.connect(self.ChangeScale)
        # self.resize(400, 450)
        self.scrollWidget = QWidget()
        self.setFrameShape(QFrame.NoFrame)
        # self.label = QLabel("asdasdasd", self.scrollWidget)
        # self.scrollWidget.resize(self.width(), 400)
        self.gridLayout = QVBoxLayout(self.scrollWidget)
        self.vBoxLayout = QVBoxLayout()
        self.hBoxLayout = QHBoxLayout()
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setMargin(0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setMargin(0)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addLayout(self.vBoxLayout)
        self.gridLayout.addLayout(self.hBoxLayout)
        self.initReadMode = None
        self.setWidget(self.scrollWidget)
        self.setStyleSheet("QLabel {background-color: transparent;}")
        self.labels = []
        self.isMove = False
        self.isPress = False
        self.lastPos = None
        self.backScale = 0
        self.setWidgetResizable(True)
        self.installEventFilter(self)
        QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)
        properties = QScroller.scroller(self).scrollerProperties()
        # properties.setScrollMetric(QScrollerProperties.FrameRate, QScrollerProperties.Fps60)
        properties.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor, 0.3)
        properties.setScrollMetric(QScrollerProperties.OvershootDragDistanceFactor, 0.5)
        properties.setScrollMetric(QScrollerProperties.OvershootScrollTime, 0.2)
        properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 1)
        properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 2)
        properties.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.3)
        QScroller.scroller(self).setScrollerProperties(properties)
        self.allQLabel = []
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.adjustSize()

        self.label1 = QLabel()
        self.label2 = QLabel()
        self.labelSize = {}  # index: value
        self.oldValue = 0
        self.resetImg = False
        QScroller.scroller(self).stateChanged.connect(self.StateChanged)

        self.verticalScrollBar().actionTriggered.connect(self.OnActionTriggered)

        self.horizontalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        self.startPos = QPoint()
        self.labelWaifu2xState = {}

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

    # 滑动切换上一页
    def ScrollNextPage(self):
        self.qtTool.NextPage()
        return

    # 滑动切换下一页
    def ScrollLastPage(self):
        self.qtTool.LastPage()
        return

    def ScrollValue(self, value):
        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode in [ReadMode.UpDown, ReadMode.LeftRight]:
            QScroller.scroller(self).scrollTo(QPoint(0, self.verticalScrollBar().value() + value), 500)
        else:
            QScroller.scroller(self).scrollTo(QPoint(self.horizontalScrollBar().value() + value, 0), 500)
        return

    def eventFilter(self, obj, ev) -> bool:
        # print(obj, ev.type())
        if obj == self:
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
        if obj == self.scrollWidget:
            if ev.type() == QEvent.KeyRelease:
                return True
            elif ev.type() == QEvent.KeyPress:
                return True
            elif ev.type() == QEvent.MouseButtonPress:
                if ev.button() == Qt.MouseButton.LeftButton:
                    self.startPos = ev.screenPos()
            elif ev.type() == QEvent.MouseButtonRelease:
                if not self.frame.helpLabel.isHidden():
                    self.frame.helpLabel.hide()
                    return True
                if ev.button() == Qt.MouseButton.LeftButton:
                    if not self.frame.helpLabel.isHidden():
                        self.frame.helpLabel.hide()
                        return True
                    endPos = ev.screenPos()
                    subPos = (endPos - self.startPos)
                    if abs(subPos.x()) <= 20:
                        curPos = endPos - self.readImg.pos()
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
        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode == ReadMode.UpDown:
            return self.verticalScrollBar()
        else:
            return self.horizontalScrollBar()

    def wheelEvent(self, e):
        return QtScroll.wheelEvent(self, e)

    def OnActionTriggered(self, action):
        if action != QAbstractSlider.SliderMove:
            return
        self.OnValueChange(self.GetScrollBar().value())

    def OnValueChange(self, value):
        from src.qt.read.qtreadimg import ReadMode
        addValue = value - self.oldValue
        # self.UpdateScrollBar(value)
        self.oldValue = value

        if self.initReadMode not in [ReadMode.LeftRightScroll, ReadMode.RightLeftScroll, ReadMode.UpDown]:
            return

        curPictureSize = self.labelSize.get(self.readImg.curIndex)
        nextPictureSize = self.labelSize.get(self.readImg.curIndex+1, 0)
        if self.initReadMode == ReadMode.RightLeftScroll:
            while True:
                label = self.allQLabel[self.readImg.curIndex]
                newValue = value + self.width()
                ## 切换上一图片
                if addValue > 0 and value >= nextPictureSize:
                    if self.readImg.curIndex <= 0:
                        return
                    self.readImg.curIndex -= 1
                    print(self.readImg.curIndex)
                    self.changeLastPage.emit(self.readImg.curIndex)

                ## 切换下一图片
                elif addValue < 0 and newValue < curPictureSize:
                    if self.readImg.curIndex >= self.readImg.maxPic - 1:
                        return
                    self.readImg.curIndex += 1
                    print(self.readImg.curIndex)
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
                        return
                    self.readImg.curIndex -= 1
                    self.changeLastPage.emit(self.readImg.curIndex)

                ## 切换下一图片
                elif addValue > 0 and value >= nextPictureSize:
                    if self.readImg.curIndex >= self.readImg.maxPic - 1:
                        return
                    self.readImg.curIndex += 1
                    self.changeNextPage.emit(self.readImg.curIndex)
                else:
                    break

                curPictureSize = self.labelSize.get(self.readImg.curIndex)
                nextPictureSize = self.labelSize.get(self.readImg.curIndex + 1, 0)
        return

    @property
    def scaleCnt(self):
        return self.readImg.frame.scaleCnt

    def SetLabel(self, label, i):
        text = str(i + 1)
        font = QFont()
        font.setPointSize(64)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)
        label.setText(text)

    def InitAllQLabel(self, maxNum, curIndex):
        if not maxNum:
            return
        self.verticalScrollBar().setValue(0)
        self.horizontalScrollBar().setValue(0)
        self.oldValue = 0
        if self.initReadMode and self.readImg.stripModel != self.initReadMode:
            for label in self.allQLabel:
                label.setParent(None)
                self.vBoxLayout.removeWidget(label)
                self.hBoxLayout.removeWidget(label)

            for label in [self.label1, self.label2]:
                label.setParent(None)
                self.vBoxLayout.removeWidget(label)
                self.hBoxLayout.removeWidget(label)

        self.initReadMode = self.readImg.stripModel
        for label in self.allQLabel[maxNum:]:
            label.setVisible(False)

        for i, label in enumerate(self.allQLabel):
            label.setPixmap(None)
            self.SetLabel(label, i)

        for label in [self.label1, self.label2]:
            label.setPixmap(None)
            self.SetLabel(label, 1)

        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if self.initReadMode == ReadMode.UpDown:
                layout = self.vBoxLayout
            else:
                layout = self.hBoxLayout

            allLabelSize = len(self.allQLabel)

            height = 0

            for i in range(0, maxNum):
                if i < allLabelSize:
                    label = self.allQLabel[i]
                else:
                    label = QLabel()
                    self.SetLabel(label, i)
                    self.allQLabel.append(label)

                if not label.parent():
                    if self.initReadMode == ReadMode.RightLeftScroll:
                        layout.insertWidget(0, label, alignment=Qt.AlignCenter)
                    else:
                        layout.addWidget(label, alignment=Qt.AlignCenter)

                label.setVisible(True)
                # label.resize(self.width(), self.height())
                label.setMinimumSize(self.width(), self.height())

            self.ResetLabelSize(maxNum)

            value = self.labelSize.get(curIndex)
            if self.initReadMode == ReadMode.RightLeftScroll:
                self.GetScrollBar().setMaximum(self.labelSize.get(0))
            elif self.initReadMode in [ReadMode.LeftRightScroll, ReadMode.UpDown]:
                self.GetScrollBar().setMaximum(self.labelSize.get(maxNum-1))
            self.oldValue = value
            self.GetScrollBar().setValue(value)
        elif self.initReadMode in [ReadMode.LeftRight]:

            self.label1.setMinimumSize(self.width(), self.height())
            if not self.label1.parent():
                self.hBoxLayout.addWidget(self.label1, alignment=Qt.AlignCenter)
        elif self.initReadMode in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            self.label1.setMinimumSize(self.width()//2, self.height())
            if not self.label1.parent():
                self.hBoxLayout.addWidget(self.label1, alignment=Qt.AlignRight)
            self.label2.setMinimumSize(self.width()//2, self.height())
            if not self.label2.parent():
                self.hBoxLayout.addWidget(self.label2, alignment=Qt.AlignLeft)
        return

    def ResetLabelSize(self, size):
        # 重新计算每个图片的位置
        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            height = 0
            if self.initReadMode != ReadMode.RightLeftScroll:
                labelIndex = list(range(0, size))
            else:
                labelIndex = list(range(size - 1, -1, -1))
            for i in labelIndex:
                label = self.allQLabel[i]
                if not label.parent():
                    continue
                self.labelSize[i] = height
                if self.initReadMode == ReadMode.UpDown:
                    height += label.height()
                else:
                    height += label.width()

    def GetLabel(self, index):
        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel == ReadMode.LeftRight:
            return self.label1
        elif self.qtTool.stripModel == ReadMode.RightLeftDouble:
            if index == self.readImg.curIndex:
                return self.label2
            else:
                return self.label1
        elif self.qtTool.stripModel == ReadMode.LeftRightDouble:
            if index == self.readImg.curIndex:
                return self.label1
            else:
                return self.label2
        elif self.qtTool.stripModel in [ReadMode.LeftRightScroll, ReadMode.UpDown, ReadMode.RightLeftScroll]:
            return self.allQLabel[index]

    def SetPixIem(self, index, data, isWaifu2x=False):
        from src.qt.read.qtreadimg import ReadMode
        if not self.allQLabel and self.readImg.stripModel in [ReadMode.UpDown, ReadMode.LeftRightScroll, ReadMode.RightLeftScroll]:
            return
        label = self.GetLabel(index)
        if not data:
            label.setPixmap(None)
            text = str(index+1)
            font = QFont()
            font.setPointSize(64)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(font)
            self.labelWaifu2xState[index] = isWaifu2x
            if index >= self.readImg.maxPic or index < 0:
                label.setText("")
            else:
                label.setText(text)
            return
        if self.readImg.stripModel in [ReadMode.UpDown, ReadMode.LeftRightScroll, ReadMode.RightLeftScroll]:
            # TODO，优化
            waifu2x = self.labelWaifu2xState.get(index, False)
            if label.pixmap() and waifu2x != isWaifu2x and not self.resetImg:
                return
        self.labelWaifu2xState[index] = isWaifu2x
        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel == ReadMode.LeftRight:
            scale = (1 + self.scaleCnt * 0.1)
            wight = min(self.width(), int(self.width() * scale))
            height = self.height() * scale
            newData = data.scaled(wight, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        elif self.qtTool.stripModel in [ReadMode.RightLeftDouble, ReadMode.LeftRightDouble]:
            scale = (1 + self.scaleCnt * 0.1)
            newData = data.scaled(min(self.width()//2, int(self.width()//2*scale)), self.height()*scale,
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif self.qtTool.stripModel in [ReadMode.LeftRightScroll]:
            scale = (1 + self.scaleCnt * 0.1)
            newData = data.scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif self.qtTool.stripModel in [ReadMode.RightLeftScroll]:
            scale = (1 + self.scaleCnt * 0.1)
            newData = data.scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif self.qtTool.stripModel in [ReadMode.UpDown]:
            scale = (0.5 + self.scaleCnt * 0.1)
            minWidth = min(self.width(), self.width() * scale)
            minHeight = self.height() * scale * 10
            newData = data.scaled(minWidth, minHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        oldHeight = label.height()
        oldWidth = label.width()
        if newData:
            label.resize(newData.width(), newData.height())
            label.setMinimumSize(newData.width(), newData.height())
            label.setMaximumSize(newData.width(), newData.height())
        label.setPixmap(newData)
        if self.initReadMode == ReadMode.UpDown:
            self.UpdateOtherHeight(index, oldHeight, label.height())
        else:
            self.UpdateOtherHeight(index, oldWidth, label.width())

    def UpdateOtherHeight(self, index, oldHeight, height):
        # 修改了图片导致label长宽变化，重新计算
        addHeight = height - oldHeight
        if addHeight == 0:
            return
        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode == ReadMode.RightLeftScroll:
            indexList = list(range(index-1, -1, -1))
            # TODO 需要重新定位
            self.GetScrollBar().setValue(self.GetScrollBar().value() + addHeight)
            self.oldValue = self.GetScrollBar().value()

        elif self.initReadMode in [ReadMode.LeftRightScroll, ReadMode.UpDown]:
            indexList = list(range(index+1, self.readImg.maxPic))
        else:
            return
        for i in indexList:
            self.labelSize[i] += addHeight
        return

    def ResetScrollValue(self, index):
        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            value = self.labelSize.get(index)
            self.GetScrollBar().setValue(value)

    def ChangeLastPage(self, index):
        # TODO 取消其他图片的显示, 节约内存占用
        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if index + 1 + 2 >= self.maxPic:
                return
            self.SetPixIem(index+1+2, None)
        elif self.initReadMode in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            self.SetPixIem(index - 1, None)
        self.ReloadImg()
        return

    def ChangeNextPage(self, index):
        # TODO 取消其他图片的显示, 节约内存占用
        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if index - 1 < 0:
                return
            self.SetPixIem(index-1, None)
        elif self.initReadMode in [ReadMode.LeftRightDouble, ReadMode.RightLeftDouble]:
            self.SetPixIem(index + 1, None)

        self.ReloadImg()
        return

    def ChangePage(self, oldIndex, index):

        # TODO 取消其他图片的显示, 节约内存占用
        from src.qt.read.qtreadimg import ReadMode
        if self.initReadMode in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            self.SetPixIem(oldIndex, None)
            if oldIndex + 1 < self.maxPic:
                self.SetPixIem(oldIndex + 1, None)
            if oldIndex + 2 < self.maxPic:
                self.SetPixIem(oldIndex + 2, None)
            value = self.labelSize.get(index)
            self.GetScrollBar().setValue(value)

        self.ReloadImg()
        return

    def ChangeScale(self, scale):
        self.resetImg = True
        self.ReloadImg()
        self.resetImg = False
        return

    def ReloadImg(self):
        self.readImg.ShowImg()
        self.readImg.ShowOtherPage()
        self.readImg.CheckLoadPicture()