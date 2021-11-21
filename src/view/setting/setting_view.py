import base64
import os
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QSettings, Qt, QSize, QUrl, QFile
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFileDialog

from config import config
from config.setting import Setting
from interface.ui_setting import Ui_Setting
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str


class SettingView(QtWidgets.QWidget, Ui_Setting):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        Ui_Setting.__init__(self)
        self.setupUi(self)
        path = os.path.join(Setting.GetConfigPath(), "config.ini")
        self.settings = QSettings(path, QSettings.IniFormat)
        self.setWindowModality(Qt.ApplicationModal)
        self.mainSize = None
        self.bookSize = None
        self.readSize = None
        self.userId = ""
        self.passwd = ""
        self.gpuInfos = []
        self.themeGroup.setId(self.themeButton0, 0)
        self.themeGroup.setId(self.themeButton1, 1)
        self.themeGroup.setId(self.themeButton2, 2)

        # self.themeGroup.idClicked.connect(self.SwitchTheme)
        # self.preDownNum.setFocusPolicy(Qt.NoFocus)
        # for text in QssDataMgr.files:
        #     self.themeBox.addItem(text)

    # def show(self):
    #     self.LoadSetting()
    #     super(self.__class__, self).show()

    def SwitchCurrent(self, **kwargs):
        self.LoadSetting()

    def LoadSetting(self):
        config.IsUpdate = int(self.settings.value("IsUpdate") or config.IsUpdate)
        self.checkBox_IsUpdate.setChecked(config.IsUpdate)

        # language
        config.Language = str(self.settings.value('Language'))
        # self.langSelect.setCurrentIndex(config.DownloadThreadNum - 2)
        self.langSelect.setCurrentText(config.Language)

        config.DownloadThreadNum = int(self.settings.value("DownloadThreadNum") or config.DownloadThreadNum)
        self.comboBox.setCurrentIndex(config.DownloadThreadNum-2)

        httpProxy = self.settings.value("Proxy/Http") or config.HttpProxy
        if httpProxy:
            config.HttpProxy = httpProxy
            self.httpEdit.setText(config.HttpProxy)

        config.IsHttpProxy = self.GetSettingV("Proxy/IsHttp", config.IsHttpProxy)
        self.httpProxy.setChecked(config.IsHttpProxy)
        # if not config.IsHttpProxy:
        #     config.HttpProxy = ""

        config.ChatProxy = self.GetSettingV("ChatProxy", config.ChatProxy)
        self.chatProxy.setChecked(bool(config.ChatProxy))

        config.SavePath = self.GetSettingV("SavePath", config.SavePath)
        self.saveEdit.setText(config.SavePath)

        config.PreLoading = self.GetSettingV("PreLoading", config.PreLoading)
        self.preDownNum.setValue(config.PreLoading)

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

        config.SelectEncodeGpu = self.GetSettingV("Waifu2x/SelectEncodeGpu", "")
        self.encodeSelect.setCurrentIndex(0)
        for index in range(self.encodeSelect.count()):
            if config.SelectEncodeGpu == self.encodeSelect.itemText(index):
                self.encodeSelect.setCurrentIndex(index)

        config.LookModel = self.GetSettingV("Waifu2x/LookModel", config.LookModel)
        config.LookNoise = self.GetSettingV("Waifu2x/LookNoise", config.LookNoise)
        config.LookScale = self.GetSettingV("Waifu2x/LookScale", config.LookScale)
        self.readModel.setCurrentIndex(config.LookModel)
        self.readNoise.setCurrentIndex(config.LookNoise+1)
        self.readScale.setValue(config.LookScale)

        config.DownloadModel = self.GetSettingV("Waifu2x/DownloadModel", config.DownloadModel)
        config.DownloadNoise = self.GetSettingV("Waifu2x/DownloadNoise", config.DownloadNoise)
        config.DownloadScale = self.GetSettingV("Waifu2x/DownloadScale", config.DownloadScale)
        config.DonwloadAuto = self.GetSettingV("Waifu2x/DonwloadAuto", config.DownloadAuto)
        self.downModel.setCurrentIndex(config.DownloadModel)
        self.downNoise.setCurrentIndex(config.DownloadNoise+1)
        self.downScale.setValue(config.DownloadScale)
        self.downAuto.setChecked(config.DownloadAuto)

        config.LogIndex = self.GetSettingV("Waifu2x/LogIndex", config.LogIndex)
        self.logBox.setCurrentIndex(config.LogIndex)
        Log.UpdateLoggingLevel()

        # config.IsTips = self.GetSettingV("Waifu2x/IsTips", config.IsTips)
        config.ChatSendAction = self.GetSettingV("Waifu2x/ChatSendAction", config.ChatSendAction)
        config.IsOpenWaifu = self.GetSettingV("Waifu2x/IsOpen2", config.IsOpenWaifu)
        self.checkBox.setChecked(config.IsOpenWaifu)

        self.userId = self.settings.value("UserId")
        self.passwd = self.settings.value("Passwd2")
        self.userId = self.userId if isinstance(self.userId, str) else ""
        self.passwd = base64.b64decode(self.passwd).decode("utf-8") if self.passwd else ""
        config.ThemeIndex = self.GetSettingV("ThemeIndex", 0)
        button = getattr(self, "themeButton{}".format(config.ThemeIndex))
        button.setChecked(True)
        self.SetTheme()

        config.LookReadMode = self.GetSettingV("Read/LookReadMode", config.LookReadMode)
        # config.LookReadScale = self.GetSettingV("Read/LookReadScale", config.LookReadScale)
        config.LookReadFull = self.GetSettingV("Read/LookReadFull", config.LookReadFull)
        config.TurnSpeed = self.GetSettingV("Read/TurnSpeed", config.TurnSpeed)
        config.ScrollSpeed = self.GetSettingV("Read/ScrollSpeed", config.ScrollSpeed)
        return

    def GetSettingV(self, key, defV=None):
        v = self.settings.value(key)
        try:
            if v:
                if isinstance(defV, int):
                    if v == "true" or v == "True":
                        return 1
                    elif v == "false" or v == "False":
                        return 0
                    return int(v)
                elif isinstance(defV, float):
                    return float(v)
                else:
                    return v
            return defV
        except Exception as es:
            Log.Error(es)
        return v

    def SetSettingV(self, key, val):
        self.settings.setValue(key, val)
        return

    def ExitSaveSetting(self, mainQsize):
        self.settings.setValue("MainSize_x", mainQsize.width())
        self.settings.setValue("MainSize_y", mainQsize.height())
        # self.settings.setValue("BookSize_x", bookQsize.width())
        # self.settings.setValue("BookSize_y", bookQsize.height())
        # self.settings.setValue("ImgRead_x", imgQsize.width())
        # self.settings.setValue("ImgRead_y", imgQsize.height())
        self.settings.setValue("UserId", self.userId)
        self.settings.setValue("Passwd", base64.b64encode(self.passwd.encode("utf-8")))
        self.settings.setValue("Passwd2", base64.b64encode(self.passwd.encode("utf-8")))
        self.settings.setValue("Waifu2x/IsOpen2", int(config.IsOpenWaifu))
        # self.settings.setValue("Waifu2x/IsTips", int(config.IsTips))
        self.settings.setValue("Waifu2x/ChatSendAction", config.ChatSendAction)

    def SwitchTheme(self):
        config.ThemeIndex = self.themeGroup.checkedId()
        self.SetTheme()

    def SetTheme(self):
        themeId = config.ThemeIndex
        if themeId == 0:
            themeId = self.GetSysColor()

        if themeId == config.CurrentSetTheme:
            return

        config.CurrentSetTheme = themeId

        if themeId == 1:
            f = QFile(":/file/theme/dark_pink.qss")
        else:
            f = QFile(":/file/theme/light_pink.qss")
        f.open(QFile.ReadOnly)
        data = str(f.readAll(), encoding='utf-8')
        QtOwner().app.setStyleSheet(data)
        f.close()

    def GetSysColor(self):
        if sys.platform == "win32":
            return self.GetWinSysColor() + 1
        return 1

    def GetWinSysColor(self):
        path = "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key = "AppsUseLightTheme"
        settings = QSettings(path, QSettings.NativeFormat)
        value = settings.value(key, 0)
        return value

    def SaveSetting(self):

        config.IsUpdate = 1 if self.checkBox_IsUpdate.isChecked() else 0
        config.Language = self.langSelect.currentText()
        config.DownloadThreadNum = int(self.comboBox.currentText())
        config.HttpProxy = self.httpEdit.text()
        config.SavePath = self.saveEdit.text()
        config.ChatProxy = 1 if self.chatProxy.isChecked() else 0
        config.IsHttpProxy = 1 if self.httpProxy.isChecked() else 0
        config.PreLoading = self.preDownNum.value()

        self.settings.setValue("IsUpdate", config.IsUpdate)
        self.settings.setValue('Language', config.Language)
        self.settings.setValue("DownloadThreadNum", config.DownloadThreadNum)
        self.settings.setValue("Proxy/Http", config.HttpProxy)
        self.settings.setValue("Proxy/IsHttp", config.IsHttpProxy)
        self.settings.setValue("SavePath", config.SavePath)
        self.settings.setValue("ChatProxy", config.ChatProxy)
        self.settings.setValue("PreLoading", config.PreLoading)

        config.SelectEncodeGpu = self.encodeSelect.currentText()
        config.Waifu2xThread = int(self.threadSelect.currentIndex()) + 1
        config.IsOpenWaifu = int(self.checkBox.isChecked())
        config.DownloadModel = int(self.downModel.currentIndex())
        config.LogIndex = int(self.logBox.currentIndex())

        self.settings.setValue("Waifu2x/DownloadModel", config.DownloadModel)
        self.settings.setValue("Waifu2x/LogIndex", config.LogIndex)
        self.settings.setValue("Waifu2x/SelectEncodeGpu", config.SelectEncodeGpu)
        self.settings.setValue("Waifu2x/IsOpen2", config.IsOpenWaifu)

        config.LookModel = self.readModel.currentIndex()
        config.LookNoise = self.readNoise.currentIndex()-1
        config.LookScale = self.readScale.value()
        self.SetSettingV("Waifu2x/LookModel", config.LookModel)
        self.SetSettingV("Waifu2x/LookNoise", config.LookNoise)
        self.SetSettingV("Waifu2x/LookScale", config.LookScale)

        config.DownloadModel = self.downModel.currentIndex()
        config.DownloadNoise = self.downNoise.currentIndex()-1
        config.DownloadScale = self.downScale.value()
        config.DownloadAuto = int(self.downAuto.isChecked())
        self.SetSettingV("Waifu2x/DownloadModel", config.DownloadModel)
        self.SetSettingV("Waifu2x/DownloadNoise", config.DownloadNoise)
        self.SetSettingV("Waifu2x/DownloadScale", config.DownloadScale)
        self.SetSettingV("Waifu2x/DownloadAuto", config.DownloadAuto)

        config.ThemeIndex = self.themeGroup.checkedId()
        self.SetSettingV("ThemeIndex", config.ThemeIndex)

        # QtOwner().owner.LoadTranslate()
        # QtOwner().owner.RetranslateUi()
        Log.UpdateLoggingLevel()
        # QtWidgets.QMessageBox.information(self, '保存成功', "成功", QtWidgets.QMessageBox.Yes)
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        self.LoadSetting()

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, self.tr("选择文件夹"))
        if url:
            self.saveEdit.setText(url)

    def SetGpuInfos(self, gpuInfo):
        self.gpuInfos = gpuInfo
        config.EncodeGpu = config.SelectEncodeGpu

        if not self.gpuInfos:
            config.EncodeGpu = "CPU"
            config.Encode = -1
            self.encodeSelect.addItem(config.EncodeGpu)
            self.encodeSelect.setCurrentIndex(0)
            return

        if not config.EncodeGpu or (config.EncodeGpu != "CPU" and config.EncodeGpu not in self.gpuInfos):
            config.EncodeGpu = self.gpuInfos[0]
            config.Encode = 0

        index = 0
        for info in self.gpuInfos:
            self.encodeSelect.addItem(info)
            if info == config.EncodeGpu:
                self.encodeSelect.setCurrentIndex(index)
                config.Encode = index
            index += 1

        self.encodeSelect.addItem("CPU")
        if config.EncodeGpu == "CPU":
            config.Encode = -1
            self.encodeSelect.setCurrentIndex(index)

        Log.Info("waifu2x GPU: " + str(self.gpuInfos) + ",select: " + config.EncodeGpu)
        return

    def GetGpuName(self):
        return config.EncodeGpu
        # index = config.Encode
        # if index >= len(self.gpuInfos) or index < 0:
        #     return "GPU"
        # return self.gpuInfos[index]

    def OpenWaifu2xHelp(self):
        QDesktopServices.openUrl(QUrl(config.Waifu2xUrl))