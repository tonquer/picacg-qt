from enum import Enum

from PySide6.QtCore import QPropertyAnimation, QRectF, Property, Qt
from PySide6.QtGui import QPaintEvent, QPainter, QPixmap
from PySide6.QtWidgets import QStackedWidget


class AnimationEnum(Enum):
    LeftToRight = 1
    RightToLeft = 2
    Top = 3

class AnimationStackWidget(QStackedWidget):
    def __init__(self, parent=None):
        QStackedWidget.__init__(self, parent)
        self._value = 0
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.valueChanged.connect(self.ValueChanged)
        self.animation.finished.connect(self.Finished)
        self.currentValue = 0
        self.nextIndex = 0
        self.subStackList = [0]
        self.animationType = AnimationEnum.LeftToRight
        self.switchArg = {}

    @Property(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def ValueChanged(self, value):
        self.currentValue = value
        self.update()
        return

    def Finished(self):
        self.widget(self.currentIndex()).show()
        self.setCurrentIndex(self.nextIndex)
        self.widget(self.currentIndex()).SwitchCurrent(**self.switchArg)
        self.switchArg = {}
        return

    def PaintPrevious(self, paint, index):
        w = self.widget(index)
        pixmap = QPixmap(w.size())
        # pixmap.setDevicePixelRatio(self.devicePixelRatio())
        w.render(pixmap)
        r = w.geometry()
        value = self.currentValue
        r1 = QRectF(0.0, 0.0, value, r.height())
        r2 = QRectF((r.width()-value), 0, value, r.height())
        paint.drawPixmap(r1, pixmap, r2)

    def SwitchWidgetByIndex(self, index, **kwargs):
        self.nextIndex = index
        # 判断是在左边还是右边 用不同动画
        oldIndex = 0
        if self.currentIndex() in self.subStackList:
            oldIndex = self.subStackList.index(self.currentIndex())

        newIndex = 0
        if index in self.subStackList:
            newIndex = self.subStackList.index(index)

        g = self.geometry()
        if oldIndex <= newIndex:
            self.animationType = AnimationEnum.LeftToRight

            self.animation.setStartValue(g.width())
            self.animation.setEndValue(0)
        else:
            self.animationType = AnimationEnum.RightToLeft
            self.animation.setStartValue(0)
            self.animation.setEndValue(g.width())
        self.switchArg = kwargs
        self.widget(self.currentIndex()).hide()
        self.animation.setDuration(250)
        self.animation.start()

    def PaintNext(self, paint, index):
        w = self.widget(index)
        r = w.geometry()
        w.resize(r.width(), r.height())
        radio = self.devicePixelRatioF()
        pixmap = QPixmap(w.size())
        # pixmap.setDevicePixelRatio(radio)
        w.render(pixmap)

        value = self.currentValue
        r1 = QRectF(value, 0.0, (r.width()-value), r.height())
        r2 = QRectF(0.0, 0.0, (r.width()-value), r.height())
        paint.drawPixmap(r1, pixmap, r2)

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.animation.state() == QPropertyAnimation.State.Running:
            paint = QPainter(self)
            paint.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
            if self.animationType == AnimationEnum.LeftToRight:
                self.PaintPrevious(paint, self.currentIndex())
                self.PaintNext(paint, self.nextIndex)
            else:
                self.PaintPrevious(paint, self.nextIndex)
                self.PaintNext(paint, self.currentIndex())
