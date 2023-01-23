from PySide6.QtCore import QByteArray, QBuffer
from PySide6.QtGui import QMovie, Qt, QPixmap
from PySide6.QtWidgets import QLabel


class GifLabel(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.movie = QMovie()
        self.byteArray = None
        self.bBuffer = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # self.movie.frameChanged.connect(self.FrameChange)

    # def FrameChange(self):
    #     currentPixmap = self.movie.currentPixmap()
    #     size = currentPixmap.size()
    #     radioF = self.devicePixelRatioF()
    #     pixmap = QPixmap()
    #     pixmap.setDevicePixelRatio(radioF)
    #     self.setPixmap(pixmap)
    #     return

    def Show(self):
        self.move(self.parent().width()//2-self.width()//2, self.parent().height()//2-self.height()//2)
        return self.show()

    def Init(self, data, size=124):
        self.resize(size, size)
        self.byteArray = QByteArray(data)
        self.bBuffer = QBuffer(self.byteArray)

        # self.movie.setFormat(QByteArray(b"GIF"))

        self.movie.setCacheMode(QMovie.CacheNone)
        self.movie.setDevice(self.bBuffer)
        # self.movie.setSpeed(100)
        self.setMovie(self.movie)

        self.movie.start()
        self.setScaledContents(True)

    def InitByFileName(self, name):
        self.resize(300, 300)
        self.movie = QMovie(name)
        # self.movie.setFileName(name)
        self.movie.setFormat(QByteArray(b"GIF"))
        self.movie.start()
        return
