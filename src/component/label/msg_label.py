import os
import time

from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRectF, Property
from PySide6.QtGui import QPen, QPainterPath, QPainter, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog

from tools.log import Log


class MsgLabel(QWidget):
    BackgroundColor = QColor(195, 195, 195)
    BorderColor = QColor(150, 150, 150)

    ShowMsgTick = {}

    def __init__(self, *args, **kwargs):
        super(MsgLabel, self).__init__(*args, **kwargs)
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setMinimumWidth(200)
        self.setMinimumHeight(48)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 16)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.animationGroup = QParallelAnimationGroup(self)
        self.opacityAnimation = None
        self.moveAnimation = None

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def stop(self):
        self.hide()
        self.animationGroup.stop()
        self.animationGroup.clear()
        self.opacityAnimation = None
        self.moveAnimation = None
        self.close()

    def show(self):
        super(MsgLabel, self).show()
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
        self.opacityAnimation = opacityAnimation
        self.moveAnimation = moveAnimation

    def paintEvent(self, event):
        super(MsgLabel, self).paintEvent(event)
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
        return super(MsgLabel, self).windowOpacity()

    def setWindowOpacity(self, opacity):
        super(MsgLabel, self).setWindowOpacity(opacity)

    opacity = Property(float, windowOpacity, setWindowOpacity)

    def ShowMsg(self, text):
        self.stop()
        self.setText(text)
        self.setStyleSheet("color:black")
        self.show()

    @staticmethod
    def ShowMsgEx(owner, text):
        msgTick = MsgLabel.ShowMsgTick.get(owner.__class__.__name__, 0)
        CurTick = int(time.time())
        if msgTick >= CurTick:
            return
        data = MsgLabel(owner)
        data.setText(text)
        data.setStyleSheet("color:black")
        data.show()
        MsgLabel.ShowMsgTick[owner.__class__.__name__] = CurTick

    def ShowError(self, text):
        self.stop()
        self.setText(text)
        self.setStyleSheet("color:red")
        self.show()

    @staticmethod
    def ShowErrorEx(owner, text):
        msgTick = MsgLabel.ShowMsgTick.get(owner.__class__.__name__, 0)
        CurTick = int(time.time())
        if msgTick >= CurTick:
            return
        data = MsgLabel(owner)
        data.setText(text)
        data.setStyleSheet("color:red")
        data.show()
        MsgLabel.ShowMsgTick[owner.__class__.__name__] = CurTick

    @staticmethod
    def OpenPicture(self, path="."):
        try:
            filename = QFileDialog.getOpenFileName(self, "Open Image", path, "Image Files(*.jpg *.png)")
            if filename and len(filename) > 1:
                name = filename[0]
                picFormat = filename[1]
                baseName = os.path.basename(name)
                if baseName[-3:] == "png":
                    picFormat = "png"
                elif baseName[-3:] == "jpg":
                    picFormat = "jpeg"
                elif baseName[-3:] == "gif":
                    picFormat = "gif"
                else:
                    return None, None, None

                if os.path.isfile(name):
                    self.cachePath = os.path.dirname(name)

                    f = open(name, "rb")
                    data = f.read()
                    f.close()
                    return data, name, picFormat
                return None, None, None
        except Exception as ex:
            Log.Error(ex)
            return None, None, None
