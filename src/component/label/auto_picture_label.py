from PySide6.QtCore import QByteArray, QBuffer, Qt, QSize
from PySide6.QtGui import QMovie, QPixmap
from PySide6.QtWidgets import QLabel

from tools.tool import ToolUtil


class AutoPictureLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.movie = None
        self.byteArray = None
        self.bBuffer = None
        self.gifWidth = 0
        self.gifHeight = 0

    def realW(self):
        return self.pixmap().width() / max(1, self.pixmap().devicePixelRatioF())

    def realH(self):
        return self.pixmap().height() / max(1, self.pixmap().devicePixelRatioF())

    # def setPixmap(self, data):
    #     if self.movie:
    #         self.movie.stop()
    #         self.widget().setMovie(None)
    #         self.movie.setDevice(None)
    #         self.movie = None
    #         self.bBuffer = None
    #         self.byteArray = None
    #     self.widget().setText("")
    #     widget = data.width() // max(1, data.devicePixelRatioF())
    #     height = data.height()//max(1, data.devicePixelRatioF())
    #     self.widget().setFixedWidth(widget)
    #     self.widget().setFixedHeight(height)
    #     # self.widget().setStyleSheet("border:2px solid rgb(177,177,177);")
    #     return self.widget().setPixmap(data)

    def paintEvent(self, ev):
        # print("paint")
        if self.movie and self.movie.state() == QMovie.NotRunning:
            self.movie.start()
        # if self.movie and self.movie.state == QMovie.Running:
        #     bound = self.boundingRect().adjused(10, 10, -5, -5)
        #     p.drawImage(bound, self.movie.currentImage)
        return QLabel.paintEvent(self, ev)

    def SetGifData(self, data, width, height):
        if self.movie:
            self.movie.stop()
            self.setMovie(None)
            self.movie.setDevice(None)
        animationFormat = ToolUtil.GetAnimationFormat(data)
        if animationFormat:
            self.movie = QMovie()
            self.gifWidth = width
            self.gifHeight = height
            self.setFixedWidth(width)
            self.setFixedHeight(height)
            self.byteArray = QByteArray(data)
            self.bBuffer = QBuffer(self.byteArray)
            # self.movie.frameChanged.connect(self.FrameChange)
            self.movie.setFormat(QByteArray(animationFormat.encode("utf-8")))
            self.movie.setCacheMode(QMovie.CacheMode.CacheAll)
            self.movie.setDevice(self.bBuffer)
            self.movie.setScaledSize(QSize(self.width(), self.height()))
            self.setMovie(self.movie)
            self.setScaledContents(True)
        else:
            pic = QPixmap()
            pic.loadFromData(data)
            radio = self.devicePixelRatio()
            pic.setDevicePixelRatio(radio)
            newPic = pic.scaled(width*radio, height*radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(newPic)
            self.setScaledContents(True)
            widget = data.width() // max(1, data.devicePixelRatioF())
            height = data.height()//max(1, data.devicePixelRatioF())
            self.setFixedWidth(widget)
            self.setFixedHeight(height)

    # def FrameChange(self):
    #     currentPixmap = self.movie.currentPixmap()
    #     size = currentPixmap.size()
    #     radioF = self.widget().devicePixelRatioF()
    #     currentPixmap.setDevicePixelRatio(radioF)
    #     newData = currentPixmap.scaled(self.gifWidth * radioF, self.gifHeight * radioF, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #     self.widget().setPixmap(newData)
    #     return