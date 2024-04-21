from PySide6.QtOpenGLWidgets import QOpenGLWidget


class ReadOpenGL(QOpenGLWidget):
    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)

    def paintGL(self) -> None:
        print("paintGL")
        return QOpenGLWidget.paintGL(self)

    def paintEngine(self) :
        print("paintEngine")
        return QOpenGLWidget.paintEngine(self)

    def paintEvent(self, e) -> None:
        print("paintEvent, e:{}".format(e))
        return QOpenGLWidget.paintEvent(self, e)

    def repaint(self) -> None:
        print("repaint")
        return QOpenGLWidget.repaint(self)

    def resize(self, arg__1) -> None:
        print("resize")
        return QOpenGLWidget.resize(self, arg__1)

    def resizeGL(self, w:int, h:int) -> None:
        print("resizeGL")
        return QOpenGLWidget.resizeGL(self, w, h)

    def resizeEvent(self, e) -> None:
        print("resizeEvent")
        return QOpenGLWidget.resizeEvent(self, e)

    def initializeGL(self) -> None:
        print("initializeGL")
        return QOpenGLWidget.initializeGL(self)