import base64
import os
import platform
import random
import re
import struct
import urllib
import uuid
from datetime import datetime, timedelta
from urllib.parse import quote
from curl_cffi import requests as requests2, CurlOpt, CurlHttpVersion

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from qt_owner import QtOwner
from tools.log import Log
from tools.tool import ToolUtil


class ServerReq(object):
    def __init__(self, url, header=None, json=None, method="POST", isOtherCloudFlare=False) -> None:
        self.resetCnt = 0
        self.isReload = False
        self.url = url
        # self.resetUrlHost = []
        self.resetUrl = []
        self.resetIndex = 0

        self.file = ""
        self.token = ""
        self.headers = header
        self.params = {}

        if not json:
            self.json = None
        else:
            self.json = json
        self.method = method
        self.isParseRes = True
        self.cookies = {}
        self.proxy = {}
        self.proxyUrl = ""
        self.curl_opt = {}

        host = ToolUtil.GetUrlHost(url)
        self.timeout = 5
        self.isOtherCloudFlare = isOtherCloudFlare
        self.isApi = False
        self.isImg = False
        if host in GlobalConfig.AllApiDomain.value:
            self.isApi = True
            self.timeout = Setting.ApiTimeOut.GetIndexV()
        if host in GlobalConfig.AllImgDomain.value:
            self.isImg = True
            self.timeout = Setting.ImgTimeOut.GetIndexV()
        if self.isApi:
            ## 图片不设置该值，否则cf-cache-status返回BYPASS
            from tools.user import User
            self.headers["authorization"] = User().token

        self.SetIndex(Setting.ProxySelectIndex.value, Setting.ProxyImgSelectIndex.value)
        self.SetProxy(Setting.IsHttpProxy.value, Setting.HttpProxy.value, Setting.Sock5Proxy.value)
        from qt_owner import QtOwner
        if (self.isApi or self.isImg) and self.proxyUrl:
            self.headers['version'] = config.UpdateVersion

        if self.isApi and not self.proxyUrl:
            self.ipList = GlobalConfig.GetAddress(Setting.ProxySelectIndex.value)
        elif self.isImg and not self.proxyUrl:
            self.ipList = GlobalConfig.GetImageAdress(Setting.ProxyImgSelectIndex.value)
        else:
            self.ipList = []
        self.SetCurlOpt(Setting.EnableEch.value, QtOwner().echConfig, self.ipList)

    def SetIndex(self, apiIndex, imgIndex, imgHost=None):
        host = ToolUtil.GetUrlHost(self.url)
        self.proxyUrl = ""

        if self.isApi:
            if apiIndex == 5:
                self.proxyUrl = GlobalConfig.ProxyApiDomain.value
            if apiIndex == 6:
                self.proxyUrl = GlobalConfig.ProxyApiDomain2.value

        if self.isImg:
            if imgIndex == 5:
                self.proxyUrl = GlobalConfig.ProxyImgDomain.value
            if imgIndex == 6:
                self.proxyUrl = GlobalConfig.ProxyImgDomain2.value
            if imgHost:
                self.url = self.url.replace(host, ToolUtil.GetUrlHost(imgHost))

    def SetToken(self, token):
        self.headers["authorization"] = token

    def SetProxy(self, proxyIndex, httpProxy, sock5Proxy):
        if proxyIndex == 1:
            self.proxy = {"http": httpProxy, "https": httpProxy}
        elif proxyIndex == 2 and sock5Proxy:
            data = sock5Proxy.replace("http://", "").replace("https://", "").replace("sock5://", "").replace(
                "socks5://", "")
            data = data.split(":")
            if len(data) == 2:
                host = data[0]
                port = data[1]
                proxy = f"socks5://{host}:{port}"
                self.proxy = {"http": proxy, "https": proxy}
        elif proxyIndex == 3:
            proxy = urllib.request.getproxies()
            if isinstance(proxy, dict) and proxy.get("http"):
                self.proxy = {"http": proxy.get("http"), "https": proxy.get("http")}
        else:
            self.proxy = {"http": None, "https": None}


    def SetCurlOpt(self, isEch=False, echConfig="", dnsIpList=None):
        self.ipList = dnsIpList
        self.curl_opt = dict()
        self.curl_opt[CurlOpt.HTTP_VERSION] = CurlHttpVersion.V2_0
        host = ToolUtil.GetUrlHost(self.url)
        isEch = isEch and (self.isImg or self.isApi or self.isOtherCloudFlare) and not self.proxyUrl
        # allUrls = GlobalConfig.DohUrlList.value[:]
        # allUrls.extend(GlobalConfig.NoHttp3Url.value[:])
        # allUrls.append(Setting.DohAddress.value)
        # for ignoreUrl in allUrls:
        #     if host in ignoreUrl:
        #         isEch = False
        #         break
        if isEch and echConfig:
            self.curl_opt[CurlOpt.ECH] = f"ecl:{echConfig}"
        if dnsIpList:
            if isinstance(dnsIpList, list):
                ipStr = ",".join(dnsIpList)
            else:
                ipStr = dnsIpList

            if ipStr:
                self.curl_opt[CurlOpt.RESOLVE] = [f"{host}:443:{ipStr}"]
                # 图片有301跳转最好设置全部域名
                if self.isImg:
                    for url in GlobalConfig.AllImgDomain.value:
                        host2 = ToolUtil.GetUrlHost(url)
                        if host != host2:
                            self.curl_opt[CurlOpt.RESOLVE].append(f"{host2}:443:{ipStr}")

    def ResetToSwitchNextUrl(self):
        if not self.resetUrl:
            return False
        if self.resetIndex >= len(self.resetUrl):
            return False
        url = self.resetUrl[self.resetIndex]
        self.resetIndex += 1
        if self.proxyUrl:
            host = ToolUtil.GetUrlHost(url)
            url = url.replace(host, self.proxyUrl + "/" + host)

        Log.Info("request switch url:{}->{}".format(self.url, url))
        self.url = url
        return True

    def GetPri(self):
        ech = False
        if CurlOpt.ECH in self.curl_opt:
            ech = True
        if Setting.LogIndex.value <= 1:
            return "{}, ech:{}, url:{}, ip:{}, proxy:{}".format(self.__class__.__name__, ech, self.url, self.ipList, self.proxy)
        headers = dict()
        headers.update(self.headers)
        params = self.params
        if isinstance(self, (LoginReq, RegisterReq, ForgotPasswordReq, ResetPasswordReq)):
            params = {}
        return "{}, ech:{}, url:{}, ip:{}, proxy:{}, method:{}, headers:{}, params:{}, proxy:{}".format(self.__class__.__name__, ech, self.url, self.ipList, self.proxy, self.method, headers, params, self.proxy)

    def __str__(self):
        return self.GetPri()

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
        if "static/static" in url:
            url = url.replace("static/static", "static")
        url = self.FixCover(url)
        oldUrl = url
        jumpDomain = {
            "storage-b.picacomic.com": "img.picacomic.com",
            "s3.picacomic.com": "img.picacomic.com",
            "storage1.picacomic.com": "img.picacomic.com",
            "storage.picacomic.com": "img.picacomic.com",
            "storage-b.diwodiwo.xyz": "img.diwodiwo.xyz",
            "s3.diwodiwo.xyz": "img.diwodiwo.xyz",
            "storage1.diwodiwo.xyz": "img.diwodiwo.xyz",
            "storage.tipatipa.xyz": "img.tipatipa.xyz",
            "storage-b.tipatipa.xyz": "img.tipatipa.xyz",
            "s3.tipatipa.xyz": "img.tipatipa.xyz",
            "storage1.tipatipa.xyz": "img.tipatipa.xyz",
        }
        # 封面会出现301跳转，可以提前设置好域名
        host = ToolUtil.GetUrlHost(url)
        isJump = "/static/tobeimg" in url and  host in jumpDomain
        if isJump:
            url = url.replace(host, jumpDomain[host])
            url = url.replace("/static/tobeimg", "")
            oldUrl2 = url

            Log.Info("jump_301_url, {}->{}".format(oldUrl, url))
            allDomain = ["img.picacomic.com", "img.diwodiwo.xyz", "img.tipatipa.xyz"]
        else:
            oldUrl2 = url
            allDomain = ["storage-b.picacomic.com", "s3.picacomic.com", "storage1.diwodiwo.xyz", "storage.tipatipa.xyz"]
        # if self.imageServer and host in GlobalConfig.ImageServerList.value:
        #     if not ToolUtil.IsipAddress(self.imageServer):
        #         ## 图片域名
        #         request.resetUrlHost = GlobalConfig.ImageServerList.value[:]
        #         if self.imageServer in request.resetUrlHost:
        #             request.resetUrlHost.remove(self.imageServer)
        #         request.url = request.url.replace(host, self.imageServer)
        self.loadPath = loadPath
        self.cachePath = cachePath
        self.savePath = savePath
        self.isReset = False
        if "static/tobeimg/" in url:
            url = url.replace("static/tobeimg/", "static/")
        if "static/tobs/" in url:
            url = url.replace("static/tobs/", "static/")
        self.url = url
        super(self.__class__, self).__init__(url, ToolUtil.GetDownImgHeader(),
                                             {}, method)
        self.isReload = isReload
        realHost = ToolUtil.GetUrlHost(url)
        if realHost in allDomain:
            allDomain.remove(realHost)
        random.shuffle(allDomain)
        self.resetUrl = [oldUrl2.replace(realHost, i) for i in allDomain]
        self.resetCnt = max(resetCnt, len(self.resetUrl)//2)

    def FixCover(self, url):
        if Setting.DownloadCoverLv.value == 0:
            return url
        elif Setting.DownloadCoverLv.value == 1:
            return url.replace(":300:400", ":450:600")
        elif Setting.DownloadCoverLv.value == 2:
            return url.replace(":300:400", ":600:800")
        else:
            return re.sub(r"\/rs:fill:\d+:\d+:\d+\/\w:\w", "", url)

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
    def __init__(self, url2, isPre=False):
        method = "GET"
        data = dict()
        data["version"] = config.RealVersion
        data["platform"] = platform.platform()
        if not isPre:
            url = url2 + "/version.txt?"
        else:
            url = url2 + "/version_pre.txt?"
        url += ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False
        self.useImgProxy = False


# 检查更新
class CheckUpdateInfoReq(ServerReq):
    def __init__(self, url2, newVersion):
        method = "GET"
        data = dict()
        data["version"] = config.RealVersion
        data["platform"] = platform.platform()
        url = url2 + "/{}.txt?".format(newVersion)
        url += ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False
        self.useImgProxy = False


# 检查更新配置
class CheckUpdateConfigReq(ServerReq):
    def __init__(self, url2):
        method = "GET"
        data = dict()
        data["version"] = config.RealVersion
        data["platform"] = platform.platform()
        url = url2 + "/config.txt?"
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
            "version": config.RealVersion,
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
            "version": config.RealVersion,
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
            "version": config.RealVersion,
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
            self.proxyUrl = GlobalConfig.ProxyApiDomain.value

        header = ToolUtil.GetDownImgHeader()
        header['cache-control'] = 'no-cache'
        header['expires'] = '0'
        header['pragma'] = 'no-cache'
        self.isReset = False
        super(self.__class__, self).__init__(url, header,
                                             {}, method)
        self.resetCnt = 0
        self.isParseRes = False
        self.isReload = False


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
        self.isParseRes = False


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


# 获取pica号
class GetShareIdReq(ServerReq):
    def __init__(self, id):
        url = "https://recommend.go2778.com/pic/share/set/?c={}".format(id)
        method = "Get"
        self.bookId = id
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 通过pica号获取id
class GetIdByShareIdReq(ServerReq):
    def __init__(self, shareId):
        url = "https://recommend.go2778.com/pic/share/get/?shareId={}".format(shareId)
        method = "Get"
        self.shareId = shareId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


class GetRecommendByIdReq(ServerReq):
    def __init__(self, bookId):
        url = "https://macapi1.com/picacomic/rec/{}?limit=10".format(bookId)
        method = "Get"
        self.bookId = bookId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method, isOtherCloudFlare=True)
        self.isParseRes = False


