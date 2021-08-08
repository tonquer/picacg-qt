import base64
import pickle
import weakref

from PySide2 import QtWidgets, QtGui  # 导入PySide2部件
from PySide2.QtCore import QTimer, QUrl
from PySide2.QtGui import QDesktopServices
from PySide2.QtWidgets import QMessageBox, QDesktopWidget

from conf import config
from src.server import req, ToolUtil
from src.server.sql_server import SqlServer
from src.util import Log, Singleton
from ui.main import Ui_MainWindow


class QtOwner(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self._owner = None

    @property
    def owner(self):
        assert isinstance(self._owner(), BikaQtMainWindow)
        return self._owner()

    def SetOwner(self, owner):
        self._owner = weakref.ref(owner)

    def GetV(self, k, defV=""):
        return self.owner.settingForm.GetSettingV(k, defV)

    def SetV(self, k, v):
        return self.owner.settingForm.SetSettingV(k, v)


class BikaQtMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        QtOwner().SetOwner(self)
        self._app = weakref.ref(app)
        from src.qt.chat.qtchat import QtChat
        from src.qt.main.qt_fried import QtFried
        from src.qt.main.qtindex import QtIndex
        from src.qt.menu.qtabout import QtAbout
        from src.qt.read.qtbookinfo import QtBookInfo
        from src.qt.com.qtbubblelabel import QtBubbleLabel
        from src.qt.main.qtcategory import QtCategory
        from src.qt.download.qtdownload import QtDownload
        from src.qt.read.qtepsinfo import QtEpsInfo
        from src.qt.user.qtfavorite import QtFavorite
        from src.qt.user.qthistory import QtHistory
        from src.qt.com.qtloading import QtLoading
        from src.qt.user.qtleavemsg import QtLeaveMsg
        from src.qt.user.qtlogin import QtLogin
        from src.qt.main.qtrank import QtRank
        from src.qt.read.qtreadimg import QtReadImg
        from src.qt.user.qtregister import QtRegister
        from src.qt.main.qtsearch import QtSearch
        from src.qt.menu.qtsetting import QtSetting
        from src.qt.util.qttask import QtTask
        from src.qt.user.qtuser import QtUser
        from src.qt.game.qt_game import QtGame
        from src.qt.game.qt_game_info import QtGameInfo
        from src.qt.user.qt_user_comment import QtUserComment

        self.userInfo = None
        self.setupUi(self)
        self.setWindowTitle("哔咔漫画")
        self.msgForm = QtBubbleLabel(self)

        self.qtTask = QtTask()
        # pix = QPixmap()
        # pix.loadFromData(resources.DataMgr.GetData("loading_2"))
        # pix = pix.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.setCursor(QCursor(pix))
        ToolUtil.SetIcon(self)

        self.settingForm = QtSetting(self)
        self.settingForm.LoadSetting()

        self.aboutForm = QtAbout()

        self.indexForm = QtIndex()
        self.searchForm = QtSearch()
        self.favoriteForm = QtFavorite()
        self.downloadForm = QtDownload()
        self.categoryForm = QtCategory()
        self.loadingForm = QtLoading(self)
        self.leaveMsgForm = QtLeaveMsg()
        self.chatForm = QtChat()
        self.rankForm = QtRank()
        self.friedForm = QtFried()
        self.gameForm = QtGame()
        self.myCommentForm = QtUserComment()

        self.loginForm = QtLogin()
        self.registerForm = QtRegister()

        self.historyForm = QtHistory()

        self.qtReadImg = QtReadImg()

        self.userForm = QtUser()
        self.bookInfoForm = QtBookInfo()
        self.gameInfoForm = QtGameInfo()

        self.epsInfoForm = QtEpsInfo()

        self.task = QtTask()
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        # self.timer.timeout.connect(self.OnTimeOut)
        # self.timer.start()

        self.stackedWidget.addWidget(self.loginForm)
        self.stackedWidget.addWidget(self.userForm)


        if self.settingForm.mainSize:
            self.resize(self.settingForm.mainSize)
        else:
            desktop = QDesktopWidget()
            self.resize(desktop.width() // 4 * 2, desktop.height() // 4 * 2)
            self.move(desktop.width() // 4, desktop.height() // 4)
        self.bookInfoForm.resize(self.settingForm.bookSize)
        self.qtReadImg.resize(self.settingForm.readSize)

        self.loginForm.userIdEdit.setText(self.settingForm.userId)
        self.loginForm.passwdEdit.setText(self.settingForm.passwd)

        self.menusetting.triggered.connect(self.OpenSetting)
        self.menuabout.triggered.connect(self.OpenAbout)
        # self.setStyleSheet("background-color:#242629;")
        self.curSubVersion = 0  # 当前子版本
        self.curUpdateTick = 0  # 当前更新日时间戳

    @property
    def app(self):
        return self._app()

        # QtImgMgr().SetOwner(self)
    # def ClearExpiredCache(self):
    #     try:
    #         toPath = os.path.join(config.SavePath, config.CachePathDir)
    #         for root, dirs, names in os.walk(toPath):
    #             for name in names:
    #                 isDel = False
    #                 filename = os.path.join(root, name)
    #                 with open(filename, "rb") as f:
    #                     nameSize = int().from_bytes(f.read(2), byteorder='little')
    #                     timeTick = int().from_bytes(f.read(4), byteorder='little')
    #                     # if int(time.time()) - timeTick >= config.CacheExpired:
    #                     #     isDel = True
    #
    #                 if isDel:
    #                     os.remove(filename)
    #
    #     except Exception as es:
    #         Log.Error(es)


    # def OnTimeOut(self):
    #     self.task.run()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        userId = self.loginForm.userIdEdit.text()
        passwd = self.loginForm.passwdEdit.text()
        self.bookInfoForm.close()
        self.settingForm.ExitSaveSetting(self.size(), self.bookInfoForm.size(), self.qtReadImg.size(), userId, passwd)

    def Init(self):
        IsCanUse = False
        if config.CanWaifu2x:
            import waifu2x
            stat = waifu2x.init()
            if stat < 0:
                self.msgForm.ShowError("waifu2x初始化错误")
            else:
                IsCanUse = True
                gpuInfo = waifu2x.getGpuInfo()
                if gpuInfo:
                    self.settingForm.SetGpuInfos(gpuInfo)
                if gpuInfo and config.Encode < 0:
                    config.Encode = 0

                waifu2x.initSet(config.Encode, config.Waifu2xThread)
                Log.Info("waifu2x初始化: " + str(stat) + " encode: " + str(config.Encode) + " version:" + waifu2x.getVersion())
                # self.msgForm.ShowMsg("waifu2x初始化成功\n" + waifu2x.getVersion())
        else:
            self.msgForm.ShowError("waifu2x无法启用, "+config.ErrorMsg)

        if not IsCanUse:
            self.settingForm.checkBox.setEnabled(False)
            self.qtReadImg.frame.qtTool.checkBox.setEnabled(False)
            config.DownloadAuto = 0
            self.downloadForm.radioButton.setEnabled(False)
            from src.qt.com.qtimg import QtImgMgr
            QtImgMgr().obj.checkBox.setEnabled(False)
            QtImgMgr().obj.changeButton.setEnabled(False)
            QtImgMgr().obj.changeButton.setEnabled(False)
            QtImgMgr().obj.comboBox.setEnabled(False)
            QtImgMgr().obj.SetStatus(False)
            config.IsOpenWaifu = 0

        self.InitUpdate()
        self.loginForm.Init()
        return

    def OpenSetting(self):
        self.settingForm.show()
        pass

    def OpenAbout(self, action):
        if action.text() == "about":
            self.aboutForm.show()
        elif action.text() == "waifu2x":
            from src.qt.com.qtimg import QtImgMgr
            QtImgMgr().ShowImg("")
        pass

    def UpdateDbInfo(self):
        from src.qt.util.qttask import QtTask
        QtTask().AddSqlTask("book", "", SqlServer.TaskTypeSelectUpdate, self.UpdateDbInfoBack)

    def UpdateDbInfoBack(self, data):
        self.LoadDatabaseVersion(data)
        return

    def LoadDatabaseVersion(self, data):
        _, timeStr, version = data
        self.curSubVersion = version
        self.curUpdateTick = ToolUtil.GetTimeTickEx(timeStr)
        if self.curUpdateTick > 0:
            self.InitUpdateDatabase()
        return

    def InitUpdate(self):
        self.qtTask.AddHttpTask(req.CheckUpdateReq(), self.InitUpdateBack)

    def InitUpdateBack(self, data):
        try:
            if not data:
                self.qtTask.AddHttpTask(req.CheckUpdateReq(config.UpdateUrlBack), self.InitUpdateBack2)
                return
            r = QMessageBox.information(self, "更新", "当前版本{} ,检查到更新，是否前往更新\n{}".format(config.UpdateVersion,
                                                                                        data),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2))
        except Exception as es:
            Log.Error(es)

    def InitUpdateBack2(self, data):
        try:
            if not data:
                return
            r = QMessageBox.information(self, "更新", "当前版本{} ,检查到更新，是否前往更新\n{}".format(config.UpdateVersion,
                                                                                        data),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2Back))
        except Exception as es:
            Log.Error(es)

    def InitUpdateDatabase(self):
        self.qtTask.AddHttpTask(req.CheckUpdateDatabaseReq(), self.InitUpdateDatabaseBack)

    def InitUpdateDatabaseBack(self, data):
        try:
            updateTick = int(data)
            self.CheckLoadNextDayData(updateTick)

        except Exception as es:
            Log.Error(es)

    def CheckLoadNextDayData(self, newTick):
        if newTick <= self.curUpdateTick:
            self.searchForm.UpdateDbInfo()
            return
        day = ToolUtil.DiffDays(newTick, self.curUpdateTick)
        if day <= 0:
            self.qtTask.AddHttpTask(req.DownloadDatabaseReq(newTick), self.DownloadDataBack, backParam=(newTick, newTick))
        else:
            self.curSubVersion = 0
            self.qtTask.AddHttpTask(req.DownloadDatabaseReq(self.curUpdateTick), self.DownloadDataBack, backParam=(ToolUtil.GetCurZeroDatatime(self.curUpdateTick + 24*3600), newTick))
        return

    def DownloadDataBack(self, data, v):
        updateTick, newTick = v
        try:
            Log.Info("db: check update, {}->{}->{}".format(self.curUpdateTick, updateTick, newTick))
            if len(data) <= 20:
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
                from src.qt.util.qttask import QtTask
                QtTask().AddSqlTask("book", (addData, updateTick, self.curSubVersion), SqlServer.TaskTypeUpdateBook)
        except Exception as es:
            Log.Error(es)
        finally:
            self.curUpdateTick = updateTick
            self.CheckLoadNextDayData(newTick)

    def Close(self):
        self.downloadForm.Close()
        SqlServer().Stop()
        from src.qt.util.qttask import QtTask
        QtTask().Stop()

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