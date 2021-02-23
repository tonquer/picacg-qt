from PySide2.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRectF, Property
from PySide2.QtGui import QPen, QPainterPath, QPainter, QColor
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication


class QtBubbleLabel(QWidget):
    BackgroundColor = QColor(195, 195, 195)
    BorderColor = QColor(150, 150, 150)

    def __init__(self, *args, **kwargs):
        super(QtBubbleLabel, self).__init__(*args, **kwargs)
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setMinimumWidth(200)
        self.setMinimumHeight(48)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 16)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self._desktop = QApplication.instance().desktop()
        self.animationGroup = QParallelAnimationGroup(self)

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def stop(self):
        self.hide()
        self.animationGroup.stop()
        self.animationGroup.clear()
        self.close()

    def show(self):
        super(QtBubbleLabel, self).show()
        x = self.parent().geometry().x()
        y = self.parent().geometry().y()
        x2 = self.parent().size().width()
        y2 = self.parent().size().height()
        startPos = QPoint(x+int(x2/2)-int(self.width()/2), y+int(y2/2))
        endPos = QPoint(x+int(x2/2)-int(self.width()/2), y+int(y2/2)-self.height()*3-5)
        self.move(startPos)
        # 初始化动画
        self.initAnimation(startPos, endPos)

    def initAnimation(self, startPos, endPos):
        # 透明度动画
        opacityAnimation = QPropertyAnimation(self, b"opacity")
        opacityAnimation.setStartValue(1.0)
        opacityAnimation.setEndValue(0.0)
        # 设置动画曲线
        opacityAnimation.setEasingCurve(QEasingCurve.InQuad)
        opacityAnimation.setDuration(3000)  # 在4秒的时间内完成
        # 往上移动动画
        moveAnimation = QPropertyAnimation(self, b"pos")
        moveAnimation.setStartValue(startPos)
        moveAnimation.setEndValue(endPos)
        moveAnimation.setEasingCurve(QEasingCurve.InQuad)
        moveAnimation.setDuration(4000)  # 在5秒的时间内完成
        # 并行动画组（目的是让上面的两个动画同时进行）
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(moveAnimation)
        self.animationGroup.finished.connect(self.close)  # 动画结束时关闭窗口
        self.animationGroup.start()

    def paintEvent(self, event):
        super(QtBubbleLabel, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        rectPath = QPainterPath()  # 圆角矩形

        height = self.height() - 8  # 往上偏移8
        rectPath.addRoundedRect(QRectF(0, 0, self.width(), height), 5, 5)
        x = self.width() / 5 * 4
        # 边框画笔
        painter.setPen(QPen(self.BorderColor, 1, Qt.SolidLine,
                            Qt.RoundCap, Qt.RoundJoin))
        # 背景画刷
        painter.setBrush(self.BackgroundColor)
        # 绘制形状
        painter.drawPath(rectPath)

    def windowOpacity(self):
        return super(QtBubbleLabel, self).windowOpacity()

    def setWindowOpacity(self, opacity):
        super(QtBubbleLabel, self).setWindowOpacity(opacity)

    opacity = Property(float, windowOpacity, setWindowOpacity)

    def ShowMsg(self, text):
        self.stop()
        self.setText(text)
        self.setStyleSheet("color:black")
        self.show()

    @staticmethod
    def ShowMsgEx(owner, text):
        data = QtBubbleLabel(owner)
        data.setText(text)
        data.setStyleSheet("color:black")
        data.show()

    def ShowError(self, text):
        self.stop()
        self.setText(text)
        self.setStyleSheet("color:red")
        self.show()

    @staticmethod
    def ShowErrorEx(owner, text):
        data = QtBubbleLabel(owner)
        data.setText(text)
        data.setStyleSheet("color:red")
        data.show()
