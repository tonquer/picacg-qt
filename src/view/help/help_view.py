import base64
import pickle

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget

from config import config
from config.setting import Setting
from interface.ui_help import Ui_Help
from server import req
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.tool import ToolUtil


class HelpView(QWidget, Ui_Help, QtTaskBase):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Help.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.updateUrl = [config.DatabaseUpdate2, config.DatabaseUpdate]
        self.updateDbUrl = [config.DatabaseDownload2, config.DatabaseDownload]
        self.curIndex = 0
        self.curSubVersion = 0
        self.curUpdateTick = 0
        self.pushButton.clicked.connect(self.OpenUrl)
        self.version.setText(config.UpdateVersion)
        self.isCheckUp = False
        self.logButton.clicked.connect(self.OpenLogDir)

    def Init(self):
        self.UpdateDbInfo()

    def SwitchCurrent(self, **kwargs):
        self.UpdateDbInfo()
        return

    def UpdateDbInfo(self):
        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectUpdate, self.UpdateDbInfoBack)

    def UpdateDbInfoBack(self, data):
        num, timeStr, version = data
        self.curSubVersion = version
        self.curUpdateTick = ToolUtil.GetTimeTickEx(timeStr)
        self.localNum.setText(str(num))
        self.local.setText(timeStr)
        if not self.isCheckUp:
            self.isCheckUp = True
            self.InitUpdateDatabase()
        return

    def InitUpdateDatabase(self):
        if self.curUpdateTick <= 0:
            return
        # self.searchForm.SetUpdateText(self.tr("正在更新"), "#7fb80e", False)
        if self.curIndex >= len(self.updateUrl):
            return
        url = self.updateUrl[self.curIndex]
        self.AddHttpTask(req.CheckUpdateDatabaseReq(url), self.InitUpdateDatabaseBack)

    def InitUpdateDatabaseBack(self, raw):
        try:
            data = raw["data"]
            updateTick = int(data)
            self.CheckLoadNextDayData(updateTick)

        except Exception as es:
            Log.Error(es)
            self.curIndex += 1
            self.InitUpdateDatabase()
            # self.searchForm.SetUpdateText(self.tr("无法连接 raw.githubusercontent.com"), "#d71345", True)

    def CheckLoadNextDayData(self, newTick):
        if newTick <= self.curUpdateTick:
            # if self.curSubVersion > 0:
            #     self.searchForm.SetUpdateText(self.tr("今日已更新") + str(self.curSubVersion), "#7fb80e", True)
            # else:
            #     self.searchForm.SetUpdateText(self.tr("已更新"), "#7fb80e", True)
            return
        day = ToolUtil.DiffDays(newTick, self.curUpdateTick)
        url = self.updateDbUrl[self.curIndex]
        if day <= 0:
            self.AddHttpTask(req.DownloadDatabaseReq(url, newTick), self.DownloadDataBack, backParam=(newTick, newTick))
        else:
            self.curSubVersion = 0
            self.AddHttpTask(req.DownloadDatabaseReq(url, self.curUpdateTick), self.DownloadDataBack, backParam=(ToolUtil.GetCurZeroDatatime(self.curUpdateTick + 24*3600), newTick))
        return

    def DownloadDataBack(self, raw, v):
        updateTick, newTick = v
        try:
            data = raw["data"]
            if not data:
                # self.searchForm.SetUpdateText(self.tr("无法连接 raw.githubusercontent.com"), "#d71345", True)
                return
            Log.Info("db: check update, {}->{}->{}".format(self.curUpdateTick, updateTick, newTick))
            if len(data) <= 100:
                Log.Info("Update code: {}".format(data))
                pass
            elif data:
                if ToolUtil.DiffDays(updateTick, self.curUpdateTick) <= 0:
                    # 分割数据
                    dataList = data.split("\r\n")
                    dataList = list(filter(lambda data: data != "", dataList))
                    rawList = dataList[self.curSubVersion:]
                    self.curSubVersion = len(dataList)
                else:
                    # 全部更新
                    rawList = data.split("\r\n")
                addData = self.ParseBookInfo(rawList)
                self.AddSqlTask("book", (addData, updateTick, self.curSubVersion), SqlServer.TaskTypeUpdateBook)
        except Exception as es:
            Log.Error(es)
        finally:
            self.curUpdateTick = updateTick
            self.CheckLoadNextDayData(newTick)

    def ParseBookInfo(self, rawList):
        infos = []
        try:
            for raw in rawList:
                if not raw:
                    continue
                data = base64.b64decode(raw.encode('utf-8'))
                book = pickle.loads(data)
                infos.append(book)
        except Exception as es:
            Log.Error(es)
        finally:
            return infos

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl(config.Issues))

    def OpenLogDir(self):
        path = Setting.GetLogPath()
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        return