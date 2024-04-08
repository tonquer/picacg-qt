# coding:utf-8
from ctypes import Structure, byref, sizeof, windll, c_int
from ctypes.wintypes import DWORD, HWND, LPARAM, RECT, UINT
from platform import platform
import sys

import win32api
import win32con
import win32gui
import win32print
from PySide6.QtCore import QOperatingSystemVersion
from PySide6.QtGui import QGuiApplication
from win32comext.shell import shellcon


def isMaximized(hWnd):
    """ Determine whether the window is maximized

    Parameters
    ----------
    hWnd: int or `sip.voidptr`
        window handle
    """
    windowPlacement = win32gui.GetWindowPlacement(hWnd)
    if not windowPlacement:
        return False

    return windowPlacement[1] == win32con.SW_MAXIMIZE


def isFullScreen(hWnd):
    """ Determine whether the window is full screen

    Parameters
    ----------
    hWnd: int or `sip.voidptr`
        window handle
    """
    if not hWnd:
        return False

    hWnd = int(hWnd)
    winRect = win32gui.GetWindowRect(hWnd)
    if not winRect:
        return False

    monitorInfo = getMonitorInfo(hWnd, win32con.MONITOR_DEFAULTTOPRIMARY)
    if not monitorInfo:
        return False

    monitorRect = monitorInfo["Monitor"]
    return all(i == j for i, j in zip(winRect, monitorRect))


def isCompositionEnabled():
    """ detect if dwm composition is enabled """
    bResult = c_int(0)
    windll.dwmapi.DwmIsCompositionEnabled(byref(bResult))
    return bool(bResult.value)


def getMonitorInfo(hWnd, dwFlags):
    """ get monitor info, return `None` if failed

    Parameters
    ----------
    hWnd: int or `sip.voidptr`
        window handle

    dwFlags: int
        Determines the return value if the window does not intersect any display monitor
    """
    monitor = win32api.MonitorFromWindow(hWnd, dwFlags)
    if not monitor:
        return

    return win32api.GetMonitorInfo(monitor)


def getResizeBorderThickness(hWnd, horizontal=True):
    """ get resize border thickness of widget

    Parameters
    ----------
    hWnd: int or `sip.voidptr`
        window handle

    dpiScale: bool
        whether to use dpi scale
    """
    window = findWindow(hWnd)
    if not window:
        return 0

    frame = win32con.SM_CXSIZEFRAME if horizontal else win32con.SM_CYSIZEFRAME
    result = getSystemMetrics(hWnd, frame, horizontal) + getSystemMetrics(hWnd, 92, horizontal)

    if result > 0:
        return result

    thickness = 8 if isCompositionEnabled() else 4
    return round(thickness*window.devicePixelRatio())


def getSystemMetrics(hWnd, index, horizontal):
    """ get system metrics """
    if not hasattr(windll.user32, 'GetSystemMetricsForDpi'):
        return win32api.GetSystemMetrics(index)

    dpi = getDpiForWindow(hWnd, horizontal)
    return windll.user32.GetSystemMetricsForDpi(index, dpi)


def getDpiForWindow(hWnd, horizontal=True):
    """ get dpi for window

    Parameters
    ----------
    hWnd: int or `sip.voidptr`
        window handle

    dpiScale: bool
        whether to use dpi scale
    """
    if hasattr(windll.user32, 'GetDpiForWindow'):
        return windll.user32.GetDpiForWindow(hWnd)

    hdc = win32gui.GetDC(hWnd)
    if not hdc:
        return 96

    dpiX = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
    dpiY = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSY)
    win32gui.ReleaseDC(hWnd, hdc)
    if dpiX > 0 and horizontal:
        return dpiX
    elif dpiY > 0 and not horizontal:
        return dpiY

    return 96


