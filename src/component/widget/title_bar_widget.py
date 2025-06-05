# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from component.widget.com_widget import ComWidget, MoveEnum
from interface.ui_title_bar import Ui_TitleBar


class TitleBarWidget(QWidget, Ui_TitleBar):
    """ 定义标题栏 """

    def __init__(self, parent):
        super().__init__(parent)
        Ui_TitleBar.__init__(self)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.resize(1360, 40)
        self.maxBt.clicked.connect(self._ShowRestoreWindow)
        self.closeButton.clicked.connect(self._Close)
        self.minButton.clicked.connect(self._ShowMinimized)
        # self.setMouseTracking(True)

    def _ShowRestoreWindow(self):
        self.__showRestoreWindow()
        return

    def mouseDoubleClickEvent(self, event):
        self._ShowRestoreWindow()

    def __showRestoreWindow(self):
        if self.window().isMaximized():
            self.maxBt.setProperty("isMax", False)
            self.maxBt.style().unpolish(self.maxBt)
            self.maxBt.style().polish(self.maxBt)
            self.window().showNormal()
        else:
            self.maxBt.setProperty("isMax", True)
            self.maxBt.style().unpolish(self.maxBt)
            self.maxBt.style().polish(self.maxBt)
            self.window().showMaximized()

    def _Close(self):
        return self.window().close()

    def _ShowMinimized(self):
        return self.window().showMinimized()

    def mousePressEvent(self, event):
        """ 移动窗口 """
        # 判断鼠标点击位置是否允许拖动
        area = ComWidget.moveArea(self.width(), self.height(), event.pos())
        if area in [MoveEnum.LEFT_TOP.value, MoveEnum.LEFT.value]:
            event.ignore()
            return
        from win32.win32gui import ReleaseCapture
        from win32.win32api import SendMessage
        from win32.lib import win32con
        if self.__isPointInDragRegion(event.pos()):
            ReleaseCapture()
            SendMessage(
                self.window().winId(),
                win32con.WM_SYSCOMMAND,
                win32con.SC_MOVE + win32con.HTCAPTION,
                0,
            )
            event.ignore()

    def __isPointInDragRegion(self, pos) -> bool:
        """ 检查鼠标按下的点是否属于允许拖动的区域 """
        x = pos.x()
        left = 0
        # 如果最小化按钮看不见也意味着最大化按钮看不见
        right = self.width() - 57
        return left < x < right