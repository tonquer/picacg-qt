from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PySide6.QtWidgets import QScrollBar

from qt_owner import QtOwner


class ReadScroll(QScrollBar):
    def __init__(self):
        QScrollBar.__init__(self)
        self.animation = QPropertyAnimation()
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b"value")
        self.scrollTime = 1000
        self.animation.setDuration(self.scrollTime)
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animationValue = self.value()
        self.backTick = 0
        self.laveValue = 0
        self.lastV = 0
        self.animation.finished.connect(self.Finished)

    def Finished(self):
        QtOwner().owner.readView.frame.scrollArea.OnValueChange(self.value())

    def StopScroll(self):
        self.backTick = 0
        self.animation.stop()

    def Scroll(self, value, time=0):
        if self.animation.state() == QAbstractAnimation.State.Running:
            self.animation.stop()
        oldValue = self.value()
        self.animation.setStartValue(oldValue)
        if not time:
            self.animation.setDuration(self.scrollTime)
        else:
            self.animation.setDuration(time)
        self.animation.setEndValue(oldValue + value)
        self.animation.start()

