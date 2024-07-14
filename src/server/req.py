import base64
import os
import platform
import random
import uuid
from datetime import datetime, timedelta
from urllib.parse import quote

from config import config
from config.setting import Setting
from tools.tool import ToolUtil


class ServerReq(object):
    def __init__(self, url, header=None, params=None, method="POST") -> None:
        self.url = url
        self.file = ""
        self.token = ""
        self.headers = header
        self.params = params
        self.method = method
        self.isParseRes = True
        self.useImgProxy = True
        self.isUseHttps = bool(Setting.IsUseHttps.value)
        self.proxyUrl = ""

        host = ToolUtil.GetUrlHost(url)
        self.timeout = 5
        IsApi = False
        IsImg = False
        if host in config.ApiDomain:
            IsApi = True
            self.timeout = Setting.ApiTimeOut.GetIndexV()
        if host in config.ImageDomain:
            IsImg = True
            self.timeout = Setting.ImgTimeOut.GetIndexV()

        if IsApi and Setting.ProxySelectIndex.value == 5:
            self.headers.pop("user-agent")
            self.proxyUrl = config.ProxyApiDomain
        if IsImg and Setting.ProxyImgSelectIndex.value == 5:
            self.headers.pop("user-agent")
            self.proxyUrl = config.ProxyImgDomain

        if IsApi and Setting.ProxySelectIndex.value == 6:
            self.headers.pop("user-agent")
            self.proxyUrl = config.ProxyApiDomain2
        if IsImg and Setting.ProxyImgSelectIndex.value == 6:
            self.headers.pop("user-agent")
            self.proxyUrl = config.ProxyImgDomain2

        if Setting.IsHttpProxy.value == 1:
            self.proxy = {"http": Setting.HttpProxy.value, "https": Setting.HttpProxy.value}
        elif Setting.IsHttpProxy.value == 3:
            self.proxy = {}
        else:
            self.proxy = {"http": None, "https": None}

    def __str__(self):
        # if Setting.LogIndex.value == 0:
        #     return self.__class__.__name__
        # elif Setting.LogIndex.value == 1:
        #     return "{}, url:{}".format(self.__class__.__name__, self.url)
        # headers = dict()
        # headers.update(self.headers)
        # if Setting.LogIndex.value == 1 and "authorization" in headers:
        #     headers["authorization"] = "**********"
        params = dict()
        params.update(self.params)
        ## 脱敏数据
        # if self.__class__.__name__ in ["LoginReq", "RegisterReq"]:
        #     params = "******"
        # if Setting.LogIndex.value == 1 and "password" in params:
        #     params["password"] = "******"
        return "{}, url:{}, method:{}, params:{}".format(self.__class__.__name__, self.url, self.method, params)


# 获得分流Ip
class InitReq(ServerReq):
    def __init__(self):
        url = config.BaseUrl + "init"
        method = "GET"
        super(self.__class__, self).__init__(url, {}, {}, method)


# 获得分流 Image的Key
class InitAndroidReq(ServerReq):
    def __init__(self):
        url = config.Url + "init?platform=android"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 登陆
class LoginReq(ServerReq):
    def __init__(self, user: str, passwd: str):
        url = config.Url + "auth/sign-in"
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {"email": user, "password": passwd}, method)


# 注册
class RegisterReq(ServerReq):
    def __init__(self, data):
        # data = {
        #     "email": email,
        #     "password": password,
        #     "name": name,
        #     "birthday": birthday,
        #     "gender": gender,  # m, f, bot
        #     "answer1": answer1,
        #     "answer2": answer2,
        #     "answer3": answer3,
        #     "question1": question1,
        #     "question2": question2,
        #     "question3": question3
        # }
        url = config.Url + "auth/register"
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             data, method)


# 忘记密码
class ForgotPasswordReq(ServerReq):
    def __init__(self, email):
        data = {
            "email": email
        }
        url = config.Url + "auth/forgot-password"
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             data, method)


# 重置密码
class ResetPasswordReq(ServerReq):
    def __init__(self, email, questionNo, answer):
        data = {
            "email": email,
            "questionNo": questionNo,
            "answer": answer,
        }
        url = config.Url + "auth/reset-password"
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             data, method)


