import os
import shutil


class SettingValue:
    def __init__(self, tag, defaultV, isNeedReset, des=None):
        self.tag = tag                 # 分类
        self._value = defaultV          # 生效值
        self.setV = defaultV           # 设置的值
        self.defaultV = defaultV       # 默认值
        self.isNeedReset = isNeedReset       # 是否重启生效
        self.des = des          # 描述
        self.autoValue = 0      # 选自动时，自动生效的值
        self.name = ""

    def __lt__(self, other):
        raise OverflowError

    def __gt__(self, other):
        raise OverflowError

    def __eq__(self, other):
        if isinstance(other, SettingValue):
            return id(self) == id(other)
        raise OverflowError

    @property
    def value(self):
        return self._value

    def InitValue(self, value, name):
        value = self.GetSettingV(value, self.defaultV)
        self._value = value
        self.setV = value
        self.name = name
        return

    @staticmethod
    def GetSettingV(v, defV=None):
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
                elif isinstance(defV, list) and isinstance(v, str):
                    return [v]
                else:
                    return v
            return defV
        except Exception as es:
            from tools.log import Log
            Log.Error(es)
        return v

    def GetIndexV(self):
        if not isinstance(self.des, list):
            return ""
        if self._value >= len(self.des):
            return ""
        return self.des[self._value]

    def SetValue(self, value):
        if self.setV == value and self._value == value:
            return

        self.setV = value
        if not self.isNeedReset:
            self._value = value
            self.autoValue = 0
        Setting.SaveSettingV(self)


