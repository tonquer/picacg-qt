from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget

from interface.ui_nas_item import Ui_NasItem


class NasItemWidget(QWidget, Ui_NasItem):
    def __init__(self):
        QWidget.__init__(self)
        Ui_NasItem.__init__(self)
        self.setupUi(self)
