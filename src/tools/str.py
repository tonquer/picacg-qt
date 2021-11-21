from PySide6.QtCore import QObject


class QtStrObj(QObject):
    def __init__(self):
        QObject.__init__(self)


class Str:
    obj = QtStrObj()
    strDict = dict()

    # Enum

    Ok = 1001              # "成功"
    Load = 1002            # "加载"
    Error = 1003           # "错误"
    WaitLoad = 1004        # "等待"
    NetError = 1005        # "网络错误，请检查代理设置"
    UserError = 1006       # "用户名密码错误"
    RegisterError = 1007   # "注册失败"
    UnKnowError = 1008     # "未知错误，"
    NotFoundBook = 1009    # "未找到书籍"
    ParseError = 1010      # "解析出错了"
    NeedGoogle = 1011      # "需要谷歌验证"
    SetHeadError = 1012    # "头像设置出错了, 请尽量选择500kb以下的图片，"
    UnderReviewBook = 1013  # "本子审核中"

    Success = 2001         # "下载完成"
    Reading = 2002         # "获取信息"
    ReadingEps = 2003      # "获取分页"
    ReadingPicture = 2004  # "获取下载地址"
    DownloadCover = 2005   # "正在下载封面"
    Downloading = 2006     # "正在下载"
    Waiting = 2007         # "等待中"
    Pause = 2008           # "暂停"
    DownError = 2009       # "出错了"
    NotFound = 2010        # "原始文件不存在"
    Converting = 2011      # "转换中"
    ConvertSuccess = 2012  # "转换成功"

    DownloadSuc = 3001     # "下载完成"
    DownloadError = 3002   # "下载错误"
    DownloadReset = 3003   # "重新下载"
    WaifuWait = 3004       # "等待中"
    WaifuStateStart = 3005     # "转换开始"
    WaifuStateCancle = 3006    # "不转换"
    WaifuStateEnd = 3007       # "转换完成"
    WaifuStateFail = 3008      # "转换失败"

    LoadingPicture = 1     # "图片加载中..."
    LoadingFail = 2        # "图片加载失败"
    LoginCookie = 3        # "使用Cookie登录"
    LoginUser = 4          # "使用账号登录"
    NotSpace = 5           # "不能为空"
    LoginFail = 6          # "登录失败"

    Menu = 10              # 菜单
    FullSwitch = 11        # 全屏切换
    ReadMode = 12          # 阅读模式

    UpDownScroll = 13      # 上下滚动
    Default = 14           # 默认
    LeftRightDouble = 15   # 左右双页
    RightLeftDouble = 16   # 右左双页
    LeftRightScroll = 17   # 左右滚动
    RightLeftScroll = 18   # 右左滚动
    Scale = 19             # 缩放
    SwitchPage = 20        # 切页
    LastChapter = 21       # 上一章
    NextChapter = 22       # 下一章
    Exit = 23              # 退出
    AutoScroll = 24        # 自动滚动/翻页
    ExitFullScreen = 25    # 退出全屏
    FullScreen = 26        # 全屏
    ContinueRead = 27      # 继续阅读
    Page = 28              # 页
    AlreadyLastPage = 29   # 已经是第一页
    AlreadyNextPage = 30   # 已经最后一页
    AutoSkipLast = 31      # 自动跳转到上一章
    AutoSkipNext = 32      # 自动跳转到下一章
    Position = 33          # 位置
    Resolution = 34        # 分辨率
    Size = 35              # 大小
    State = 36             # 状态
    DownloadNot = 37       # 下载未完成
    NotRecommendWaifu2x = 38  # Waifu2x当前为CPU模式，看图模式下不推荐开启
    StopAutoScroll = 39    # 自动滚动/翻页已停止
    LastPage = 40          # 上一页
    NextPage = 41          # 下一页
    LastScroll = 42        # 上滑
    NextScroll = 43        # 下滑
    NoProxy = 44           # 无代理
    SaveSuc = 45           # 保存成功
    Login = 46             # 登录
    Register = 47          # 注册
    SpeedTest = 48         # 测速
    PasswordShort = 49     # 密码太短
    RegisterSuc = 50       # 注册成功
    ComicFinished = 51     # 完本
    SelectFold = 52        # 选择文件夹
    Save = 53              # 保存
    CommentLoadFail = 54   # 评论加载失败
    Top = 55               # 置顶
    The = 56               # 第
    Floor = 57             # 楼
    DayAgo = 58            # 天前
    HourAgo = 59           # 小时前
    MinuteAgo = 60         # 分钟前
    SecondAgo = 61         # 秒前
    FavoriteNum = 62       # 收藏数
    FavoriteLoading = 63   # 正在加载收藏分页
    Updated = 64           # 更新完成
    Picture = 65           # 图片
    Sending = 66           # "正在发送"
    OnlineNum = 67         # "在线人数"
    AlreadyLastChapter = 68  # 已经是第一章
    AlreadyNextChapter = 69  # 已经最后一章
    ChapterLoadFail = 70     # 章节加载失败
    AddFavoriteSuc = 71      # 添加收藏成功
    Convert = 72             # 转换
    CopySuc = 73             # 复制成功
    HeadUpload = 74          # "头像上传中......"
    Update = 75              # 更新
    AlreadySign = 76         # 已打卡
    Sign = 77                # 打卡
    Hidden = 78              # 屏蔽
    NotHidden = 79           # 取消屏蔽
    OpenDir = 80             # 打开目录
    DeleteRecord = 81        # 删除记录
    DeleteRecordFile = 82    # 删除记录和文件
    SelectEps = 83           # 选择下载章节
    Start = 84               # 开始
    StartConvert = 85        # 开始转换
    PauseConvert = 86        # 暂停转换

    @classmethod
    def Reload(cls):
        cls.strDict[cls.Ok] = cls.obj.tr("成功")
        cls.strDict[cls.Load] = cls.obj.tr("加载")
        cls.strDict[cls.Error] = cls.obj.tr("错误")
        cls.strDict[cls.WaitLoad] = cls.obj.tr("等待")
        cls.strDict[cls.NetError] = cls.obj.tr("网络错误，请检查代理设置")
        cls.strDict[cls.UserError] = cls.obj.tr("用户名密码错误")
        cls.strDict[cls.RegisterError] = cls.obj.tr("注册失败")
        cls.strDict[cls.UnKnowError] = cls.obj.tr("未知错误")
        cls.strDict[cls.NotFoundBook] = cls.obj.tr("未找到书籍")
        cls.strDict[cls.ParseError] = cls.obj.tr("解析出错了")
        cls.strDict[cls.NeedGoogle] = cls.obj.tr("需要谷歌验证")
        cls.strDict[cls.SetHeadError] = cls.obj.tr("头像设置出错了, 请尽量选择500kb以下的图片")
        cls.strDict[cls.UnderReviewBook] = cls.obj.tr("本子审核中")

        cls.strDict[cls.LoadingPicture] = cls.obj.tr("图片加载中...")
        cls.strDict[cls.LoadingFail] = cls.obj.tr("图片加载失败")
        cls.strDict[cls.LoginCookie] = cls.obj.tr("使用Cookie登录")
        cls.strDict[cls.LoginUser] = cls.obj.tr("使用账号登录")
        cls.strDict[cls.NotSpace] = cls.obj.tr("不能为空")
        cls.strDict[cls.LoginFail] = cls.obj.tr("登录失败")
        cls.strDict[cls.Success] = cls.obj.tr("下载完成")
        cls.strDict[cls.Reading] = cls.obj.tr("获取信息")
        cls.strDict[cls.ReadingEps] = cls.obj.tr("获取分页")
        cls.strDict[cls.ReadingPicture] = cls.obj.tr("获取下载地址")
        cls.strDict[cls.DownloadCover] = cls.obj.tr("正在下载封面")
        cls.strDict[cls.Downloading] = cls.obj.tr("正在下载")
        cls.strDict[cls.Waiting] = cls.obj.tr("等待中")
        cls.strDict[cls.Pause] = cls.obj.tr("暂停")
        cls.strDict[cls.DownError] = cls.obj.tr("出错了")
        cls.strDict[cls.NotFound] = cls.obj.tr("原始文件不存在")
        cls.strDict[cls.Converting] = cls.obj.tr("转换中")
        cls.strDict[cls.ConvertSuccess] = cls.obj.tr("转换成功")
        cls.strDict[cls.DownloadSuc] = cls.obj.tr("下载完成")
        cls.strDict[cls.DownloadError] = cls.obj.tr("下载错误")
        cls.strDict[cls.DownloadReset] = cls.obj.tr("重新下载")
        cls.strDict[cls.WaifuWait] = cls.obj.tr("等待中")
        cls.strDict[cls.WaifuStateStart] = cls.obj.tr("转换开始")
        cls.strDict[cls.WaifuStateCancle] = cls.obj.tr("不转换")
        cls.strDict[cls.WaifuStateEnd] = cls.obj.tr("转换完成")
        cls.strDict[cls.WaifuStateFail] = cls.obj.tr("转换失败")

        cls.strDict[cls.Menu] = cls.obj.tr("菜单")
        cls.strDict[cls.FullSwitch] = cls.obj.tr("全屏切换")
        cls.strDict[cls.ReadMode] = cls.obj.tr("阅读模式")
        cls.strDict[cls.UpDownScroll] = cls.obj.tr("上下滚动")
        cls.strDict[cls.Default] = cls.obj.tr("默认")
        cls.strDict[cls.LeftRightDouble] = cls.obj.tr("左右双页")
        cls.strDict[cls.RightLeftDouble] = cls.obj.tr("右左双页")
        cls.strDict[cls.LeftRightScroll] = cls.obj.tr("左右滚动")
        cls.strDict[cls.RightLeftScroll] = cls.obj.tr("右左滚动")
        cls.strDict[cls.Scale] = cls.obj.tr("缩放")
        cls.strDict[cls.SwitchPage] = cls.obj.tr("切页")
        cls.strDict[cls.LastChapter ]= cls.obj.tr("上一章")
        cls.strDict[cls.NextChapter] = cls.obj.tr("下一章")
        cls.strDict[cls.Exit] = cls.obj.tr("退出")
        cls.strDict[cls.AutoScroll] = cls.obj.tr("自动滚动/翻页")
        cls.strDict[cls.ExitFullScreen] = cls.obj.tr("退出全屏")
        cls.strDict[cls.FullScreen] = cls.obj.tr("全屏")
        cls.strDict[cls.ContinueRead] = cls.obj.tr("继续阅读")
        cls.strDict[cls.Page] = cls.obj.tr("页")
        cls.strDict[cls.AlreadyLastPage] = cls.obj.tr("已经是第一页")
        cls.strDict[cls.AlreadyNextPage] = cls.obj.tr("已经最后一页")
        cls.strDict[cls.AutoSkipLast] = cls.obj.tr("自动跳转到上一章")
        cls.strDict[cls.AutoSkipNext] = cls.obj.tr("自动跳转到下一章")
        cls.strDict[cls.Position] = cls.obj.tr("位置")
        cls.strDict[cls.Resolution] = cls.obj.tr("分辨率")
        cls.strDict[cls.Size] = cls.obj.tr("大小")
        cls.strDict[cls.State] = cls.obj.tr("状态")
        cls.strDict[cls.DownloadNot] = cls.obj.tr("下载未完成")
        cls.strDict[cls.NotRecommendWaifu2x] = cls.obj.tr("Waifu2x当前为CPU模式，看图模式下不推荐开启")
        cls.strDict[cls.StopAutoScroll] = cls.obj.tr("自动滚动/翻页已停止")
        cls.strDict[cls.LastPage] = cls.obj.tr("上一页")
        cls.strDict[cls.NextPage] = cls.obj.tr("下一页")
        cls.strDict[cls.LastScroll] = cls.obj.tr("上滑")
        cls.strDict[cls.NextScroll] = cls.obj.tr("下滑")

        cls.strDict[cls.NoProxy] = cls.obj.tr("无代理")
        cls.strDict[cls.SaveSuc] = cls.obj.tr("保存成功")
        cls.strDict[cls.Login] = cls.obj.tr("登录")
        cls.strDict[cls.Register] = cls.obj.tr("注册")
        cls.strDict[cls.SpeedTest] = cls.obj.tr("测速")
        cls.strDict[cls.PasswordShort] = cls.obj.tr("密码太短")
        cls.strDict[cls.RegisterSuc] = cls.obj.tr("注册成功")
        cls.strDict[cls.ComicFinished] = cls.obj.tr("完本")
        cls.strDict[cls.SelectFold] = cls.obj.tr("选择文件夹")
        cls.strDict[cls.Save] = cls.obj.tr("保存")
        cls.strDict[cls.CommentLoadFail] = cls.obj.tr("评论加载失败")
        cls.strDict[cls.Top] = cls.obj.tr("置顶")
        cls.strDict[cls.The] = cls.obj.tr("第")
        cls.strDict[cls.Floor] = cls.obj.tr("楼")
        cls.strDict[cls.DayAgo] = cls.obj.tr("天前")
        cls.strDict[cls.HourAgo] = cls.obj.tr("小时前")
        cls.strDict[cls.MinuteAgo] = cls.obj.tr("分钟前")
        cls.strDict[cls.SecondAgo] = cls.obj.tr("秒前")
        cls.strDict[cls.FavoriteNum] = cls.obj.tr("收藏数")
        cls.strDict[cls.FavoriteLoading] = cls.obj.tr("正在加载收藏分页")
        cls.strDict[cls.Updated] = cls.obj.tr("更新完成")
        cls.strDict[cls.Picture] = cls.obj.tr("图片")
        cls.strDict[cls.Sending] = cls.obj.tr("正在发送")
        cls.strDict[cls.OnlineNum] = cls.obj.tr("在线人数")
        cls.strDict[cls.AlreadyLastChapter] = cls.obj.tr("已经是第一章")
        cls.strDict[cls.AlreadyNextChapter] = cls.obj.tr("已经最后一章")
        cls.strDict[cls.ChapterLoadFail] = cls.obj.tr("章节加载失败")
        cls.strDict[cls.AddFavoriteSuc] = cls.obj.tr("添加收藏成功")
        cls.strDict[cls.Convert] = cls.obj.tr("转换")
        cls.strDict[cls.CopySuc] = cls.obj.tr("复制成功")
        cls.strDict[cls.HeadUpload] = cls.obj.tr("头像上传中......")
        cls.strDict[cls.Update] = cls.obj.tr("更新")
        cls.strDict[cls.AlreadySign] = cls.obj.tr("已打卡")
        cls.strDict[cls.Sign] = cls.obj.tr("打卡")
        cls.strDict[cls.Hidden] = cls.obj.tr("屏蔽")
        cls.strDict[cls.NotHidden] = cls.obj.tr("取消屏蔽")
        cls.strDict[cls.OpenDir] = cls.obj.tr("打开目录")
        cls.strDict[cls.DeleteRecord] = cls.obj.tr("删除记录")
        cls.strDict[cls.DeleteRecordFile] = cls.obj.tr("删除记录和文件 ")
        cls.strDict[cls.SelectEps] = cls.obj.tr("选择下载章节")
        cls.strDict[cls.Start] = cls.obj.tr("开始")
        cls.strDict[cls.StartConvert] = cls.obj.tr("开始转换")
        cls.strDict[cls.PauseConvert] = cls.obj.tr("暂停转换")

    @classmethod
    def GetStr(cls, enumType):
        return cls.strDict.get(enumType, "")