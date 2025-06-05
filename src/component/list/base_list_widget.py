from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QListWidget, QAbstractItemView, QScroller, QScrollerProperties

from component.scroll.smooth_scroll_bar import SmoothScrollBar
from config.setting import Setting
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.str import Str


class BaseListWidget(QListWidget, QtTaskBase):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        QtTaskBase.__init__(self)
        self.page = 1
        self.pages = 1
        # self.verticalScrollBar().valueChanged.connect(self.OnMove)
        self.isLoadingPage = False
        self.LoadCallBack = None
        self.OpenBack = None
        self.LikeBack = None
        self.KillBack = None
        self.parentId = -1
        self.vScrollBar = None
        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)
            propertiesOne = QScroller.scroller(self).scrollerProperties()
            # print(propertiesOne.scrollMetric(propertiesOne.MousePressEventDelay))
            propertiesOne.setScrollMetric(QScrollerProperties.MousePressEventDelay, 1)
            propertiesOne.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
            propertiesOne.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
            propertiesOne.setScrollMetric(QScrollerProperties.AcceleratingFlickMaximumTime , 0)
            QScroller.scroller(self).setScrollerProperties(propertiesOne)
            self.verticalScrollBar().valueChanged.connect(self.ValueChange)
        else:
            self.vScrollBar = SmoothScrollBar()
            self.vScrollBar.setOrientation(Qt.Vertical)
            self.setVerticalScrollBar(self.vScrollBar)
            self.vScrollBar.MoveEvent.connect(self.OnActionTriggered)

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(30)
        # self.timer = QTimer()
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.TimeOut)

        self.wheelStatus = True
        self.lastClick = 0
        self.lastIndex = -1
        self.doubleClickType = 0

    def ValueChange(self, v):
        if v >= self.verticalScrollBar().maximum():
            if Setting.IsGrabGesture.value:
                QScroller.ungrabGesture(self)

            self.ClearWheelEvent()
            self.isLoadingPage = True
            if self.LoadCallBack:
                self.LoadCallBack()

            if Setting.IsGrabGesture.value:
                QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)

    # def event(self, e) -> bool:
    #     print(e)
    #     return QListWidget.event(self, e)

    def ClearWheelEvent(self):
        pass
        # self.vScrollBar.stop()

    def SetWheelStatus(self, status):
        self.wheelStatus = status

    def wheelEvent(self, arg__1) -> None:
        if not self.wheelStatus:
            return
        if self.vScrollBar:
            self.vScrollBar.ScrollValue(-arg__1.angleDelta().y())
        else:
            # print(self.verticalScrollMode())
            # print(self.verticalScrollBar().singleStep())
            return QListWidget.wheelEvent(self, arg__1)

    def OnActionTriggered(self):
        if self.isLoadingPage:
            return
        if self.page >= self.pages:
            return
        if self.verticalScrollBar().sliderPosition() == self.verticalScrollBar().maximum():
            self.ClearWheelEvent()
            self.isLoadingPage = True
            if self.LoadCallBack:
                self.LoadCallBack()

    def UpdatePage(self, page, pages):
        self.page = page
        self.pages = pages
        self.UpdateState()

    def UpdateMaxPage(self, pages):
        self.pages = pages

    def UpdateState(self, isLoading=False):
        self.isLoadingPage = isLoading

    def GetPageStr(self):
        return Str.GetStr(Str.Page) + ": " + str(self.page) + "/" + str(self.pages)

    def clear(self) -> None:
        QListWidget.clear(self)

        # 防止异步加载时，信息错乱
        self.ClearTask()
        if self.vScrollBar:
            self.vScrollBar.ResetValue(0)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.ForwardButton:
            # QtOwner().SwitchWidgetNext()
            event.ignore()
        elif event.button() == Qt.BackButton:
            event.ignore()
            # QtOwner().SwitchWidgetLast()
        return QListWidget.mousePressEvent(self, event)