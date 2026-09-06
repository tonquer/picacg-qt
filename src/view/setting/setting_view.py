import base64
import os
import re
import sys
from contextlib import contextmanager, ExitStack
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import QSettings, Qt, QSize, QUrl, QFile, QTranslator, QLocale, QEvent, QObject, QSignalBlocker
from PySide6.QtGui import QDesktopServices, QFont, QFontDatabase
from PySide6.QtWidgets import QFileDialog, QScroller, QScrollerProperties, QToolTip

from config import config
from config.setting import Setting, SettingValue
from interface.ui_setting_new import Ui_SettingNew
from qt_owner import QtOwner
from tools.langconv import Converter
from tools.log import Log
from tools.str import Str


class SettingView(QtWidgets.QWidget, Ui_SettingNew):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        Ui_SettingNew.__init__(self)
        self._settingControlsReady = False
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

        # RadioButton:
        self.themeGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.ThemeIndex))
        self.languageGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.Language))
        self.logGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.LogIndex))
        # self.mainScaleGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.ScaleLevel))
        self.proxyGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.IsHttpProxy))
        self.saveNameGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.SaveNameType))
        self.showCloseButtonGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.ShowCloseType))

        # CheckButton:
        self.mainScaleBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsUseScaleFactor, self.mainScaleBox))

        self.checkBox_IsUpdate.clicked.connect(partial(self.CheckButtonEvent, Setting.IsUpdate, self.checkBox_IsUpdate))
        self.chatProxy.clicked.connect(partial(self.CheckButtonEvent, Setting.ChatProxy, self.chatProxy))
        self.readCheckBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsOpenWaifu, self.readCheckBox))
        self.preDownWaifu2x.clicked.connect(partial(self.CheckButtonEvent, Setting.PreDownWaifu2x, self.preDownWaifu2x))
        self.coverCheckBox.clicked.connect(partial(self.CheckButtonEvent, Setting.CoverIsOpenWaifu, self.coverCheckBox))
        self.downAuto.clicked.connect(partial(self.CheckButtonEvent, Setting.DownloadAuto, self.downAuto))
        # self.titleBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsUseTitleBar, self.titleBox))
        self.openglBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsOpenOpenGL, self.openglBox))
        self.crossChapterPrefetch.clicked.connect(partial(self.CheckButtonEvent, Setting.CrossChapterPrefetch, self.crossChapterPrefetch))
        self.prefetchWholeChapter.clicked.connect(partial(self.CheckButtonEvent, Setting.PrefetchWholeChapter, self.prefetchWholeChapter))
        self.grabGestureBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsGrabGesture, self.grabGestureBox))
        # self.isShowClose.clicked.connect(partial(self.CheckButtonEvent, Setting.IsNotShowCloseTip, self.isShowClose))

        # LineEdit:
        self.httpEdit.editingFinished.connect(partial(self.LineEditEvent, Setting.HttpProxy, self.httpEdit))
        self.sockEdit.editingFinished.connect(partial(self.LineEditEvent, Setting.Sock5Proxy, self.sockEdit))

        # Button:

        # comboBox:
        # self.encodeSelect.currentIndexChanged.connect(partial(self.CheckRadioEvent, "LookReadMode"))
        # self.readModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.LookModel))
        # self.readNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.LookNoise))
        # self.coverModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.CoverLookModel))
        # self.coverNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.CoverLookNoise))
        # self.downModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.DownloadModel))
        # self.downNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.DownloadNoise))
        self.coverLvBox.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.DownloadCoverLv))

        self.readModelName.clicked.connect(partial(self.CheckOpenSrSelect, Setting.LookModelName, self.readModelName))
        self.coverModelName.clicked.connect(partial(self.CheckOpenSrSelect, Setting.CoverLookModelName, self.coverModelName))
        self.downModelName.clicked.connect(partial(self.CheckOpenSrSelect, Setting.DownloadModelName, self.downModelName))
        self.encodeSelect.currentIndexChanged.connect(partial(self.ChoiceTextEvent, Setting.SelectEncodeGpu, self.encodeSelect))
        self.threadSelect.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.Waifu2xCpuCore))
        self.titleLineBox.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.TitleLine))
        self.categoryBox.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.NotCategoryShow))

        self.fontBox.currentIndexChanged.connect(partial(self.ChoiceTextEvent, Setting.FontName, self.fontBox))
        self.fontSize.currentIndexChanged.connect(partial(self.ChoiceTextEvent, Setting.FontSize, self.fontSize))
        self.fontStyle.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.FontStyle))
        self.tileComboBox.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.Waifu2xTileSize))

        # spinBox
        # self.preDownNum.valueChanged.connect(partial(self.SpinBoxEvent, "", self.preDownNum))
        self.scaleBox.valueChanged.connect(partial(self.SpinBoxEvent, Setting.ScaleFactor))
        self.coverSize.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverSize))
        self.categorySize.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CategorySize))
        self.readScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.LookScale))
        self.coverScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverLookScale))
        self.downScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.DownloadScale))
        self.lookMaxBox.valueChanged.connect(partial(self.SpinBoxEvent, Setting.LookMaxNum))
        self.coverMaxBox.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverMaxNum))
        self.prefetchCount.valueChanged.connect(partial(self.SpinBoxEvent, Setting.PicturePrefetchCount))
        self.prefetchFrontCount.valueChanged.connect(partial(self.SpinBoxEvent, Setting.PicturePrefetchFrontCount))

        self.showCount.valueChanged.connect(partial(self.SpinBoxEvent, Setting.PictureShowCount))
        self.showFrontCount.valueChanged.connect(partial(self.SpinBoxEvent, Setting.PictureShowFrontCount))

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

    def ButtonClickEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        mo = re.search(r"\d+", button.objectName())
        if mo:
            value = int(mo.group())
            setItem.SetValue(value)
            if setItem == Setting.ThemeIndex:
                self.SetTheme()
            elif setItem == Setting.LogIndex:
                Log.UpdateLoggingLevel()
            elif setItem == Setting.Language:
                self.SetLanguage()
            # elif setItem == Setting.IsHttpProxy:
            #     from server.server import Server
            #     Server().UpdateProxy()
            QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

    def CheckButtonEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(button.isChecked()))
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return
    
    def CheckOpenSrSelect(self, setItem, button):
        if button == self.coverModelName:
            QtOwner().OpenSrSelectModel(setItem.value, self.CheckOpenSrSelectCoverBack)
        elif button == self.readModelName:
            QtOwner().OpenSrSelectModel(setItem.value, self.CheckOpenSrSelectReadBack)
        elif button == self.downModelName:
            QtOwner().OpenSrSelectModel(setItem.value, self.CheckOpenSrSelectDownBack)
        pass

    def CheckOpenSrSelectCoverBack(self, modelName):
        Setting.CoverLookModelName.SetValue(modelName)
        self.coverModelName.setText(modelName)
        return modelName

    def CheckOpenSrSelectReadBack(self, modelName):
        Setting.LookModelName.SetValue(modelName)
        self.readModelName.setText(modelName)
        return modelName

    def CheckOpenSrSelectDownBack(self, modelName):
        Setting.DownloadModelName.SetValue(modelName)
        self.downModelName.setText(modelName)
        return modelName
    
    def CheckRadioEvent(self, setItem, value):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(value)
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        # if setItem == Setting.IsHttpProxy:
        #     from server.server import Server
        #     Server().UpdateProxy()
        self.CheckMsgLabel()
        return

    def ChoiceTextEvent(self, setItem, comboBox, *_):
        if comboBox.currentIndex() < 0:
            return
        self.CheckRadioEvent(setItem, comboBox.currentData())

    def LineEditEvent(self, setItem, lineEdit):
        assert isinstance(setItem, SettingValue)
        value = lineEdit.text()
        setItem.SetValue(value)
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        # from server.server import Server
        # Server().UpdateProxy()
        return

    def SpinBoxEvent(self, setItem, value):
        assert isinstance(setItem, SettingValue)
        converter = float if isinstance(setItem.defaultV, float) else int
        setItem.SetValue(converter(value))
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

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
        # 回填展示待生效值，不能通过控件信号覆盖用户已经保存的设置。
        with self._BlockSettingSignals():
            self.checkBox_IsUpdate.setChecked(bool(Setting.IsUpdate.setV))
            self.mainScaleBox.setChecked(bool(Setting.IsUseScaleFactor.setV))
            self.SetRadioGroup("themeButton", Setting.ThemeIndex.setV)
            self.SetRadioGroup("languageButton", Setting.Language.setV)
            self.SetRadioGroup("proxy", Setting.IsHttpProxy.setV)
            self.SetRadioGroup("saveNameButton", Setting.SaveNameType.setV)
            self.SetRadioGroup("showCloseButton", Setting.ShowCloseType.setV)
            self.coverSize.setValue(Setting.CoverSize.setV)
            self.coverLvBox.setCurrentIndex(Setting.DownloadCoverLv.setV)
            self.categorySize.setValue(Setting.CategorySize.setV)
            self.SetRadioGroup("logutton", Setting.LogIndex.setV)
            self.httpEdit.setText(Setting.HttpProxy.setV)
            self.sockEdit.setText(Setting.Sock5Proxy.setV)
            self.chatProxy.setChecked(bool(Setting.ChatProxy.setV))
            self.openglBox.setChecked(bool(Setting.IsOpenOpenGL.setV))
            self.prefetchCount.setValue(Setting.PicturePrefetchCount.setV)
            self.prefetchFrontCount.setValue(Setting.PicturePrefetchFrontCount.setV)
            self.showCount.setValue(Setting.PictureShowCount.setV)
            self.showFrontCount.setValue(Setting.PictureShowFrontCount.setV)
            self.crossChapterPrefetch.setChecked(bool(Setting.CrossChapterPrefetch.setV))
            self.prefetchWholeChapter.setChecked(bool(Setting.PrefetchWholeChapter.setV))
            self.grabGestureBox.setChecked(bool(Setting.IsGrabGesture.setV))
            self._SetTextChoice(self.encodeSelect, Setting.SelectEncodeGpu.setV, config.EncodeGpu)
            self._SetIndexChoice(self.threadSelect, Setting.Waifu2xCpuCore.setV, config.UseCpuNum)
            self._SetTextChoice(self.fontSize, self._FontChoiceValue(Setting.FontSize.setV))
            self.fontStyle.setCurrentIndex(int(Setting.FontStyle.setV))
            self._SetTextChoice(self.fontBox, self._FontChoiceValue(Setting.FontName.setV))
            self.readCheckBox.setChecked(bool(Setting.IsOpenWaifu.setV))
            self.preDownWaifu2x.setChecked(bool(Setting.PreDownWaifu2x.setV))
            self.readScale.setValue(Setting.LookScale.setV)
            self.scaleBox.setValue(Setting.ScaleFactor.setV)
            self.lookMaxBox.setValue(Setting.LookMaxNum.setV)
            self.coverMaxBox.setValue(Setting.CoverMaxNum.setV)
            self.categoryBox.setCurrentIndex(Setting.NotCategoryShow.setV)
            self.titleLineBox.setCurrentIndex(Setting.TitleLine.setV)
            self.tileComboBox.setCurrentIndex(Setting.Waifu2xTileSize.setV)
            self.coverCheckBox.setChecked(bool(Setting.CoverIsOpenWaifu.setV))
            self.coverScale.setValue(Setting.CoverLookScale.setV)
            self.downAuto.setChecked(bool(Setting.DownloadAuto.setV))
            self.downScale.setValue(Setting.DownloadScale.setV)
            self.coverModelName.setText(Setting.CoverLookModelName.setV)
            self.readModelName.setText(Setting.LookModelName.setV)
            self.downModelName.setText(Setting.DownloadModelName.setV)
        self.SetDownloadLabel()
        self.CheckMsgLabel(notify=False)

    def retranslateUi(self, SettingNew):
        with self._BlockSettingSignals():
            Ui_SettingNew.retranslateUi(self, SettingNew)
        if self._settingControlsReady:
            self.InitSetting()
        else:
            self.SetDownloadLabel()
            self.coverModelName.setText(Setting.CoverLookModelName.setV)
            self.readModelName.setText(Setting.LookModelName.setV)
            self.downModelName.setText(Setting.DownloadModelName.setV)

    def SetRadioGroup(self, text, index):
        radio = getattr(self, text+str(index), None)
        if radio:
            radio.setChecked(True)

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
            self._SetTextChoice(self.encodeSelect, Setting.SelectEncodeGpu.setV, config.EncodeGpu)

            autoText = self.threadSelect.itemText(0)
            self.threadSelect.clear()
            self.threadSelect.addItem(autoText)
            for i in range(cpuNum):
                self.threadSelect.addItem(str(i + 1))
            self._SetIndexChoice(self.threadSelect, Setting.Waifu2xCpuCore.setV, config.UseCpuNum)

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
