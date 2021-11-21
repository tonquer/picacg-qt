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
        self.maxBt.clicked.connect(self._showRestoreWindow)
        self.closeButton.clicked.connect(self._close)
        self.minButton.clicked.connect(self._showMinimized)
        self.menuButton.clicked.connect(self._showMenu)
        # self.setAttribute(Qt.WA_TranslucentBackground)

    def _showRestoreWindow(self):
        return

    def _close(self):
        return self.window().close()

    def _showMinimized(self):
        return self.window().showMinimized()

    def _showMenu(self):
        return