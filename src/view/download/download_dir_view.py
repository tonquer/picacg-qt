import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog

from component.dialog.base_mask_dialog import BaseMaskDialog
from config import config
from config.setting import Setting
from interface.ui_download_dir import Ui_DownloadDir
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.str import Str


class DownloadDirView(BaseMaskDialog, Ui_DownloadDir, QtTaskBase):

    def __init__(self, parent=None):
        BaseMaskDialog.__init__(self, parent)
        Ui_DownloadDir.__init__(self)
        QtTaskBase.__init__(self)
        self.widget.adjustSize()
        self.setupUi(self.widget)
        self.selectDir.clicked.connect(self.SelectSavePath)
        self.saveDir.clicked.connect(self.SavePath)

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            self.lineEdit.setText(url)
            self.downloadDir.setText(os.path.join(url, config.SavePathDir))
            self.chatDir.setText(os.path.join(url, config.ChatSavePath))
            self.cacheDir.setText(os.path.join(url, config.CachePathDir))
            self.waifu2xDir.setText(os.path.join(os.path.join(url, config.CachePathDir), config.Waifu2xPath))

    def SavePath(self):
        path = self.lineEdit.text()
        if not path:
            QtOwner().ShowMsg(Str.GetStr(Str.SetDir))
            return
        Setting.SavePath.SetValue(path)
        self.close()