# 修改密码
class ChangePasswordReq(ServerReq):
    def __init__(self, token, oldPassword, newPassword):
        data = {
            "new_password": newPassword,
            "old_password": oldPassword
        }
        url = config.Url + "users/password"
        method = "PUT"
        hearder = ToolUtil.GetHeader(url, method)
        super(self.__class__, self).__init__(url, hearder, data, method)
        self.token = token


# 获得用户信息
class GetUserInfo(ServerReq):
    def __init__(self):
        url = config.Url + "users/profile"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得我的评论
class GetUserCommentReq(ServerReq):
    def __init__(self, id="", page=1):
        self.id = id
        url = config.Url + "users/my-comments?page={}".format(str(page))
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 设置头像
class SetAvatarInfoReq(ServerReq):
    def __init__(self, data, picFormat="jpg"):
        url = config.Url + "users/avatar"
        method = "PUT"
        if picFormat[-3:] == "png":
            picFormat = "png"
        else:
            picFormat = "jpeg"

        imgData = base64.b64encode(data).decode("utf-8")
        imgData = "data:image/" + picFormat + ";base64," + imgData
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {"avatar": imgData}, method)


# 设置称号
class SetTitleReq(ServerReq):
    def __init__(self, userId, title):
        url = config.Url + "users/{}/title".format(userId)
        method = "PUT"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {"title": title}, method)


# 签到
class PunchIn(ServerReq):
    def __init__(self):
        url = config.Url + "users/punch-in"
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获取目录
class CategoryReq(ServerReq):
    def __init__(self):
        url = config.Url + "categories"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 获得收藏
class FavoritesReq(ServerReq):
    def __init__(self, page="", sort="da"):
        url = config.Url + "users/favourite?s={}&page={}".format(sort, page)
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 添加收藏
class FavoritesAdd(ServerReq):
    def __init__(self, bookId):
        url = config.Url + "comics/{}/favourite".format(bookId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 添加爱心
class BookLikeReq(ServerReq):
    def __init__(self, bookId):
        url = config.Url + "comics/{}/like".format(bookId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 高级搜索
class AdvancedSearchReq(ServerReq):
    def __init__(self, page, categories, keyword="", sort=""):
        url = config.Url + "comics/advanced-search?page={}".format(page)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {"categories": categories, "keyword": keyword, "sort": sort}, method)


# 分类搜索
class CategoriesSearchReq(ServerReq):
    def __init__(self, page, categories, sort=""):
        categories = quote(categories)
        url = config.Url + "comics?page={}&c={}&s={}".format(page, categories, sort)
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 排行榜
class RankReq(ServerReq):
    def __init__(self, data):
        url = config.Url + "comics/leaderboard?tt={}&ct=VC".format(data)
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 骑士榜
class KnightRankReq(ServerReq):
    def __init__(self):
        url = config.Url + "comics/knight-leaderboard"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 获得一本书
class GetComicsBookReq(ServerReq):
    def __init__(self, bookId=""):
        url = config.Url + "comics/{}".format(bookId)
        method = "GET"
        self.bookId = bookId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得一本书章节列表
class GetComicsBookEpsReq(ServerReq):
    def __init__(self, bookId="", page="1"):
        url = config.Url + "comics/{}/eps?page={}".format(bookId, page)
        method = "GET"
        self.bookId = bookId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得一个章节的图片信息
class GetComicsBookOrderReq(ServerReq):
    def __init__(self, bookId="", epsId="", page="1"):
        url = config.Url + "comics/{}/order/{}/pages?page={}".format(bookId, epsId, page)
        method = "GET"
        self.bookId = bookId
        self.epsId = epsId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得推荐信息
class GetComicsRecommendation(ServerReq):
    def __init__(self, bookId=""):
        url = config.Url + "comics/{}/recommendation".format(bookId)
        method = "GET"
        self.bookId = bookId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 下载图片
class DownloadBookReq(ServerReq):
    def __init__(self, url, loadPath="", cachePath="", savePath="", isReload=False, resetCnt=1):
        method = "Download"
        self.url = url
        self.loadPath = loadPath
        self.cachePath = cachePath
        self.savePath = savePath
        self.isReload = isReload
        self.resetCnt = resetCnt
        self.isReset = False
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)

