# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

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
