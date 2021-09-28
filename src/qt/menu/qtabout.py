from PySide2 import QtWidgets
from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices

from conf import config
from ui.about import Ui_AboutForm, Qt
from src.util import ToolUtil


class QtAbout(QtWidgets.QWidget, Ui_AboutForm):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_AboutForm.__init__(self)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        ToolUtil.SetIcon(self)  # set window icon
        if config.Language == 'English':
            self.label.setText("picacg-windows {}".format(config.UpdateVersion))
        # elif config.Language == 'Chinese':
        else:
            self.label.setText("哔咔漫画 {}".format(config.UpdateVersion))

        self.label_3.linkActivated.connect(self.OpenUrl)
        self.label_8.linkActivated.connect(self.OpenUrl2)
        self.label_10.linkActivated.connect(self.OpenUrl3)

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl(config.UpdateUrl))

    def OpenUrl2(self):
        QDesktopServices.openUrl(QUrl("https://github.com/tonquer/waifu2x-ncnn-vulkan-python"))

    def OpenUrl3(self):
        QDesktopServices.openUrl(QUrl("https://github.com/tonquer/ehentai-windows"))