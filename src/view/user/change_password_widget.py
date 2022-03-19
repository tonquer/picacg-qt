from tkinter import E
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from component.label.msg_label import MsgLabel
from interface.ui_register_widget import Ui_RegisterWidget
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class ChangePasswordWidget(QtWidgets.QWidget, Ui_RegisterWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_RegisterWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.token = ""
        self.userId = ""

    def Init(self):
        return

    def ClickButton(self):
        if self.token and self.userId:
            self.ChangePassword()
        else:
            self.Login()

    def Login(self):
        if not self.buttonGroup.checkedButton():
            MsgLabel.ShowErrorEx(self, Str.GetStr(Str.NotSpace))
            return
        if len(self.passwdEdit.text()) < 8:
            MsgLabel.ShowErrorEx(self, Str.GetStr(Str.PasswordShort))
            return
        userId = ""
        oldPassword = ""
        newPassword = ""
        QtOwner().ShowLoading()
        self.AddHttpTask(req.LoginReq(userId, oldPassword), self.LoginBack, (userId, oldPassword, newPassword))
        return

    def LoginBack(self, raw, v):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            QtOwner().ShowMsg(Str.GetStr(Str.RegisterSuc))
            token = raw["token"]
            self.token = token
            userId, oldPassword, newPassword = v
            self.userId = userId
            self.ChangePassword()
            self.AddHttpTask(req.ChangePasswordReq(oldPassword, newPassword), self.ChangePasswordBack)
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
        if st == Status.OK:
            QtOwner().ShowMsg(Str.GetStr(Str.Success))
            return
        else:
            msg = raw["data"]
            QtOwner().ShowError(Str.GetStr(st) + "\n" + msg)