# 获得评论
class GetCommentsReq(ServerReq):
    def __init__(self, bookId="", page=1):
        url = config.Url + "comics/{}/comments?page={}".format(bookId, page)
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 评论点赞
class CommentsLikeReq(ServerReq):
    def __init__(self, commentId=""):
        url = config.Url + "comments/{}/like".format(commentId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 评论举报
class CommentsReportReq(ServerReq):
    def __init__(self, commentId=""):
        url = config.Url + "comments/{}/report".format(commentId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 检查更新
class CheckUpdateReq(ServerReq):
    def __init__(self, isPre=False):
        method = "GET"
        data = dict()
        data["version"] = config.UpdateVersion
        data["platform"] = platform.platform()
        if not isPre:
            url = config.AppUrl + "/version.txt?"
        else:
            url = config.AppUrl + "/version_pre.txt?"
        url += ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False
        self.useImgProxy = False


# 检查更新
class CheckUpdateInfoReq(ServerReq):
    def __init__(self, newVersion):
        method = "GET"
        data = dict()
        data["version"] = config.UpdateVersion
        data["platform"] = platform.platform()
        url = config.AppUrl + "/{}.txt?".format(newVersion)
        url += ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False
        self.useImgProxy = False


# 检查更新配置
class CheckUpdateConfigReq(ServerReq):
    def __init__(self):
        method = "GET"
        data = dict()
        data["version"] = config.UpdateVersion
        data["platform"] = platform.platform()
        url = config.AppUrl + "/config.txt?"
        url += ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False
        self.useImgProxy = False

# 检查更新
class CheckUpdateDatabaseReq(ServerReq):
    def __init__(self, url):
        method = "GET"
        header = {
            "Pragma": "No-cache",
            "Cache-Control": "no-cache",
            "Expires": '0',
            "version": config.UpdateVersion,
        }
        super(self.__class__, self).__init__(url, header, {}, method)
        self.isParseRes = False
        self.useImgProxy = False


# 下载
class DownloadDatabaseReq(ServerReq):
    def __init__(self, url, tick):
        import time
        day = time.strftime('%Y-%m-%d', time.localtime(tick))
        url = url + day + ".data"
        method = "GET"
        header = {
            "Pragma": "No-cache",
            "Cache-Control": "no-cache",
            "Expires": '0',
            "version": config.UpdateVersion,
        }
        super(self.__class__, self).__init__(url, header, {}, method)
        self.isParseRes = False
        self.useImgProxy = False


# 下载
class DownloadDatabaseWeekReq(ServerReq):
    def __init__(self, url, tick):
        import time
        curTime = datetime.fromtimestamp(tick)
        curEndTime = curTime + timedelta(6-curTime.weekday())
        newTick = curEndTime.timestamp()

        day = time.strftime('%Y-%m-%d', time.localtime(newTick))
        url = url +"week/"+ day + "_week.data"
        method = "GET"
        header = {
            "Pragma": "No-cache",
            "Cache-Control": "no-cache",
            "Expires": '0',
            "version": config.UpdateVersion,
        }
        super(self.__class__, self).__init__(url, header, {}, method)
        self.isParseRes = False
        self.useImgProxy = False


# 热词
class GetKeywords(ServerReq):
    def __init__(self):
        url = config.Url + "keywords"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 发送评论
class SendCommentReq(ServerReq):
    def __init__(self, bookId="", content=""):
        url = config.Url + "comics/{}/comments".format(bookId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {"content": content}, method)


# 发送子评论
class SendCommentChildrenReq(ServerReq):
    def __init__(self, comentId="", content=""):
        url = config.Url + "comments/{}".format(comentId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {"content": content}, method)


# 查看子评论
class GetCommentsChildrenReq(ServerReq):
    def __init__(self, comentId="", page=1):
        url = config.Url + "comments/{}/childrens?page={}".format(comentId, page)
        method = "Get"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 测速
class SpeedTestReq(ServerReq):
    Index = 0
    URLS = [
        "https://storage1.picacomic.com/static/fc75975a-af8e-40c5-8679-725d6f64d6f5.jpg",
        # "https://storage1.picacomic.com/static/5aa5c52b-8fb5-4c16-866c-d6d92fb4a761.jpg",
        # "https://storage1.picacomic.com/static/7e7d1320-9717-4702-883d-2899975283b2.jpg",
        # "https://storage1.picacomic.com/static/91c3f41a-e6de-4de1-a80f-10af17aee5a8.jpg",
        # "https://storage1.picacomic.com/static/60c852b9-e47d-400c-af9d-bee86ce20b6d.jpg",
        # "https://storage1.picacomic.com/static/66541fe6-caaa-4965-ac1a-1b1b793e5677.jpg",
    ]

    def __init__(self):
        url = SpeedTestReq.URLS[SpeedTestReq.Index]
        SpeedTestReq.Index += 1
        if SpeedTestReq.Index >= len(SpeedTestReq.URLS):
            SpeedTestReq.Index = 0
        method = "Download"
        host = ToolUtil.GetUrlHost(url)
        if host in config.ApiDomain and Setting.ProxySelectIndex.value == 5:
            self.headers.pop("user-agent")
            self.proxyUrl = config.ProxyApiDomain

        header = ToolUtil.GetHeader(url, method)
        header['cache-control'] = 'no-cache'
        header['expires'] = '0'
        header['pragma'] = 'no-cache'
        self.isReload = False
        self.resetCnt = 1
        self.isReset = False
        super(self.__class__, self).__init__(url, header,
                                             {}, method)


# 测试Ping
class SpeedTestPingReq(ServerReq):
    def __init__(self):
        url = config.Url + "categories"
        method = "GET"
        header = ToolUtil.GetHeader(url, method)
        header['cache-control'] = 'no-cache'
        header['expires'] = '0'
        header['pragma'] = 'no-cache'
        header["authorization"] = ""
        super(self.__class__, self).__init__(url, header,
                                             {}, method)


# 获取聊天频道
class GetChatReq(ServerReq):
    def __init__(self):
        url = config.Url + "chat"
        method = "Get"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获取神魔推荐
class GetCollectionsReq(ServerReq):
    def __init__(self):
        url = config.Url + "collections"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 获取随机本子
class GetRandomReq(ServerReq):
    def __init__(self):
        url = config.Url + "comics/random"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 获取小程序列表
class GetAPPsReq(ServerReq):
    def __init__(self):
        url = config.Url + "pica-apps"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)
        self.isParseRes = False


# 锅贴登陆
class LoginAPPReq(ServerReq):
    def __init__(self, url, token):
        url = url + "/?token=" + token
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)
        self.isParseRes = False


