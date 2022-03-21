from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from component.label.msg_label import MsgLabel
from interface.ui_change_password_widget import Ui_ChangePasswordWidget
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class ChangePasswordWidget(QtWidgets.QWidget, Ui_ChangePasswordWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_ChangePasswordWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.token = ""
        self.userId = ""

    def Init(self):
        return

    def ClickButton(self):
        userId = self.userEdit.text()
        old = self.passwordEdit.text()
        new = self.passwordEdit.text()
        if self.token and self.userId and self.userId == userId:
            self.ChangePassword(old, new)
        else:
            self.Login()

    def Login(self):
        userId = self.userEdit.text()
        oldPassword = self.passwordEdit.text()
        newPassword = self.newPasswordEdit.text()
        if not userId or not oldPassword or not newPassword:
            QtOwner().ShowMsg(Str.GetStr(Str.NotSpace))
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.LoginReq(userId, oldPassword), self.LoginBack, (userId, oldPassword, newPassword))
        return

    def LoginBack(self, raw, v):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            # QtOwner().ShowMsg(Str.GetStr(Str.RegisterSuc))
            token = raw["token"]
            self.token = token
            userId, oldPassword, newPassword = v
            self.userId = userId
            self.ChangePassword(oldPassword, newPassword)
        else:
            msg = raw["data"]
            QtOwner().ShowError(Str.GetStr(st) + "\n" + msg)
    
    def ChangePassword(self, oldPassword, newPassword):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.ChangePasswordReq(self.token, oldPassword, newPassword), self.ChangePasswordBack)
        return
    
    def ChangePasswordBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            QtOwner().ShowMsg(Str.GetStr(Str.Ok))
            return
        else:
            msg = raw["data"]
            QtOwner().ShowError(Str.GetStr(st) + "\n" + msg)
