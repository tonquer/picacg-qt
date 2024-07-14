from config import config
from tools.log import Log
from tools.singleton import Singleton
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class CategoryInfo(object):
    def __init__(self):
        self._id = ""
        self.title = ""

    @property
    def id(self):
        return self._id


class User(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.userId = ""
        self.passwd = ""
        self.isLogin = False
        self.initRes = None

        self.token = ""
        self.page = 1       # 当前收藏
        self.pages = 1      # 收藏页
        self.category = {}  # 收藏夹 page: 收藏列表
        self.total = 0      # 累计收藏

        self.name = ""      # 姓名
        self.level = 0      # 等级
        self.exp = 0        # 经验
        self.created = ""   # 创建日期
        self.title = ""     # 称号
        self.gender = ""    # 性别
        self.isPunched = False  # 是否签到
        self.userInfo = {}

        self.avatar = {}

        # self.addresss = ['104.20.180.50', '104.20.181.50']  # 列表
        self.imageServer = 'storage.wikawika.xyz'
        self.searchCache = []

    @property
    def server(self):
        from server.server import Server
        return Server()

    @property
    def address(self):
        return self.server.address

    @address.setter
    def address(self, value):
        self.server.address = value

    # def InitBack(self, backData):
    #     try:
    #         if backData.status == Status.Ok and backData.res.status == "ok":
    #
    #             from config.setting import Setting
    #             if len(backData.res.address) >= 1:
    #                 # 只更新分流三 第一个地址
    #                 config.Address[1] = backData.res.address[0]
    #                 Setting.SaveCacheAddress.SetValue(backData.res.address[0])
    #             #     self.address = backData.res.addresses[0]
    #             Log.Info("初始化成功,  Ips:{}, {}".format(backData.res.address, config.Address))
    #             # 需要更新DNS
    #             if Setting.ProxySelectIndex.value == 3:
    #                 imageServer = config.ImageServer3
    #                 address = config.Address[1]
    #                 if not Setting.PreIpv6.value:
    #                     self.server.UpdateDns(address, imageServer)
    #             self.initRes = backData.res
    #             return Status.Ok
    #         else:
    #             Log.Info("初始化失败, info:{}".format(backData.res))
    #             return Status.Error
    #     except Exception as es:
    #         Log.Error(es)
    #         return Status.Error

    # def InitImageServer(self, backData):
    #     try:
    #         if self.server.address:
    #             self.server.imageServer = self.imageServer
    #         if backData.res.code == 200:
    #             # 选择了分流才设置
    #             # if self.server.address:
    #             #     self.server.imageServer = ToolUtil.GetUrlHost(backData.res.data["imageServer"])
    #             #     Log.Info("初始化图片服务器成功, info:{}".format(self.server.imageServer))
    #
    #             return Status.Ok
    #         else:
    #             return Status.Error
    #     except Exception as es:
    #         Log.Error(es)
    #         return Status.Error

    def SetUserInfo(self, userId, passwd):
        self.userId = userId
        self.passwd = passwd
        return

    def SetToken(self, token):
        self.token = token
        self.server.token = token

    def LoginBack(self, backData):
        try:
            if backData.status != Status.Ok:
                return backData.status, ""

            if backData.res.code == 200 and backData.res.data.get("token"):
                self.isLogin = True
                token = backData.res.data.get("token")
                Log.Info("登陆成功，userId: {}".format(self.userId))
                # if self.server.address:
                    # self.server.Send(req.InitAndroidReq())
                return Status.Ok, token
            elif backData.res.code == 400:
                Log.Info("登陆失败！！！, userId:{}, code:{}, text:{}".format(self.userId, str(backData.res.code), backData.res.GetText()))
                if backData.res.error == "1004":
                    return Status.UserError, ""
                return Status.Error, ""
            else:
                Log.Info("登陆失败！！！, userId:{}, code:{}, text:{}".format(self.userId, str(backData.res.code), backData.res.GetText()))
                return Status.UnKnowError, ""
        except Exception as es:
            Log.Error(es)
            return Status.NetError, ""

    def Logout(self):
        self.server.token = ""
        self.isLogin = False
        self.userId = ""
        self.passwd = ""
        return

    def UpdateUserInfoBack(self, backData):
        try:
            if backData.res.code == 200:
                self.userInfo = backData.res.data["user"]
                self.name = backData.res.data["user"]["name"]
                self.level = backData.res.data["user"]["level"]
                self.exp = backData.res.data["user"]["exp"]
                self.created = backData.res.data["user"]["created_at"]
                self.gender = backData.res.data["user"]["gender"]
                self.title = backData.res.data["user"]["title"]
                self.title = backData.res.data["user"]["title"]
                self.isPunched = backData.res.data["user"]["isPunched"]
                self.avatar = backData.res.data["user"].get("avatar")
        except Exception as es:
            Log.Error(es)
            return Status.NetError

    def PunchedBack(self, backData):
        if backData.res.code == 200:
            Log.Info("签到成功")
            # self.UpdateUserInfo()
            # self.UpdateFavorites()
            return Status.Ok
        else:
            Log.Info("签到失败！！！, userId:{}, msg:{}".format(self.userId, backData.res.message))
            return Status.Error

    def RegisterBack(self, backData):
        try:
            if backData.status != Status.Ok:
                return backData.status
            if backData.res.code == 200:
                Log.Info("注册成功: {}".format(backData.res.raw.text))
                return Status.Ok
            elif backData.res.code == 400:
                Log.Info("注册失败！！！, userId:{}, msg:{}".format(self.userId, backData.res.message))
                if backData.res.message == "email is already exist":
                    return Str.AccountAlready
                elif backData.res.message == "validation error":
                    return Str.NotAdult

                return Status.RegisterError
            else:
                return Status.RegisterError
        except Exception as es:
            Log.Error(es)
            return Status.NetError

    def UpdateFavoritesBack(self, backData):
        try:
            if backData.status != Status.Ok:
                return backData.status, self.page
            if backData.res.code == 200:
                info = backData.res.data.get("comics", {})
                self.total = info["total"]
                self.page = info["page"]
                self.pages = info["pages"]
                self.category[self.page] = []
                for bookInfo in info["docs"]:
                    data = CategoryInfo()
                    ToolUtil.ParseFromData(data, bookInfo)
                    self.category[self.page].append(data)
                Log.Info("收藏夹加载成功, page:{}, pages:{}, num:{}".format(self.page, self.pages, self.total))
                return Status.Ok, self.page
            else:
                return Status.Error + backData.res.message, self.page
        except Exception as es:
            Log.Error(es)
            return Status.Error, self.page
