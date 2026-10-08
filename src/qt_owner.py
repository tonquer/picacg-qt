from __future__ import annotations

import sys
import weakref

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from view.category.category_view import CategoryView
    from view.category.rank_view import RankView

    from view.chat.chat_view import ChatView
    from view.chat_new.chat_new_view import ChatNewView

    from view.comment.comment_view import CommentView
    from view.comment.fried_comment_view import FriedCommentView
    from view.comment.game_comment_view import GameCommentView
    from view.comment.my_comment_view import MyCommentView
    from view.comment.sub_comment_view import SubCommentView

    from view.convert.convert_view import ConvertView

    from view.download.download_all_view import DownloadAllView
    from view.download.download_dir_view import DownloadDirView
    from view.download.download_view import DownloadView

    from view.fried.fried_view import FriedView

    from view.game.game_view import GameView

    from view.help.help_view import HelpView

    from view.index.index_view import IndexView

    from view.info.book_eps_view import BookEpsView
    from view.info.book_info_view import BookInfoView
    from view.info.game_info_view import GameInfoView

    from view.main.main_view import MainView

    from view.nas.nas_add_view import NasAddView
    from view.nas.nas_view import NasView

    from view.read.read_graphics import ReadGraphicsView
    from view.read.read_view import ReadView

    from view.search.search_view import SearchView

    from view.setting.setting_sr_select_view import SettingSrSelectView
    from view.setting.setting_view import SettingView

    from view.tool.batch_sr_tool_view import BatchSrToolView
    from view.tool.forbid_words_view import ForbidWordsView
    from view.tool.local_eps_read_view import LocalEpsReadView
    from view.tool.local_fold_view import LocalFoldView
    from view.tool.local_read_all_view import LocalReadAllView
    from view.tool.local_read_eps_view import LocalReadEpsView
    from view.tool.local_read_view import LocalReadView
    from view.tool.waifu2x_tool_view import Waifu2xToolView

    from view.user.favorite_view import FavoriteView
    from view.user.history_view import HistoryView
    from view.user.local_favorite_fold_view import LocalFavoriteFoldView
    from view.user.local_favorite_view import LocalFavoriteView
    from view.user.login_new_view import LoginNewView
    from component.widget.navigation_widget import NavigationWidget

