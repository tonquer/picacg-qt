import json
import os
import pickle
import re
import time

from config import config
from task.qt_task import TaskBase
from tools.log import Log
from tools.status import Status
from tools.tool import ToolUtil
from tools.user import User
from . import req
from .server import handler, Server

@handler(req.InitReq)
class InitHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().InitBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.InitAndroidReq)
class InitAndroidHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().InitImageServer(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.LoginReq)
class LoginHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st, token = User().LoginBack(task)
            data["st"] = st
            data["token"] = token
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))

@handler(req.RegisterReq)
class RegisterHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().RegisterBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetUserInfo)
class GetUserInfoHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().UpdateUserInfoBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.SetAvatarInfoReq)
class SetAvatarInfoHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.res.code != 200:
                data["st"] = Status.SetHeadError
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.PunchIn)
class PunchInHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().PunchedBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CategoryReq)
class CategoryHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            from tools.category import CateGoryMgr
            CateGoryMgr().UpdateCateGoryBack(task)
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetComicsBookEpsReq)
class GetComicsBookEpsHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status == Status.Ok:
                from tools.book import BookMgr
                st = BookMgr().AddBookEpsInfoBack(task)
                if st == Status.WaitLoad:
                    return
                data["st"] = st
        except Exception as es:
            Log.Error(es)
        if task.bakParam:
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetComicsBookOrderReq)
class GetComicsBookOrderHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status == Status.Ok:
                from tools.book import BookMgr
                st = BookMgr().AddBookEpsPicInfoBack(task)
                if st == Status.WaitLoad:
                    return
                data["st"] = st
        except Exception as es:
            Log.Error(es)
        if task.bakParam:
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetComicsBookReq)
class GetComicsBookHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            from tools.book import BookMgr
            st = BookMgr().AddBookByIdBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.SpeedTestPingReq)
class SpeedTestPingHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        if hasattr(task.res.raw, "elapsed"):
            if task.res.raw.status_code == 401 or task.res.raw.status_code == 200:
                data["data"] = str(task.res.raw.elapsed.total_seconds()*1000//4)
            else:
                data["st"] = Status.Error
                data["data"] = "0"
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
        else:
            data["data"] = "0"
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.DownloadBookReq)
class DownloadBookHandler(object):
    def __call__(self, backData):
        if backData.status != Status.Ok:
            if backData.bakParam:
                TaskBase.taskObj.downloadBack.emit(backData.bakParam, -backData.status, b"")
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    if backData.bakParam:
                        TaskBase.taskObj.downloadBack.emit(backData.bakParam, -Status.Error, b"")
                    return
                
                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                data = b""
                
                now = time.time()
                isAlreadySend = False
                # 网速快，太卡了，优化成最多100ms一次
                try:
                    for chunk in r.iter_content(chunk_size=4096):
                        cur = time.time()
                        tick = cur - now
                        if tick >= 0.1:
                            isAlreadySend = True
                            if backData.bakParam and fileSize-getSize > 0:
                                TaskBase.taskObj.downloadBack.emit(backData.bakParam, fileSize-getSize, b"")
                            now = cur

                        getSize += len(chunk)
                        data += chunk
                    if not isAlreadySend:
                        if backData.bakParam:
                            TaskBase.taskObj.downloadBack.emit(backData.bakParam, getSize, b"")

                except Exception as es:
                    Log.Error(es)
                    if backData.req.resetCnt > 0:
                        backData.req.isReset = True
                        Server().ReDownload(backData)
                        return

                # Log.Info("size:{}, url:{}".format(ToolUtil.GetDownloadSize(fileSize), backData.req.url))
                if config.IsUseCache and len(data) > 0:
                    try:
                        for path in [backData.req.cachePath, backData.req.savePath]:
                            filePath = path
                            if not path:
                                continue
                            fileDir = os.path.dirname(filePath)
                            if not os.path.isdir(fileDir):
                                os.makedirs(fileDir)

                            with open(filePath, "wb+") as f:
                                f.write(data)
                            Log.Debug("add download cache, cachePath:{}".format(filePath))
                    except Exception as es:
                        Log.Error(es)
                        # 保存失败了
                        if backData.bakParam:
                            TaskBase.taskObj.downloadBack.emit(backData.bakParam, -2, b"")

                if backData.bakParam:
                    TaskBase.taskObj.downloadBack.emit(backData.bakParam, 0, data)
                    
            except Exception as es:
                backData.status = Status.DownloadFail
                Log.Error(es)
                if backData.bakParam:
                    TaskBase.taskObj.downloadBack.emit(backData.bakParam, -backData.status, b"")


@handler(req.CheckUpdateDatabaseReq)
@handler(req.DownloadDatabaseReq)
@handler(req.DownloadDatabaseWeekReq)
class DownloadDatabaseReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        if not task.res.GetText() or task.status == Status.NetError:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
            return
        if task.bakParam:
            data["data"] = task.res.GetText()
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CheckUpdateReq)
class CheckUpdateHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return
            verData = task.res.GetText()
            info = verData.replace("v", "").split(".")
            version = int(info[0]) * 100 + int(info[1]) * 10 + int(info[2]) * 1
            
            info2 = re.findall(r"\d+\d*", os.path.basename(config.UpdateVersion))
            curversion = int(info2[0]) * 100 + int(info2[1]) * 10 + int(info2[2]) * 1
            
            if version > curversion:
                data["data"] = verData.replace("\r\n", "").replace("\n", "")
            else:
                data["data"] = "no"
        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CheckUpdateInfoReq)
class CheckUpdateInfoHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return

            data["data"] =  task.res.GetText()
        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CheckUpdateConfigReq)
class CheckUpdateConfigHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return

            data["data"] = task.res.GetText()
        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.SpeedTestReq)
class SpeedTestHandler(object):
    def __call__(self, backData):
        data = {"st": backData.status, "data": ""}
        if backData.status != Status.Ok:
            if backData.bakParam:
                TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    data["st"] = Status.Error
                    if backData.bakParam:
                        data["st"] = Status.Error
                        TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))
                    return

                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                now = time.time()
                for chunk in r.iter_content(chunk_size=1024):
                    getSize += len(chunk)
                    consume = time.time() - now
                    if consume >= 3.0:
                        break
                consume = time.time() - now
                downloadSize = getSize / consume
                speed = ToolUtil.GetDownloadSize(downloadSize)
                if backData.bakParam:
                    data["data"] = speed
                    TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))

            except Exception as es:
                Log.Error(es)
                data["st"] = Status.DownloadFail
                if backData.bakParam:
                    TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))


@handler(req.GetUserCommentReq)
@handler(req.FavoritesAdd)
@handler(req.FavoritesReq)
@handler(req.AdvancedSearchReq)
@handler(req.CategoriesSearchReq)
@handler(req.RankReq)
@handler(req.KnightRankReq)
@handler(req.GetCommentsReq)
@handler(req.GetComicsRecommendation)
@handler(req.BookLikeReq)
@handler(req.CommentsLikeReq)
@handler(req.CommentsReportReq)
@handler(req.GetKeywords)
@handler(req.SendCommentReq)
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
@handler(req.ForgotPasswordReq)
@handler(req.ResetPasswordReq)
@handler(req.ChangePasswordReq)
@handler(req.GetNewChatReq)
@handler(req.GetNewChatProfileReq)
@handler(req.GetNewChatLoginReq)
@handler(req.SendNewChatMsgReq)
@handler(req.SendNewChatImgMsgReq)
class MsgHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        if task.bakParam:
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
