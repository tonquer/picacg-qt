import os
import time

from config import config
from config.setting import Setting
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from task.task_upload import QtUpTask
from tools.str import Str
from tools.tool import ToolUtil

class SaveNameType:
    Default = 0
    AuthorAndTitle = 1
    AuthorDir = 2


class NasUploadItem(QtTaskBase):
    Success = Str.CvSuccess
    WaitWaifu2x = Str.CvWaifu2x
    Waiting = Str.CvWaitDown
    Uploading = Str.CvUpload
    Pause = Str.CvPause
    Error = Str.CvError
    WaitXmlInfo = Str.CvXMLInfo

    def __init__(self):
        QtTaskBase.__init__(self)
        self.nasId = ""
        self.bookId = ""
        self.title = ""
        self.tick = int(time.time())                #
        self.status = self.Pause       # 状态
        self.statusMsg = 0
        self.tableRow = 0                # 索引

        self.epsIds = []                 # 所有完成的章节
        self.curPreUpIndex = -1       # 当前正在下载的章节, 不是索引
        self.type = 1
        self.dirty = True

    @property
    def isCbz(self):
        nasInfo = QtOwner().owner.nasView.nasDict.get(self.nasId)
        if not nasInfo:
            return False
        return nasInfo.compress_index == 1

    @property
    def completeNum(self):
        return len(self.epsIds)

    @property
    def key(self):
        return "{}-{}".format(self.nasId, self.bookId)

    @property
    def maxDownloadPic(self):
        if not hasattr(QtOwner().owner, "downloadView"):
            return  0
        downloadInfo = QtOwner().downloadView.downloadDict.get(self.bookId)
        if not downloadInfo:
            return max(1, len(self.epsIds))
        return len(set(downloadInfo.epsIds) | set(self.epsIds))

    @property
    def nasTitle(self):
        if not hasattr(QtOwner().owner, "nasView"):
            return  ""
        nasInfo = QtOwner().owner.nasView.nasDict.get(self.nasId)
        if not nasInfo:
            return ""
        return nasInfo.title

    def GetStatusMsg(self):
        if self.statusMsg:
            return Str.GetStr(self.statusMsg)
        return ""

    def UploadInit(self):
        downloadInfo = QtOwner().downloadView.downloadDict.get(self.bookId)
        if not downloadInfo:
            return Str.CvWaitDown
        from view.download.download_item import DownloadItem
        assert isinstance(downloadInfo, DownloadItem)
        if not downloadInfo.epsIds:
            return Str.CvWaitDown
        if self.curPreUpIndex < 0:
            self.curPreUpIndex = downloadInfo.epsIds[0]
        if self.curPreUpIndex not in downloadInfo.epsInfo:
            return Str.CvWaitDown

        if self.IsNeedGetXml():
            return self.WaitXmlInfo
        return self.Uploading

    def IsNeedGetXml(self):
        if self.isCbz:
            from tools.book import BookMgr
            book = BookMgr().GetBook(self.bookId)
            if not book:
                return True
        return False

    def UploadSucCallBack(self):
        self.type += 1
        if self.type > QtUpTask.Upload:
            st, nexEpsId = self.GetNextEps()
            if st != Str.Ok:
                return st
            if self.curPreUpIndex >= 0:
                self.epsIds.append(self.curPreUpIndex)
            self.curPreUpIndex = nexEpsId
            return Str.CvUpload
        return Str.CvUpload

    def GetNextEps(self):
        downloadInfo = QtOwner().downloadView.downloadDict.get(self.bookId)
        if not downloadInfo:
            return Str.CvWaitDown, ""
        notEps = sorted(list(set(downloadInfo.epsIds) - set(self.epsIds)))
        if not notEps:
            return Str.CvSuccess, ""
        return Str.Ok, notEps[0]

    def GetNextParams(self):
        # srcDir
        # desFile
        # upPath
        params = ("", "", "", "")
        st = self.CheckIsOk()
        if st != Str.Ok:
            return st, params
        downloadInfo = QtOwner().downloadView.downloadDict.get(self.bookId)
        if not downloadInfo:
            return Str.CvWaitDown, params

        if self.curPreUpIndex in self.epsIds:
            st, epsId = self.GetNextEps()
            if st != Str.Ok:
                return st, params
            self.type = 1
            self.curPreUpIndex = epsId

        if self.curPreUpIndex not in downloadInfo.epsInfo:
            return Str.CvWaitDown, params
        epsInfo = downloadInfo.epsInfo[self.curPreUpIndex]
        from view.download.download_item import DownloadItem
        assert isinstance(downloadInfo, DownloadItem)
        from view.download.download_item import DownloadEpsItem
        assert isinstance(epsInfo, DownloadEpsItem)
        if not epsInfo.epsTitle:
            return Str.CvWaitDown, params

        srcDir = os.path.join(downloadInfo.savePath, ToolUtil.GetCanSaveName(epsInfo.epsTitle))

        nasInfo = QtOwner().owner.nasView.nasDict.get(self.nasId)
        if not nasInfo:
            return Str.CvNotNet, params


        if nasInfo.is_waifu2x:
            srcDir = os.path.join(downloadInfo.convertPath, ToolUtil.GetCanSaveName(epsInfo.epsTitle))

        desPath = os.path.join(os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), "zip"), ToolUtil.GetCanSaveName(downloadInfo.title))

        if self.curPreUpIndex == 0:
            desFile = os.path.join(desPath, "{}.zip".format(ToolUtil.GetCanSaveName(downloadInfo.title)))
        else:
            desFile = os.path.join(desPath, "{}_{}.zip".format(ToolUtil.GetCanSaveName(downloadInfo.title),
                                                               self.curPreUpIndex + 1))
        # 不单独新增目录
        if nasInfo.dir_index == 0:
            upPath = nasInfo.path + "/"
        elif nasInfo.dir_index == 1:
            upPath = nasInfo.path + "/" + ToolUtil.GetCanSaveName(downloadInfo.title) + "/"
            desFile = os.path.join(desPath, "{}.zip".format(epsInfo.epsTitle))
        else :
            tick = int(time.time())
            day = time.strftime('%Y-%m-%d', time.localtime(tick))
            upPath = nasInfo.path + "/" + day + "/"
        if self.isCbz:
            desFile = desFile.replace(".zip", ".cbz")

        return Str.CvUpload, (nasInfo, srcDir, desFile, upPath)

    def CheckIsOk(self):
        nasInfo = QtOwner().owner.nasView.nasDict.get(self.nasId)
        if not nasInfo:
            return Str.CvNotNet
        assert isinstance(nasInfo, NasInfoItem)
        downloadInfo = QtOwner().downloadView.downloadDict.get(self.bookId)
        if not downloadInfo:
            return Str.CvWaitDown
        from view.download.download_item import DownloadItem
        assert isinstance(downloadInfo, DownloadItem)
        if not downloadInfo.epsInfo:
            return Str.CvWaitDown
        if self.curPreUpIndex < 0:
            self.curPreUpIndex = downloadInfo.epsInfo[0]
        if self.curPreUpIndex not in downloadInfo.epsInfo:
            return Str.CvWaitDown
        isDownload = downloadInfo.IsEpsComplete(self.curPreUpIndex)
        if not isDownload:
            return Str.CvWaitDown

        if nasInfo.is_waifu2x:
            IsWaifu2x = downloadInfo.IsWaifu2xComplete(self.curPreUpIndex)
            if not IsWaifu2x:
                return Str.CvWaifu2x
        return Str.Ok


class NasInfoItem(QtTaskBase):
    def __init__(self):
        QtTaskBase.__init__(self)
        self.nasId = ""
        self.title = ""
        self.eps_ids = []
        self.address = ""
        self.port = 0
        self.path = ""
        self.type = 0
        self.user = ""
        self.passwd = ""
        self.compress_index = 0  # 压缩方式 0: zip, 1: cbz
        self.save_index = 0      #
        self.dir_index = 0       # 目录设置
        self.is_waifu2x = 0

        self.tick = int(time.time())
        self.dirty = True

    @property
    def isCbz(self):
        return self.compress_index == 1

    @property
    def showTitle(self):
        if self.is_waifu2x:
            return self.title + "(waifu2x)"
        return self.title

    def GetCompressName(self):
        if self.compress_index == 0:
            return "zip"
        return "cbz"