from collections import deque
from enum import Enum
from math import cos, pi

from PySide2.QtCore import QTimer, QDateTime, Qt, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PySide2.QtGui import QWheelEvent
from PySide2.QtWidgets import QApplication, QGraphicsView, QScrollBar


class SmoothMode(Enum):
    """ 滚动模式 """
    NO_SMOOTH = 0
    CONSTANT = 1
    LINEAR = 2
    QUADRATI = 3
    COSINE = 4


class SmoothScroll(QScrollBar):
    def __init__(self):
        QScrollBar.__init__(self)
        self.animation = QPropertyAnimation()
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b"value")
        self.scrollTime = 500
        self.animation.setDuration(self.scrollTime)
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animationValue = self.value()
        self.backTick = 0
        self.laveValue = 0
        self.lastV = 0

    # def setValue(self, value):
    #     self.animation.stop()
    #     oldValue = self.value()
    #     self.animation.setStartValue(oldValue)
    #     self.animation.setEndValue(value)
    #     self.animation.start()
    #     return

    def UpdateCurrentValue(self, value):
        print(value)

    def StopScroll(self):
        self.backTick = 0
        self.animation.stop()

    def ResetScroll(self):
        if self.animation.state() == QAbstractAnimation.State.Running:
            startValue = self.animation.startValue()
            endValue = self.animation.endValue()
            time = self.animation.currentTime()
            value = self.animation.currentValue()
            laveTime = self.animation.duration() - time
            if laveTime > 0:
                self.backTick = laveTime
                self.laveValue = endValue - value
            else:
                self.backTick = 0
        else:
            self.backTick = 0

        self.animation.stop()
        return

    def RestartScroll(self):
        if self.backTick == 0 or self.laveValue == 0:
            return
        print(self.backTick, self.laveValue)
        self.animation.stop()
        oldValue = self.value()
        # print(self.animation.duration())
        self.animation.setStartValue(oldValue)
        self.animation.setEndValue(oldValue + self.laveValue)
        self.animation.setDuration(self.backTick)
        self.animation.start()

    def Scroll(self, value):
        if value * self.lastV < 0:
            if self.animation.state() == QAbstractAnimation.State.Running:
                self.lastV = value
                self.animation.stop()
                return

        self.lastV = value
        self.animation.stop()
        oldValue = self.value()
        # print(self.animation.duration())
        self.animation.setStartValue(oldValue)
        self.animation.setDuration(self.scrollTime)
        self.animation.setEndValue(oldValue - value)
        self.animation.start()

