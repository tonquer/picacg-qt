# coding:utf-8
from ctypes import POINTER, Structure, c_int
from ctypes.wintypes import DWORD, HWND, ULONG, POINT, RECT, UINT, BOOL, HRGN
from enum import Enum


class WINDOWCOMPOSITIONATTRIB(Enum):
    WCA_UNDEFINED = 0
    WCA_NCRENDERING_ENABLED = 1
    WCA_NCRENDERING_POLICY = 2
    WCA_TRANSITIONS_FORCEDISABLED = 3
    WCA_ALLOW_NCPAINT = 4
    WCA_CAPTION_BUTTON_BOUNDS = 5
    WCA_NONCLIENT_RTL_LAYOUT = 6
    WCA_FORCE_ICONIC_REPRESENTATION = 7
    WCA_EXTENDED_FRAME_BOUNDS = 8
    WCA_HAS_ICONIC_BITMAP = 9
    WCA_THEME_ATTRIBUTES = 10
    WCA_NCRENDERING_EXILED = 11
    WCA_NCADORNMENTINFO = 12
    WCA_EXCLUDED_FROM_LIVEPREVIEW = 13
    WCA_VIDEO_OVERLAY_ACTIVE = 14
    WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15
    WCA_DISALLOW_PEEK = 16
    WCA_CLOAK = 17
    WCA_CLOAKED = 18
    WCA_ACCENT_POLICY = 19
    WCA_FREEZE_REPRESENTATION = 20
    WCA_EVER_UNCLOAKED = 21
    WCA_VISUAL_OWNER = 22
    WCA_HOLOGRAPHIC = 23
    WCA_EXCLUDED_FROM_DDA = 24
    WCA_PASSIVEUPDATEMODE = 25
    WCA_USEDARKMODECOLORS = 26
    WCA_CORNER_STYLE = 27
    WCA_PART_COLOR = 28
    WCA_DISABLE_MOVESIZE_FEEDBACK = 29
    WCA_LAST = 30


class ACCENT_STATE(Enum):
    """ Client area status enumeration class """
    ACCENT_DISABLED = 0
    ACCENT_ENABLE_GRADIENT = 1
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
    ACCENT_ENABLE_BLURBEHIND = 3           # Aero effect
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4    # Acrylic effect
    ACCENT_ENABLE_HOSTBACKDROP = 5         # Mica effect
    ACCENT_INVALID_STATE = 6


class ACCENT_POLICY(Structure):
    """ Specific attributes of client area """

    _fields_ = [
        ("AccentState",     DWORD),
        ("AccentFlags",     DWORD),
        ("GradientColor",   DWORD),
        ("AnimationId",     DWORD),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ("Attribute",   DWORD),
        # Pointer() receives any ctypes type and returns a pointer type
        ("Data",        POINTER(ACCENT_POLICY)),
        ("SizeOfData",  ULONG),
    ]


class DWMNCRENDERINGPOLICY(Enum):
    DWMNCRP_USEWINDOWSTYLE = 0
    DWMNCRP_DISABLED = 1
    DWMNCRP_ENABLED = 2
    DWMNCRP_LAS = 3


class DWMWINDOWATTRIBUTE(Enum):
    DWMWA_NCRENDERING_ENABLED = 1
    DWMWA_NCRENDERING_POLICY = 2
    DWMWA_TRANSITIONS_FORCEDISABLED = 3
    DWMWA_ALLOW_NCPAINT = 4
    DWMWA_CAPTION_BUTTON_BOUNDS = 5
    DWMWA_NONCLIENT_RTL_LAYOUT = 6
    DWMWA_FORCE_ICONIC_REPRESENTATION = 7
    DWMWA_FLIP3D_POLICY = 8
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    DWMWA_HAS_ICONIC_BITMAP = 10
    DWMWA_DISALLOW_PEEK = 11
    DWMWA_EXCLUDED_FROM_PEEK = 12
    DWMWA_CLOAK = 13
    DWMWA_CLOAKED = 14
    DWMWA_FREEZE_REPRESENTATION = 15
    DWMWA_PASSIVE_UPDATE_MODE = 16
    DWMWA_USE_HOSTBACKDROPBRUSH = 17
    DWMWA_USE_IMMERSIVE_DARK_MODE = 18
    DWMWA_WINDOW_CORNER_PREFERENCE = 19
    DWMWA_BORDER_COLOR = 20
    DWMWA_CAPTION_COLOR = 21
    DWMWA_TEXT_COLOR = 22
    DWMWA_VISIBLE_FRAME_BORDER_THICKNESS = 23
    DWMWA_LAST = 24


class MARGINS(Structure):
    _fields_ = [
        ("cxLeftWidth",     c_int),
        ("cxRightWidth",    c_int),
        ("cyTopHeight",     c_int),
        ("cyBottomHeight",  c_int),
    ]


class MINMAXINFO(Structure):
    _fields_ = [
        ("ptReserved",      POINT),
        ("ptMaxSize",       POINT),
        ("ptMaxPosition",   POINT),
        ("ptMinTrackSize",  POINT),
        ("ptMaxTrackSize",  POINT),
    ]


class PWINDOWPOS(Structure):
    _fields_ = [
        ('hWnd',            HWND),
        ('hwndInsertAfter', HWND),
        ('x',               c_int),
        ('y',               c_int),
        ('cx',              c_int),
        ('cy',              c_int),
        ('flags',           UINT)
    ]


class NCCALCSIZE_PARAMS(Structure):
    _fields_ = [
        ('rgrc', RECT*3),
        ('lppos', POINTER(PWINDOWPOS))
    ]


LPNCCALCSIZE_PARAMS = POINTER(NCCALCSIZE_PARAMS)


class DWM_BLURBEHIND(Structure):
    _fields_ = [
        ('dwFlags',                DWORD),
        ('fEnable',                BOOL),
        ('hRgnBlur',               HRGN),
        ('fTransitionOnMaximized', BOOL),
    ]
