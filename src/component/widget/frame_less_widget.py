# coding:utf-8
import sys
from enum import Enum

from PySide6 import QtGui
from PySide6.QtCore import Qt, QPointF, QRect
from PySide6.QtWidgets import QWidget


class MoveEnum(Enum):
    LEFT_TOP = 11
    TOP = 12
    RIGHT_TOP = 13
    LEFT = 21
    CENTER = 22
    RIGHT = 23
    LEFT_BOTTOM = 31
    BOTTOM = 32
    RIGHT_BOTTOM = 33


class FrameLessWidget(QWidget):
    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        self.resize(500, 500)
        self.m_nBorder = 40
        # self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.m_bPress = False
        self.m_area = 0
        self.m_currentPos = 0
        plat = sys.platform
        self.isWin = False
        # self.setMouseTracking(True)

    def moveArea(self, pos: QPointF):
        if pos.y() < self.m_nBorder:
            k = 10
        elif pos.y() > self.height() - self.m_nBorder:
            k = 30
        else:
            k = 20

        if pos.x() < self.m_nBorder:
            v = 1
        elif pos.x() > self.width() - self.m_nBorder:
            v = 3
        else:
            v = 2

        return k + v

    def setMouseStyle(self, moveArea):
        if moveArea == MoveEnum.LEFT_TOP.value:
            self.setCursor(Qt.SizeFDiagCursor)
        elif moveArea == MoveEnum.TOP.value:
            self.setCursor(Qt.ArrowCursor)
        elif moveArea == MoveEnum.RIGHT_TOP.value:
            self.setCursor(Qt.SizeBDiagCursor)
        elif moveArea == MoveEnum.LEFT.value:
            self.setCursor(Qt.SizeHorCursor)
        elif moveArea == MoveEnum.CENTER.value:
            self.setCursor(Qt.ArrowCursor)
        elif moveArea == MoveEnum.RIGHT.value:
            self.setCursor(Qt.SizeHorCursor)
        elif moveArea == MoveEnum.LEFT_BOTTOM.value:
            self.setCursor(Qt.SizeBDiagCursor)
        elif moveArea == MoveEnum.BOTTOM.value:
            self.setCursor(Qt.SizeVerCursor)
        elif moveArea == MoveEnum.RIGHT_BOTTOM.value:
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        # print(event.globalPos())
        if self.isWin:
            return QWidget.mousePressEvent(self, event)
        area = self.moveArea(event.pos())
        self.setMouseStyle(area)
        if self.m_bPress:
            tempPos = event.globalPos() - self.m_currentPos

            if self.m_area == MoveEnum.TOP.value:
                self.move(self.pos() + tempPos)
                self.m_currentPos = event.globalPos()
            else:
                tl = self.mapToGlobal(self.rect().topLeft())
                rb = self.mapToGlobal(self.rect().bottomRight())
                gloPoint = event.globalPos()
                rMove = QRect(tl, rb)
                if self.m_area == MoveEnum.LEFT_TOP.value:
                    if rb.x() - gloPoint.x() <= self.minimumWidth():
                        rMove.setX(tl.x())
                    else:
                        rMove.setX(gloPoint.x())
                    if rb.y() - gloPoint.y() <= self.minimumHeight():
                        rMove.setY(tl.y())
                    else:
                        rMove.setY(gloPoint.y())
                elif self.m_area == MoveEnum.RIGHT_TOP.value:
                    rMove.setWidth(gloPoint.x()-tl.x())
                    rMove.setY(gloPoint.y())
                elif self.m_area == MoveEnum.LEFT.value:
                    if rb.x() - gloPoint.x() <= self.minimumWidth():
                        rMove.setX(tl.x())
                    else:
                        rMove.setX(gloPoint.x())
                elif self.m_area == MoveEnum.RIGHT.value:
                    rMove.setWidth(gloPoint.x()-tl.x())
                elif self.m_area == MoveEnum.LEFT_BOTTOM.value:
                    rMove.setX(gloPoint.x())
                    rMove.setHeight(gloPoint.y()-tl.y())
                elif self.m_area == MoveEnum.BOTTOM.value:
                    rMove.setHeight(gloPoint.y()-tl.y())
                elif self.m_area == MoveEnum.RIGHT_BOTTOM.value:
                    rMove.setWidth(gloPoint.x()-tl.x())
                    rMove.setHeight(gloPoint.y()-tl.y())
                self.setGeometry(rMove)
            event.accept()

    def mousePressEvent(self, event):
        if self.isWin:
            return QWidget.mousePressEvent(self, event)
        area = self.moveArea(event.pos())
        self.setMouseStyle(area)
        if event.buttons() == Qt.LeftButton:
            self.m_bPress = True
            self.m_area = area
            self.m_currentPos = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.isWin:
            return QWidget.mouseReleaseEvent(self, event)
        self.m_bPress = False
        self.setCursor(Qt.ArrowCursor)
