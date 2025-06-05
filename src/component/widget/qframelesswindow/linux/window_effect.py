# coding:utf-8

class LinuxWindowEffect:
    """ Linux window effect """

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
        pass

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
        pass

    def setAeroEffect(self, hWnd):
        """ add Aero effect to the window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

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
        pass

    def addMenuShadowEffect(self, hWnd):
        """ add shadow to menu

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    @staticmethod
    def removeMenuShadowEffect(hWnd):
        """ Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    def removeShadowEffect(self, hWnd):
        """ Remove shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

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