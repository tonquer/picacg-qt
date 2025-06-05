from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from component.label.msg_label import MsgLabel
from interface.ui_register_widget import Ui_RegisterWidget
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class RegisterWidget(QtWidgets.QWidget, Ui_RegisterWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_RegisterWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        reg = QRegularExpression("^[A-Z0-9a-z\\.\\_]{1,16}$")
        validator = QRegularExpressionValidator(reg, self.userEdit)
        self.userEdit.setValidator(validator)

    def Init(self):
        return

    def ClickButton(self):
        self.Register()

    def Register(self):
        if not self.buttonGroup.checkedButton():
            # QtWidgets.QMessageBox.information(self, '错误', "不能为空", QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(Str.GetStr(Str.NotSpace))
            return
        if len(self.passwdEdit.text()) < 8:
            # QtWidgets.QMessageBox.information(self, '错误', "密码太短", QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(Str.GetStr(Str.PasswordShort))
            return
        birthday = self.birthdayEdit.date()
        data = {
            "email": self.userEdit.text(),
            "password": self.passwdEdit.text(),
            "name": self.nameEdit.text(),
            "birthday": birthday.toString("yyyy-MM-dd"),
            "gender": self.buttonGroup.checkedButton().objectName().replace("gender_", ""),  # m, f, bot
            "answer1": self.answer1Edit.text(),
            "answer2": self.answer2Edit.text(),
            "answer3": self.answer3Edit.text(),
            "question1": self.question1Edit.text(),
            "question2": self.question2Edit.text(),
            "question3": self.question3Edit.text()
        }
        for v in data.values():
            if not v:
                # QtWidgets.QMessageBox.information(self, '错误', "不能为空", QtWidgets.QMessageBox.Yes)
                QtOwner().ShowError(Str.GetStr(Str.NotSpace))
                return

        QtOwner().ShowLoading()
        self.AddHttpTask(req.RegisterReq(data), self.RegisterBack)
        return

    def RegisterBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            # self.close()
            # QtWidgets.QMessageBox.information(self, '注册成功', "注册成功", QtWidgets.QMessageBox.Yes)
            QtOwner().ShowMsg(Str.GetStr(Str.RegisterSuc))
        else:
            msg = raw["data"]
            # QtWidgets.QMessageBox.information(self, '注册失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(Str.GetStr(st) + "\n" + msg)
