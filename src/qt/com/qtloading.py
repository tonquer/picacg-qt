import weakref

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QPoint, QTimer
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QDesktopWidget

from resources import resources
from ui.loading import Ui_Loading


class QtLoading(QtWidgets.QDialog, Ui_Loading):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_Loading.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        # frmX = self.width()
        # frmY = self.height()
        # w = QDesktopWidget()
        # w.width()
        # movePoint = QPoint(int(w.width()/2-frmX/2), int(w.height()/2 - frmY/2))
        # self.move(movePoint)
        self.index = 1
        self.qMapList = []
        for i in range(1, 11):
            data = resources.DataMgr.GetData("loading_{}".format(str(i)))
            img = QImage ()
            img.loadFromData(data)
            self.qMapList.append(img)

        self.label.setFixedSize(QPixmap.fromImage(self.qMapList[0]).size())
        self.label.setPixmap(QPixmap.fromImage(self.qMapList[0]))
        self.label.setScaledContents(True)
        self.timer = QTimer(self.label)
        self.timer.setInterval(100)

        self.cnt = 0
        self.closeCnt = 50
        self.timer.timeout.connect(self.UpdatePic)

    def show(self) -> None:
        self.timer.start()
        self.cnt = 0
        super(self.__class__, self).show()

    def close(self):
        self.timer.stop()
        super(self.__class__, self).close()

    def UpdatePic(self):
        self.index += 1
        if self.index >= 10:
            self.index = 0
        # self.label.setPixmap(QPixmap("resources/loading_{}_big.png".format(self.index)))
        self.label.setPixmap(QPixmap.fromImage(self.qMapList[self.index]))
        self.cnt += 1
        if self.cnt >= self.closeCnt:
            self.close()
        pass

