import hashlib
import os
import time

import requests

from conf import config
from src.qt.qttask import QtTask
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
        from src.index.category import CateGoryMgr
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
        from src.index.category import CateGoryMgr
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
                fileSize = int(r.headers.get('Content-Length'))
                getSize = 0
                data = b""
                for chunk in r.iter_content(chunk_size=1024):
                    if backData.bakParam:
                        QtTask().downloadBack.emit(backData.bakParam, fileSize-getSize, chunk)
                    getSize += len(chunk)
                    data += chunk
                if backData.bakParam:
                    QtTask().downloadBack.emit(backData.bakParam, 0, b"")

                if backData.req.isSaveCache and config.IsUseCache:
                    path = backData.req.path

                    filePath = os.path.join(os.path.join(config.SavePath, config.CachePathDir), os.path.dirname(path))

                    if not os.path.isdir(filePath):
                        os.makedirs(filePath)

                    a = hashlib.md5(path.encode("utf-8")).hexdigest()

                    with open(os.path.join(filePath, a), "wb+") as f:
                        f.write(data)
            except Exception as es:
                import sys
                cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
                e = sys.exc_info()[1]
                Log.Error(cur_tb, e)
                if backData.bakParam:
                    QtTask().downloadBack.emit(backData.bakParam, -1, b"")


@handler(req.CheckUpdateReq)
class CheckUpdateReq(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.url)
