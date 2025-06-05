from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from interface.ui_setting_item import Ui_SettingItem


class SettingItemWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setStyleSheet("""
        QWidget
        {
            background-color: rgb(253, 253, 253);
            
            border:2px solid rgb(234,234,234);
            border-radius:5px
        }
        """)