# 锅贴列表
class AppInfoReq(ServerReq):
    def __init__(self, token, page=0):
        url = "https://post-api.wikawika.xyz"
        url = url + "/posts?offset=" + str(page)
        method = "GET"
        header = {
            "Referer": url + "/?token=" + token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "token": token,
        }
        super(self.__class__, self).__init__(url, header, {}, method)


# 锅贴评论列表
class AppCommentInfoReq(ServerReq):
    def __init__(self, id, token="", page=0):
        url = "https://post-api.wikawika.xyz"
        url = url + "/posts/{}/comments?offset={}".format(id, str(page))
        method = "GET"
        if not token:
            from server.server import Server
            token = Server().token
        header = {
            "Referer": url + "/?token=" + token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "token": token,
        }
        super(self.__class__, self).__init__(url, header, {}, method)


# 锅贴发送评论列表
class AppSendCommentInfoReq(ServerReq):
    def __init__(self, id, data="", token=""):
        url = "https://post-api.wikawika.xyz"
        url = url + "/comments"
        method = "POST"
        if not token:
            from server.server import Server
            token = Server().token
        header = {
            "Referer": url + "/?token=" + token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "token": token,
            "Content-Type": "application/json",
        }
        data = {"content": data, "postId": id}
        super(self.__class__, self).__init__(url, header, data, method)


# 锅贴发送评论列表
class AppCommentLikeReq(ServerReq):
    def __init__(self, id, subID, token=""):
        url = "https://post-api.wikawika.xyz"
        url = url + "/comments/{}/like".format(subID)
        method = "PUT"
        if not token:
            from server.server import Server
            token = Server().token
        header = {
            "Referer": url + "/?token=" + token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "token": token,
            "Content-Type": "application/json",
        }
        data = {"postId": id}
        super(self.__class__, self).__init__(url, header, data, method)


# 游戏区列表
class GetGameReq(ServerReq):
    def __init__(self, page=1):
        url = config.Url + "games?page={}".format(page)
        method = "Get"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 游戏区详情
class GetGameInfoReq(ServerReq):
    def __init__(self, gameId):
        url = config.Url + "games/{}".format(gameId)
        method = "Get"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 游戏区评论列表
class GetGameCommentsReq(ServerReq):
    def __init__(self, gameId, page=1):
        url = config.Url + "games/{}/comments?page={}".format(gameId,page)
        method = "Get"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 游戏区评论爱心
