from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from interface.ui_setting_item import Ui_SettingItem


class SettingItemWidget(QWidget, Ui_SettingItem):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_SettingItem.__init__(self)
        self.setupUi(self)
        self.widget.hide()
        self.toolButton.clicked.connect(self._switchWidget)

    def _switchWidget(self):
        if self.widget.isHidden():
            self.widget.show()
            self.toolButton.setArrowType(Qt.ArrowType.DownArrow)
        else:
            self.widget.hide()
            self.toolButton.setArrowType(Qt.ArrowType.UpArrow)
        return
