from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtWidgets import QWidget

from config import config
from interface.ui_navigation import Ui_Navigation
from qt_owner import QtOwner
from server import req
from task.qt_task import QtTaskBase
from tools.status import Status
from tools.str import Str
from tools.user import User
from view.user.login_view import LoginView


class NavigationWidget(QWidget, Ui_Navigation, QtTaskBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.resize(260, 800)
        self.__ani = QPropertyAnimation(self, b"geometry")
        self.__connect = None
        self.pictureData = ""
        self.pushButton.clicked.connect(self.OpenLoginView)

    def OpenLoginView(self):
        if User().isLogin:
            self.Sign()
            return

        loginView = LoginView(QtOwner().owner)
        loginView.exec_()

        if User().isLogin:
            self.LoginSucBack()
            QtOwner().owner.LoginSucBack()
        return

    def LoginSucBack(self):
        self.pushButton.setText(Str.GetStr(Str.Sign))
        self.AddHttpTask(req.GetUserInfo(), self.UpdateUserBack)

    def UpdateUserBack(self, raw):
        self.levelLabel.setText("LV" + str(User().level))
        self.expLabel.setText("Exp: " + str(User().exp))
        self.titleLabel.setText(str(User().title))
        self.nameLabel.setText(str(User().name))
        if User().isPunched:
            self.pushButton.setText(Str.GetStr(Str.AlreadySign))
            self.pushButton.setVisible(False)
        if not User().avatar:
            return
        url = User().avatar.get("fileServer")
        path = User().avatar.get("path")
        if url and path and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.ShowUserImg)

    def ShowUserImg(self, data, st):
        if st == Status.Ok:
            self.SetPicture(data)
        return

    def Sign(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.PunchIn(), self.SignBack)

        return

    def SignBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            self.pushButton.setVisible(False)
            self.pushButton.setText(Str.GetStr(Str.AlreadySign))
            # self.signButton.setHidden(True)
            self.AddHttpTask(req.GetUserInfo(), self.UpdateUserBack)
        return

    def SetPicture(self, data):
        self.pictureData = data
        self.picLabel.SetPicture(data)

    def aniShow(self):
        """ 动画显示 """
        super().show()
        self.activateWindow()
        self.__ani.setStartValue(QRect(self.x(), self.y(), 30, self.height()))
        self.__ani.setEndValue(QRect(self.x(), self.y(), 260, self.height()))
        self.__ani.setEasingCurve(QEasingCurve.InOutQuad)
        self.__ani.setDuration(85)
        self.__ani.start()

    def aniHide(self):
        """ 动画隐藏 """
        self.__ani.setStartValue(QRect(self.x(), self.y(), 260, self.height()))
        self.__ani.setEndValue(QRect(self.x(), self.y(), 30, self.height()))
        self.__connect = self.__ani.finished.connect(self.__hideAniFinishedSlot)
        self.__ani.setDuration(85)
        self.__ani.start()

    def __hideAniFinishedSlot(self):
        """ 隐藏窗体的动画结束 """
        super().hide()
        self.resize(60, self.height())
        if self.__connect:
            self.__ani.disconnect(self.__connect)
            self.__connect = None
