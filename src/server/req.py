from src.util import ToolUtil
from conf import config
from urllib.parse import quote


class ServerReq(object):
    def __init__(self, url, header=None, params=None, method="POST") -> None:
        self.url = url
        self.headers = header
        self.params = params
        self.method = method
        self.isParseRes = True
        self.proxy = {"http": config.HttpProxy, "https": config.HttpProxy}


# 获得Ip
class InitReq(ServerReq):
    def __init__(self):
        url = config.BaseUrl + "init"
        method = "GET"
        super(self.__class__, self).__init__(url, {}, {}, method)


# 获得Image的Key
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


# 获得信息
class GetUserInfo(ServerReq):
    def __init__(self):
        url = config.Url + "users/profile"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


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


# 获得一本书
class GetComicsBookReq(ServerReq):
    def __init__(self, bookId=""):
        url = config.Url + "comics/{}".format(bookId)
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得一本书章节列表
class GetComicsBookEpsReq(ServerReq):
    def __init__(self, bookId="", page=""):
        url = config.Url + "comics/{}/eps?page={}".format(bookId, page)
        method = "GET"
        self.bookId = bookId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得一个章节的图片信息
class GetComicsBookOrderReq(ServerReq):
    def __init__(self, bookId="", epsId="", page=""):
        url = config.Url + "comics/{}/order/{}/pages?page={}".format(bookId, epsId, page)
        method = "GET"
        self.bookId = bookId
        self.epsId = epsId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 下载图片
class DownloadBookReq(ServerReq):
    def __init__(self, url, path="", isSaveCache=False):
        url = url + "/static/{}".format(path)
        method = "Download"
        self.url = url
        self.path = path
        self.isSaveCache = isSaveCache
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得评论
class GetComments(ServerReq):
    def __init__(self, bookId="", page=1):
        url = config.Url + "comics/{}/comments?page={}".format(bookId, page)
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 检查更新
class CheckUpdateReq(ServerReq):
    def __init__(self):
        url = config.UpdateUrl
        method = "GET"
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False


# 热词
class GetKeywords(ServerReq):
    def __init__(self):
        url = config.Url + "keywords"
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 发送评论
class SendComment(ServerReq):
    def __init__(self, bookId="", content=""):
        url = config.Url + "comics/{}/comments".format(bookId)
        method = "POST"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {"content": content}, method)
