BaseUrl = "http://68.183.234.72/"            # 获得ip列表接口
Url = "https://picaapi.picacomic.com/"       # 域名
ApiKey = "C69BAF41DA5ABD1FFEDC6D2FEA56B"     # apiKey
AppChannel = "3"
Version = "2.2.1.3.3.4"                      # 版本号
BuildVersion = "45"
Accept = "application/vnd.picacomic.com.v1+json"
Agent = "okhttp/3.8.1"
Platform = "android"

IsUpdate = 1                   # 是否在启动时检查更新
Language = 'Chinese-Simplified'           # 选择的语言
ThreadNum = 10                 # 线程
DownloadThreadNum = 5          # 下载线程
ImageQuality = "original"      # 画质，original, low, medium, high
Uuid = "defaultUuid"
IsHttpProxy = 0                # 是否启用代理
HttpProxy = ""                 # 代理
ChatProxy = 1                  # 聊天室启用代理
ChatSavePath = "chat"

SavePath = ''
SavePathDir = "commies"        # 下载目录
ResetCnt = 5                   # 下载重试次数

IsUseCache = True              # 是否使用cache
CachePathDir = "cache"         # cache目录
# CacheExpired = 24 * 60 * 60  # cache过期时间24小时
PreLoading = 10                # 预加载5页

IsLoadingPicture = True

UpdateUrl = "https://github.com/tonquer/picacg-pyqt/releases/latest"
UpdateUrlBack = "https://hub.fastgit.org/tonquer/picacg-pyqt/releases/latest"
UpdateUrl2 = "https://github.com/tonquer/picacg-pyqt/releases"
UpdateUrl2Back = "https://hub.fastgit.org/tonquer/picacg-pyqt/releases"

DatabaseUpdate = "https://raw.githubusercontent.com/bika-robot/picacg-database/main/version.txt"
DatabaseDownload = "https://raw.githubusercontent.com/bika-robot/picacg-database/main/data/"
UpdateVersion = "v1.2.5"

# waifu2x
CanWaifu2x = True
ErrorMsg = ""

Encode = 0
Waifu2xThread = 2
Format = "jpg"
Waifu2xPath = "waifu2x"
IsOpenWaifu = 0

ThemeText = ""  # 主题

LogIndex = 0    # Warn Info Debug
IsTips = 1

ChatSendAction = 2

DownloadModel = 0
DownloadNoise = 3
DownloadScale = 2.0
DownloadAuto = 0

# 看图模式
LookModel = 0
LookNoise = 3
LookScale = 2.0

LookReadMode = 1      # 看图模式
# LookReadScale = 2     # 默认缩放
LookReadFull = 0      # 是否全屏

# 代理与分流相关
ProxyUrl = "https://github.com/tonquer/picacg-windows/discussions/48"

ProxySelectIndex = 1
IsUseHttps = 1   # 使用Https

Address = ['104.20.180.50', '104.20.181.50']  # 分类2，3 Ip列表
ImageServer = 'storage.wikawika.xyz'          # 分流2，3 使用的图片服务器

ApiDomain = [
    "picaapi.picacomic.com",
]

ImageDomain = [
    "storage.wikawika.xyz",
    "storage1.picacomic.com",
    "img.tipatipa.xyz",
    "img.picacomic.com",
    "pica-pica.wikawika.xyz",
    "www.picacomic.com"
]

# https://www.cloudflare.com/zh-cn/ips/
# https://cloud.tencent.com/developer/article/1675133
PreferCDNIP = "1.0.0.1"   # CloudFlare的优选Ip，
