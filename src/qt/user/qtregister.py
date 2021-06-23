from PySide2 import QtWidgets
from PySide2.QtCore import QRegExp, Qt
from PySide2.QtGui import QRegExpValidator

from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtloading import QtLoading
from src.server import req, QtTask
from src.util.status import Status
from ui.register import Ui_Register


class QtRegister(QtWidgets.QWidget, Ui_Register):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Register.__init__(self)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("注册")
        self.loadingForm = QtLoading(self)
        reg = QRegExp("^[A-Z0-9a-z\\.\\_]{1,16}$")
        validator = QRegExpValidator(reg, self.userEdit)
        self.userEdit.setValidator(validator)

    def Register(self):
        if not self.buttonGroup.checkedButton():
            # QtWidgets.QMessageBox.information(self, '错误', "不能为空", QtWidgets.QMessageBox.Yes)
            QtBubbleLabel.ShowErrorEx(self, "不能为空")
            return
        if len(self.passwdEdit.text()) < 8:
            # QtWidgets.QMessageBox.information(self, '错误', "密码太短", QtWidgets.QMessageBox.Yes)
            QtBubbleLabel.ShowErrorEx(self, "密码太短")
            return
        data = {
            "email": self.userEdit.text(),
            "password": self.passwdEdit.text(),
            "name": self.nameEdit.text(),
            "birthday": self.birthdayEdit.text().replace("/", "-"),
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
                QtBubbleLabel.ShowErrorEx(self, "不能为空")
                return

        self.loadingForm.show()
        QtTask().AddHttpTask(req.RegisterReq(data), self.RegisterBack)
        return

    def RegisterBack(self, msg):
        self.loadingForm.close()
        if msg == Status.Ok:
            # self.close()
            # QtWidgets.QMessageBox.information(self, '注册成功', "注册成功", QtWidgets.QMessageBox.Yes)
            QtBubbleLabel.ShowMsgEx(self, "注册成功")
            self.close()
        else:
            # QtWidgets.QMessageBox.information(self, '注册失败', msg, QtWidgets.QMessageBox.Yes)
            QtBubbleLabel.ShowErrorEx(self, msg)