class GameCommentsLikeReq(ServerReq):
    def __init__(self, gameId):
        url = config.Url + "comments/{}/like".format(gameId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 游戏区发送评论
class SendGameCommentsReq(ServerReq):
    def __init__(self, gameId, content):
        url = config.Url + "games/{}/comments".format(gameId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {"content": content}, method)

# 新聊天频道登录
class GetNewChatLoginReq(ServerReq):
    def __init__(self, user, passwd):
        url = config.NewChatUrl + "auth/signin"
        method = "POST"
        header = ToolUtil.GetNewChatHeader()
        data = {
            "email": user,
            "password": passwd
        }
        super(self.__class__, self).__init__(url, header,
                                             data, method)
#{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidG9ucXVlcjIiLCJpZCI6IjYwMTIyODdjNjFhYWU4MmZkMmMwZDM1NSIsImVtYWlsIjoidG9ucXVlcjIiLCJpYXQiOjE2Nzk1NDQ0MzMsImV4cCI6MTcxNTU0NDQzM30.DyFOhNnJtgfei0FzTFem66GVWrWyiPbnx7dP_IdO1Ho"}

# 获取新聊天频道
class GetNewChatReq(ServerReq):
    def __init__(self, token):
        url = config.NewChatUrl + "room/list"
        method = "Get"
        header = ToolUtil.GetNewChatHeader()
        header["authorization"] = "Bearer " + token
        super(self.__class__, self).__init__(url, header,
                                             {}, method)
        self.token = "Bearer " + token
# {"rooms":[{"isAvailable":true,"id":"63de3c05eaa71845c0647003","title":"嗶咔公眾澡堂","description":"嗶咔公眾澡堂","minLevel":1,"minRegisterDays":2,"isPublic":true,"allowedCharacters":[],"icon":"https://live-server.bidobido.xyz/media/0pTiqgSSCrDw8bA_GTM8-.jpg"},{"isAvailable":true,"id":"63de1a77ba9358b220392bd4","title":"嗶咔高級會所","description":"嗶咔高級會所","minLevel":20,"minRegisterDays":365,"isPublic":true,"allowedCharacters":[],"icon":"https://live-server.bidobido.xyz/media/-YCNHEpt7KJQdyITWWjML.jpg"},{"isAvailable":true,"id":"63de14e8ba9358b220392bac","title":"嗶咔學習教室","description":"嗶咔學習教室","minLevel":2,"minRegisterDays":10,"isPublic":true,"allowedCharacters":[],"icon":"https://live-server.bidobido.xyz/media/01tXnwXH0NhR2SazzmHfg.jpg"}]}

# 获取新聊天用户信息
class GetNewChatProfileReq(ServerReq):
    def __init__(self, token):
        url = config.NewChatUrl + "user/profile"
        method = "Get"
        header = ToolUtil.GetNewChatHeader()
        header["authorization"] = "Bearer " + token,
        super(self.__class__, self).__init__(url, header,
                                             {}, method)
                                             
        self.token = "Bearer " + token


# 发送消息
class SendNewChatMsgReq(ServerReq):
    def __init__(self, token, roomId, msg, userMentions, replyId):
        url = config.NewChatUrl + "message/send-message"
        method = "POST"
        header = ToolUtil.GetNewChatHeader()
        header["authorization"] = "Bearer " + token,
        data = {
            "roomId": roomId,
            "message": msg,
            "referenceId": str(uuid.uuid1()),
            "userMentions": userMentions,
        }
        if replyId:
            data["replyId"] = replyId
        super(self.__class__, self).__init__(url, header,
                                             data, method)
        self.token = "Bearer " + token


# 发送图片
class SendNewChatImgMsgReq(ServerReq):
    def __init__(self, token, roomId, msg, filePath):
        url = config.NewChatUrl + "message/send-image"
        method = "POST"
        header = ToolUtil.GetNewChatHeader()
        header.pop("content-type")

        header["authorization"] = "Bearer " + token,
        super(self.__class__, self).__init__(url, header,
                                             {}, method)
        self.token = "Bearer " + token
        self.file = {
            "roomId": (None, roomId),
            "caption": (None, msg),
            "referenceId": (None, str(uuid.uuid1())),
            "userMentions": (None, "[]"),
            "medias": (os.path.basename(filePath), open(filePath, 'rb'))
        }