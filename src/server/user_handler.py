import os
import re
import time

from conf import config
from src.qt.util.qttask import QtTask
from src.server import req, Status, Log, ToolUtil
from .server import handler


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


@handler(req.CategoryReq)
class CategoryHandler(object):
    def __call__(self, backData):
        from src.index.category import CateGoryMgr
        CateGoryMgr().UpdateCateGoryBack(backData)
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, Status.Ok)


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
        if not backData.res.GetText() or backData.status == Status.NetError:
            if backData.bakParam:
                QtTask().taskBack.emit(backData.bakParam, "")
            return
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


@handler(req.GetUserCommentReq)
@handler(req.FavoritesAdd)
@handler(req.FavoritesReq)
@handler(req.AdvancedSearchReq)
@handler(req.CategoriesSearchReq)
@handler(req.RankReq)
@handler(req.GetComments)
@handler(req.GetComicsRecommendation)
@handler(req.BookLikeReq)
@handler(req.CommentsLikeReq)
@handler(req.GetKeywords)
@handler(req.SendComment)
@handler(req.SendCommentChildrenReq)
@handler(req.GetCommentsChildrenReq)
@handler(req.GetChatReq)
@handler(req.GetCollectionsReq)
@handler(req.GetRandomReq)
@handler(req.GetAPPsReq)
@handler(req.LoginAPPReq)
@handler(req.AppInfoReq)
@handler(req.AppCommentInfoReq)
@handler(req.GetGameReq)
@handler(req.GetGameInfoReq)
@handler(req.GetGameCommentsReq)
@handler(req.SendGameCommentsReq)
@handler(req.GameCommentsLikeReq)
@handler(req.CheckUpdateDatabaseReq)
@handler(req.DownloadDatabaseReq)
class MsgHandler(object):
    def __call__(self, backData):
        if backData.bakParam:
            QtTask().taskBack.emit(backData.bakParam, backData.res.raw.text)
