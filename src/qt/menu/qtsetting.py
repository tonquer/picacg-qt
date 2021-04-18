from PySide2 import QtWidgets
from PySide2.QtCore import QSettings, Qt, QSize
from PySide2.QtWidgets import QFileDialog

from conf import config
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.util import Log
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
        self.readSize = QSize(1120, 1020)
        self.userId = ""
        self.passwd = ""
        self.gpuInfos = []

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

        ChatProxy = self.settings.value("ChatProxy")
        if ChatProxy is not None:
            config.ChatProxy = int(ChatProxy)
            self.checkBox_2.setChecked(bool(config.ChatProxy))

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

        x = self.settings.value("ImgRead_x")
        y = self.settings.value("ImgRead_y")
        if x and y:
            self.readSize = QSize(int(x), int(y))

        v = self.settings.value("Waifu2x/Encode")
        if v:
            config.Encode = int(v)

        v = self.settings.value("Waifu2x/LookModel")
        if v:
            config.LookModel = int(v)
        self.lookModel.setCurrentIndex(config.LookModel)

        v = self.settings.value("Waifu2x/DownloadModel")
        if v:
            config.DownloadModel = int(v)
        self.downloadModel.setCurrentIndex(config.DownloadModel)

        v = self.settings.value("Waifu2x/LogIndex")
        if v:
            config.LogIndex = int(v)
        self.logBox.setCurrentIndex(config.LogIndex)
        Log.UpdateLoggingLevel()
        # v = self.settings.value("Waifu2x/Scale")
        # if v:
        #     config.Scale = int(v)
        # self.scaleSelect.setCurrentIndex(0)

        # v = self.settings.value("Waifu2x/Model")
        # if v:
        #     config.Model = int(v)
        # self.noiseSelect.setCurrentIndex(config.Model-1)

        v = self.settings.value("Waifu2x/Open")
        if v:
            config.IsOpenWaifu = False if v == "false" else True
        self.checkBox.setChecked(config.IsOpenWaifu)

        self.userId = self.settings.value("UserId")
        self.passwd = self.settings.value("Passwd")
        return

    def ExitSaveSetting(self, mainQsize, bookQsize, imgQsize, userId, passwd):
        self.settings.setValue("MainSize_x", mainQsize.width())
        self.settings.setValue("MainSize_y", mainQsize.height())
        self.settings.setValue("BookSize_x", bookQsize.width())
        self.settings.setValue("BookSize_y", bookQsize.height())
        self.settings.setValue("ImgRead_x", imgQsize.width())
        self.settings.setValue("ImgRead_y", imgQsize.height())
        self.settings.setValue("UserId", userId)
        self.settings.setValue("Passwd", passwd)
        self.settings.setValue("Waifu2x/Open", config.IsOpenWaifu)

    def SaveSetting(self):
        config.DownloadThreadNum = int(self.comboBox.currentText())
        config.ImageQuality = self.buttonGroup.checkedButton().objectName().replace("quality_", "")
        httpProxy = self.httpEdit.text()
        config.SavePath = self.saveEdit.text()
        config.ChatProxy = 1 if self.checkBox_2.isChecked() else 0

        self.settings.setValue("DownloadThreadNum", config.DownloadThreadNum)
        self.settings.setValue("ImageQuality", config.ImageQuality)
        config.HttpProxy = httpProxy
        self.settings.setValue("Proxy/Http", config.HttpProxy)

        self.settings.setValue("SavePath", config.SavePath)
        self.settings.setValue("ChatProxy", config.ChatProxy)

        config.Encode = self.encodeSelect.currentIndex()
        config.Waifu2xThread = int(self.threadSelect.currentIndex()) + 1
        config.IsOpenWaifu = self.checkBox.isChecked()
        config.LookModel = int(self.lookModel.currentIndex())
        config.DownloadModel = int(self.downloadModel.currentIndex())
        config.LogIndex = int(self.logBox.currentIndex())

        self.settings.setValue("Waifu2x/Encode", config.Encode)
        # self.settings.setValue("Waifu2x/Thread", config.Waifu2xThread)
        # self.settings.setValue("Waifu2x/Scale", config.Scale)
        # self.settings.setValue("Waifu2x/Model", config.Model)
        self.settings.setValue("Waifu2x/Open", config.IsOpenWaifu)
        self.settings.setValue("Waifu2x/LookModel", config.LookModel)
        self.settings.setValue("Waifu2x/DownloadModel", config.DownloadModel)
        self.settings.setValue("Waifu2x/LogIndex", config.LogIndex)
        Log.UpdateLoggingLevel()
        # QtWidgets.QMessageBox.information(self, '保存成功', "成功", QtWidgets.QMessageBox.Yes)
        QtBubbleLabel.ShowMsgEx(self, "保存成功")

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if url:
            self.saveEdit.setText(url)

    def SetGpuInfos(self, gpuInfo):
        self.gpuInfos = gpuInfo
        if config.Encode >= len(self.gpuInfos):
            config.Encode = 0

        if not self.gpuInfos:
            return
        for info in self.gpuInfos:
            self.encodeSelect.addItem(info)
        self.encodeSelect.setCurrentIndex(config.Encode)
        Log.Info("waifu2x GPU: " + str(self.gpuInfos))
        return

    def GetGpuName(self):
        index = config.Encode
        if index >= len(self.gpuInfos) or index < 0:
            return "GPU"
        return self.gpuInfos[index]
