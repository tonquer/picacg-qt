import os
import sys

from PySide6.QtCore import Qt

from config.setting import Setting
from tools.log import Log

MainType = 1

Main = None

if  Setting.IsUseTitleBar.value:
    try:
        from interface.ui_main_windows import Ui_MainWindows
        # from .windows.frame_less_widget import FrameLessWidget
        from .qframelesswindow import FramelessMainWindow

        class MainWidget(FramelessMainWindow, Ui_MainWindows):
            def __init__(self):
                FramelessMainWindow.__init__(self)
                Ui_MainWindows.__init__(self)
                self.setupUi(self)
                self.setTitleBar(self.widget)
                self.totalStackWidget.setAttribute(Qt.WA_TranslucentBackground)
                self.widget.setAttribute(Qt.WA_TranslucentBackground)

            def showFullScreen(self):
                self.widget.setVisible(False)
                self.verticalLayout.setContentsMargins(0, 0, 0, 0)
                return FramelessMainWindow.showFullScreen(self)

            def showNormal(self):
                self.widget.setVisible(True)
                self.verticalLayout.setContentsMargins(3, 3, 3, 3)
                return FramelessMainWindow.showNormal(self)

            def showMaximized(self):
                self.widget.setVisible(True)
                self.verticalLayout.setContentsMargins(3, 3, 3, 3)
                return FramelessMainWindow.showMaximized(self)

            def setSubTitle(self, text):
                self.widget.subTitle.setText(text)
                return

            def hide(self):
                self.widget.hide()
                return super(MainWidget, self).hide()

            def show(self):
                self.widget.show()
                return super(MainWidget, self).show()

        Main = MainWidget
        MainType = 2
    except Exception as es:
        Log.Error(es)

if not Main:
    from interface.ui_main import Ui_Main
    from PySide6.QtWidgets import QMainWindow

    class MainWidget(QMainWindow, Ui_Main):
        def __init__(self):
            QMainWindow.__init__(self)
            Ui_Main.__init__(self)
            self.setupUi(self)

        def setSubTitle(self, text):
            return

    Main = MainWidget
