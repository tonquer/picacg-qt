# coding:utf-8
import objc
import Cocoa
from PySide6.QtWidgets import QMacCocoaViewContainer
from ..utils.mac_utils import getNSWindow

class MacWindowEffect:
    """ Mac OS window effect """

    def __init__(self, window):
        self.window = window

    def setAcrylicEffect(self, hWnd, gradientColor="F2F2F230", isEnableShadow=True, animationId=0):
        """ set acrylic effect for window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            window handle

        gradientColor: str
            hexadecimal acrylic mixed color, corresponding to RGBA components

        isEnableShadow: bool
            whether to enable window shadow

        animationId: int
            turn on blur animation or not
        """
        frame = Cocoa.NSMakeRect(
            0, 0, self.window.width(), self.window.height())
        visualEffectView = Cocoa.NSVisualEffectView.new()
        visualEffectView.setAutoresizingMask_(
            Cocoa.NSViewWidthSizable | Cocoa.NSViewHeightSizable)  # window resizable
        visualEffectView.setFrame_(frame)
        visualEffectView.setState_(Cocoa.NSVisualEffectStateActive)

        # https://developer.apple.com/documentation/appkit/nsvisualeffectmaterial
        visualEffectView.setMaterial_(Cocoa.NSVisualEffectMaterialPopover)
        visualEffectView.setBlendingMode_(
            Cocoa.NSVisualEffectBlendingModeBehindWindow)

        nsWindow = getNSWindow(self.window.winId())
        content = nsWindow.contentView()
        container = QMacCocoaViewContainer(0, self.window)
        content.addSubview_positioned_relativeTo_(
            visualEffectView, Cocoa.NSWindowBelow, container)

    def setMicaEffect(self, hWnd, isDarkMode=False, isAlt=False):
        """ Add mica effect to the window (Win11 only)

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        isDarkMode: bool
            whether to use dark mode mica effect

        isAlt: bool
            whether to use mica alt effect
        """
        self.setAcrylicEffect(hWnd)

    def setAeroEffect(self, hWnd):
        """ add Aero effect to the window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        self.setAcrylicEffect(hWnd)

    def setTransparentEffect(self, hWnd):
        """ set transparent effect for window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        pass

    def removeBackgroundEffect(self, hWnd):
        """ Remove background effect

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        pass

    def addShadowEffect(self, hWnd):
        """ add shadow to window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        getNSWindow(hWnd).setHasShadow_(True)

    def addMenuShadowEffect(self, hWnd):
        """ add shadow to menu

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        self.addShadowEffect(hWnd)

    @staticmethod
    def removeMenuShadowEffect(hWnd):
        """ Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        getNSWindow(hWnd).setHasShadow_(False)

    def removeShadowEffect(self, hWnd):
        """ Remove shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        getNSWindow(hWnd).setHasShadow_(False)

    @staticmethod
    def addWindowAnimation(hWnd):
        """ Enables the maximize and minimize animation of the window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """

    @staticmethod
    def disableMaximizeButton(hWnd):
        """ Disable the maximize button of window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """

    def enableBlurBehindWindow(self, hWnd):
        """ enable the blur effect behind the whole client
        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """