import weakref

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt, QSize, QEvent
from PySide2.QtGui import  QPixmap
from PySide2.QtWidgets import  QListWidgetItem

from resources import resources
from src.qt.com.qtimg import QtImgMgr
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
        self.pictureData = None
        self.icon.installEventFilter(self)
        self.listWidget.currentRowChanged.connect(self.Switch)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setFrameShape(self.listWidget.NoFrame)
        for name in ["主页", "搜索", "分类", "排行", "收藏", "历史记录", "下载", "留言板", "聊天室"]:
            item = QListWidgetItem(
                name,
                self.listWidget
            )
            item.setSizeHint(QSize(16777215, 60))
            item.setTextAlignment(Qt.AlignCenter)

        self.stackedWidget.addWidget(self.owner().indexForm)
        self.stackedWidget.addWidget(self.owner().searchForm)
        self.stackedWidget.addWidget(self.owner().categoryForm)
        self.stackedWidget.addWidget(self.owner().rankForm)
        self.stackedWidget.addWidget(self.owner().favoriteForm)
        self.stackedWidget.addWidget(self.owner().historyForm)
        self.stackedWidget.addWidget(self.owner().downloadForm)
        self.stackedWidget.addWidget(self.owner().leaveMsgForm)
        self.stackedWidget.addWidget(self.owner().chatForm)

    def SetPicture(self, data):
        a = QPixmap()
        a.loadFromData(data)
        self.pictureData = data
        self.icon.setPixmap(a)

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

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.pictureData:
                    QtImgMgr().ShowImg(self.pictureData)
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)
