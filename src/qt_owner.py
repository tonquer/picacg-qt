import sys
import weakref

from PySide6.QtCore import QFile

from component.label.msg_label import MsgLabel
from tools.singleton import Singleton
from tools.str import Str
from tools.tool import ToolUtil


class QtOwner(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self._owner = None
        self._app = None
        self._localServer = None
        self.backSock = None
        self.isUseDb = True
        self.isOfflineModel = False
        self.closeType = 1   # 1普通， 2关闭弹窗触发， 3任务栏触发

    # db不可使用
    def SetDbError(self):
        self.owner.searchView.SetDbError()
        self.isUseDb = False
        return

    def ShowError(self, msg):
        return MsgLabel.ShowErrorEx(self.owner, msg)

    def ShowMsg(self, msg):
        return MsgLabel.ShowMsgEx(self.owner, msg)

    def IsInFilter(self, name1, name2, name3):
        return self.owner.navigationWidget.IsInFilter(name1, name2, name3)
    
    def CheckShowMsg(self, raw):
        msg = raw.get("st")
        code = raw.get("code")
        if code:
            errorMsg = ToolUtil.GetCodeErrMsg(code)
            if errorMsg:
                return self.ShowError(errorMsg)

        errorMsg = raw.get("errorMsg")
        if errorMsg:
            return self.ShowError(errorMsg)

        message = raw.get("message")
        if message:
            return self.ShowMsg(message)

        elif isinstance(msg, int):
            return self.ShowError(Str.GetStr(msg))
        else:
            return self.ShowError(msg)

    def ShowMsgOne(self, msg):
        if not hasattr(self.owner, "msgLabel"):
            return
        return self.owner.msgLabel.ShowMsg(msg)

    def ShowErrOne(self, msg):
        if not hasattr(self.owner, "msgLabel"):
            return
        return self.owner.msgLabel.ShowError(msg)

    def ShowLoading(self):
        self.owner.loadingDialog.show()
        return

    def CloseLoading(self):
        self.owner.loadingDialog.close()
        return

    def GetNasInfo(self, nasId):
        return self.owner.nasView.nasDict.get(nasId)

    def CopyText(self, text):
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        from tools.str import Str
        QtOwner().ShowMsg(Str.GetStr(Str.CopySuc))

    def OpenProxy(self):
        from view.user.login_view import LoginView
        loginView = LoginView(QtOwner().owner, False)
        loginView.tabWidget.setCurrentIndex(3)
        loginView.tabWidget.removeTab(0)
        loginView.tabWidget.removeTab(0)
        loginView.tabWidget.removeTab(0)
        loginView.loginButton.setText(Str.GetStr(Str.Save))
        loginView.show()

        loginView.closed.connect(QtOwner().owner.navigationWidget.UpdateProxyName)
        return

    @property
    def owner(self):
        from view.main.main_view import MainView
        assert isinstance(self._owner(), MainView)
        return self._owner()

    @property
    def app(self):
        return self._app()

    @property
    def localServer(self):
        return self._localServer()

    @property
    def localFavoriteView(self):
        return self.owner.localFavoriteView

    @property
    def nasView(self):
        return self.owner.nasView

    @property
    def downloadView(self):
        return self.owner.downloadView

    @property
    def loginWebView(self):
        return self.owner.loginWebView

    @property
    def historyView(self):
        return self.owner.historyView

    @property
    def gameInfoView(self):
        return self.owner.gameInfoView

    @property
    def bookInfoView(self):
        return self.owner.bookInfoView

    @property
    def localReadView(self):
        return self.owner.localReadView

    @property
    def favoriteView(self):
        return self.owner.favorityView

    @property
    def indexView(self):
        return self.owner.indexView

    @property
    def settingView(self):
        return self.owner.settingView

    @property
    def searchView(self):
        return self.owner.searchView

    def SetSubTitle(self, text):
        return self.owner.setSubTitle(text)

    def GetFileData(self, fileName):
        f = QFile(fileName)
        f.open(QFile.ReadOnly)
        data = f.readAll()
        f.close()
        return bytes(data)

    def AddLocalHistory(self, bookId):
        self.owner.localReadView.AddDataToDB(bookId)

    def OpenComment(self, bookId):
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.owner.commentView, **arg)

    def OpenGameComment(self, commentId):
        arg = {"bookId": commentId}
        self.owner.SwitchWidget(self.owner.gameCommentView, **arg)

    def OpenRank(self):
        arg = {"refresh": True}
        self.owner.SwitchWidget(self.owner.rankView, **arg)

    def OpenIndex(self):
        arg = {"refresh": True}
        self.owner.SwitchWidget(self.owner.indexView, **arg)

    def OpenDownloadAll(self, books):
        arg = {"books": books}
        self.owner.SwitchWidget(self.owner.downloadAllView, **arg)

    def OpenLocalDelAll(self):
        arg = {}
        self.owner.SwitchWidget(self.owner.localReadAllView, **arg)

    def OpenSubComment(self, commentId, widget):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": commentId}
        self.owner.subCommentView.SetWidget(widget)
        self.owner.SwitchWidget(self.owner.subCommentView, **arg)

    def OpenSearch(self, text, isLocal, isTitle, isDes, isCategory, isTag, isAuthor, isUpLoad):
        arg = {"text": text, "isLocal": isLocal, "isTitle": isTitle, "isDes": isDes, "isCategory": isCategory, "isTag":isTag, "isAuthor":isAuthor, "isUpLoad": isUpLoad}
        self.owner.SwitchWidget(self.owner.searchView, **arg)

    def OpenSearch2(self, text, isLocal, isTitle, isDes, isCategory, isTag, isAuthor, isUpLoad):
        arg = {"text": text, "isLocal": isLocal, "isTitle": isTitle, "isDes": isDes, "isCategory": isCategory, "isTag":isTag, "isAuthor":isAuthor, "isUpLoad": isUpLoad}

        if isAuthor:
            title = "作者: {}".format(ToolUtil.GetStrMaxLen(text))
            self.owner.searchView2.setWindowTitle(title)
            self.owner.searchView2.searchTab.setText("作者: {}".format(text))
        elif isTag:
            title = "TAG: {}".format(ToolUtil.GetStrMaxLen(text))
            self.owner.searchView2.setWindowTitle(title)
            self.owner.searchView2.searchTab.setText("TAG: {}".format(text))
        self.owner.SwitchWidget(self.owner.searchView2, **arg)

    def OpenRecomment(self, bookId):
        Title = "看了这边本子的人也在看"
        arg = {"recoment": 1, "bookId": bookId}
        self.owner.searchView2.setWindowTitle(Title)
        self.owner.searchView2.searchTab.setText(Title)
        self.owner.SwitchWidget(self.owner.searchView2, **arg)

    def OpenLocalEpsView(self, bookId):
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.owner.localReadEpsView, **arg)

    def OpenSearchByText(self, text):
        self.owner.searchView.lineEdit.setText(text)
        self.owner.searchView.lineEdit.Search()

    def OpenReadView(self, bookId, index, pageIndex, isOffline=False):
        self.owner.totalStackWidget.setCurrentIndex(1)
        self.owner.readView.OpenPage(bookId, index, pageIndex=pageIndex, isOffline=isOffline)

    def OpenLocalReadView(self, v, epsId=0):
        self.owner.totalStackWidget.setCurrentIndex(1)
        self.owner.readView.OpenLocalPage(v, epsId)

    def CloseReadView(self):
        self.owner.totalStackWidget.setCurrentIndex(0)
        QtOwner().SetSubTitle("")
        QtOwner().bookInfoView.ReloadHistory.emit()

    def OpenSearchByCategory(self, categories):
        arg = {"categories": categories}
        self.owner.SwitchWidget(self.owner.searchView, **arg)

    def OpenSearchByCategory2(self, categories):
        arg = {"categories": categories}
        title = "分类: {}".format(ToolUtil.GetStrMaxLen(categories))
        self.owner.searchView2.setWindowTitle(title)
        self.owner.searchView2.searchTab.setText("分类: {}".format(categories))
        self.owner.SwitchWidget(self.owner.searchView2, **arg)

    def OpenSearchByCreate(self, text):
        arg = {"text": text, "isTitle": False, "isDes": False, "isCategory": False, "isTag":False, "isAuthor": False, "isUpLoad": True}
        title = "上传者: {}".format(ToolUtil.GetStrMaxLen(text))
        self.owner.searchView2.setWindowTitle(title)
        self.owner.searchView2.searchTab.setText("上传者: {}".format(text))
        self.owner.SwitchWidget(self.owner.searchView2, **arg)

    def OpenBookInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.owner.bookInfoView, **arg)

    def OpenLocalBook(self, bookId):
        self.owner.localReadView.OpenLocalBook(bookId)

    def OpenLocalEpsBook(self, bookId):
        self.owner.localReadEpsView.OpenLocalBook(bookId)

    def OpenEpsInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.owner.bookEpsView, **arg)

    def OpenGameInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.owner.gameInfoView, **arg)

    def OpenWaifu2xTool(self, data):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"data": data}
        self.owner.SwitchWidget(self.owner.waifu2xToolView, **arg)

    def SwitchWidgetLast(self):
        self.owner.SwitchWidgetLast()
        return

    def SwitchWidgetNext(self):
        self.owner.SwitchWidgetNext()
        return

    def SetOwner(self, owner):
        self._owner = weakref.ref(owner)

    def SetApp(self, app):
        self._app = weakref.ref(app)

    def SetLocalServer(self, app):
        self._localServer = weakref.ref(app)

    def SetDirty(self):
        pass

    @staticmethod
    def SetFont(app):
        try:
            from tools.log import Log
            from config.setting import Setting
            from PySide6.QtGui import QFont
            f = QFont()
            from tools.langconv import Converter
            if Converter('zh-hans').convert(Setting.FontName.value) == "默认":
                Setting.FontName.InitValue("", "FontName")

            if not Setting.FontName.value and sys.platform == "win32":
                Setting.FontName.InitValue("微软雅黑", "FontName")

            if Converter('zh-hans').convert(str(Setting.FontSize.value)) == "默认":
                Setting.FontSize.InitValue("", "FontSize")

            if Converter('zh-hans').convert(str(Setting.FontStyle.value)) == "默认":
                Setting.FontStyle.InitValue(0, "FontStyle")

            if not Setting.FontName.value and not Setting.FontSize.value and not Setting.FontStyle.value:
                return

            if Setting.FontName.value:
                f = QFont(Setting.FontName.value)

            if Setting.FontSize.value:
                f.setPointSize(int(Setting.FontSize.value))

            if Setting.FontStyle.value:
                fontStyleList = [QFont.Light, QFont.Normal, QFont.DemiBold, QFont.Bold, QFont.Black]
                f.setWeight(fontStyleList[Setting.FontStyle.value - 1])

            app.setFont(f)

        except Exception as es:
            Log.Error(es)

    # def ShowMsg(self, data):
    #     return self.owner.msgForm.ShowMsg(data)
    #
    # def ShowError(self, data):
    #     return self.owner.msgForm.ShowError(data)

    # def ShowMsgBox(self, type, title, msg):
    #     msg = QMessageBox(type, title, msg)
    #     msg.addButton("Yes", QMessageBox.AcceptRole)
    #     if type == QMessageBox.Question:
    #         msg.addButton("No", QMessageBox.RejectRole)
    #     if config.ThemeText == "flatblack":
    #         msg.setStyleSheet("QWidget{background-color:#2E2F30}")
    #     return msg.exec_()