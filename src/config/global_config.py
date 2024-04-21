from config.setting import Setting
from tools.log import Log
from tools.singleton import Singleton


class GlobalItem(object):
    def __init__(self, default):
        self.value = default
        self.def_value = default

    def is_same(self):
        return self.value == self.def_value

    def set_value(self, value):
        if isinstance(self.def_value, int):
            self.value = int(value)
        elif isinstance(self.def_value, list) and isinstance(value, str):
            self.value = value.split(",")
        else:
            self.value = value


class GlobalConfig:
    Ver = GlobalItem(0)
    LocalProxyIndex = [2, 3]
    Address = GlobalItem(["104.21.91.145", "188.114.98.153"])
    AddressIpv6 = GlobalItem(["2606:4700:d:28:dbf4:26f3:c265:73bc", "2a06:98c1:3120:ca71:be2c:c721:d2b5:5dbf"])
    ImageUrl = GlobalItem("s3.picacomic.com")
    ImageServerList = GlobalItem(["s3.picacomic.com", "storage.diwodiwo.xyz", "s2.picacomic.com", "storage1.picacomic.com", "storage-b.picacomic.com"])
    ImageJumList = GlobalItem(["img.picacomic.com", "img.diwodiwo.xyz"])

    def __init__(self):
        pass

    @staticmethod
    def GetAddress(index):
        if index in GlobalConfig.LocalProxyIndex:
            i = GlobalConfig.LocalProxyIndex.index(index)
            if Setting.PreIpv6.value > 0:
                return GlobalConfig.AddressIpv6.value[i]
            else:
                return GlobalConfig.Address.value[i]
        else:
            return ""
    #
    # @staticmethod
    # def GetImageServer(index):
    #     if index in GlobalConfig.LocalProxyIndex:
    #         i = GlobalConfig.LocalProxyIndex.index(index)
    #         return GlobalConfig.ImageServerList.value[i]
    #     else:
    #         return  ""

    @staticmethod
    def GetImageAdress(index):
        if index in GlobalConfig.LocalProxyIndex:
            i = GlobalConfig.LocalProxyIndex.index(index)
            if Setting.PreIpv6.value > 0:
                return GlobalConfig.AddressIpv6.value[i]
            else:
                return GlobalConfig.Address.value[i]
        else:
            return  ""

    @staticmethod
    def LoadSetting():
        try:
            for k, v in dict(Setting.GlobalConfig.value).items():
                Log.Debug("load global setting, k={}, v={}".format(k, v))
                value = getattr(GlobalConfig, k)
                if isinstance(value, GlobalItem) :
                    value.set_value(v)
        except Exception as es:
            Log.Error(es)
        pass

    @staticmethod
    def SaveSetting():
        saveData = {}
        try:
            for name in dir(GlobalConfig):
                value = getattr(GlobalConfig, name)
                if isinstance(value, GlobalItem) and not value.is_same():
                    saveData[name] = value.value
            Setting.GlobalConfig.SetValue(saveData)
        except Exception as es:
            Log.Error(es)
        pass

    @staticmethod
    def SetSetting(k, v):
        value = getattr(GlobalConfig, k)
        if isinstance(value, GlobalItem):
            Log.Info("set setting, k:{}, v:{}".format(k, v))
            value.set_value(v)
            GlobalConfig.SaveSetting()

    # 下载配置文件
    @staticmethod
    def UpdateSetting(data):
        allKvs = {}
        for v in data.replace("\r", "").split("\n"):
            if not v:
                continue
            [k, v2] = v.split("=")
            allKvs[k] = v2
        ver = int(allKvs.get("Ver", 0))
        if ver > GlobalConfig.Ver.value:
            Log.Info("update setting, {}".format(allKvs))
            for name, value in allKvs.items():
                item = getattr(GlobalConfig, name)
                if isinstance(item, GlobalItem):
                    item.set_value(value)
            GlobalConfig.SaveSetting()
        pass
