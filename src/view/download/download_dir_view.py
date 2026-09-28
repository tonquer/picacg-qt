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
        self.openMemBox.setChecked(bool(Setting.IsOpenMemCache.value))
        self.openDiskBox.setChecked(bool(Setting.IsOpenDiskCache.value))
        self.memBox.setValue(Setting.MemCacheSize.value)
        self.diskBox.setValue(Setting.DiskCacheSize.value)
        self.diskDayBox.setValue(Setting.DiskCacheDay.value)
        if Setting.SavePath.value:
            self.lineEdit.setText(Setting.SavePath.value)
            self.downloadDir.setText(os.path.join(Setting.SavePath.value, config.SavePathDir))
            self.chatDir.setText(os.path.join(Setting.GetCachePath(), config.ChatSavePath))
            self.cacheDir.setText(Setting.GetCachePath())
            self.waifu2xDir.setText(os.path.join(Setting.GetCachePath(), config.Waifu2xPath))

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            self.lineEdit.setText(url)
            self.downloadDir.setText(os.path.join(url, config.SavePathDir))
            self.chatDir.setText(os.path.join(Setting.GetCachePath(), config.ChatSavePath))
            self.cacheDir.setText(Setting.GetCachePath())
            self.waifu2xDir.setText(os.path.join(Setting.GetCachePath(), config.Waifu2xPath))

    def SavePath(self):
        path = self.lineEdit.text()
        if not path:
            QtOwner().ShowMsg(Str.GetStr(Str.SetDir))
            return
        Setting.SavePath.SetValue(path)
        Setting.IsOpenMemCache.SetValue(int(self.openMemBox.isChecked()))
        Setting.IsOpenDiskCache.SetValue(int(self.openDiskBox.isChecked()))
        Setting.MemCacheSize.SetValue(self.memBox.value())
        Setting.DiskCacheSize.SetValue(self.diskBox.value())
        Setting.DiskCacheDay.SetValue(self.diskDayBox.value())
        Setting.IsInitSave.SetValue(1)
        self.close()
