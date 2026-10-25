import base64
import json
import pickle
import time
from datetime import datetime, timedelta, timezone
from functools import partial

from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QDesktopServices, Qt
from PySide6.QtWidgets import QWidget, QMessageBox

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from interface.ui_help import Ui_Help
from qt_owner import QtOwner
from server import req
from server.sql_server import SqlServer, DbBook
from task.qt_task import QtTaskBase
# from task.task_thread import ThreadPrintDns
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil
from view.help.help_log_widget import HelpLogWidget


class HelpView(QWidget, Ui_Help, QtTaskBase):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Help.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.dbUpdateUrl = GlobalConfig.DBUpdateUrl.value[:]
        # self.dbUpdateDbUrl = [config.DatabaseDownload, config.DatabaseDownload2, config.DatabaseDownload3]
        self.curIndex = 0
        self.curSubVersion = 0
        self.curUpdateTick = 0
        self.pushButton.clicked.connect(self.OpenUrl)
        self.version.setText(config.UpdateVersion)
        self.isCheckUp = False
        self.logButton.clicked.connect(self.OpenLogDir)

        self.isHaveDb = False
        self.dbCheck.clicked.connect(self.ReUpdateDatabase)
        self.verCheck.clicked.connect(self.InitUpdate)

        # self.updateUrl = [config.UpdateUrl, config.UpdateUrl2, config.UpdateUrl3]
        # self.updatePreUrl = [config.UpdateUrlApi, config.UpdateUrl2Api, config.UpdateUrl3Api]
        self.updateBackUrl = [config.UpdateUrlBack]
        self.checkUpdateIndex = 0
        self.helpLogWidget = HelpLogWidget()
        if Setting.IsShowCmd.value:
            self.helpLogWidget.show()
        else:
            self.helpLogWidget.hide()
        self.openCmd.clicked.connect(self.helpLogWidget.show)
        self.updateWidget.setVisible(False)
        self.selectUrl = ""
        self.updateButton.clicked.connect(self.OpenUpdateUrl)
        self.preCheckBox.setChecked(bool(Setting.IsPreUpdate.value))
        self.preCheckBox.clicked.connect(self.SwitchCheckPre)
        self.configVer.setText("{}({})".format(GlobalConfig.Ver.value, GlobalConfig.VerTime.value))
        # self.dnsCheck = ThreadPrintDns()
        self.configUrlList = [config.AppUrl, config.AppUrl2, config.AppUrl3]
        self.configUrlIndex = 0
        self.updateUrlIndex = 0

        self.timer = QTimer(self)
        minute = 10
        self.timer.setInterval(1000 * (minute * 60))
        self.timer.timeout.connect(self.HourTimeOut)
        self.timer.start()
        self.isUpdating = False

        self.localDbMaxNum = 0
        self.checkJson = {}
        self.allDbBookIds = set()
        self.curFetchLaterPage = 0
        self.maxFetchLaterPage = 20

    def retranslateUi(self, Help):
        Ui_Help.retranslateUi(self, Help)
        self.version.setText(config.RealVersion)
        self.upTimeLabel.setText(config.TimeVersion)
        if config.CanWaifu2x:
            self.waifu2x.setText(config.Waifu2xVersion)
        else:
            self.waifu2x.setText("")
        self.configVer.setText("{}({})".format(GlobalConfig.Ver.value, GlobalConfig.VerTime.value))

    def SwitchCheckPre(self):
        Setting.IsPreUpdate.SetValue(int(self.preCheckBox.isChecked()))

    def Init(self):
        # self.InitUpdateConfig()
        self.CheckDb()
        # self.UpdateDbInfo()

    def InitUpdate(self):
        self.checkUpdateIndex = 0
        self.UpdateText(self.verCheck, Str.CheckUp, "#7fb80e", False)
        self.StartUpdate()

    def StartUpdate(self):
        self.updateWidget.setVisible(False)
        # if self.checkUpdateIndex > len(self.updateUrl) -1:
        #     self.UpdateText(self.verCheck, Str.AlreadyUpdate, "#ff4081", True)
        #     return
        self.updateUrlIndex = 0
        self.AddHttpTask(req.CheckUpdateReq(self.configUrlList[self.updateUrlIndex], Setting.IsPreUpdate.value),
                         self.InitUpdateBack)

    def InitUpdateBack(self, raw):
        try:
            st = raw.get("st")
            if st != Str.Ok:
                self.UpdateText(self.verCheck, st, "#d71345", True)
                self.updateUrlIndex += 1
                if self.updateUrlIndex >= len(self.configUrlList):
                    return
                self.AddHttpTask(req.CheckUpdateReq(self.configUrlList[self.updateUrlIndex], Setting.IsPreUpdate.value),
                                 self.InitUpdateBack)
                return
            data = raw.get("data")
            if not data:
                self.UpdateText(self.verCheck, Str.AlreadyUpdate, "#ff4081", True)
                return
            if data == "no":
                self.UpdateText(self.verCheck, Str.AlreadyUpdate, "#ff4081", True)
                return

            self.AddHttpTask(req.CheckUpdateInfoReq(self.configUrlList[self.updateUrlIndex], data),
                             self.InitUpdateInfoBack)
            self.UpdateText(self.verCheck, Str.HaveUpdate, "#d71345", True)
        except Exception as es:
            Log.Error(es)

    def InitUpdateInfoBack(self, raw):
        data = raw.get("data")
        self.SetNewUpdate(self.updateBackUrl[self.checkUpdateIndex],
                          Str.GetStr(Str.CurVersion) + config.UpdateVersion + ", " + Str.GetStr(
                              Str.CheckUpdateAndUp) + "\n\n" + data)

    def InitUpdateConfig(self):
        self.AddHttpTask(req.CheckUpdateConfigReq(self.configUrlList[self.configUrlIndex]), self.InitUpdateConfigBack)

    def InitUpdateConfigBack(self, raw):
        try:
            st = raw.get("st")
            if st != Str.Ok:
                self.configUrlIndex += 1
                if self.configUrlIndex >= len(self.configUrlList):
                    # self.StartCheckDns()
                    return
                self.AddHttpTask(req.CheckUpdateConfigReq(self.configUrlList[self.configUrlIndex]),
                                 self.InitUpdateConfigBack)
                return
            # self.StartCheckDns()
            data = raw.get("data")
            if not data:
                return
            GlobalConfig.UpdateSetting(data)
            self.configVer.setText("{}({})".format(GlobalConfig.Ver.value, GlobalConfig.VerTime.value))
        except Exception as es:
            Log.Error(es)

    # def StartCheckDns(self):
    #     self.dnsCheck.hostList.append(config.AppUrl)
    #     self.dnsCheck.hostList.append(config.AppUrl2)
    #     self.dnsCheck.hostList.append(config.AppUrl3)
    #     self.dnsCheck.hostList.append(config.Url)
    #     self.dnsCheck.hostList.append(GlobalConfig.ProxyApiDomain.value)
    #     self.dnsCheck.hostList.append(GlobalConfig.ProxyApiDomain2.value)
    #     self.dnsCheck.hostList.extend(GlobalConfig.ImageServerList.value)
    #     self.dnsCheck.hostList.extend(GlobalConfig.ImageJumList.value)
    #     self.dnsCheck.start()

    def CheckDb(self):
        self.AddSqlTask("book", "", SqlServer.TaskCheck, self.CheckDbBack)

    def CheckDbBack(self, data):
        from qt_owner import QtOwner
        if not data:
            Log.Error("Not found book.db !!!!!!!!!!!!!!!")
            QtOwner().SetDbError()
            QtOwner().ShowErrOne("无法加载本地数据库db/book.db")
            QtOwner().favorityView.InitFavorite()
            return
        self.isHaveDb = True
        QtOwner().canUseDb = True
        self.UpdateDbInfo()
        QtOwner().favorityView.InitFavorite()
        return

    def SwitchCurrent(self, **kwargs):
        self.configVer.setText("{}({})".format(GlobalConfig.Ver.value, GlobalConfig.VerTime.value))
        self.UpdateDbInfo()
        return

    def UpdateDbInfo(self):
        if not self.isHaveDb:
            return
        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectUpdate, self.UpdateDbInfoBack)

    def UpdateDbInfoBack(self, data):
        if data is None:
            QtOwner().ShowError(Str.GetStr(Str.Error))
            return

        dbVer, num, timeStr, version = data
        config.DbVersion = dbVer
        self.curSubVersion = version
        lastUpdateDate = datetime.strptime(timeStr+" +0800", "%Y-%m-%d %H:%M:%S %z")
        self.curUpdateTick = int(lastUpdateDate.timestamp())

        self.localVer.setText(dbVer)
        self.localDbMaxNum = num
        self.localNum.setText(str(num))

        sysNum = self.checkJson.get("num", 0)
        if sysNum:
            self.localNum.setText(Str.GetStr(Str.Local) + f":{self.localDbMaxNum}," + Str.GetStr(Str.Remote) + f":{sysNum}")

        self.localTime.setText(timeStr)
        QtOwner().searchView.UpdateTime(timeStr)
        # if config.RealVersion != dbVer:
        #     self.UpdateText(self.dbCheck, "错误的data.db版本", "#7fb80e", False)
        #     return

        if not self.isCheckUp:
            self.isCheckUp = True
            self.ReUpdateDatabase()
        return

    def HourTimeOut(self):
        if self.isUpdating:
            return
        self.ReUpdateDatabase()

    def ReUpdateDatabase(self):
        self.curIndex = 0
        self.dbUpdateUrl = GlobalConfig.DBUpdateUrl.value[:]
        self.isUpdating = True
        self.InitUpdateDatabase()

    def InitUpdateDatabase(self):
        if QtOwner().isOfflineModel:
            return

        if self.curIndex >= len(self.dbUpdateUrl):
            self.UpdateText(self.dbCheck, Str.NetError, "#d71345", True)
            self.FinishFailUpdateDatabase()
            return

        if self.curUpdateTick <= 0:
            return

        self.UpdateText(self.dbCheck, Str.CheckUp, "#7fb80e", False)
        self.dbCheck.setEnabled(False)
        url = self.dbUpdateUrl[self.curIndex]
        self.AddHttpTask(req.CheckUpdateDatabaseReq(url), self.InitUpdateDatabaseBack)

    def InitUpdateDatabaseBack(self, raw):
        try:
            data = raw["data"]
            self.checkJson = json.loads(data)
            updateTick = self.checkJson.get("version", 0)
            updateDateList = ToolUtil.GetAllNeedUpdateDate(self.curUpdateTick, updateTick)
            self.CheckLoadNextDayData(updateDateList)
        except Exception as es:
            Log.Error(es)
            self.curIndex += 1
            self.InitUpdateDatabase()
            self.UpdateText(self.dbCheck, Str.NetError, "#d71345", True)

    def UpdateText(self, label, text, color, enable):
        label.setStyleSheet("background-color:transparent;color:{}".format(color))
        label.setText("{}".format(Str.GetStr(text, text)))
        label.setEnabled(enable)
        if enable:
            label.setCursor(Qt.PointingHandCursor)
        else:
            label.setCursor(Qt.ArrowCursor)
        return

    def CheckLoadNextDayData(self, updateDateList):
        if not updateDateList:
            if self.curSubVersion > 0:
                self.UpdateText(self.dbCheck, Str.DailyUpdated, "#7fb80e", True)
            else:
                self.UpdateText(self.dbCheck, Str.Updated, "#7fb80e", True)
            self.FinishSucUpdateDatabase()
            return

        if self.curIndex >= len(self.dbUpdateUrl):
            self.UpdateText(self.dbCheck, Str.NetError, "#d71345", True)
            self.FinishFailUpdateDatabase()
            return

        url = self.dbUpdateUrl[self.curIndex]
        dateStr, newTick, type = updateDateList[0]
        if type == "day":
            self.AddHttpTask(req.DownloadDatabaseReq(url, dateStr), self.DownloadDataBack, backParam=updateDateList)
        else:
            assert (type == "week")
            self.AddHttpTask(req.DownloadDatabaseWeekReq(url, dateStr), self.DownloadDataBack, backParam=updateDateList)

    def FinishSucUpdateDatabase(self):
        self.isUpdating = False
        self.timer.setInterval(1000 * 3600)
        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectBookAllIds, self.CheckLocalDbNumBack)
        # 如果数量不对等，则自己爬取数据
        pass

    def CheckLocalDbNumBack(self, data):
        if isinstance(data, set):
            self.allDbBookIds = data
            self.localDbMaxNum = len(self.allDbBookIds)
            ver = self.checkJson.get("version", 0)
            sysNum = self.checkJson.get("num", 0)
            self.localNum.setText(Str.GetStr(Str.Local)+ f":{self.localDbMaxNum},"+Str.GetStr(Str.Remote)+ f":{sysNum}")
            if sysNum > 0 and sysNum > self.localDbMaxNum:
                Log.Warn("db num not equal, ver: {}, sysNum: {}, curNum: {}".format(ver, sysNum, self.localDbMaxNum))
                # self.StartFetchLater()
        return

    def FinishFailUpdateDatabase(self):
        self.isUpdating = False
        self.timer.setInterval(1000 * 60)
        pass

    def DownloadDataBack(self, raw, updateDateList):
        if not updateDateList:
            return
        dateStr, newTick, type = updateDateList[0]
        try:
            CHINA_TZ = timezone(timedelta(hours=8))
            lastUpdateDate = datetime.fromtimestamp(self.curUpdateTick, tz=CHINA_TZ)

            st = raw.get("st")
            data = raw.get('data')
            bookList = raw.get('list', [])
            if st == Str.Ok:
                if not bookList:
                    return
                Log.Info("db: check update, {}, {}->{}, len:{}".format(
                    type,
                    lastUpdateDate.strftime('%Y-%m-%d'),
                    dateStr, len(bookList))
                )
                if datetime.now(tz=CHINA_TZ).strftime('%Y-%m-%d') == dateStr:
                    self.curSubVersion = len(bookList)
                self.curUpdateTick = newTick
                updateDateList.pop(0)
                self.AddSqlTask("book", (bookList, newTick, self.curSubVersion), SqlServer.TaskTypeUpdateBook)
            else:
                Log.Warn("db: check update err, index:{}, {}, {}->{}, st:{}, data:{}".format(
                    self.curIndex, type,
                    lastUpdateDate.strftime('%Y-%m-%d'),
                    dateStr, st, data)
                )
                self.curIndex += 1
        except Exception as es:
            self.curIndex += 1
            Log.Error(es)
        finally:
            self.CheckLoadNextDayData(updateDateList)

    def OpenUrl(self):
        UrlList = [config.Issues1]
        url = UrlList[0] if self.checkUpdateIndex >= len(UrlList) else UrlList[self.checkUpdateIndex]
        QDesktopServices.openUrl(QUrl(url))

    def OpenProxyUrl(self):
        UrlList = [config.ProxyUrl1]
        url = UrlList[0] if self.checkUpdateIndex >= len(UrlList) else UrlList[self.checkUpdateIndex]
        QDesktopServices.openUrl(QUrl(url))

    def OpenLogDir(self):
        path = Setting.GetLogPath()
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        return

    def SetNewUpdate(self, updateUrl, updateLog):
        self.updateWidget.setVisible(True)
        self.selectUrl = updateUrl
        self.updateLabel.setText(updateLog)
        QtOwner().owner.navigationWidget.SetNewUpdate()
        return

    def OpenUpdateUrl(self):
        QDesktopServices.openUrl(QUrl(self.selectUrl))
        return

    def Stop(self):
        self.timer.stop()

    # def StartFetchLater(self, fetchPage=20):
    #     self.curFetchLaterPage = 0
    #     self.maxFetchLaterPage = self.checkJson.get("fetch_page", 0)
    #     if self.maxFetchLaterPage <= 0:
    #         self.maxFetchLaterPage = fetchPage
    #     pass