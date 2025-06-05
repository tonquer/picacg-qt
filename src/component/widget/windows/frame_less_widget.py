# coding:utf-8
import sys
from enum import Enum
from PySide6.QtCore import Qt, QRect, QPointF, QEvent

from ctypes import cast
from ctypes.wintypes import MSG

from ctypes import POINTER

from PySide6.QtGui import QPainter, QBrush, QColor, QPainterPath, QMouseEvent
from PySide6.QtWidgets import QWidget, QStyleOption, QStyle
from win32 import win32api, win32gui
from win32.lib import win32con

from config.setting import Setting
from .window_effect import WindowEffect
from .c_structures import MINMAXINFO, NCCALCSIZE_PARAMS
from ..com_widget import ComWidget, MoveEnum


class FrameLessWidget(QWidget):
    BORDER_WIDTH = 10

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(500, 500)
        self.m_nBorder = FrameLessWidget.BORDER_WIDTH
        # self.setMouseTracking(True)
        self.m_bPress = False
        self.setAttribute(Qt.WA_Hover, True)
        self.m_area = 0
        self.m_currentPos = 0
        self.isWin = False
        self.__monitorInfo = None
        self.windowEffect = WindowEffect()
        self.windowEffect.addWindowAnimation(self.winId())

        # 修复多屏不同 dpi 的显示问题
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)
        # self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.installEventFilter(self)
        # self.setMouseTracking(True)

    def eventFilter(self, obj, e):
        if not self.m_bPress:
            if e.type() == QEvent.HoverEnter or e.type() == QEvent.HoverLeave or e.type() == QEvent.HoverMove:
                self.mouseMoveEvent(e)
        return QWidget.eventFilter(self, obj, e)

    def paintEvent(self, event):
        if self.window().isFullScreen():
            return
        QWidget.paintEvent(self, event)
        painter = QPainter(self)
        painter.setPen(Qt.transparent)
        if Setting.ThemeIndex.autoValue == 2:
            painter.setBrush(QBrush(QColor(243, 243, 243)))
        else:
            painter.setBrush(QBrush(QColor(49, 54, 59)))
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        rect = self.rect()
        rect.setWidth(rect.width()-1)
        rect.setHeight(rect.height()-1)
        painter.drawRoundedRect(rect, 10, 10)
        # painterPath = QPainterPath()
        # painterPath.addRoundedRect(rect, 15, 15)
        # painter.drawPath(painterPath)

    # def paintEvent(self, event):
    #     # 解决QSS问题
    #     option = QStyleOption()
    #     option.initFrom(self)
    #     painter = QPainter(self)
    #     self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
    #     QWidget.paintEvent(self, event)

    def nativeEvent(self, eventType, message):
        if eventType == "windows_generic_MSG":
            """ 处理windows消息 """
            msg = MSG.from_address(message.__int__())
            # print(msg.message)
            # if msg.message == win32con.WM_NCHITTEST:
            #     # 解决多屏下会出现鼠标一直为拖动状态的问题
            #     x = win32api.LOWORD(msg.lParam)
            #     y = win32api.HIWORD(msg.lParam)
            #
            #     radio = self.devicePixelRatioF()
            #
            #     seekX = self.screen().geometry().left()
            #     if self.frameGeometry().x() > seekX:
            #         seekX = seekX + (self.frameGeometry().x() - seekX)*radio
            #     else:
            #         seekX = self.frameGeometry().x() * radio
            #
            #     xPos = (x - seekX) % 65536
            #     yPos = y - self.frameGeometry().y()*radio
            #     # print(self.frameGeometry().x(), self.frameGeometry().width(), seekX, x, xPos)
            #     w, h = self.width()*radio, self.height()*radio
            #     lx = xPos < self.BORDER_WIDTH
            #     rx = xPos + 9 > w - self.BORDER_WIDTH
            #     ty = yPos < self.BORDER_WIDTH
            #     by = yPos > h - self.BORDER_WIDTH
                # if lx and ty:
                #     return True, win32con.HTTOPLEFT
                # elif rx and by:
                #     return True, win32con.HTBOTTOMRIGHT
                # elif rx and ty:
                #     return True, win32con.HTTOPRIGHT
                # elif lx and by:
                #     return True, win32con.HTBOTTOMLEFT
                # elif ty:
                #     return True, win32con.HTTOP
                # elif by:
                #     return True, win32con.HTBOTTOM
                # elif lx:
                #     return True, win32con.HTLEFT
                # elif rx:
                #     return True, win32con.HTRIGHT
            if msg.message == win32con.WM_NCCALCSIZE:
                if self._isWindowMaximized(msg.hWnd):
                    self.__monitorNCCALCSIZE(msg)
                return True, 0
            elif msg.message == win32con.WM_GETMINMAXINFO:
                if self._isWindowMaximized(msg.hWnd):
                    window_rect = win32gui.GetWindowRect(msg.hWnd)
                    if not window_rect:
                        return False, 0
                    # 获取显示器句柄
                    monitor = win32api.MonitorFromRect(window_rect)
                    if not monitor:
                        return False, 0
                    # 获取显示器信息
                    __monitorInfo = win32api.GetMonitorInfo(monitor)
                    monitor_rect = __monitorInfo['Monitor']
                    work_area = __monitorInfo['Work']
                    # 将lParam转换为MINMAXINFO指针
                    info = cast(msg.lParam, POINTER(MINMAXINFO)).contents
                    # 调整窗口大小
                    info.ptMaxSize.x = work_area[2] - work_area[0]
                    info.ptMaxSize.y = work_area[3] - work_area[1]
                    info.ptMaxTrackSize.x = info.ptMaxSize.x
                    info.ptMaxTrackSize.y = info.ptMaxSize.y
                    # 修改左上角坐标
                    info.ptMaxPosition.x = abs(window_rect[0] - monitor_rect[0])
                    info.ptMaxPosition.y = abs(window_rect[1] - monitor_rect[1])
                    return True, 1
        return QWidget.nativeEvent(self, eventType, message)

    def _isWindowMaximized(self, hWnd) -> bool:
        """ 判断窗口是否最大化 """
        # 返回指定窗口的显示状态以及被恢复的、最大化的和最小化的窗口位置，返回值为元组
        windowPlacement = win32gui.GetWindowPlacement(hWnd)
        if not windowPlacement:
            return False
        return windowPlacement[1] == win32con.SW_MAXIMIZE

    def __monitorNCCALCSIZE(self, msg: MSG):
        """ 调整窗口大小 """
        monitor = win32api.MonitorFromWindow(msg.hWnd)
        # 如果没有保存显示器信息就直接返回，否则接着调整窗口大小
        if monitor is None and not self.__monitorInfo:
            return
        elif monitor is not None:
            self.__monitorInfo = win32api.GetMonitorInfo(monitor)
        # 调整窗口大小
        params = cast(msg.lParam, POINTER(NCCALCSIZE_PARAMS)).contents
        # params.rgrc[0].left = self.__monitorInfo['Work'][0]
        # params.rgrc[0].top = self.__monitorInfo['Work'][1]
        # params.rgrc[0].right = self.__monitorInfo['Work'][2]
        # params.rgrc[0].bottom = self.__monitorInfo['Work'][3]

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

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
        area = ComWidget.moveArea(self.width(), self.height(), event.pos())
        self.setMouseStyle(area)
        if self.m_bPress:
            # tempPos = event.globalPos() - self.m_currentPos

            if self.m_area == MoveEnum.TOP.value:
                return
                # self.move(self.pos() + tempPos)
                # self.m_currentPos = event.globalPos()
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
                # print(rMove)
                self.setGeometry(rMove)
            # event.accept()

    def mousePressEvent(self, event):
        if self.isWin:
            return QWidget.mousePressEvent(self, event)
        area = self.moveArea(event.pos())
        self.setMouseStyle(area)
        if event.buttons() == Qt.LeftButton:
            self.m_bPress = True
            self.m_area = area
            self.m_currentPos = event.globalPos()
            # event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.isWin:
            return QWidget.mouseReleaseEvent(self, event)
        self.m_bPress = False
        self.setCursor(Qt.ArrowCursor)

