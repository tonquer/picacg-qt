from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QListWidgetItem, QLabel

from component.list.base_list_widget import BaseListWidget


class TagListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.setViewMode(self.ListMode)
        self.setFlow(self.LeftToRight)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumHeight(30)
        self.setFocusPolicy(Qt.NoFocus)

    def AddItem(self, name, isSelectable=False):
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        label.setFont(font)

        item = QListWidgetItem(name)
        item.setTextAlignment(Qt.AlignCenter)
        # item.setBackground(QColor(87, 195, 194))
        # item.setBackground(QColor(0, 0, 0, 0))
        item.setSizeHint(label.sizeHint()+ QSize(20, 10))
        if not isSelectable:
            item.setFlags(item.flags() & (~Qt.ItemIsSelectable))

        self.addItem(item)