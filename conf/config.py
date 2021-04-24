import sys

BaseUrl = "http://68.183.234.72/"            # 获得ip列表接口
Url = "https://picaapi.picacomic.com/"       # 域名
ApiKey = "C69BAF41DA5ABD1FFEDC6D2FEA56B"     # apiKey
AppChannel = "3"
Version = "2.2.1.3.3.4"                      # 版本号
BuildVersion = "45"
Accept = "application/vnd.picacomic.com.v1+json"
Agent = "okhttp/3.8.1"
Platform = "android"

ThreadNum = 10                                # 线程
DownloadThreadNum = 5                        # 下载线程
ImageQuality = "original"                    # 画质，original, low, medium, high
Uuid = "defaultUuid"
HttpProxy = ""                               # 代理
ChatProxy = 1                             # 聊天室启用代理
ChatSavePath = "chat"

SavePath = ''
SavePathDir = "commies"       # 下载目录
ResetCnt = 5                  # 下载重试次数

IsUseCache = True             # 是否使用cache
CachePathDir = "cache"        # cache目录
# CacheExpired = 24 * 60 * 60    # cache过期时间24小时
PreLoading = 5    # 预加载5页

IsLoadingPicture = True

UpdateUrl = "https://github.com/tonquer/picacg-windows/releases/latest"
UpdateUrl2 = "https://github.com/tonquer/picacg-windows/releases"
UpdateVersion = "v1.1.5"

# waifu2x
CanWaifu2x = True
ErrorMsg = ""

Encode = 0
Waifu2xThread = 2
Format = "jpg"
Waifu2xPath = "waifu2x"
IsOpenWaifu = True

LookModel = 0       # 默认值
DownloadModel = 0   # 默认值
LogIndex = 0


Model0 = "cunet"     # 通用
Model1 = "cunet"     # 通用
Model2 = "photo"     # 写真
Model3 = "anime_style_art_rgb"  # 动漫

