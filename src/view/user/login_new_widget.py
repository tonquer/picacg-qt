import base64
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QTimer, Qt

from config.setting import Setting, SettingValue
from interface.ui_login_widget import Ui_LoginWidget
from qt_owner import QtOwner
from server import req, Status, config
from task.qt_task import QtTaskBase
from tools.str import Str
from tools.user import User


class LoginNewWidget(object):
    def __init__(self, owner):
        self.owner = owner
        self.autoTimer = QTimer()
        self.autoTimer.setInterval(2000)
        self.autoTimer.timeout.connect(self.AutoTimeOut)
        self.owner.autoBox.setChecked(bool(Setting.AutoLogin.value))
        self.owner.autoSign.setChecked(bool(Setting.AutoSign.value))
        self.owner.saveBox.setChecked(bool(Setting.SavePassword.value))
        self.owner.autoBox.clicked.connect(partial(self.CheckButtonEvent, Setting.AutoLogin, self.owner.autoBox))
        self.owner.autoSign.clicked.connect(partial(self.CheckButtonEvent, Setting.AutoSign, self.owner.autoSign))
        self.owner.saveBox.clicked.connect(partial(self.CheckButtonEvent, Setting.SavePassword, self.owner.saveBox))
        self.owner.loginButton.clicked.connect(self.Login)
        userId = Setting.UserId.value
        if userId and isinstance(userId, str):
            self.owner.userEdit_2.setText(userId)

        passwd = Setting.Password.value
        passwd = base64.b64decode(passwd).decode("utf-8") if passwd else ""
        if passwd and isinstance(passwd, str):
            self.owner.passwdEdit_2.setText(passwd)
        self.loginIsInit = False
        self.owner.loginButton.setShortcut(Qt.Key_Return)
        self.isLogining = False

        # self.buttonGroup = QtWidgets.QButtonGroup(self)
        # self.buttonGroup.addButton(self.selectIp1)
        # self.selectIp1.setChecked(True)

    def CheckButtonEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(button.isChecked()))
        return

    def Init(self):
        if self.loginIsInit:
            return
        self.loginIsInit = True
        if Setting.AutoLogin.value:
            self.autoTimer.start()
        # self.userEdit_2.setText()
        # request = req.InitReq()
        # request.proxy = {}
        # self.AddHttpTask(request, self.InitBack)
        return

    def AutoTimeOut(self):
        self.autoTimer.stop()
        if not Setting.AutoLogin.value:
            return
        if self.isLogining:
            return
        if not QtOwner().IsCurView(self.owner):
            return
        self.ClickButton()

    def ClickButton(self):
        self.Login()

    def Login(self):
        QtOwner().ShowLoading()
        self.isLogining = True
        userId = self.owner.userEdit_2.text()
        passwd = self.owner.passwdEdit_2.text()
        self.owner.AddHttpTask(req.LoginReq(userId, passwd), self.LoginBack)

    def LoginBack(self, raw):
        self.isLogining = False
        QtOwner().CloseLoading()
        st = raw["st"]
        QtOwner().CheckShowMsg(raw)
        if st == Status.Ok:
            Setting.UserId.SetValue(self.owner.userEdit_2.text())
            if Setting.SavePassword.value:
                Setting.Password.SetValue(base64.b64encode(self.owner.passwdEdit_2.text().encode("utf-8")))
            else:
                Setting.Password.SetValue("")
            token = raw["token"]
            User().SetToken(token)
            # QtOwner().SetUser(user)
            # QtOwner().SetLogin()
            QtOwner().OpenIndex()
            QtOwner().owner.navigationWidget.LoginSucBack()

