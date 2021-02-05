from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, Qt, QSize
from PyQt5.QtWidgets import QFileDialog

from conf import config
from src.qt.qtbubblelabel import QtBubbleLabel
from ui.setting import Ui_Setting


class QtSetting(QtWidgets.QWidget, Ui_Setting):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        Ui_Setting.__init__(self)
        self.setupUi(self)
        self.settings = QSettings('config.ini', QSettings.IniFormat)
        self.setWindowModality(Qt.ApplicationModal)
        self.mainSize = QSize(1500, 1100)
        self.bookSize = QSize(900, 1020)
        self.userId = ""
        self.passwd = ""

    def show(self):
        self.LoadSetting()
        super(self.__class__, self).show()

    def LoadSetting(self):
        config.DownloadThreadNum = int(self.settings.value("DownloadThreadNum") or config.DownloadThreadNum)
        self.comboBox.setCurrentIndex(config.DownloadThreadNum-2)
        config.ImageQuality = self.settings.value("ImageQuality") or config.ImageQuality
        getattr(self, "quality_"+config.ImageQuality).setChecked(True)
        httpProxy = self.settings.value("Proxy/Http") or config.HttpProxy

        if httpProxy:
            config.HttpProxy = httpProxy
            self.httpEdit.setText(config.HttpProxy)

        config.SavePath = self.settings.value("SavePath") or config.SavePath
        self.saveEdit.setText(config.SavePath)

        x = self.settings.value("MainSize_x")
        y = self.settings.value("MainSize_y")
        if x and y:
            self.mainSize = QSize(int(x), int(y))
        x = self.settings.value("BookSize_x")
        y = self.settings.value("BookSize_y")
        if x and y:
            self.bookSize = QSize(int(x), int(y))

        self.userId = self.settings.value("UserId")
        self.passwd = self.settings.value("Passwd")
        return

    def ExitSaveSetting(self, mainQsize, bookQsize, userId, passwd):
        self.settings.setValue("MainSize_x", mainQsize.width())
        self.settings.setValue("MainSize_y", mainQsize.height())
        self.settings.setValue("BookSize_x", bookQsize.width())
        self.settings.setValue("BookSize_y", bookQsize.height())
        self.settings.setValue("UserId", userId)
        self.settings.setValue("Passwd", passwd)

    def SaveSetting(self):
        config.DownloadThreadNum = int(self.comboBox.currentText())
        config.ImageQuality = self.buttonGroup.checkedButton().objectName().replace("quality_", "")
        httpProxy = self.httpEdit.text()
        config.SavePath = self.saveEdit.text()

        self.settings.setValue("DownloadThreadNum", config.DownloadThreadNum)
        self.settings.setValue("ImageQuality", config.ImageQuality)
        config.HttpProxy = httpProxy
        self.settings.setValue("Proxy/Http", config.HttpProxy)

        self.settings.setValue("SavePath", config.SavePath)
        # QtWidgets.QMessageBox.information(self, '保存成功', "成功", QtWidgets.QMessageBox.Yes)
        QtBubbleLabel.ShowMsgEx(self, "保存成功")

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if url:
            self.saveEdit.setText(url)