class QtComGraphicsView(QGraphicsView):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.fps = 60
        self.duration = 400
        self.stepsTotal = 0
        self.stepRatio = 1.5
        self.acceleration = 1
        self.lastWheelEvent = None
        self.scrollStamps = deque()
        self.stepsLeftQueue = deque()
        self.smoothMoveTimer = QTimer(self)
        self.smoothMode = SmoothMode(SmoothMode.COSINE)
        self.smoothMoveTimer.timeout.connect(self.__smoothMove)
        self.qEventParam = []

        self.vScrollBar = SmoothScroll()
        self.vScrollBar.setOrientation(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(self.vScrollBar)

        self.hScrollBar = SmoothScroll()
        self.hScrollBar.setOrientation(Qt.Orientation.Horizontal)
        self.setHorizontalScrollBar(self.hScrollBar)
        self.scrollSize = 500
        self.scrollTime = 500


    def wheelEvent(self, e) -> None:
        from src.qt.read.qtreadimg import ReadMode
        if self.parent().qtTool.stripModel not in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            if e.angleDelta().y() < 0:
                self.parent().qtTool.NextPage()
            else:
                self.parent().qtTool.LastPage()
            return

        if self.smoothMode == SmoothMode.NO_SMOOTH:
            super().wheelEvent(e)
            return
        if self.parent().qtTool.stripModel == ReadMode.UpDown:
            scrollBar = self.vScrollBar
        else:
            scrollBar = self.hScrollBar

        if e.angleDelta().y() > 0:
            scrollBar.Scroll(self.scrollSize)
        else:
            scrollBar.Scroll(-self.scrollSize)
        # return super().wheelEvent(e)

    def SetScrollValue(self, size, time):
        if size == self.scrollSize and time == self.scrollTime:
            return
        self.StopScroll()
        self.scrollSize = size
        self.scrollTime = time
        self.vScrollBar.scrollTime = time
        self.hScrollBar.scrollTime = time
        self.vScrollBar.animation.setDuration(self.scrollTime)
        self.hScrollBar.animation.setDuration(self.scrollTime)

    def StopScroll(self):
        self.hScrollBar.StopScroll()
        self.vScrollBar.StopScroll()

    def Scroll(self, value):
        from src.qt.read.qtreadimg import ReadMode
        if self.parent().qtTool.stripModel == ReadMode.UpDown:
            self.vScrollBar.Scroll(value)
        else:
            self.hScrollBar.Scroll(value)

    # def wheelEvent(self, e):
    #     from src.qt.read.qtreadimg import ReadMode
    #     if self.parent().qtTool.stripModel not in [ReadMode.UpDown, ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
    #         if e.angleDelta().y() < 0:
    #             self.parent().qtTool.NextPage()
    #         else:
    #             self.parent().qtTool.LastPage()
    #         return
    #
    #     if self.smoothMode == SmoothMode.NO_SMOOTH:
    #         super().wheelEvent(e)
    #         return
    #
    #     # 将当前时间点插入队尾
    #     now = QDateTime.currentDateTime().toMSecsSinceEpoch()
    #     self.scrollStamps.append(now)
    #     while now - self.scrollStamps[0] > 500:
    #         self.scrollStamps.popleft()
    #     # 根据未处理完的事件调整移动速率增益
    #     accerationRatio = min(len(self.scrollStamps) / 15, 1)
    #     self.qEventParam = (e.pos(), e.globalPos(), e.buttons())
    #     # 计算步数
    #     self.stepsTotal = self.fps * self.duration / 1000
    #     # 计算每一个事件对应的移动距离
    #     delta = e.angleDelta().y() * self.stepRatio
    #     if self.acceleration > 0:
    #         delta += delta * self.acceleration * accerationRatio
    #     # 将移动距离和步数组成列表，插入队列等待处理
    #     self.stepsLeftQueue.append([delta, self.stepsTotal])
    #     # 定时器的溢出时间t=1000ms/帧数
    #     self.smoothMoveTimer.start(1000 // self.fps)
    #     # print(e)

    def __smoothMove(self):
        """ 计时器溢出时进行平滑滚动 """
        totalDelta = 0
        # 计算所有未处理完事件的滚动距离，定时器每溢出一次就将步数-1
        for i in self.stepsLeftQueue:
            totalDelta += self.__subDelta(i[0], i[1])
            i[1] -= 1
        # 如果事件已处理完，就将其移出队列
        while self.stepsLeftQueue and self.stepsLeftQueue[0][1] == 0:
            self.stepsLeftQueue.popleft()
        # 构造滚轮事件
        e = QWheelEvent(self.qEventParam[0],
                        self.qEventParam[1],
                        round(totalDelta),
                        self.qEventParam[2],
                        Qt.NoModifier)
        # print(e)
        # 将构造出来的滚轮事件发送给app处理
        from src.qt.read.qtreadimg import ReadMode
        if self.parent().qtTool.stripModel in [ReadMode.UpDown]:
            QApplication.sendEvent(self.verticalScrollBar(), e)
        else:
            QApplication.sendEvent(self.horizontalScrollBar(), e)
        # 如果队列已空，停止滚动
        if not self.stepsLeftQueue:
            self.smoothMoveTimer.stop()

    def __subDelta(self, delta, stepsLeft):
        """ 计算每一步的插值 """
        m = self.stepsTotal / 2
        x = abs(self.stepsTotal - stepsLeft - m)
        # 根据滚动模式计算插值
        res = 0
        if self.smoothMode == SmoothMode.NO_SMOOTH:
            res = 0
        elif self.smoothMode == SmoothMode.CONSTANT:
            res = delta / self.stepsTotal
        elif self.smoothMode == SmoothMode.LINEAR:
            res = 2 * delta / self.stepsTotal * (m - x) / m
        elif self.smoothMode == SmoothMode.QUADRATI:
            res = 3 / 4 / m * (1 - x * x / m / m) * delta
        elif self.smoothMode == SmoothMode.COSINE:
            res = (cos(x * pi / m) + 1) / (2 * m) * delta
        return res