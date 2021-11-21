from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QTimer, QFile
from PySide6.QtWidgets import QGridLayout

from component.label.gif_label import GifLabel


class LoadingDialog(QtWidgets.QDialog):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        self.gridLayout = QGridLayout(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.label = GifLabel(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.timer = QTimer(self.label)
        self.timer.setInterval(100)
        f = QFile(":/png/icon/loading2.gif")
        f.open(QFile.ReadOnly)
        self.label.Init(f.readAll())
        f.close()
        self.label.resize(200, 200)
        self.cnt = 0
        self.closeCnt = 50
        self.timer.timeout.connect(self.UpdatePic)
        self.resize(200, 200)

    def show(self) -> None:
        self.timer.start()
        self.cnt = 0
        super(self.__class__, self).show()

    def close(self):
        self.timer.stop()
        super(self.__class__, self).close()

    def UpdatePic(self):
        self.cnt += 1
        if self.cnt >= self.closeCnt:
            self.close()
        pass
