import re

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QEvent

from resources import resources
from src.qt.com.qtimg import QtImgMgr
from src.qt.qtmain import QtOwner
from src.server import req, QtTask
from src.util.status import Status
from ui.user import Ui_User


class QtUser(QtWidgets.QWidget, Ui_User):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_User.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("哔咔漫画")

        self.icon.SetPicture(resources.DataMgr.GetData("placeholder_avatar"))
        self.pictureData = None
        self.icon.installEventFilter(self)
        # self.listWidget.currentRowChanged.connect(self.Switch)
        # self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # QScroller.grabGesture(self.listWidget, QScroller.LeftMouseButtonGesture)
        # self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.listWidget.setFrameShape(self.listWidget.NoFrame)
        # self.listWidget.setResizeMode(self.listWidget.Fixed)
        # for name in ["主页", "搜索", "分类", "排行", "收藏", "历史记录", "下载", "留言板", "聊天室"]:
        #     item = QListWidgetItem(
        #         name,
        #         self.listWidget
        #     )
        #     item.setSizeHint(QSize(16777215, 60))
        #     item.setTextAlignment(Qt.AlignCenter)
        #
        self.stackedWidget.addWidget(QtOwner().owner.indexForm)
        self.stackedWidget.addWidget(QtOwner().owner.searchForm)
        self.stackedWidget.addWidget(QtOwner().owner.categoryForm)
        self.stackedWidget.addWidget(QtOwner().owner.rankForm)
        self.stackedWidget.addWidget(QtOwner().owner.favoriteForm)
        self.stackedWidget.addWidget(QtOwner().owner.historyForm)
        self.stackedWidget.addWidget(QtOwner().owner.downloadForm)
        self.stackedWidget.addWidget(QtOwner().owner.leaveMsgForm)
        self.stackedWidget.addWidget(QtOwner().owner.chatForm)
        self.stackedWidget.addWidget(QtOwner().owner.friedForm)
        self.stackedWidget.addWidget(QtOwner().owner.gameForm)
        self.buttonGroup.buttonClicked.connect(self.Switch)
        self.isHeadUp = False

    def SetPicture(self, data):
        self.pictureData = data
        self.icon.SetPicture(data)

    def Switch(self, button):
        # data = {
        #     "search": 0,
        #     "category": 1,
        #     "favorite": 2,
        #     "download": 3
        # }
        # index = data.get(name)
        index = int(re.findall(r"\d+", button.objectName())[0])
        # button.setChecked(True)
        self.stackedWidget.setCurrentIndex(index)
        self.stackedWidget.currentWidget().SwitchCurrent()

    def Sign(self):
        QtOwner().owner.loadingForm.show()
        QtTask().AddHttpTask(req.PunchIn(), self.SignBack)

        return

    def SignBack(self, msg):
        QtOwner().owner.loadingForm.close()
        if msg == Status.Ok:
            self.signButton.setEnabled(False)
            self.signButton.setText("已签到")
            QtTask().AddHttpTask(req.GetUserInfo(), QtOwner().owner.loginForm.UpdateUserBack)
            self.update()
        return

    def UpdateLabel(self, name, level, exp, title, sign):
        self.name.setText(name)
        self.level.setText("level: "+str(level))
        self.title.setText(title)
        self.level.setText("LV"+str(level))
        self.exp.setText("exp: " + str(exp))
        if not sign:
            self.signButton.setEnabled(True)
            self.signButton.setText("签到")
        self.update()

    def UpdatePictureData(self, data):
        if not data:
            return
        self.icon.setPixmap(None)
        self.icon.setText("头像上传中......")
        self.isHeadUp = True
        QtImgMgr().SetHeadStatus(not self.isHeadUp)
        QtTask().AddHttpTask(req.SetAvatarInfoReq(data), self.UpdatePictureDataBack)
        return

    def UpdatePictureDataBack(self, msg):
        self.isHeadUp = False
        QtImgMgr().SetHeadStatus(not self.isHeadUp)
        if msg == Status.Ok:
            QtOwner().owner.loginForm.InitUser()
        else:
            QtOwner().owner.msgForm.ShowError(msg)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                QtImgMgr().ShowImg(self.pictureData)
                # self.UpdatePictureData()
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)
