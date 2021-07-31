from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QTimer
from PySide2.QtGui import QPixmap, QImage

from resources import resources
from resources.resources import DataMgr
from src.qt.com.qt_git_label import QtGifLabel
from ui.loading import Ui_Loading, QGridLayout


class QtLoading(QtWidgets.QDialog):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        self.gridLayout = QGridLayout(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.label = QtGifLabel(self)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        # self.index = 1
        # self.qMapList = []
        # for i in range(1, 11):
        #     data = resources.DataMgr.GetData("loading_{}".format(str(i)))
        #     img = QImage ()
        #     img.loadFromData(data)
        #     self.qMapList.append(img)

        # self.label.setFixedSize(QPixmap.fromImage(self.qMapList[0]).size())
        # self.label.setPixmap(QPixmap.fromImage(self.qMapList[0]))
        # self.label.setScaledContents(True)
        self.timer = QTimer(self.label)
        self.timer.setInterval(100)
        self.label.Init(DataMgr().GetData("loading"))
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
        # self.index += 1
        # if self.index >= 10:
        #     self.index = 0
        # self.label.setPixmap(QPixmap("resources/loading_{}_big.png".format(self.index)))
        # self.label.setPixmap(QPixmap.fromImage(self.qMapList[self.index]))
        self.cnt += 1
        if self.cnt >= self.closeCnt:
            self.close()
        pass

