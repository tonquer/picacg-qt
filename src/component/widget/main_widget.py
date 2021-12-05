import os
import sys


from tools.log import Log

MainType = 1

Main = None

# if sys.platform == "win32":
#     try:
#         from interface.ui_main_windows import Ui_MainWindows
#         from .windows.frame_less_widget import FrameLessWidget
#
#         class MainWidget(FrameLessWidget, Ui_MainWindows):
#             def __init__(self):
#                 FrameLessWidget.__init__(self)
#                 Ui_MainWindows.__init__(self)
#                 self.setupUi(self)
#         Main = MainWidget
#     except Exception as es:
#         Log.Error(es)

if not Main:
    from interface.ui_main import Ui_Main
    from PySide6.QtWidgets import QMainWindow

    class MainWidget(QMainWindow, Ui_Main):
        def __init__(self):
            QMainWindow.__init__(self)
            Ui_Main.__init__(self)
            self.setupUi(self)


    Main = MainWidget
