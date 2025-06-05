from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

from config import config
from qt_owner import QtOwner
from tools.str import Str


class MySystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0
        self.setIcon(QIcon(":/png/icon/logo_round.png"))
        self.setToolTip(config.ProjectName)
        self.menu = QMenu()
        mainUi = QAction(Str.GetStr(Str.MainUi), self)
        mainUi.triggered.connect(self.ShowMainUi)

        showMin = QAction(Str.GetStr(Str.ShowMin), self)
        showMin.triggered.connect(self.ShowMin)

        quit = QAction(Str.GetStr(Str.Exit), self)
        quit.triggered.connect(self.Close)

        self.menu.addAction(mainUi)
        self.menu.addAction(showMin)
        self.menu.addAction(quit)
        self.setContextMenu(self.menu)
        self.activated.connect(self.OnActive)

    def ShowMainUi(self):
        QtOwner().owner.show()
        pass

    def ShowMin(self):
        QtOwner().owner.hide()
        pass

    def Close(self):
        QtOwner().closeType = 3
        QtOwner().owner.close()

    def OnActive(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            return
        elif reason == QSystemTrayIcon.DoubleClick:
            self.ShowMainUi()
            return
        pass