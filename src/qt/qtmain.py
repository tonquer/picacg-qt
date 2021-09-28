import base64
import pickle
import weakref

from PySide2 import QtWidgets, QtGui  # 导入PySide2部件
from PySide2.QtCore import QTimer, QUrl, QObject, QCoreApplication, QSize
from PySide2.QtGui import QDesktopServices, Qt, QGuiApplication
from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import QTranslator, QLocale
from PySide2.QtCore import QSettings

from conf import config
from src.server import req, ToolUtil, Status
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

    @property
    def readForm(self):
        form = self._owner().qtReadImg
        from src.qt.read.qtreadimg import QtReadImg
        assert isinstance(form, QtReadImg)
        return form

    def SetOwner(self, owner):
        self._owner = weakref.ref(owner)

    def GetV(self, k, defV=""):
        return self.owner.settingForm.GetSettingV(k, defV)

    def SetV(self, k, v):
        return self.owner.settingForm.SetSettingV(k, v)

    def ShowMsgBox(self, type, title, msg):
        msg = QMessageBox(type, title, msg)
        msg.addButton("Yes", QMessageBox.AcceptRole)
        if type == QMessageBox.Question:
            msg.addButton("No", QMessageBox.RejectRole)
        if config.ThemeText == "flatblack":
            msg.setStyleSheet("QWidget{background-color:#2E2F30}")
        return msg.exec_()


class BikaQtMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        config.Language = QSettings('config.ini', QSettings.IniFormat).value('Language', '')
        # self.language = 'English'
        # self.language = config.Language

        self.translator_about = None
        self.translator_bookinfo = None
        self.translator_booksimple = None
        self.translator_category = None
        self.translator_chatroom = None
        self.translator_chatroomsg = None
        self.translator_comment = None
        self.translator_download = None
        self.translator_favorite = None
        self.translator_fried = None
        self.translator_fried_msg = None
        self.translator_game = None
        self.translator_gameinfo = None
        self.translator_history = None
        self.translator_img = None
        self.translator_index = None
        self.translator_leavemsg = None
        self.translator_loading = None
        self.translator_login = None
        self.translator_login_proxy = None
        self.translator_main = None
        self.translator_qtespinfo = None
        self.translator_rank = None
        self.translator_readimg = None
        self.translator_register = None
        self.translator_search = None
        self.translator_setting = None
        self.translator_user = None
        self.translator_user_info = None
        self.translator_common = None

        # self.translator_setting = QTranslator()
        # self.translator_setting.load(QLocale(), "./translations/setting_en.qm")
        # if not self.app.installTranslator(self.translator_setting):
        #     Log.Warn('Setting translation load failed.')

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        QtOwner().SetOwner(self)
        self._app = weakref.ref(app)

        self.LoadTranslate()

        from src.qt.chat.qtchat import QtChat
        from src.qt.main.qt_fried import QtFried
        from src.qt.main.qtindex import QtIndex
        from src.qt.menu.qtabout import QtAbout
        from src.qt.read.qtbookinfo import QtBookInfo
        from src.qt.com.qtmsg import QtMsgLabel
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
        from src.qt.user.qt_login_proxy import QtLoginProxy

        self.userInfo = None
        self.setupUi(self)
        self.msgForm = QtMsgLabel(self)

        self.qtTask = QtTask()
        # pix = QPixmap()
        # pix.loadFromData(resources.DataMgr.GetData("loading_2"))
        # pix = pix.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.setCursor(QCursor(pix))
        ToolUtil.SetIcon(self)

        self.settingForm = QtSetting(self)
        self.qtReadImg = QtReadImg()
        self.settingForm.LoadSetting()
        self.qtReadImg.LoadSetting()

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
        self.loginProxyForm = QtLoginProxy()
        self.registerForm = QtRegister()

        self.historyForm = QtHistory()


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
        desktop = QGuiApplication.primaryScreen().geometry()
        self.resize(desktop.width() // 4 * 3, desktop.height() // 4 * 3)
        self.move(desktop.width() // 8, desktop.height() // 8)

        if self.settingForm.mainSize:
            assert isinstance(self.settingForm.mainSize, QSize)
            desktop = QGuiApplication.primaryScreen().geometry()
            if self.settingForm.mainSize.width() == desktop.width():
                self.setMinimumSize(desktop.width() // 4 * 3, desktop.height() // 4 * 3)
                self.setWindowState(Qt.WindowMaximized)
            else:
                self.resize(self.settingForm.mainSize)
                x = (desktop.width() - self.settingForm.mainSize.width()) // 2
                y = (desktop.height() - self.settingForm.mainSize.height()) // 2
                self.move(x, max(0, y))

        if self.settingForm.bookSize:
            desktop = QGuiApplication.primaryScreen().geometry()
            if self.settingForm.bookSize.width() == desktop.width():
                self.bookInfoForm.setMinimumSize(desktop.width() // 4 * 3, desktop.height() // 4 * 3)
                self.bookInfoForm.setWindowState(Qt.WindowMaximized)
            else:
                self.bookInfoForm.resize(self.settingForm.bookSize)
                x = (desktop.width() - self.settingForm.bookSize.width()) // 2
                y = (desktop.height() - self.settingForm.bookSize.height()) // 2
                self.bookInfoForm.move(x, max(0, y))

        # self.qtReadImg.resize(self.settingForm.readSize)

        self.loginForm.userIdEdit.setText(self.settingForm.userId)
        self.loginForm.passwdEdit.setText(self.settingForm.passwd)

        # self.menusetting.
        self.menusetting.triggered.connect(self.OpenSetting)
        self.menuabout.triggered.connect(self.OpenAbout)
        # self.setStyleSheet("background-color:#242629;")
        self.curSubVersion = 0  # 当前子版本
        self.curUpdateTick = 0  # 当前更新日时间戳

    @property
    def app(self):
        return self._app()

    def LoadTranslate(self):
        installTag = ""
        if config.Language == "":
            locale = QLocale.system().name()
            Log.Info("Init translate {}".format(locale))
            if locale[:3].lower() == "zh_":
                if locale.lower() != "zh_cn":
                    config.Language = "Chinese-Traditional"
                    installTag = "tc"
                else:
                    config.Language = "Chinese-Simplified"

            else:
                config.Language = "English"

        if config.Language == "Chinese-Traditional":
            install = True
            installTag = "tc"
        elif config.Language == "English":
            install = True
            installTag = "en"
        else:
            install = False

        self.loadTrans(self.app, 'about', installTag, install)
        self.loadTrans(self.app, 'bookinfo', installTag, install)
        self.loadTrans(self.app, 'common', installTag, install)
        # self.loadTrans(app, 'booksimple', 'en')
        # self.loadTrans(app, 'chatroom', 'en')
        # self.loadTrans(app, 'chatroomsg', 'en')
        self.loadTrans(self.app, 'comment', installTag, install)
        self.loadTrans(self.app, 'download', installTag, install)
        # self.loadTrans(app, 'favorite', 'en')
        # self.loadTrans(app, 'fried', 'en')
        # self.loadTrans(app, 'fried_msg', 'en')
        # self.loadTrans(app, 'game', 'en')
        # self.loadTrans(app, 'gameinfo', 'en')
        # self.loadTrans(app, 'history', 'en')
        self.loadTrans(self.app, 'img', installTag, install)
        self.loadTrans(self.app, 'index', installTag, install)

        # self.loadTrans(app, 'leavemsg', 'en')
        # self.loadTrans(app, 'loading', 'en')
        self.loadTrans(self.app, 'login', installTag, install)
        self.loadTrans(self.app, 'login_proxy', installTag, install)

        self.loadTrans(self.app, 'main', installTag, install)
        # self.loadTrans(app, 'qtespinfo', 'en')
        self.loadTrans(self.app, 'rank', installTag, install)
        self.loadTrans(self.app, 'readimg', installTag, install)
        self.loadTrans(self.app, 'register', installTag, install)
        self.loadTrans(self.app, 'search', installTag, install)
        self.loadTrans(self.app, 'setting', installTag, install)
        self.loadTrans(self.app, 'user', installTag, install)

    def RetranslateUi(self):
        self.retranslateUi(self)
        self.aboutForm.retranslateUi(self.aboutForm)
        self.bookInfoForm.retranslateUi(self.bookInfoForm)
        self.downloadForm.retranslateUi(self.downloadForm)
        self.qtReadImg.qtTool.retranslateUi(self.qtReadImg.qtTool)
        self.indexForm.retranslateUi(self.indexForm)
        self.loginForm.retranslateUi(self.loginForm)
        self.loginProxyForm.retranslateUi(self.loginProxyForm)
        self.rankForm.retranslateUi(self.rankForm)
        self.searchForm.retranslateUi(self.searchForm)
        self.registerForm.retranslateUi(self.registerForm)
        self.settingForm.retranslateUi(self.settingForm)
        self.userForm.retranslateUi(self.userForm)
        self.aboutForm.retranslateUi(self.aboutForm)

    def loadTrans(self, app, ui, lang, isInstall):
        setattr(self, "translator_{0}".format(ui), QTranslator())
        translator = getattr(self, "translator_{0}".format(ui))
        translator.load(QLocale(), "./translations/{0}_{1}.qm".format(ui, lang))
        if isInstall:
            if not app.installTranslator(translator):
                Log.Warn("{0}_{1}.qm load failed".format(ui, lang))
        else:
            app.removeTranslator(translator)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        # reply = QtOwner().ShowMsgBox(QMessageBox.Question, self.tr('提示'), self.tr('确定要退出吗？'))
        reply = 0
        if reply == 0:
            a0.accept()
            userId = self.loginForm.userIdEdit.text()
            passwd = self.loginForm.passwdEdit.text()
            self.bookInfoForm.close()
            self.settingForm.ExitSaveSetting(self.size(), self.bookInfoForm.size(), self.qtReadImg.size(), userId, passwd)
        else:
            a0.ignore()

    def Init(self):
        IsCanUse = False
        if config.CanWaifu2x:
            import waifu2x
            stat = waifu2x.init()
            if stat < 0:
                self.msgForm.ShowError(self.tr("waifu2x初始化错误"))
            else:
                IsCanUse = True
                gpuInfo = waifu2x.getGpuInfo()
                if gpuInfo:
                    self.settingForm.SetGpuInfos(gpuInfo)
                if gpuInfo and config.Encode < 0:
                    config.Encode = 0

                waifu2x.initSet(config.Encode, config.Waifu2xThread)
                Log.Info("waifu2x初始化: " + str(stat) + " encode: " + str(config.Encode) + " version:" + waifu2x.getVersion())
        else:
            self.msgForm.ShowError(self.tr("waifu2x无法启用, ")+config.ErrorMsg)

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

        if config.IsUpdate:
            self.InitUpdate()

        self.loginForm.Init()
        return

    def OpenSetting(self, action):
        if action.text() in ("设置", "設置", "Settings"):
            self.settingForm.show()
        elif action.text() in ("代理", "Proxy"):
            self.loginProxyForm.show()
        pass

    def OpenAbout(self, action):
        if action.text() in ("关于", "關於", "About"):
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
            r = QMessageBox.information(self, self.tr("更新"), self.tr("当前版本") + config.UpdateVersion + ", "+ self.tr("检查到更新，是否前往更新\n") + data,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2))
        except Exception as es:
            Log.Error(es)

    def InitUpdateBack2(self, data):
        try:
            if not data:
                return
            r = QMessageBox.information(self, self.tr("更新"), self.tr("当前版本") + config.UpdateVersion + ", "+ self.tr("检查到更新，是否前往更新\n") + data,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2Back))
        except Exception as es:
            Log.Error(es)

    def InitUpdateDatabase(self):
        self.searchForm.SetUpdateText(self.tr("正在更新"), "#7fb80e", False)
        self.qtTask.AddHttpTask(req.CheckUpdateDatabaseReq(), self.InitUpdateDatabaseBack)

    def InitUpdateDatabaseBack(self, data):
        try:
            updateTick = int(data)
            self.CheckLoadNextDayData(updateTick)

        except Exception as es:
            Log.Error(es)
            self.searchForm.SetUpdateText(self.tr("无法连接 raw.githubusercontent.com"), "#d71345", True)

    def CheckLoadNextDayData(self, newTick):
        if newTick <= self.curUpdateTick:
            self.searchForm.UpdateDbInfo()
            if self.curSubVersion > 0:
                self.searchForm.SetUpdateText(self.tr("今日已更新") + str(self.curSubVersion), "#7fb80e", True)
            else:
                self.searchForm.SetUpdateText(self.tr("已更新"), "#7fb80e", True)
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
            if not data:
                self.searchForm.SetUpdateText(self.tr("无法连接 raw.githubusercontent.com"), "#d71345", True)
                return
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

    def GetStatusStr(self, data):
        if data == Status.NetError:
            return self.tr("网络错误，请检查代理设置")
        elif data == Status.UserError:
            return self.tr("用户名密码错误")
        elif data == Status.RegisterError:
            return self.tr("注册失败")
        elif data == Status.NotFoundBook:
            return self.tr("未找到书籍")
        elif data == Status.UnderReviewBook:
            return self.tr("本子审核中")
        elif data == Status.UnderReviewBook:
            return self.tr("头像设置出错了, 请尽量选择500kb以下的图片，")
        elif data == Status.UnKnowError:
            return self.tr("未知错误, ")
        return data