def findWindow(hWnd):
    """ find window by hWnd, return `None` if not found

    Parameters
    ----------
    hWnd: int or `sip.voidptr`
        window handle
    """
    if not hWnd:
        return

    windows = QGuiApplication.topLevelWindows()
    if not windows:
        return

    hWnd = int(hWnd)
    for window in windows:
        if window and int(window.winId()) == hWnd:
            return window


def isGreaterEqualVersion(version):
    """ determine if the windows version ≥ the specifics version

    Parameters
    ----------
    version: QOperatingSystemVersion
        windows version
    """
    return QOperatingSystemVersion.current() >= version


def isGreaterEqualWin8_1():
    """ determine if the windows version ≥ Win8.1 """
    return isGreaterEqualVersion(QOperatingSystemVersion.Windows8_1)


def isGreaterEqualWin10():
    """ determine if the windows version ≥ Win10 """
    return isGreaterEqualVersion(QOperatingSystemVersion.Windows10)


def isGreaterEqualWin11():
    """ determine if the windows version ≥ Win10 """
    return isGreaterEqualVersion(QOperatingSystemVersion.Windows10) and sys.getwindowsversion().build >= 22000


def isWin7():
    """ determine if the windows version is Win7 """
    return "Windows-7" in platform()


class APPBARDATA(Structure):
    _fields_ = [
        ('cbSize',            DWORD),
        ('hWnd',              HWND),
        ('uCallbackMessage',  UINT),
        ('uEdge',             UINT),
        ('rc',                RECT),
        ('lParam',            LPARAM),
    ]


class Taskbar:

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4

    AUTO_HIDE_THICKNESS = 2

    @staticmethod
    def isAutoHide():
        """ detect whether the taskbar is hidden automatically """
        appbarData = APPBARDATA(sizeof(APPBARDATA), 0,
                                0, 0, RECT(0, 0, 0, 0), 0)
        taskbarState = windll.shell32.SHAppBarMessage(
            shellcon.ABM_GETSTATE, byref(appbarData))

        return taskbarState == shellcon.ABS_AUTOHIDE

    @classmethod
    def getPosition(cls, hWnd):
        """ get the position of auto-hide task bar

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            window handle
        """
        if isGreaterEqualWin8_1():
            monitorInfo = getMonitorInfo(
                hWnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not monitorInfo:
                return cls.NO_POSITION

            monitor = RECT(*monitorInfo['Monitor'])
            appbarData = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, monitor, 0)
            positions = [cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM]
            for position in positions:
                appbarData.uEdge = position
                if windll.shell32.SHAppBarMessage(11, byref(appbarData)):
                    return position

            return cls.NO_POSITION

        appbarData = APPBARDATA(sizeof(APPBARDATA), win32gui.FindWindow(
            "Shell_TrayWnd", None), 0, 0, RECT(0, 0, 0, 0), 0)
        if appbarData.hWnd:
            windowMonitor = win32api.MonitorFromWindow(
                hWnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not windowMonitor:
                return cls.NO_POSITION

            taskbarMonitor = win32api.MonitorFromWindow(
                appbarData.hWnd, win32con.MONITOR_DEFAULTTOPRIMARY)
            if not taskbarMonitor:
                return cls.NO_POSITION

            if taskbarMonitor == windowMonitor:
                windll.shell32.SHAppBarMessage(
                    shellcon.ABM_GETTASKBARPOS, byref(appbarData))
                return appbarData.uEdge

        return cls.NO_POSITION


class WindowsMoveResize:
    """ Tool class for moving and resizing Mac OS window """

    @staticmethod
    def startSystemMove(window, globalPos):
        """ resize window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event
        """
        win32gui.ReleaseCapture()
        win32api.SendMessage(
            int(window.winId()),
            win32con.WM_SYSCOMMAND,
            win32con.SC_MOVE | win32con.HTCAPTION,
            0
        )

    @classmethod
    def starSystemResize(cls, window, globalPos, edges):
        """ resize window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event

        edges: `Qt.Edges`
            window edges
        """
        pass
