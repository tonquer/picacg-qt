from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QListWidget, QAbstractItemView, QScroller, QTableWidget

from component.scroll.smooth_scroll_bar import SmoothScrollBar
from config.setting import Setting
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.str import Str


class BaseTableWidget(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.ForwardButton:
            # QtOwner().SwitchWidgetNext()
            event.ignore()
        elif event.button() == Qt.BackButton:
            event.ignore()
            # QtOwner().SwitchWidgetLast()
        return QTableWidget.mousePressEvent(self, event)