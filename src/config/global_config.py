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
    Ver = GlobalItem(20)
    VerTime = GlobalItem("2026-7-29")
    # web url
    WebDnsList = GlobalItem([])


    LocalProxyIndex = [2, 3]
    Address = GlobalItem(["104.21.91.145", "188.114.98.153"])
    # AddressIpv6 = GlobalItem(["2606:4700:d:28:dbf4:26f3:c265:73bc", "2a06:98c1:3120:ca71:be2c:c721:d2b5:5dbf"])
    # ImageUrl = GlobalItem("s3.picacomic.com")
    ImageServerList = GlobalItem(["s3.picacomic.com", "storage.diwodiwo.xyz", "s2.picacomic.com",
                                  "storage1.picacomic.com", "storage-b.picacomic.com",
                                  ])
    ImageJumList = GlobalItem(["img.picacomic.com", "img.tipatipa.xyz", "img.diwodiwo.xyz", "img.safedataplj.com"])

    ProxyApiDomain = GlobalItem("bika-api.jpacg.cc")
    ProxyImgDomain = GlobalItem("bika-img.jpacg.cc")

    ProxyApiDomain2 = GlobalItem("bika2-api.jpacg.cc")
    ProxyImgDomain2 = GlobalItem("bika21-img.jpacg.cc")

    AllApiDomain = GlobalItem([
        "picaapi.picacomic.com",
        "post-api.wikawika.xyz",
        "picaapi.go2778.com"
    ])

    AllImgDomain = GlobalItem([
        "s3.picacomic.com",
        "s2.picacomic.com",
        "storage.diwodiwo.xyz",
        "storage1.picacomic.com",
        "storage-b.picacomic.com",
        "img.diwodiwo.xyz",
        "img.tipatipa.xyz",
        "img.picacomic.com",
        "www.picacomic.com",
        "storage.tipatipa.xyz",
        "pica-pica.wikawika.xyz",
        "storage1.go2778.com",
        "diwodiwo.xyz",
        "wikawika.xyz",
        "tipatipa.xyz",
        "picacomic.com",
    ])

    CdnApiUrl = GlobalItem("https://picaapi.picacomic.com")
    CdnImgUrl = GlobalItem("https://storage-b.picacomic.com")

    DohUrlList = GlobalItem(["https://parse.jpacg.cc/parse",
                             "https://doh.pub/dns-query",
                             "https://parse2.jpacg.cc/parse",
                             "https://dot.pub/dns-query"])

    EchDomain = GlobalItem("cloudflare-ech.com")

    # 其他cloudflare域名，启用ech和ip分流
    OtherCloudflareDomain = GlobalItem([
        "raw2.jpacg.cc", 
        "check.jpacg.cc",
        "macapi1.com"])

    ProxyIpList = GlobalItem([
        "158.180.231.216",
        "163.47.42.64",
        "43.170.8.95",
        "150.136.219.11",
        "159.89.91.17",
        "165.232.51.34",
        "172.174.11.248",
        "198.199.84.192",
        "43.153.105.7",
        "43.170.25.96",
        "103.7.138.56",
        "107.151.188.57",
        "107.172.32.207",
        "129.213.150.222",
        "147.75.230.33",
        "192.9.250.241",
        "47.251.95.178",
        "152.70.232.72",
        "95.216.46.85",
        "159.203.34.9",
        "107.172.145.153",
        "46.224.21.216",
        "91.99.20.251",
        "159.60.146.82",
        "204.168.238.95",
        "62.238.51.190",
    ])
    BestCfIpList = GlobalItem([
        "104.18.40.104",
        "172.64.229.155",
        "198.41.208.26",
        "162.159.39.157",  # CF 电信优选
        "188.164.248.179",  # CF 电信优选
        "162.159.32.130",  # CF 电信优选
        "8.39.125.218",  # CF 电信优选
        "172.67.74.21",  # CF 联通优选
        "172.67.74.74",  # CF 联通优选
        "104.26.15.77",  # CF 联通优选
        "104.26.9.248",  # CF 联通优选
        "104.17.159.180",  # CF 移动优选
        "104.18.33.232",  # CF 移动优选
        "172.66.0.147",  # CF 移动优选
        "91.193.58.245",  # CF 移动优选
        "2606:4700:0:f920:12e9:bef7:bd1b:bf3",
        "2606:4700:0:77:ba66:ef50:489c:299d",
        "2606:4700:0:a0:6574:f93:6c28:17c5",
        "2606:4700::2d:a321:64d3",
        "2606:4700:0:a0:a55f:f7f9:5a17:8b8e",
        "2606:4700:0:e0:9996:e26c:4b53:e69a",
        "2606:4700:0:a0:65dc:517c:ad49:a2fd",
        "2606:4700:0:f920:12c2:bb61:198a:ca56",
        "2606:4700:0:e0:c653:a255:83dc:d0c"])

    # 使用sni欺骗，避免
    # SniDomain = GlobalItem(["picacomic.com", "diwodiwo.xyz", "tipatipa.xyz", "wikawika.xyz"])

    # Pica22Params = GlobalItem('{"image-quality": "medium", "user-agent": "okhttp/3.8.1", "app-build-version": "20250144", "app-platform": "android", "app-uuid": "65fa25356ba9a519f4a8982db3ad9a11", "app-version": "2.3.1.20241111", "app-channel": "1", "api-key": "C69BAF41DA5ABD1FFEDC6D2FEA56B", "nonce": "gcawj1sfon03w0rrteciywa5r5l74bmb", "time": "1778921548", "accept": "application/vnd.picacomic.com.v1+json", "Host": "picaapi.picacomic.com", "content-type": "application/json; charset=UTF-8"}')
    # Pica26Params = GlobalItem('{"image-quality": "medium", "user-agent": "okhttp/3.8.1", "app-build-version": "20250144", "app-platform": "android", "app-uuid": "65fa25356ba9a519f4a8982db3ad9a11", "app-version": "2.3.1.20241111", "app-channel": "1", "api-key": "C69BAF41DA5ABD1FFEDC6D2FEA56B", "nonce": "gcawj1sfon03w0rrteciywa5r5l74bmb", "time": "1778921548", "accept": "application/vnd.picacomic.com.v1+json", "Host": "picaapi.picacomic.com", "content-type": "application/json; charset=UTF-8"}')

    def __init__(self):
        pass

    @staticmethod
    def GetAddress(index):
        if index in GlobalConfig.LocalProxyIndex:
            i = GlobalConfig.LocalProxyIndex.index(index)
            # if Setting.PreIpv6.value > 0:
            #     return GlobalConfig.AddressIpv6.value[i]
            # else:
            return [GlobalConfig.Address.value[i]]
        elif index == 4:
            return [Setting.ProxyIpValue.value]
        else:
            return []
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
            # if Setting.PreIpv6.value > 0:
            #     return GlobalConfig.AddressIpv6.value[i]
            # else:
            return [GlobalConfig.Address.value[i]]
        elif index == 4:
            return [Setting.ProxyIpValue.value]
        else:
            return  []

    @staticmethod
    def LoadSetting():
        try:
            newKv = {}
            for k, v in dict(Setting.GlobalConfig.value).items():
                Log.Debug("load global setting, k={}, v={}".format(k, v))
                newKv[k] = v
            oldV = newKv.get("Ver", 0)
            if GlobalConfig.Ver.value > oldV:
                Log.Debug("can not load old config, ver:{}->{}".format(oldV, GlobalConfig.Ver.value))
            else:
                for k, v in newKv.items():
                    value = getattr(GlobalConfig, k, "")
                    if isinstance(value, GlobalItem):
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
