from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QListWidget, QAbstractItemView

from component.list.base_list_widget import BaseListWidget
from component.scroll.smooth_scroll_bar import SmoothScrollBar
from qt_owner import QtOwner
from task.qt_task import QtTaskBase


class EpsListWidget(BaseListWidget, QtTaskBase):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        QtTaskBase.__init__(self)

    def wheelEvent(self, arg__1) -> None:
        if not self.wheelStatus:
            return
        if -arg__1.angleDelta().y() > 0 and abs(self.verticalScrollBar().value() - self.verticalScrollBar().maximum()) <= 2:
            arg__1.ignore()
            return
        elif -arg__1.angleDelta().y() < 0 and abs(self.verticalScrollBar().value() - self.verticalScrollBar().minimum()) <= 2:
            arg__1.ignore()
            return
        self.vScrollBar.ScrollValue(-arg__1.angleDelta().y())