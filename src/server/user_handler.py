import hashlib
import os
import re
import time

from conf import config
from src.qt.util.qttask import QtTask
from .server import handler
from src.server import req, Status, Log


@handler(req.InitReq)
class InitHandler(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().InitBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.InitAndroidReq)
class InitAndroidReq(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().InitImageServer(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.LoginReq)
class LoginHandler(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().LoginBack(backData)
        time.sleep(0.1)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.RegisterReq)
class RegisterHandler(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().RegisterBack(backData)
        time.sleep(0.1)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.GetUserInfo)
class GetUserInfo(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().UpdateUserInfoBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.PunchIn)
class PunchIn(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().PunchedBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.FavoritesAdd)
class FavoritesAdd(object):
    def __call__(self, backData):
        if backData.res.code == 200:
            if backData.res.data.get("action") == "un_favourite":
                pass
            else:
                pass
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, Status.Ok)


@handler(req.FavoritesReq)
class FavoritesAdd(object):
    def __call__(self, backData):
        from src.user.user import User
        st, page = User().UpdateFavoritesBack(backData)
        time.sleep(0.1)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.CategoryReq)
class CategoryReq(object):
    def __call__(self, backData):
        from src.index.category import CateGoryMgr
        CateGoryMgr().UpdateCateGoryBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, Status.Ok)


@handler(req.AdvancedSearchReq)
class AdvancedSearchReq(object):
    def __call__(self, backData):
        if backData.res.code == 200:
            for data in backData.res.data['comics']["docs"]:
                pass
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.CategoriesSearchReq)
class CategoriesSearchReq(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.RankReq)
class RankReq(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.GetComments)
class GetComments(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.GetComicsBookEpsReq)
class GetComicsBookEpsReq(object):
    def __call__(self, backData):
        from src.index.book import BookMgr
        st = BookMgr().AddBookEpsInfoBack(backData)
        if st == Status.WaitLoad:
            return
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.GetComicsBookOrderReq)
class GetComicsBookOrderReq(object):
    def __call__(self, backData):
        from src.index.book import BookMgr
        st = BookMgr().AddBookEpsPicInfoBack(backData)
        if st == Status.WaitLoad:
            return
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.GetComicsBookReq)
class GetComicsBookReq(object):
    def __call__(self, backData):
        from src.index.book import BookMgr
        st = BookMgr().AddBookByIdBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.DownloadBookReq)
class DownloadBookReq(object):
    def __call__(self, backData):
        if backData.status != Status.Ok:
            if backData.bakParam:
                QtTask().downloadBack.emit(backData.bakParam, -1, b"")
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    if backData.bakParam:
                        QtTask().downloadBack.emit(backData.bakParam, -1, b"")
                    return
                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                data = b""
                for chunk in r.iter_content(chunk_size=1024):
                    if backData.bakParam:
                        QtTask().downloadBack.emit(backData.bakParam, fileSize-getSize, chunk)
                    getSize += len(chunk)
                    data += chunk
                if backData.bakParam:
                    QtTask().downloadBack.emit(backData.bakParam, 0, b"")

                if backData.cacheAndLoadPath and config.IsUseCache and len(data) > 0:
                    filePath = backData.cacheAndLoadPath
                    fileDir = os.path.dirname(filePath)
                    if not os.path.isdir(fileDir):
                        os.makedirs(fileDir)

                    with open(filePath, "wb+") as f:
                        f.write(data)
            except Exception as es:
                Log.Error(es)
                if backData.bakParam:
                    QtTask().downloadBack.emit(backData.bakParam, -1, b"")


@handler(req.CheckUpdateReq)
class CheckUpdateReq(object):
    def __call__(self, backData):
        updateInfo = re.findall(r"<meta property=\"og:description\" content=\"([^\"]*)\"", backData.res.raw.text)
        if updateInfo:
            data = updateInfo[0]
        else:
            data = ""

        info = re.findall(r"\d+\d*", os.path.basename(backData.res.raw.url))
        version = int(info[0]) * 100 + int(info[1]) * 10 + int(info[2]) * 1
        info2 = re.findall(r"\d+\d*", os.path.basename(config.UpdateVersion))
        curversion = int(info2[0]) * 100 + int(info2[1]) * 10 + int(info2[2]) * 1

        data = "\n\nv" + ".".join(info) + "\n" + data
        if version > curversion:
            if backData.bakParam:
                QtTask().taskBack.emit(backData.bakParam, data)


@handler(req.GetKeywords)
class GetKeywordsHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.SendComment)
class GetKeywordsHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)