from PySide6.QtCore import QFile
from PySide6.QtNetwork import QLocalServer
from PySide6.QtWidgets import QApplication

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
        self.canUseDb = False
        self.isUseDb = True
        self.isDbHavePicaID = False
        self.isOfflineModel = False
        self.closeType = 1  # 1普通， 2关闭弹窗触发， 3任务栏触发
        self.isMaxSize = 0
        self.echConfig = ""

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
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        from tools.str import Str
        QtOwner().ShowMsg(Str.GetStr(Str.CopySuc))

    def OpenProxy(self):
        arg = {"refresh": True, "page": 3}
        self.owner.SwitchWidget(self.owner.loginNewView, **arg)
        # from view.user.login_view import LoginView
        # loginView = LoginView(QtOwner().owner, False)
        # loginView.tabWidget.setCurrentIndex(3)
        # loginView.tabWidget.removeTab(0)
        # loginView.tabWidget.removeTab(0)
        # loginView.tabWidget.removeTab(0)
        # loginView.loginButton.setText(Str.GetStr(Str.Save))
        # loginView.show()
        #
        # loginView.closed.connect(QtOwner().owner.navigationWidget.UpdateProxyName)
        return

    @property
    def owner(self) -> MainView:
        return self._owner()

    @property
    def app(self) -> QApplication:
        return self._app()

    @property
    def loginNewView(self) -> LoginNewView:
        return self.owner.loginNewView

    @property
    def localServer(self) -> QLocalServer:
        return self._localServer()

    @property
    def localFavoriteView(self) -> LocalFavoriteView:
        return self.owner.localFavoriteView

    @property
    def nasView(self) -> NasView:
        return self.owner.nasView

    @property
    def downloadView(self) -> DownloadView:
        return self.owner.downloadView

    @property
    def historyView(self) -> HistoryView:
        return self.owner.historyView

    @property
    def gameInfoView(self) -> GameInfoView:
        return self.owner.gameInfoView

    @property
    def bookInfoView(self) -> BookInfoView:
        return self.owner.bookInfoView

    @property
    def localReadView(self) -> LocalReadView:
        return self.owner.localReadView

    @property
    def localReadEpsView(self) -> LocalReadEpsView:
        return self.owner.localReadEpsView

    @property
    def readView(self) -> ReadView:
        return self.owner.readView

    @property
    def favoriteView(self) -> LocalFavoriteView:
        return self.owner.favoriteView

    @property
    def indexView(self) -> IndexView:
        return self.owner.indexView

    @property
    def settingView(self) -> SettingView:
        return self.owner.settingView

    @property
    def searchView(self) -> SearchView:
        return self.owner.searchView

    @property
    def navigationWidget(self) -> NavigationWidget:
        return self.owner.navigationWidget

    @property
    def commentView(self) -> CommentView:
        return self.owner.commentView

    @property
    def gameCommentView(self) -> GameCommentView:
        return self.owner.gameCommentView

    @property
    def rankView(self) -> RankView:
        return self.owner.rankView

    @property
    def bookEpsView(self) -> BookEpsView:
        return self.owner.bookEpsView

    @property
    def subCommentView(self) -> SubCommentView:
        return self.owner.subCommentView

    @property
    def waifu2xToolView(self) -> Waifu2xToolView:
        return self.owner.waifu2xToolView

    @property
    def bookInfoView2(self) -> BookInfoView:
        return self.owner.bookInfoView2

    @property
    def searchView2(self) -> SearchView:
        return self.owner.searchView2

    @property
    def downloadAllView(self) -> DownloadAllView:
        return self.owner.downloadAllView

    @property
    def localReadAllView(self) -> LocalReadAllView:
        return self.owner.localReadAllView

    def UpdateProxyName(self):
        self.owner.navigationWidget.UpdateProxyName()
        return

    def SetSubTitle(self, text):
        return self.owner.setSubTitle(text)

    def GetFileData(self, fileName):
        f = QFile(fileName)
        f.open(QFile.ReadOnly)
        data = f.readAll()
        f.close()
        return bytes(data)

    def OpenSrSelectModel(self, curModelName, callBack):
        from view.setting.setting_sr_select_view import SettingSrSelectView
        loginView = SettingSrSelectView(QtOwner().owner, curModelName)
        loginView.show()
        loginView.Close.connect(callBack)
        return

    def OpenLocalFavoriteFold(self, bookIds="", moveBack=None, foldChangeBack=None):
        from view.user.local_favorite_fold_view import LocalFavoriteFoldView
        w = LocalFavoriteFoldView(QtOwner().owner, bookIds)
        w.show()
        if moveBack:
            w.MoveOkBack.connect(moveBack)
        if foldChangeBack:
            w.FoldChange.connect(foldChangeBack)

    def AddLocalHistory(self, bookId):
        self.localReadView.AddDataToDB(bookId)

    def OpenComment(self, bookId):
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.commentView, **arg)

    def OpenGameComment(self, commentId):
        arg = {"bookId": commentId}
        self.owner.SwitchWidget(self.gameCommentView, **arg)

    def OpenRank(self):
        arg = {"refresh": True}
        self.owner.SwitchWidget(self.rankView, **arg)

    def OpenIndex(self):
        self.navigationWidget.indexButton.click()
        # arg = {"refresh": True}
        # self.owner.SwitchWidget(self.owner.indexView, **arg)

    def OpenLogin(self):
        arg = {"refresh": True, "page": 0}
        self.owner.SwitchWidget(self.loginNewView, **arg)

    def OpenDownloadAll(self, books):
        arg = {"books": books}
        self.owner.SwitchWidget(self.downloadAllView, **arg)

    def OpenLocalDelAll(self):
        arg = {}
        self.owner.SwitchWidget(self.localReadAllView, **arg)

    def OpenSubComment(self, commentId, widget):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": commentId}
        self.subCommentView.SetWidget(widget)
        self.owner.SwitchWidget(self.subCommentView, **arg)

    def OpenSearch(self, text, isLocal, isTitle, isDes, isCategory, isTag, isAuthor, isUpLoad, isFinish=False):
        arg = {"text": text, "isLocal": isLocal, "isTitle": isTitle, "isDes": isDes, "isCategory": isCategory,
               "isTag": isTag, "isAuthor": isAuthor, "isUpLoad": isUpLoad, "isFinish": isFinish}
        self.owner.SwitchWidget(self.searchView, **arg)

    def OpenSearch2(self, text, isLocal, isTitle, isDes, isCategory, isTag, isAuthor, isUpLoad):
        arg = {"text": text, "isLocal": isLocal, "isTitle": isTitle, "isDes": isDes, "isCategory": isCategory,
               "isTag": isTag, "isAuthor": isAuthor, "isUpLoad": isUpLoad}

        if isAuthor:
            title = "作者: {}".format(ToolUtil.GetStrMaxLen(text))
            self.searchView2.setWindowTitle(title)
            self.searchView2.searchTab.setText("作者: {}".format(text))
        elif isTag:
            title = "TAG: {}".format(ToolUtil.GetStrMaxLen(text))
            self.searchView2.setWindowTitle(title)
            self.searchView2.searchTab.setText("TAG: {}".format(text))
        self.owner.SwitchWidget(self.searchView2, **arg)

    def OpenRecomment(self, bookId):
        Title = "看了这边本子的人也在看"
        arg = {"recoment": 1, "bookId": bookId}
        self.searchView2.setWindowTitle(Title)
        self.searchView2.searchTab.setText(Title)
        self.owner.SwitchWidget(self.searchView2, **arg)

    def OpenRecomment2(self, bookId):
        Title = "猜你喜欢"
        arg = {"recoment": 2, "bookId": bookId}
        self.searchView2.setWindowTitle(Title)
        self.searchView2.searchTab.setText(Title)
        self.owner.SwitchWidget(self.searchView2, **arg)

    def OpenLocalEpsView(self, bookId):
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.localReadEpsView, **arg)

    def OpenSearchByText(self, text):
        self.searchView.lineEdit.setText(text)
        self.searchView.lineEdit.Search()

    def OpenReadView(self, bookId, index, pageIndex, isOffline=False):
        self.owner.BackOldSize()
        self.owner.totalStackWidget.setCurrentIndex(1)
        self.readView.OpenPage(bookId, index, pageIndex=pageIndex, isOffline=isOffline)

    def OpenLocalReadView(self, v, epsId=0):
        self.owner.BackOldSize()
        self.owner.totalStackWidget.setCurrentIndex(1)
        self.readView.OpenLocalPage(v, epsId)

    def CloseReadView(self):
        self.owner.totalStackWidget.setCurrentIndex(0)
        self.SetSubTitle("")
        self.bookInfoView.ReloadHistory.emit()

    def OpenSearchByCategory(self, categories):
        arg = {"categories": categories}
        self.owner.SwitchWidget(self.searchView, **arg)

    def OpenSearchByCategory2(self, categories):
        arg = {"categories": categories}
        title = "分类: {}".format(ToolUtil.GetStrMaxLen(categories))
        self.searchView2.setWindowTitle(title)
        self.searchView2.searchTab.setText("分类: {}".format(categories))
        self.owner.SwitchWidget(self.searchView2, **arg)

    def OpenSearchByCreate(self, text):
        arg = {"text": text, "isTitle": False, "isDes": False, "isCategory": False, "isTag": False, "isAuthor": False,
               "isUpLoad": True}
        title = "上传者: {}".format(ToolUtil.GetStrMaxLen(text))
        self.searchView2.setWindowTitle(title)
        self.searchView2.searchTab.setText("上传者: {}".format(text))
        self.owner.SwitchWidget(self.searchView2, **arg)

    def OpenBookInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.bookInfoView, **arg)

    def OpenBookInfoByShareId(self, shareId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"shareId": shareId}
        self.owner.SwitchWidget(self.bookInfoView, **arg)

    def OpenBookInfo2(self, bookId):
        Title = "漫画详情2"
        self.bookInfoView2.setWindowTitle(Title)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.bookInfoView2, **arg)

    def OpenSomeDownload(self, bookList=None):
        arg = {"books": bookList}
        self.owner.SwitchWidget(self.downloadAllView, **arg)

    def OpenLocalBook(self, bookId):
        self.owner.localReadView.OpenLocalBook(bookId)

    def OpenLocalEpsBook(self, bookId):
        self.owner.localReadEpsView.OpenLocalBook(bookId)

    def OpenEpsInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.bookEpsView, **arg)

    def OpenGameInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.gameInfoView, **arg)

    def OpenWaifu2xTool(self, data):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"data": data}
        self.owner.SwitchWidget(self.waifu2xToolView, **arg)

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

    def SetLocalServer(self, server):
        self._localServer = weakref.ref(server)

    def SetDirty(self):
        pass

    @staticmethod
    def SetFont():
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

            if Setting.FontSize.value and Setting.FontSize.value != "Default":
                if isinstance(Setting.FontSize.value, int):
                    f.setPointSize(int(Setting.FontSize.value))
                elif isinstance(Setting.FontSize.value, str) and Setting.FontSize.value.isdigit():
                    f.setPointSize(int(Setting.FontSize.value))

            if Setting.FontStyle.value:
                fontStyleList = [QFont.Light, QFont.Normal, QFont.DemiBold, QFont.Bold, QFont.Black]
                f.setWeight(fontStyleList[Setting.FontStyle.value - 1])

            QtOwner().app.setFont(f)

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