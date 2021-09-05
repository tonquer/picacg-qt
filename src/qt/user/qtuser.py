import re

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QPixmap, QIcon

from resources import resources
from resources.resources import DataMgr
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

        q = QPixmap()
        q.loadFromData(DataMgr.GetData("icon_bookmark_on"))
        p = QPixmap()
        p.loadFromData(DataMgr.GetData("icon_comic"))
        self.signButton.setIcon(QIcon(q.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.signButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton11.setIcon(QIcon(p.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.toolButton11.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        p = QPixmap()
        p.loadFromData(DataMgr.GetData("icon_like"))
        self.toolButton4.setIcon(QIcon(p.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.toolButton4.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        p = QPixmap()
        p.loadFromData(DataMgr.GetData("icon_comicviewer_nightfilter_on"))
        self.toolButton5.setIcon(QIcon(p.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.toolButton5.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.icon.SetPicture(resources.DataMgr.GetData("placeholder_avatar"))
        self.pictureData = None
        self.icon.installEventFilter(self)

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
        self.stackedWidget.addWidget(QtOwner().owner.myCommentForm)
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
            self.signButton.setText(self.tr("已打卡"))
            # self.signButton.setHidden(True)
            QtTask().AddHttpTask(req.GetUserInfo(), QtOwner().owner.loginForm.UpdateUserBack)
            self.update()
        return

    def UpdateLabel(self, name, level, exp, title, sign):
        self.name.setText(name)
        self.level.setText("level: "+str(level))
        self.title.setText(title)
        self.level.setText("LV"+str(level))
        self.exp.setText("exp: " + str(exp))
        if sign:
            self.signButton.setText(self.tr("已打卡"))
            self.signButton.setEnabled(False)
        self.update()

    def UpdatePictureData(self, data):
        if not data:
            return
        self.icon.setPixmap(None)
        self.icon.setText(self.tr("头像上传中......"))
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
            QtOwner().owner.msgForm.ShowError(QtOwner().owner.GetStatusStr(msg))

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