# 通过cf优选ip
class GetCfDnsReq(ServerReq):
    def __init__(self, domain):
        domain = ToolUtil.GetUrlHost(domain)
        url = "https://macapi1.com/app/picacomic/dns/resolve?domain={}".format(domain)
        method = "Get"
        self.domain = domain
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method, isOtherCloudFlare=True)


# Doh域名解析
class DnsOverHttpsReq(ServerReq):
    def __init__(self, domain="", dohAddress=""):
        url = dohAddress + "?name={}&type=A".format(ToolUtil.GetUrlHost(domain))
        method = "GET"
        header = dict()
        header["accept"] = "application/dns-json"
        header["Content-Type"] = "application/dns-json"
        header["version"] = config.RealVersion
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.timeout = 5
        self.headers = header
        self.isParseRes = True


# Doh域名解析
class GetEchConfigReq(ServerReq):
    TYPE_HTTPS = 65

    @staticmethod
    def build_dns_query(domain: str, qtype: int) -> bytes:
        parts = [b"\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"]
        for label in domain.split("."):
            label_bytes = label.encode("idna")
            parts.append(bytes([len(label_bytes)]))
            parts.append(label_bytes)
        parts.append(b"\x00")
        parts.append(struct.pack("!HH", qtype, 1))
        return b"".join(parts)

    @staticmethod
    def _skip_dns_name(packet: bytes, offset: int) -> int:
        while offset < len(packet):
            length = packet[offset]
            if length & 0xC0 == 0xC0:
                return offset + 2
            if length == 0:
                return offset + 1
            offset += length + 1
        return offset

    @staticmethod
    def parse_https_record(data: bytes) -> str:
        if len(data) < 2:
            return ""
        offset = 2
        if offset < len(data) and data[offset] == 0:
            offset += 1
        else:
            offset = GetEchConfigReq._skip_dns_name(data, offset)
        while offset + 4 <= len(data):
            key, length = struct.unpack("!HH", data[offset: offset + 4])
            offset += 4
            if offset + length > len(data):
                break
            value = data[offset: offset + length]
            offset += length
            if key == 5:
                return base64.b64encode(value).decode("ascii")
        return ""

    @staticmethod
    def parse_dns_response(response: bytes) :
        if len(response) < 12:
            return ""
        ancount = struct.unpack("!H", response[6:8])[0]
        if ancount == 0:
            return ""

        offset = GetEchConfigReq._skip_dns_name(response, 12) + 4
        for _ in range(ancount):
            offset = GetEchConfigReq._skip_dns_name(response, offset)
            if offset + 10 > len(response):
                break
            rr_type = struct.unpack("!H", response[offset : offset + 2])[0]
            offset += 8
            data_len = struct.unpack("!H", response[offset : offset + 2])[0]
            offset += 2
            if offset + data_len > len(response):
                break
            data = response[offset : offset + data_len]
            offset += data_len
            if rr_type == GetEchConfigReq.TYPE_HTTPS:
                ech = GetEchConfigReq.parse_https_record(data)
                if ech:
                    return ech
        return ""

    def __init__(self, domain="", dohAddress=None):
        url = dohAddress[0]
        method = "POST"
        super(self.__class__, self).__init__(url, {}, {}, method)
        headers = {
                    "Accept": "application/dns-message",
                    "Content-Type": "application/dns-message",
                    "version": config.RealVersion
        }
        self.timeout = 5
        self.params = self.build_dns_query(domain, GetEchConfigReq.TYPE_HTTPS)
        self.headers = headers
        self.isParseRes = False
        self.resetUrl = dohAddress[1:]
        self.resetCnt = len(dohAddress)


