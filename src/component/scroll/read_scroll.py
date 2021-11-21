from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PySide6.QtWidgets import QScrollBar


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

    def StopScroll(self):
        self.backTick = 0
        self.animation.stop()

    def Scroll(self, value):
        if self.animation.state() == QAbstractAnimation.State.Running:
            self.animation.stop()
        oldValue = self.value()
        self.animation.setStartValue(oldValue)
        self.animation.setDuration(self.scrollTime)
        self.animation.setEndValue(oldValue + value)
        self.animation.start()

