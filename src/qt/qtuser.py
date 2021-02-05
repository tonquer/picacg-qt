import weakref

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from resources import resources
from src.user.user import User
from src.util.status import Status
from ui.user import Ui_User


class QtUser(QtWidgets.QWidget, Ui_User):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_User.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.setWindowTitle("哔咔漫画")

        pix = QtGui.QPixmap()
        pix.loadFromData(resources.DataMgr.GetData("placeholder_avatar"))
        pix.scaled(self.icon.size(), Qt.KeepAspectRatio)
        self.icon.setScaledContents(True)
        self.icon.setPixmap(pix)

        self.listWidget.currentRowChanged.connect(self.Switch)
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for name in ["搜索", "分类", "排行", "收藏", "历史记录", "下载"]:
            item = QListWidgetItem(
                name,
                self.listWidget
            )
            item.setSizeHint(QSize(16777215, 60))
            item.setTextAlignment(Qt.AlignCenter)

        self.stackedWidget.addWidget(self.owner().searchForm)
        self.stackedWidget.addWidget(self.owner().categoryForm)
        self.stackedWidget.addWidget(self.owner().rankForm)
        self.stackedWidget.addWidget(self.owner().favoriteForm)
        self.stackedWidget.addWidget(self.owner().historyForm)
        self.stackedWidget.addWidget(self.owner().downloadForm)

    def Switch(self, index):
        # data = {
        #     "search": 0,
        #     "category": 1,
        #     "favorite": 2,
        #     "download": 3
        # }
        # index = data.get(name)
        self.stackedWidget.setCurrentIndex(index)
        self.stackedWidget.currentWidget().SwitchCurrent()

    def Sign(self):
        self.owner().loadingForm.show()
        self.owner().qtTask.AddHttpTask(lambda x: User().Punched(x), self.SignBack)

        return

    def SignBack(self, msg):
        self.owner().loadingForm.close()
        if msg == Status.Ok:
            self.signButton.setEnabled(False)
            self.signButton.setText("已签到")
            self.owner().qtTask.AddHttpTask(lambda x: User().UpdateUserInfo(x), self.owner().loginForm.UpdateUserBack)
            self.update()
        return

    def UpdateLabel(self, name, level, exp, sign):
        self.name.setText(name)
        self.level.setText("level: "+str(level))
        self.exp.setText("exp: " + str(exp))
        if not sign:
            self.signButton.setEnabled(True)
            self.signButton.setText("签到")
        self.update()
