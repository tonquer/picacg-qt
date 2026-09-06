import os
import re
import sys
from contextlib import contextmanager, ExitStack
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import QSettings, Qt, QUrl, QFile, QTranslator, QLocale, QEvent, QObject, QSignalBlocker
from PySide6.QtGui import QDesktopServices, QFontDatabase
from PySide6.QtWidgets import QFileDialog, QScroller, QScrollerProperties, QToolTip

from config import config
from config.setting import Setting, SettingValue
from interface.ui_setting_new import Ui_SettingNew
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str
from view.setting.setting_binding import BindCheck, BindRadio, BindLine, BindIndex, BindValue, BindSpin


class SettingView(QtWidgets.QWidget, Ui_SettingNew):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        Ui_SettingNew.__init__(self)
        self._settingControlsReady = False
        self._settingBindingsConnected = False
        self.setupUi(self)

        self.mainSize = None
        self.bookSize = None
        self.readSize = None
        self.userId = ""
        self.passwd = ""
        self.gpuInfos = []
        self.translate = QTranslator()
        self.fontBox.setItemData(0, "")
        for name in QFontDatabase.families():
            self.fontBox.addItem(name, name)
        self.fontSize.setItemData(0, "")
        for index in range(1, self.fontSize.count()):
            self.fontSize.setItemData(index, self.fontSize.itemText(index))

        self._settingBindings = self._CreateSettingBindings()
        self._modelBindings = (
            (Setting.LookModelName, self.readModelName),
            (Setting.CoverLookModelName, self.coverModelName),
            (Setting.DownloadModelName, self.downModelName),
        )
        self._ConnectSettingBindings()
        for setting, button in self._modelBindings:
            button.setText(setting.setV)

        self.generalButton.clicked.connect(partial(self.MoveToLabel, self.generalLabel))
        self.prefetchButton.clicked.connect(partial(self.MoveToLabel, self.prefetchLabel))
        # self.readButton.clicked.connect(partial(self.MoveToLabel, self.readLabel))
        self.proxyButton.clicked.connect(partial(self.MoveToLabel, self.proxyLabel))
        self.waifu2xButton.clicked.connect(partial(self.MoveToLabel, self.waifu2xLabel))
        self.downloadButton.clicked.connect(partial(self.MoveToLabel, self.downloadLabel))

        self.setDirButton.clicked.connect(self.SelectSavePath)
        self.setLogDirButton.clicked.connect(self.SelectSaveLogPath)
        self.openDownloadDir.clicked.connect(partial(self.OpenDir, self.downloadDir))
        self.openChatDir.clicked.connect(partial(self.OpenDir, self.chatDir))
        self.openCacheDir.clicked.connect(partial(self.OpenDir, self.cacheDir))
        self.openWaifu2xDir.clicked.connect(partial(self.OpenDir, self.waifu2xDir))
        self.openLogDir.clicked.connect(partial(self.OpenDir, self.logLabel))

        self.openProxy.clicked.connect(QtOwner().OpenProxy)
        # TODO
        # self.languageButton3.setVisible(False)

        self.msgLabel.setVisible(False)

        self.prefetchHelpLabels = (
            self.prefetchCountHelp,
            self.crossChapterPrefetchHelp,
            self.prefetchWholeChapterHelp,
            self.showCountHelp
        )
        for label in self.prefetchHelpLabels:
            label.setMouseTracking(True)
            label.setAttribute(Qt.WA_Hover, True)
            label.installEventFilter(self)

        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)
            propertiesOne = QScroller.scroller(self).scrollerProperties()
            propertiesOne.setScrollMetric(QScrollerProperties.MousePressEventDelay, 0)
            propertiesOne.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
            propertiesOne.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
            QScroller.scroller(self.scrollArea).setScrollerProperties(propertiesOne)

        self._settingControlsReady = True

        #     QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)
    #     self.grabGestureBox.installEventFilter(self)
    #
    def eventFilter(self, watched, event) -> bool:
        if watched in getattr(self, "prefetchHelpLabels", ()):
            if event.type() in (QEvent.Enter, QEvent.HoverEnter, QEvent.ToolTip):
                position = watched.mapToGlobal(watched.rect().bottomLeft())
                QToolTip.showText(position, watched.toolTip(), watched)
                return event.type() == QEvent.ToolTip
            if event.type() in (QEvent.Leave, QEvent.HoverLeave):
                QToolTip.hideText()
        return super(self.__class__, self).eventFilter(watched, event)

    def MoveToLabel(self, label):
        p = label.pos()
        self.scrollArea.vScrollBar.ScrollTo(p.y())
        return

    def CheckMsgLabel(self, notify=True):
        isNeed = False
        for name in dir(Setting):
            setItem = getattr(Setting, name)
            if isinstance(setItem, SettingValue):
                if setItem.isNeedReset:
                    if setItem.value != setItem.setV:
                        isNeed = True
        if isNeed:
            self.msgLabel.setVisible(True)
            if notify:
                QtOwner().ShowErrOne(Str.GetStr(Str.NeedResetSave))
        else:
            self.msgLabel.setVisible(False)
        return

    def _CreateSettingBindings(self):
        return (
            BindRadio(Setting.ThemeIndex, self.themeGroup,
                      (self.themeButton0, self.themeButton1, self.themeButton2),
                      lambda: self.SetTheme()),
            BindRadio(Setting.Language, self.languageGroup,
                      (self.languageButton0, self.languageButton1, self.languageButton2, self.languageButton3),
                      lambda: self.SetLanguage()),
            BindRadio(Setting.LogIndex, self.logGroup,
                      (self.logutton0, self.logutton1, self.logutton2),
                      lambda: Log.UpdateLoggingLevel()),
            BindRadio(Setting.IsHttpProxy, self.proxyGroup, (self.proxy0, self.proxy1, self.proxy2, self.proxy3)),
            BindRadio(Setting.SaveNameType, self.saveNameGroup,
                      (self.saveNameButton0, self.saveNameButton1, self.saveNameButton2)),
            BindRadio(Setting.ShowCloseType, self.showCloseButtonGroup, (self.showCloseButton0, self.showCloseButton1)),
            BindCheck(Setting.IsUseScaleFactor, self.mainScaleBox),
            BindCheck(Setting.IsUpdate, self.checkBox_IsUpdate),
            BindCheck(Setting.ChatProxy, self.chatProxy),
            BindCheck(Setting.IsOpenWaifu, self.readCheckBox),
            BindCheck(Setting.PreDownWaifu2x, self.preDownWaifu2x),
            BindCheck(Setting.CoverIsOpenWaifu, self.coverCheckBox),
            BindCheck(Setting.DownloadAuto, self.downAuto),
            BindCheck(Setting.IsOpenOpenGL, self.openglBox),
            BindCheck(Setting.CrossChapterPrefetch, self.crossChapterPrefetch),
            BindCheck(Setting.PrefetchWholeChapter, self.prefetchWholeChapter),
            BindCheck(Setting.IsGrabGesture, self.grabGestureBox),
            BindLine(Setting.HttpProxy, self.httpEdit),
            BindLine(Setting.Sock5Proxy, self.sockEdit),
            BindIndex(Setting.DownloadCoverLv, self.coverLvBox),
            BindIndex(Setting.Waifu2xCpuCore, self.threadSelect,
                      lambda value: self._SetIndexChoice(self.threadSelect, value, config.UseCpuNum)),
            BindIndex(Setting.TitleLine, self.titleLineBox),
            BindIndex(Setting.NotCategoryShow, self.categoryBox),
            BindIndex(Setting.FontStyle, self.fontStyle, lambda value: self.fontStyle.setCurrentIndex(int(value))),
            BindIndex(Setting.Waifu2xTileSize, self.tileComboBox),
            BindValue(Setting.SelectEncodeGpu, self.encodeSelect,
                      lambda value: self._SetTextChoice(self.encodeSelect, value, config.EncodeGpu)),
            BindValue(Setting.FontName, self.fontBox,
                      lambda value: self._SetTextChoice(self.fontBox, self._FontChoiceValue(value))),
            BindValue(Setting.FontSize, self.fontSize,
                      lambda value: self._SetTextChoice(self.fontSize, self._FontChoiceValue(value))),
            BindSpin(Setting.ScaleFactor, self.scaleBox),
            BindSpin(Setting.CoverSize, self.coverSize),
            BindSpin(Setting.CategorySize, self.categorySize),
            BindSpin(Setting.LookMaxNum, self.lookMaxBox),
            BindSpin(Setting.CoverMaxNum, self.coverMaxBox),
            BindSpin(Setting.PicturePrefetchCount, self.prefetchCount),
            BindSpin(Setting.PicturePrefetchFrontCount, self.prefetchFrontCount),
            BindSpin(Setting.PictureShowCount, self.showCount),
            BindSpin(Setting.PictureShowFrontCount, self.showFrontCount),
            BindSpin(Setting.LookScale, self.readScale, float),
            BindSpin(Setting.CoverLookScale, self.coverScale, float),
            BindSpin(Setting.DownloadScale, self.downScale, float),
        )

    def _ConnectSettingBindings(self):
        if self._settingBindingsConnected:
            return
        for binding in self._settingBindings:
            binding.signal.connect(partial(self._SaveSettingBinding, binding))
        for setting, button in self._modelBindings:
            button.clicked.connect(partial(self._OpenModelSelection, setting, button))
        self._settingBindingsConnected = True

    def _SaveSettingBinding(self, binding, *_):
        value = binding.read()
        if value is None:
            return
        self._SaveSettingValue(binding.setting, value, binding.after_save)

    def _SaveSettingValue(self, setting, value, after_save=None):
        setting.SetValue(value)
        if after_save is not None:
            after_save()
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()

    # 登录代理页仍复用这三个入口，保留兼容并共用保存逻辑。
    def ButtonClickEvent(self, setItem, button):
        match = re.search(r"\d+", button.objectName())
        if match is None:
            self.CheckMsgLabel()
            return
        after_save = next((binding.after_save for binding in self._settingBindings
                           if binding.setting is setItem), None)
        self._SaveSettingValue(setItem, int(match.group()), after_save)

    def CheckButtonEvent(self, setItem, button):
        self._SaveSettingValue(setItem, int(button.isChecked()))

    def LineEditEvent(self, setItem, lineEdit):
        self._SaveSettingValue(setItem, lineEdit.text())

    def _OpenModelSelection(self, setting, button, *_):
        QtOwner().OpenSrSelectModel(setting.value, partial(self._SaveModelSelection, setting, button))

    def _SaveModelSelection(self, setting, button, modelName):
        setting.SetValue(modelName)
        button.setText(modelName)
        return modelName

    def SwitchCurrent(self, **kwargs):
        self.InitSetting()
        return

    def LoadSetting(self):
        self.InitSetting()
        self.SetTheme()
        self.SetLanguage()
        # from server.server import Server
        # Server().UpdateProxy()
        # self.SetSock5Proxy()
        return

    def ExitSaveSetting(self, mainQsize):
        return

    @contextmanager
    def _BlockSettingSignals(self):
        controlTypes = (QtWidgets.QAbstractButton, QtWidgets.QButtonGroup,
                        QtWidgets.QComboBox, QtWidgets.QAbstractSpinBox,
                        QtWidgets.QLineEdit)
        with ExitStack() as stack:
            for control in self.findChildren(QObject):
                if isinstance(control, controlTypes):
                    stack.enter_context(QSignalBlocker(control))
            yield

    @staticmethod
    def _FontChoiceValue(value):
        if value in ("", "默认", "默認", "Default"):
            return ""
        return str(value)

    @staticmethod
    def _SetTextChoice(comboBox, value, fallback=""):
        index = comboBox.findData(value)
        if index < 0:
            index = comboBox.findData(fallback)
        if index >= 0:
            comboBox.setCurrentIndex(index)

    @staticmethod
    def _SetIndexChoice(comboBox, value, fallback=0):
        index = value if 0 <= value < comboBox.count() else fallback
        if 0 <= index < comboBox.count():
            comboBox.setCurrentIndex(index)

    def InitSetting(self):
        self._LoadSettingBindings()
        self.SetDownloadLabel()
        self.CheckMsgLabel(notify=False)

    def _LoadSettingBindings(self, controls=None):
        # 回填展示待生效值，不能通过控件信号覆盖用户已经保存的设置。
        with self._BlockSettingSignals():
            for binding in self._settingBindings:
                if controls is None or binding.control in controls:
                    binding.write(binding.setting.setV)
            for setting, button in self._modelBindings:
                if controls is None or button in controls:
                    button.setText(setting.setV)

    def retranslateUi(self, SettingNew):
        with self._BlockSettingSignals():
            Ui_SettingNew.retranslateUi(self, SettingNew)
        if self._settingControlsReady:
            self.InitSetting()
        else:
            self.SetDownloadLabel()

    # def SetSock5Proxy(self):
    #     try:
    #         import socket
    #         if not QtOwner().backSock:
    #             QtOwner().backSock = socket.socket
    #         if Setting.IsHttpProxy.value == 2 and Setting.Sock5Proxy.value:
    #             data = Setting.Sock5Proxy.value.replace("http://", "").replace("https://", "").replace("sock5://", "").replace("socks5://", "")
    #             data = data.split(":")
    #             if len(data) == 2:
    #                 host = data[0]
    #                 port = data[1]
    #                 socks.set_default_proxy(socks.SOCKS5, host, int(port))
    #                 socket.socket = socks.socksocket
    #             else:
    #                 QtOwner().ShowMsg(Str.GetStr(Str.Sock5Error))
    #         else:
    #             socks.set_default_proxy()
    #             socket.socket = QtOwner().backSock
    #     except Exception as es:
    #         Log.Error(es)
    #         QtOwner().ShowMsg(Str.GetStr(Str.Sock5Error))

    def SetLanguage(self):
        language = Setting.Language.value

        # Auto
        if language == 0:
            locale = QLocale.system().name()
            Log.Info("Init translate {}".format(locale))
            if locale[:3].lower() == "zh_":
                if locale.lower() == "zh_cn":
                    language = 1
                else:
                    language = 2
            else:
                # TODO
                language = 3
                # language = 2

        if language == Setting.Language.autoValue:
            return

        Setting.Language.autoValue = language

        if language == 1:
            QtOwner().app.removeTranslator(self.translate)
        elif language == 2:
            self.translate.load(":/file/tr/tr_hk.qm")
            QtOwner().app.installTranslator(self.translate)
        else:
            self.translate.load(":/file/tr/tr_en.qm")
            QtOwner().app.installTranslator(self.translate)
        Str.Reload()
        QtOwner().owner.RetranslateUi()

    def SetTheme(self):
        themeId = Setting.ThemeIndex.value
        if themeId == 0:
            themeId = self.GetSysColor()

        if themeId == Setting.ThemeIndex.autoValue:
            return

        Setting.ThemeIndex.autoValue = themeId

        if themeId == 1:
            f = QFile(":/file/theme/dark_pink.qss")
        else:
            f = QFile(":/file/theme/light_pink.qss")
        f.open(QFile.ReadOnly)
        data = str(f.readAll(), encoding='utf-8')
        if Setting.FontName.value:
            data = data.replace("/*replace*/", "font-family: {};".format(Setting.FontName.value))
        QtOwner().app.setStyleSheet(data)
        self.SetSettingTheme(themeId)
        f.close()

    def SetSettingTheme(self, themId):
        if themId != 1:
            qss = """
                .QFrame
                {
                    background-color: rgb(253, 253, 253);
                    
                    border:2px solid rgb(234,234,234);
                    border-radius:5px
                }        
                """
        else:
            qss = """
                .QFrame
                {
                    background-color: rgb(50, 50, 50);

                    border:2px solid rgb(35,35,35);
                    border-radius:5px
                }        
                """
        self.scrollArea.setStyleSheet(qss)

    def GetSysColor(self):
        # TODO KDE如何获取系统颜色
        if sys.platform == "win32":
            return self.GetWinSysColor() + 1
        elif sys.platform == "darwin":
            return self.GetMacOsSysColor()
        return 1

    def GetWinSysColor(self):
        try:
            path = "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            key = "AppsUseLightTheme"
            settings = QSettings(path, QSettings.NativeFormat)
            value = settings.value(key, 0)
            return value
        except Exception as es:
            Log.Error(es)
        return 1

    def GetMacOsSysColor(self):
        try:
            import subprocess
            cmd = "defaults read -g AppleInterfaceStyle"
            results = subprocess.getoutput(cmd)
            if results == "Dark":
                return 1
            else:
                return 2
        except Exception as es:
            Log.Error(es)
        return 1

    def SaveSetting(self):
        return

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            Setting.SavePath.SetValue(url)
        self.SetDownloadLabel()

    def SelectSaveLogPath(self):
        url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            Setting.LogDirPath.SetValue(url)
            Log.Init()

        self.SetDownloadLabel()

    def SetDownloadLabel(self):
        url = Setting.SavePath.value
        if not url:
            url = "./"
        self.downloadDir.setText(os.path.join(url, config.SavePathDir))
        self.chatDir.setText(os.path.join(Setting.GetCachePath(), config.ChatSavePath))
        self.cacheDir.setText(Setting.GetCachePath())
        self.waifu2xDir.setText(os.path.join(Setting.GetCachePath(), config.Waifu2xPath))

        self.logLabel.setText(Setting.GetLogPath())

    def OpenDir(self, label):
        QDesktopServices.openUrl(QUrl.fromLocalFile(label.text()))
        return

    def SetGpuInfos(self, gpuInfo, cpuNum):
        self.gpuInfos = gpuInfo
        config.EncodeGpu = Setting.SelectEncodeGpu.value
        if not self.gpuInfos:
            config.EncodeGpu = "CPU"
        elif not config.EncodeGpu or (config.EncodeGpu != "CPU" and config.EncodeGpu not in self.gpuInfos):
            config.EncodeGpu = self.gpuInfos[0]
        config.Encode = -1 if config.EncodeGpu == "CPU" else self.gpuInfos.index(config.EncodeGpu)
        config.UseCpuNum = Setting.Waifu2xCpuCore.value
        if config.UseCpuNum > cpuNum:
            config.UseCpuNum = cpuNum

        # 硬件变化只调整本次运行的选择，不改写用户的待生效偏好。
        with self._BlockSettingSignals():
            self.encodeSelect.clear()
            for info in self.gpuInfos:
                self.encodeSelect.addItem(info, info)
            self.encodeSelect.addItem("CPU", "CPU")

            autoText = self.threadSelect.itemText(0)
            self.threadSelect.clear()
            self.threadSelect.addItem(autoText)
            for i in range(cpuNum):
                self.threadSelect.addItem(str(i + 1))
            self._LoadSettingBindings((self.encodeSelect, self.threadSelect))

        Log.Warn("waifu2x GPU: " + str(self.gpuInfos) + ",select: " + str(config.EncodeGpu) + ",use cpu num: " + str(config.UseCpuNum))
        return

    def GetGpuName(self):
        return config.EncodeGpu
        # index = config.Encode
        # if index >= len(self.gpuInfos) or index < 0:
        #     return "GPU"
        # return self.gpuInfos[index]

    def OpenWaifu2xHelp(self):
        QDesktopServices.openUrl(QUrl(config.Waifu2xUrl))
