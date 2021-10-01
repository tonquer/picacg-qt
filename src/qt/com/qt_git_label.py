from PySide6.QtCore import QByteArray, QBuffer
from PySide6.QtGui import QMovie, Qt
from PySide6.QtWidgets import QLabel


class QtGifLabel(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.movie = QMovie()
        self.byteArray = None
        self.bBuffer = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def Init(self, data):

        self.byteArray = QByteArray(data)
        self.bBuffer = QBuffer(self.byteArray)
        self.movie.setFormat(QByteArray(b"GIF"))
        self.movie.setCacheMode(QMovie.CacheNone)
        self.movie.setDevice(self.bBuffer)
        # self.movie.setSpeed(100)
        self.setMovie(self.movie)
        self.movie.start()
        self.setScaledContents(True)
        self.resize(500, 500)