# 测试Ping
class SpeedTestPing2Req(ServerReq):
    def __init__(self, url):
        # url = url + "/cdn-cgi/trace"
        url = url + "/static/3142c39a-02aa-45db-a082-b4d9c9b4c251.jpg"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetDownImgHeader(), {}, method)
        self.headers['cache-control'] = 'no-cache'
        self.headers['expires'] = '0'
        self.headers['pragma'] = 'no-cache'
        self.isReload = False
        self.isParseRes = False
        self.timeout = 3


# 获取ip信息
class GetIpInfoReq(ServerReq):
    def __init__(self, ip=""):
        url = f"https://parse.jpacg.cc/ipinfo?ip={ip}"
        method = "GET"
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.timeout = 5
        self.headers = {
            "version": config.RealVersion
        }
        self.isParseRes = False
        self.resetUrl = [f"https://parse2.jpacg.cc/ipinfo?ip={ip}"]
        self.resetCnt = len(self.resetUrl)
        

# 获取proxyip
class GetProxyIpInfoReq(ServerReq):
    def __init__(self, country=""):
        if country:
            url = f"https://check.jpacg.cc/resolve?proxyip=proxyip.{country}.cmliussss.net"
        else:
            url = f"https://check.jpacg.cc/resolve?proxyip=proxyip.cmliussss.net"
        method = "GET"
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.timeout = 7
        self.headers = {}
        self.isParseRes = False
        realUrl = ToolUtil.GetUrlHost(url)
        self.resetUrl = [url.replace(realUrl, "check2.jpacg.cc")]
        self.resetCnt = len(self.resetUrl)