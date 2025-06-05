# coding:utf-8

from ctypes import POINTER, WinDLL, byref, c_bool, c_int, pointer, sizeof
from ctypes.wintypes import DWORD, LONG, LPCVOID

from win32 import win32api, win32gui
from win32.lib import win32con

from .c_structures import (ACCENT_POLICY, ACCENT_STATE, DWMNCRENDERINGPOLICY,
                           DWMWINDOWATTRIBUTE, MARGINS,
                           WINDOWCOMPOSITIONATTRIB,
                           WINDOWCOMPOSITIONATTRIBDATA)


class WindowEffect:
    """ 调用windows api实现窗口效果 """

    def __init__(self):
        # 调用api
        self.user32 = WinDLL("user32")
        self.dwmapi = WinDLL("dwmapi")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmSetWindowAttribute = self.dwmapi.DwmSetWindowAttribute
        self.SetWindowCompositionAttribute.restype = c_bool
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmSetWindowAttribute.restype = LONG
        self.SetWindowCompositionAttribute.argtypes = [
            c_int,
            POINTER(WINDOWCOMPOSITIONATTRIBDATA),
        ]
        self.DwmSetWindowAttribute.argtypes = [c_int, DWORD, LPCVOID, DWORD]
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]
        # 初始化结构体
        # self.accentPolicy = ACCENT_POLICY()
        # self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        # self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value[
        #     0
        # ]
        # self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        # self.winCompAttrData.Data = pointer(self.accentPolicy)

    @staticmethod
    def addWindowAnimation(hWnd):
        """ 打开窗口动画效果

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            窗口句柄
        """
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )
