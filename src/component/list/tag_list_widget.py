from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QListWidgetItem, QLabel, QAbstractItemView, QListView

from component.list.base_list_widget import BaseListWidget
from component.scroll.smooth_scroll_bar import SmoothScrollBar


class TagListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.setViewMode(QListView.ListMode)
        self.setFlow(QListView.LeftToRight)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumHeight(30)
        self.setFocusPolicy(Qt.NoFocus)
        self.hScrollBar = SmoothScrollBar()
        self.hScrollBar.setOrientation(Qt.Horizontal)
        self.setHorizontalScrollBar(self.hScrollBar)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalScrollBar().setSingleStep(30)

    def wheelEvent(self, arg__1) -> None:
        if not self.wheelStatus:
            return
        if -arg__1.angleDelta().y() > 0 and abs(self.horizontalScrollBar().value() - self.horizontalScrollBar().maximum()) <= 2:
            arg__1.ignore()
            return
        elif -arg__1.angleDelta().y() < 0 and abs(self.horizontalScrollBar().value() - self.horizontalScrollBar().minimum()) <= 2:
            arg__1.ignore()
            return
        self.hScrollBar.ScrollValue(-arg__1.angleDelta().y())

    def AddItem(self, name, isSelectable=False):
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color:#d5577c")
        # font = QFont()
        # font.setPointSize(12)
        # font.setBold(True)
        # label.setFont(font)

        item = QListWidgetItem(self)
        item.setTextAlignment(Qt.AlignCenter)
        # item.setBackground(QColor(87, 195, 194))
        # item.setBackground(QColor(0, 0, 0, 0))
        fm = QFontMetrics(item.font())

        width = fm.boundingRect(name).width()
        height = fm.height()
        self.setItemWidget(item, label)
        item.setSizeHint(QSize(width, height) + QSize(20, 0))
        if not isSelectable:
            item.setFlags(item.flags() & (~Qt.ItemIsSelectable))

        self.addItem(item)
        return item