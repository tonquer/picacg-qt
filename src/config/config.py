BaseUrl = "http://68.183.234.72/"            # 获得ip列表接口
Url = "https://picaapi.picacomic.com/"       # 域名
ApiKey = "C69BAF41DA5ABD1FFEDC6D2FEA56B"     # apiKey
AppChannel = "3"
Version = "2.2.1.3.3.4"                      # 版本号
BuildVersion = "45"
Accept = "application/vnd.picacomic.com.v1+json"
Agent = "okhttp/3.8.1"
Platform = "android"
ImageQuality = "original"      # 画质，original, low, medium, high
Uuid = "defaultUuid"


ThreadNum = 10                 # 线程
DownloadThreadNum = 5          # 下载线程
ConvertThreadNum = 3           # 同时转换数量
ChatSavePath = "chat"
SavePathDir = "commies"        # 下载目录
ResetCnt = 5                   # 下载重试次数

IsUseCache = True              # 是否使用cache
CachePathDir = "cache"         # cache目录
# CacheExpired = 24 * 60 * 60  # cache过期时间24小时
PreLoading = 10                # 预加载5页
PreLook = 4                    # 预显示

IsLoadingPicture = True

UpdateUrl = "https://github.com/tonquer/picacg-qt/releases/latest"
UpdateUrlApi = "https://api.github.com/repos/tonquer/picacg-qt/releases"
UpdateUrlBack = "https://github.com/tonquer/picacg-qt"

UpdateUrl2 = "https://hub.ggo.icu/tonquer/picacg-qt/releases/latest"
UpdateUrl2Api = "https://api.ggo.icu/repos/tonquer/picacg-qt/releases"
UpdateUrl2Back = "https://hub.ggo.icu/tonquer/picacg-qt"

UpdateUrl3 = "https://hub.fastgit.xyz/tonquer/picacg-qt/releases/latest"
UpdateUrl3Api = "https://api.fastgit.xyz/repos/tonquer/picacg-qt/releases"
UpdateUrl3Back = "https://hub.fastgit.xyz/tonquer/picacg-qt"

DatabaseUpdate = "https://raw.ggo.icu/bika-robot/picacg-database/main/version3.txt"
DatabaseDownload = "https://raw.ggo.icu/bika-robot/picacg-database/main/data3/"

DatabaseUpdate2 = "https://raw.githubusercontent.com/bika-robot/picacg-database/main/version3.txt"
DatabaseDownload2 = "https://raw.githubusercontent.com/bika-robot/picacg-database/main/data3/"

DatabaseUpdate3 = "https://raw.fastgit.org/bika-robot/picacg-database/main/version3.txt"
DatabaseDownload3 = "https://raw.fastgit.org/bika-robot/picacg-database/main/data3/"

Issues1 = "https://github.com/tonquer/picacg-qt/issues"
Issues2 = "https://hub.ggo.icu/tonquer/picacg-qt/issues"
Issues3 = "https://hub.fastgit.xyz/tonquer/picacg-qt/issues"

UpdateVersion = "v1.4.3"
RealVersion = "v1.4.3"
TimeVersion = "2023-2-25"

Waifu2xVersion = "1.1.6"


# waifu2x
CanWaifu2x = True
ErrorMsg = ""

Encode = 0             # 当前正在使用的索引
UseCpuNum = 0
EncodeGpu = ""

Format = "jpg"
Waifu2xPath = "waifu2x"

IsTips = 1

# 代理与分流相关
ProxyUrl1 = "https://github.com/tonquer/picacg-qt/discussions/48"
ProxyUrl2 = "https://hub.ggo.icu/tonquer/picacg-qt/discussions/48"
ProxyUrl3 = "https://hub.fastgit.xyz/tonquer/picacg-qt/discussions/48"

# Waifu2x相关
Waifu2xUrl = "https://github.com/tonquer/picacg-qt/discussions/76"

Address = ["188.114.98.153", "104.21.91.145"]  # 分类2，3 Ip列表

ImageServer2 = 's3.picacomic.com'          # 分流2 使用的图片服务器
ImageServer2Jump = 'img.picacomic.com'          # 分流2 跳转的图片服务器

ImageServer3 = 'storage.diwodiwo.xyz'          # 分流3 使用的图片服务器

ProxyApiDomain = "bika-api.ggo.icu"
ProxyImgDomain = "bika-img.ggo.icu"

ProxyApiDomain2 = "bika2-api.ggo.icu"
ProxyImgDomain2 = "bika2-img.ggo.icu"

ApiDomain = [
    "picaapi.picacomic.com",
    "post-api.wikawika.xyz"
]

ImageDomain = [
    "s3.picacomic.com",
    "storage.diwodiwo.xyz",
    "storage1.picacomic.com",
    "img.tipatipa.xyz",
    "img.picacomic.com",
    "storage.tipatipa.xyz",
    # "pica-pica.wikawika.xyz",
    "www.picacomic.com",
    "storage-b.picacomic.com",

]
