


import sys

from PySide6.QtWidgets import QApplication, QWidget

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_login import Ui_Login
from tools.str import Str


class LoginView(BaseMaskDialog, Ui_Login):
    def __init__(self, parent=None):
        BaseMaskDialog.__init__(self, parent)
        Ui_Login.__init__(self)
        self.setupUi(self.widget)
        self.switchButton.clicked.connect(self._SwitchLoginMode)
        self.loginModel = True
        self.SetLoginMode()

    def _SwitchLoginMode(self):
        self.loginModel = not self.loginModel
        self.SetLoginMode()

    def SetLoginMode(self):
        if not self.loginModel:
            self.userWidget.setVisible(False)
            self.cookieWidget.setVisible(True)
            self.switchButton.setText(Str.GetStr(Str.LoginUser))
        else:
            self.cookieWidget.setVisible(False)
            self.userWidget.setVisible(True)
            self.switchButton.setText(Str.GetStr(Str.LoginCookie))
        return

app = QApplication(sys.argv)
# 创建主界面
p = QWidget()
p.resize(500, 500)
Str.Reload()
p.show()

main = LoginView(p)
main.show()
sys.exit(app.exec())
