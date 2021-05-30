import hashlib
import os
import re
import time

from conf import config
from src.qt.util.qttask import QtTask
from .server import handler
from src.server import req, Status, Log, ToolUtil


@handler(req.InitReq)
class InitHandler(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().InitBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.InitAndroidReq)
class InitAndroidHandler(object):
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
class GetUserInfoHandler(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().UpdateUserInfoBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.SetAvatarInfoReq)
class SetAvatarInfoHandler(object):
    def __call__(self, backData):
        st = Status.Ok
        if backData.res.code != 200:
            st = Status.SetHeadError + backData.res.message + backData.res.error
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.SetTitleReq)
class SetTitleHandler(object):
    def __call__(self, backData):
        st = Status.Ok
        if backData.res.code != 200:
            st = Status.SetHeadError + backData.res.message
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.PunchIn)
class PunchInHandler(object):
    def __call__(self, backData):
        from src.user.user import User
        st = User().PunchedBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.FavoritesAdd)
class FavoritesAddHandler(object):
    def __call__(self, backData):
        if backData.res.code == 200:
            if backData.res.data.get("action") == "un_favourite":
                pass
            else:
                pass
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, Status.Ok)


@handler(req.FavoritesReq)
class FavoritesAddHandler(object):
    def __call__(self, backData):
        from src.user.user import User
        st, page = User().UpdateFavoritesBack(backData)
        time.sleep(0.1)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.CategoryReq)
class CategoryHandler(object):
    def __call__(self, backData):
        from src.index.category import CateGoryMgr
        CateGoryMgr().UpdateCateGoryBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, Status.Ok)


@handler(req.AdvancedSearchReq)
class AdvancedSearchHandler(object):
    def __call__(self, backData):
        if backData.res.code == 200:
            for data in backData.res.data['comics']["docs"]:
                pass
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.CategoriesSearchReq)
class CategoriesSearchHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.RankReq)
class RankHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.GetComments)
class GetCommentsHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.GetComicsBookEpsReq)
class GetComicsBookEpsHandler(object):
    def __call__(self, backData):
        from src.index.book import BookMgr
        st = BookMgr().AddBookEpsInfoBack(backData)
        if st == Status.WaitLoad:
            return
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.GetComicsBookOrderReq)
class GetComicsBookOrderHandler(object):
    def __call__(self, backData):
        from src.index.book import BookMgr
        st = BookMgr().AddBookEpsPicInfoBack(backData)
        if st == Status.WaitLoad:
            return
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.GetComicsBookReq)
class GetComicsBookHandler(object):
    def __call__(self, backData):
        from src.index.book import BookMgr
        st = BookMgr().AddBookByIdBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, st)


@handler(req.DownloadBookReq)
class DownloadBookHandler(object):
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
                # Log.Info("size:{}, url:{}".format(ToolUtil.GetDownloadSize(fileSize), backData.req.url))
                if backData.cacheAndLoadPath and config.IsUseCache and len(data) > 0:
                    filePath = backData.cacheAndLoadPath
                    fileDir = os.path.dirname(filePath)
                    if not os.path.isdir(fileDir):
                        os.makedirs(fileDir)

                    with open(filePath, "wb+") as f:
                        f.write(data)
                    Log.Debug("add download cache, cachePath:{}".format(filePath))
            except Exception as es:
                Log.Error(es)
                if backData.bakParam:
                    QtTask().downloadBack.emit(backData.bakParam, -1, b"")


@handler(req.CheckUpdateReq)
class CheckUpdateHandler(object):
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


@handler(req.SendCommentChildrenReq)
class SendCommentChildrenHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.GetCommentsChildrenReq)
class GetKeywordsHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.SpeedTestReq)
class SpeedTestHandler(object):
    def __call__(self, backData):
        if backData.status != Status.Ok:
            if backData.bakParam:
                QtTask().taskBack.emit(backData.bakParam, "")
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    if backData.bakParam:
                        QtTask().taskBack.emit(backData.bakParam, "")
                    return

                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                now = time.time()
                consume = 1
                for chunk in r.iter_content(chunk_size=10240):
                    getSize += len(chunk)
                    consume = time.time() - now
                    if consume >= 2:
                        break

                downloadSize = getSize / consume
                speed = ToolUtil.GetDownloadSize(downloadSize)
                if backData.bakParam:
                    QtTask().taskBack.emit(backData.bakParam, speed)

            except Exception as es:
                Log.Error(es)
                if backData.bakParam:
                    QtTask().taskBack.emit(backData.bakParam, "")


@handler(req.GetChatReq)
class GetChatHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.GetCollectionsReq)
class GetCollectionsHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.GetRandomReq)
class GetRandomHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.GetAPPsReq)
class GetAPPsHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.LoginAPPReq)
class LoginAPPHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)


@handler(req.AppInfoReq)
class AppInfoHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)