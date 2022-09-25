from PySide6.QtWidgets import QApplication

from component.dialog.base_mask_dialog import BaseMaskDialog
from config.setting import Setting
from interface.ui_exit import Ui_Exit
from qt_owner import QtOwner


class ShowCloseDialog(BaseMaskDialog, Ui_Exit):

    def __init__(self, parent=None):
        BaseMaskDialog.__init__(self, parent)
        Ui_Exit.__init__(self)
        self.widget.adjustSize()
        self.setupUi(self.widget)
        self.buttonGroup.setId(self.radioButton1, 0)
        self.buttonGroup.setId(self.radioButton2, 1)
        self.button.clicked.connect(self.Click)
        self.checkBox.clicked.connect(self.SwitchCheckBox)

    def SwitchCheckBox(self, check):
        Setting.IsNotShowCloseTip.SetValue(int(self.checkBox.isChecked()))

    def Click(self):
        if self.radioButton1.isChecked():
            Setting.ShowCloseType.SetValue(0)
            self.close()
            QtOwner().closeType = 2
            QApplication.quit()
        else:
            QtOwner().owner.myTrayIcon.show()
            Setting.ShowCloseType.SetValue(1)
            self.close()
            QtOwner().owner.hide()
        return

    def LoadSetting(self):
        self.checkBox.setChecked(bool(Setting.IsNotShowCloseTip.value))
        button = getattr(self, "radioButton{}".format(int(Setting.ShowCloseType.value+1)))
        button.setChecked(True)
        return