class Setting:
    # 通用设置
    IsUpdate = SettingValue("GeneraSetting", 1, False)
    Language = SettingValue("GeneraSetting", 0, False, ["Auto", "zh", "hk", "en"])  # ch-zh ch-hk eu
    ThemeIndex = SettingValue("GeneraSetting", 0, False, ["Auto", "dark", "light"])  #
    LogIndex = SettingValue("GeneraSetting", 0, False, ["warn", "info", "debug"])  # Warn Info Debug

    LogDirPath = SettingValue("GeneraSetting", "", False)

    CoverSize = SettingValue("GeneraSetting", 100, False)  #
    TitleLine = SettingValue("GeneraSetting", 2, False)  #
    NotCategoryShow = SettingValue("GeneraSetting", 0, False)  #

    CategorySize = SettingValue("GeneraSetting", 80, False)  #
    # ScaleLevel = SettingValue("GeneraSetting", 0, True, ["Auto", 100, 125, 150, 175, 200])
    IsUseScaleFactor = SettingValue("GeneraSetting", 0, True)
    ScaleFactor = SettingValue("GeneraSetting", 100, True)

    # IsUseTitleBar = SettingValue("GeneraSetting", 1, True)

    FontName = SettingValue("GeneraSetting", "", True)
    FontSize = SettingValue("GeneraSetting", "", True)
    FontStyle = SettingValue("GeneraSetting", 0, True)

    IsNotShowCloseTip = SettingValue("GeneraSetting", 0, False)
    ShowCloseType = SettingValue("GeneraSetting", 0, False)

    # 代理设置
    IsHttpProxy = SettingValue("ProxySetting", 0, False, ["", "Http", "Sock5", "system"])
    HttpProxy = SettingValue("ProxySetting", "", False)
    Sock5Proxy = SettingValue("ProxySetting", "", False)
    ChatProxy = SettingValue("ProxySetting", 0, False)
    PreferCDNIP = SettingValue("ProxySetting", "104.18.227.172", False)
    IsUseHttps = SettingValue("ProxySetting", 1, False)
    PreIpv6 = SettingValue("ProxySetting", 0, False)
    LastProxyResult = SettingValue("ProxySetting", {}, False)
    IsUseSniPretend = SettingValue("ProxySetting", 1, False)

    ProxySelectIndex = SettingValue("ProxySetting", 1, False)
    ProxyImgSelectIndex = SettingValue("ProxySetting", 1, False)
    PreferCDNIPImg = SettingValue("ProxySetting", "104.18.227.172", False)
    ApiTimeOut = SettingValue("ProxySetting", 1, False, [2, 5, 7, 10])
    ImgTimeOut = SettingValue("ProxySetting", 1, False, [2, 5, 7, 10, 15])

    # 下载与缓存
    SavePath = SettingValue("DownloadSetting", "", False)
    SaveNameType = SettingValue("DownloadSetting", 0, False)

    # Waifu2x设置
    SelectEncodeGpu = SettingValue("Waifu2xSetting", "", True)
    Waifu2xCpuCore = SettingValue("Waifu2xSetting", 0, True)
    Waifu2xTileSize = SettingValue("Waifu2xSetting", 0, False, [0, 200, 100, 32])

    # 封面 Waifu2x
    CoverIsOpenWaifu = SettingValue("Waifu2xSetting", 0, False)
    CoverMaxNum = SettingValue("Waifu2xSetting", 400, False)
    CoverLookModel = SettingValue("Waifu2xSetting", 0, False)
    CoverLookModelName = SettingValue("Waifu2xSetting", "MODEL_WAIFU2X_ANIME_UP2X_DENOISE3X", False)
    # CoverLookModel = SettingValue("Waifu2xSetting", 0, False)
    # CoverLookNoise = SettingValue("Waifu2xSetting", 3, False)
    CoverLookScale = SettingValue("Waifu2xSetting", 2.0, False)

    IsOpenWaifu = SettingValue("Waifu2xSetting", 0, False)
    LookMaxNum = SettingValue("Waifu2xSetting", 4096, False)
    LookModelName = SettingValue("Waifu2xSetting", "MODEL_WAIFU2X_ANIME_UP2X_DENOISE3X", False)
    # LookModel = SettingValue("Waifu2xSetting", 0, False)
    # LookNoise = SettingValue("Waifu2xSetting", 3, False)
    LookScale = SettingValue("Waifu2xSetting", 2.0, False)

    DownloadAuto = SettingValue("Waifu2xSetting", 0, False)
    DownloadModelName = SettingValue("Waifu2xSetting", "MODEL_WAIFU2X_CUNET_UP2X_DENOISE3X", False)
    # DownloadModel = SettingValue("Waifu2xSetting", 1, False)
    # DownloadNoise = SettingValue("Waifu2xSetting", 3, False)
    DownloadScale = SettingValue("Waifu2xSetting", 2.0, False)

    # 看图设置
    LookReadMode = SettingValue("ReadSetting", 1, False)
    LookReadFull = SettingValue("ReadSetting", 0, False)
    TurnSpeed = SettingValue("ReadSetting", 5000, False)
    ScrollSpeed = SettingValue("ReadSetting", 400, False)
    PreDownWaifu2x = SettingValue("ReadSetting", 1, False)
    IsOpenOpenGL = SettingValue("ReadSetting", 0, True)

    # 批量超分
    BatchSrImportDir = SettingValue("BatchSrTool", "", False)
    BatchSrExportDir = SettingValue("BatchSrTool", "", False)
    BatchSrState = SettingValue("BatchSrTool", "", False)
    BatchSrFmt = SettingValue("BatchSrTool", "", False)

    BatchSrModelName = SettingValue("BatchSrTool", "MODEL_WAIFU2X_CUNET_UP2X_DENOISE3X", False)
    BatchSrScale = SettingValue("BatchSrTool", 2.0, False)

    # Other
    UserId = SettingValue("Other", "", False)
    Password = SettingValue("Other", "", False)
    ChatSendAction = SettingValue("Other", 0, False, ["CtrlEnter", "Enter"])
    ScreenIndex = SettingValue("Other", 0, False)
    AutoLogin = SettingValue("Other", 0, False)
    AutoSign = SettingValue("Other", 1, False)
    SavePassword = SettingValue("Other", 1, False)
    IsShowCmd = SettingValue("Other", 0, False)
    IsGrabGesture = SettingValue("Other", 0, True)
    IsShowProxy5 = SettingValue("Other", 0, False)
    IsPreUpdate = SettingValue("Other", 0, False)
    SaveCacheAddress = SettingValue("Other", "104.21.91.145", False)
    IsReDownload = SettingValue("Other", 0, False)
    GlobalConfig = SettingValue("Other", "", False)
    ForbidWords = SettingValue("Other", [], False)
    AddForbidWords = SettingValue("Other", [], False)
    IsForbidCategory =SettingValue("Other", True, False)
    IsForbidTag = SettingValue("Other", False, False)
    IsForbidTitle = SettingValue("Other", False, False)
    IsSkipSpace = SettingValue("Other", 0, False)
    IsSkipPic = SettingValue("Other", 0, False)

    @staticmethod
    def InitLoadSetting():
        path = os.path.join(Setting.GetConfigPath(), "config.ini")
        from PySide6.QtCore import QSettings
        settings = QSettings(path, QSettings.IniFormat)
        for name in dir(Setting):
            setItem = getattr(Setting, name)
            if isinstance(setItem, SettingValue):
                value = settings.value(setItem.tag + "/" + name, setItem.defaultV)
                setItem.InitValue(value, name)
        from tools.log import Log
        Log.UpdateLoggingLevel()
        return

    @staticmethod
    def SaveSetting():
        path = os.path.join(Setting.GetConfigPath(), "config.ini")
        from PySide6.QtCore import QSettings
        settings = QSettings(path, QSettings.IniFormat)
        for name in dir(Setting):
            setItem = getattr(Setting, name)
            if isinstance(setItem, SettingValue):
                settings.setValue(setItem.tag + "/" + name, setItem.setV)
        return

    @staticmethod
    def SaveSettingV(setItem):
        path = os.path.join(Setting.GetConfigPath(), "config.ini")
        from PySide6.QtCore import QSettings
        settings = QSettings(path, QSettings.IniFormat)
        if isinstance(setItem, SettingValue) and setItem.name:
            settings.setValue(setItem.tag + "/" + setItem.name, setItem.setV)

    @staticmethod
    def Init():
        path = Setting.GetConfigPath()
        if not os.path.isdir(path):
            os.mkdir(path)
        path2 = Setting.GetLocalHomePath()
        if not os.path.isdir(path2):
            os.mkdir(path2)
        Setting.CheckRepair()
        Setting.CheckRepairLocalDb()
        return

    @staticmethod
    def GetLocalHomePath():
        from PySide6.QtCore import QDir
        homePath = QDir.homePath()
        projectName = ".comic-qt"
        return os.path.join(homePath, projectName)

    @staticmethod
    def GetConfigPath():
        import sys
        if sys.platform == "win32":
            return "data"
        else:
            from PySide6.QtCore import QDir
            homePath = QDir.homePath()
            projectName = ".picacg"
            return os.path.join(homePath, projectName)

    @staticmethod
    def GetLogPath():
        import sys
        if Setting.LogDirPath.value:
            return Setting.LogDirPath.value

        if sys.platform == "win32":
            return "logs"
        else:
            return os.path.join(Setting.GetConfigPath(), "logs")

    @staticmethod
    def CheckRepair():
        import sys
        if not sys.platform == "win32":
            return
        try:
            from PySide6.QtCore import QDir
            homePath = QDir.homePath()
            projectName = ".picacg"
            oldPath = os.path.join(homePath, projectName)
            fileList = ["download.db", "config.ini", "history.db", "cache_word"]
            for file in fileList:
                filePath = os.path.join("data", file)
                if not os.path.isfile(filePath):
                    oldFilePath = os.path.join(oldPath, file)
                    if os.path.isfile(oldFilePath):
                        shutil.move(oldFilePath, filePath)
                    elif os.path.isfile(file):
                        shutil.move(file, filePath)

        except Exception as es:
            from tools.log import Log
            Log.Error(es)

    @staticmethod
    def CheckRepairLocalDb():
        try:
            fileName = os.path.join(Setting.GetLocalHomePath(), "local_read.db")
            toFileName = os.path.join(Setting.GetConfigPath(), "local_read.db")
            from config import config
            copyOkName = os.path.join(Setting.GetLocalHomePath(), "{}_local.ok".format(config.ProjectName))
            from PySide6.QtCore import QDir
            if os.path.isfile(copyOkName):
                return
            if not os.path.isfile(fileName):
                return
            if os.path.isfile(toFileName):
                return
            shutil.copy(fileName, copyOkName)
            shutil.copy(fileName, toFileName)
            from server import Log
            Log.Warn("copy local read db")
        except Exception as es:
            from tools.log import Log
            Log.Error(es)