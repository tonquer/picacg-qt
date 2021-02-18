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
SavePath = ''
SavePathDir = "commies"       # 下载目录
ResetCnt = 5                  # 下载重试次数

IsUseCache = True             # 是否使用cache
CachePathDir = "cache"        # cache目录
# CacheExpired = 24 * 60 * 60    # cache过期时间24小时
PreLoading = 10    # 预加载10页

IsLoadingPicture = True

UpdateUrl = "https://github.com/tonquer/picacg-windows/releases/latest"
UpdateVersion = "v1.0.6"

# waifu2x
Encode = 0
Waifu2xThread = 1
Scale = 2
Noise = 3
Format = "jpg"
Model = 2
Waifu2xPath = "waifu2x"
IsOpenWaifu = True

Model2 = "models-cunet"
