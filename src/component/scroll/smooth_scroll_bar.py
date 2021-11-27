from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtWidgets import QScrollBar


class SmoothScrollBar(QScrollBar):
    MoveEvent = Signal()

    def __init__(self, parent=None):
        QScrollBar.__init__(self, parent)
        self.__animation = QPropertyAnimation()
        self.__animation.setTargetObject(self)
        self.__animation.setPropertyName(b"value")
        self.__animation.setEasingCurve(QEasingCurve.OutQuint)
        self.__animation.setDuration(500)
        self.__value = self.value()
        self.__animation.finished.connect(self._Finished)

    def _Finished(self):
        self.MoveEvent.emit()
        return

    def setValue(self, value):
        # if self.__animation.state == QPropertyAnimation.State.Running:
        #     self.__animation.stop()
        #     self.MoveEvent.emit()
        if value == self.value():
            return
        self.__animation.stop()
        self.MoveEvent.emit()
        self.__animation.setStartValue(self.value())
        self.__animation.setEndValue(value)
        self.__animation.start()

    def ScrollValue(self, value):
        self.__value += value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value)

    def ScrollTo(self, value):
        self.__value = value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value)

    def ResetValue(self, value):
        self.__value = value

    def mousePressEvent(self, event):
        self.__animation.stop()
        QScrollBar.mousePressEvent(self, event)
        self.__value = self.value()

    def mouseReleaseEvent(self, event):
        self.__animation.stop()
        QScrollBar.mouseReleaseEvent(self, event)
        self.__value = self.value()

    def mouseMoveEvent(self, event):
        self.__animation.stop()
        QScrollBar.mouseMoveEvent(self, event)
        self.__value = self.value()
