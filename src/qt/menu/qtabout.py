import weakref

from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from conf import config
from ui.about import Ui_AboutForm


class QtAbout(QtWidgets.QWidget, Ui_AboutForm):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        Ui_AboutForm.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("关于")
        self.owner = weakref.ref(owner)
        self.label.setText("哔咔漫画{}".format(config.UpdateVersion))
        self.label_3.linkActivated.connect(self.OpenUrl)

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl(config.UpdateUrl))
