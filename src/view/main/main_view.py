import sys
from functools import partial

from PySide6.QtCore import Qt, QEvent, QPoint, Signal, QTimer, QSize
from PySide6.QtGui import QIcon, QMouseEvent, QGuiApplication, QFont
from PySide6.QtWidgets import QButtonGroup, QToolButton, QLabel

from component.dialog.loading_dialog import LoadingDialog
from component.dialog.show_close_dialog import ShowCloseDialog
from component.label.msg_label import MsgLabel
from component.system_tray_icon.my_system_tray_icon import MySystemTrayIcon
from component.widget.main_widget import Main
from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from qt_owner import QtOwner
from server import req
from server.server import Server
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from task.task_qimage import TaskQImage
from task.task_waifu2x import TaskWaifu2x
from tools.log import Log
from view.download.download_dir_view import DownloadDirView


class MainView(Main, QtTaskBase):
    """ 主窗口 """
    WindowsSizeChange = Signal()

    def __init__(self):
        QtOwner().SetOwner(self)
        Main.__init__(self)
        QtTaskBase.__init__(self)
        # self.setAttribute(Qt.WA_PaintOnScreen, False)  # 禁用屏幕缓存
        # self.setAttribute(Qt.WA_NoSystemBackground, True)  # 去除系统背景
        # self.setAttribute(Qt.WA_OpaquePaintEvent, True)  # 设置为不透明的paint event
        self.resize(600, 600)
        self.setWindowTitle(config.ProjectName)
        self.setWindowIcon(QIcon(":/png/icon/logo_round.png"))
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_QuitOnClose, True)
        # self.setAttribute(Qt.WA_NoSystemBackground,True)
        # self.setAutoFillBackground(False)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.AfterStartSuc)
        screens = QGuiApplication.screens()
        # print(screens[0].geometry(), screens[1].geometry())
        if Setting.ScreenIndex.value >= len(screens):
            desktop = QGuiApplication.primaryScreen().geometry()
        else:
            desktop = screens[Setting.ScreenIndex.value].geometry()

        self.adjustSize()
        # self.downloadView.setFixedWidth(150)
        # self.bookInfoView.setFixedWidth(150)
        self.myInitSize = QSize(desktop.width() // 4 * 3, desktop.height() // 4 * 3)
        self.resize(desktop.width() // 4 * 3, desktop.height() // 4 * 3)
        self.move(self.width() // 8+desktop.x(), max(0, desktop.height()-self.height()) // 2+desktop.y())
        print(desktop.size(), self.size())
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.loadingDialog = LoadingDialog(self)
        self.navigationWidget.helpButton.click()
        self.subStackWidget.setCurrentIndex(self.subStackWidget.indexOf(self.helpView))

        self.__initWidget()

        # 窗口切换相关
        self.toolButtons = []
        self.toolLabels = []
        self.toolButtonGroup = QButtonGroup()
        self.toolButtonGroup.idClicked.connect(self.SwitchWidgetByIndex)
        self.menuButton.clicked.connect(self.CheckShowMenu)
        self.UpdateTabBar()

        # self.subStackWidget.setCurrentIndex(0)
        self.settingView.LoadSetting()
        GlobalConfig.LoadSetting()

        self.searchView.searchTab.hide()
        self.searchView2.searchWidget.hide()
        self.myTrayIcon = MySystemTrayIcon()
        self.myTrayIcon.show()
        self.totalStackWidget.currentChanged.connect(self.SwitchReadView)
        # self.myTrayIcon.hide()
        # self.readView.LoadSetting()
        # QApplication.instance().installEventFilter(self)
        # QtOwner().app.paletteChanged.connect(self.CheckPaletteChanged)

    @property
    def isMaxSize(self):
        return QtOwner().isMaxSize

    @isMaxSize.setter
    def isMaxSize(self, v):
        QtOwner().isMaxSize = v

    def BackOldSize(self):
        self.isMaxSize = self.isMaximized()
        return

    def SwitchReadView(self, i):
        ## 备份原来的大小
        if i == 0:
            # windows
            if not sys.platform == "darwin":
                if self.isMaxSize and self.windowState != Qt.WindowState.WindowMaximized:
                    self.showMaximized()
            # Macos只有全屏和非全屏
        return

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.WindowsSizeChange.emit()
            print(event.type(), event.oldState(), self.windowState())
        return super(self.__class__, self).changeEvent(event)

    # def eventFilter(self, watched, event) -> bool:
    #     if watched == QtOwner().app:
    #         print(event.type(), event)
    #     return False

    # def event(self, ev):
    #     """Catch system events."""
    #     # print(ev)
    #     if ev.type() == QEvent.ApplicationPaletteChange:  # detect theme switches
    #         pass
    #         # style = interface_style()  # light or dark
    #         # if style is not None:
    #         #     QIcon.setThemeName(style)
    #         # else:
    #         #     QIcon.setThemeName("light")  # fallback
    #     return super().event(ev)
    #
    # def CheckPaletteChanged(self, data):
    #     print(data)

    @property
    def subStackList(self):
        return self.subStackWidget.subStackList

    @subStackList.setter
    def subStackList(self, value):
        self.subStackWidget.subStackList = value

    def __initWidget(self):
        self.navigationWidget.indexButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.indexView)))
        self.navigationWidget.settingButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.settingView)))
        self.navigationWidget.downloadButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.downloadView)))
        self.navigationWidget.categoryButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.categoryView)))
        self.navigationWidget.searchButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.searchView)))
        self.navigationWidget.rankButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.rankView)))
        self.navigationWidget.msgButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.commentView)))
        self.navigationWidget.chatButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.chatView)))
        self.navigationWidget.collectButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.favorityView)))
        self.navigationWidget.lookButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.historyView)))
        self.navigationWidget.myCommentButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.myCommentView)))
        self.navigationWidget.gameButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.gameView)))
        self.navigationWidget.helpButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.helpView)))
        self.navigationWidget.waifu2xButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.waifu2xToolView)))
        self.navigationWidget.localReadButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.localReadView)))
        self.navigationWidget.friedButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.friedView)))
        self.navigationWidget.chatNewButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.chatNewView)))
        self.navigationWidget.convertButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.convertView)))
        self.navigationWidget.friedButton.hide()
        self.navigationWidget.convertButton.hide()
        self.navigationWidget.chatNewButton.hide()
        self.navigationWidget.chatButton.hide()
        self.navigationWidget.nasButton.clicked.connect(partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.nasView)))
        self.navigationWidget.batchSrButton.clicked.connect(
            partial(self.SwitchWidgetAndClear, self.subStackWidget.indexOf(self.batchSrView)))


    def RetranslateUi(self):
        Main.retranslateUi(self, self)
        self.indexView.retranslateUi(self.indexView)
        self.settingView.retranslateUi(self.settingView)
        self.downloadView.retranslateUi(self.downloadView)
        self.categoryView.retranslateUi(self.categoryView)
        self.searchView.retranslateUi(self.searchView)
        self.rankView.retranslateUi(self.rankView)
        self.commentView.retranslateUi(self.commentView)
        self.chatView.retranslateUi(self.chatView)
        self.favorityView.retranslateUi(self.favorityView)
        self.readView.retranslateUi(self.readView)
        self.myCommentView.retranslateUi(self.myCommentView)
        self.gameCommentView.retranslateUi(self.gameCommentView)
        self.subCommentView.retranslateUi(self.subCommentView)
        self.gameView.retranslateUi(self.gameView)
        self.helpView.retranslateUi(self.helpView)
        self.waifu2xToolView.retranslateUi(self.waifu2xToolView)
        self.navigationWidget.retranslateUi(self.navigationWidget)

    def Init(self):
        print(self.size())
        IsCanUse = False
        self.downloadView.Init()
        self.nasView.Init()
        self.InitApiProxy()
        if config.CanWaifu2x:
            from sr_vulkan import sr_vulkan as sr
            stat = sr.init()
            sr.setDebug(True)
            if stat < 0:
                pass
                # QtOwner().ShowMsg(self.tr("未发现支持VULKAN的GPU, Waiuf2x当前为CPU模式, " + ", code:{}".format(str(stat))))
                # CPU 模式，暂时不开放看图下的转换
                # config.IsOpenWaifu = 0
                # self.settingForm.checkBox.setEnabled(False)
                # self.qtReadImg.frame.qtTool.checkBox.setEnabled(False)

            IsCanUse = True
            gpuInfo = sr.getGpuInfo()
            cpuNum = sr.getCpuCoreNum()
            gpuNum = sr.getGpuCoreNum()
            self.settingView.SetGpuInfos(gpuInfo, cpuNum)
            # if not gpuInfo or (gpuInfo and config.Encode < 0) or (gpuInfo and config.Encode >= len(gpuInfo)):
            #     config.Encode = 0

            sts = sr.initSet(config.Encode, config.UseCpuNum)
            TaskWaifu2x().Start()
            version = sr.getVersion()
            config.Waifu2xVersion = version
            self.helpView.waifu2x.setText(config.Waifu2xVersion)
            import sys, os
            Log.Warn("Waifu2x init:{}, encode:{}, version:{}, code:{}, cpuNum:{}/{}, gpuNum:{}, gpuList:{}".format(
                stat, config.Encode, version, sts, config.UseCpuNum, cpuNum, gpuNum, gpuInfo
            ))

        else:
            if not config.CloseWaifu2x:
                QtOwner().ShowError("Waifu2x Error, " + config.ErrorMsg)
            Log.Warn("Waifu2x Error: " + str(config.ErrorMsg))

        if not IsCanUse:
            self.settingView.readCheckBox.setEnabled(False)
            self.settingView.coverCheckBox.setEnabled(False)
            self.settingView.downAuto.setEnabled(False)
            self.readView.frame.qtTool.checkBox.setEnabled(False)
            Setting.DownloadAuto.SetValue(0)
            Setting.CoverIsOpenWaifu.SetValue(0)
            self.downloadView.radioButton.setEnabled(False)
            self.waifu2xToolView.checkBox.setEnabled(False)
            self.waifu2xToolView.changeButton.setEnabled(False)
            self.waifu2xToolView.changeButton.setEnabled(False)
            self.waifu2xToolView.modelName.setEnabled(False)
            self.waifu2xToolView.ttaModel.setEnabled(False)
            self.waifu2xToolView.changeButton.setEnabled(False)
            self.waifu2xToolView.SetStatus(False)
            Setting.IsOpenWaifu.SetValue(0)

        if Setting.IsUpdate.value:
            self.helpView.InitUpdate()
        self.helpView.InitUpdateConfig()
        self.searchView.InitWord()
        self.msgLabel = MsgLabel(self)
        self.msgLabel.hide()
        if not Setting.SavePath.value:
            view = DownloadDirView(self)
            view.show()
            view.closed.connect(self.OpenLoginView)
        else:
            self.OpenLoginView()
        # self.timer.start()

    # def AfterStartSuc(self):
    #     # self.timer.stop()
    #     self.resize(self.myInitSize.width(), self.myInitSize.height())

    def InitApiProxy(self):
        request = req.InitReq()
        request.proxy = {}
        # self.AddHttpTask(request)

    def ClearTabBar(self):
        for toolButton in self.toolButtons:
            self.menuLayout.removeWidget(toolButton)
            toolButton.setParent(None)
        for label in self.toolLabels:
            self.menuLayout.removeWidget(label)
            label.setParent(None)
        self.toolButtons = []
        self.toolLabels = []
        self.subStackList = []
        return

    def UpdateTabBar(self):
        for index, i in enumerate(self.subStackList):
            if index >= len(self.toolButtons):
                button = QToolButton()
                button.setCheckable(True)
                button.setText(self.subStackWidget.widget(i).windowTitle())

                if index == 0:
                    button.setChecked(True)
                else:
                    label = QLabel(">")
                    self.menuLayout.addWidget(label)
                    self.toolLabels.append(label)

                self.toolButtonGroup.addButton(button)
                self.toolButtonGroup.setId(button, i)
                self.menuLayout.addWidget(button)
                self.toolButtons.append(button)
        return

    def OpenLoginView(self):
        self.navigationWidget.OpenLoginView()

    def LoginSucBack(self):
        self.helpView.Init()
        self.favorityView.InitFavorite()
        self.SwitchWidget(self.indexView)

    def SwitchWidgetNext(self):
        index = self.subStackWidget.currentIndex()
        if index in self.subStackList:
            subIndex = self.subStackList.index(index)
            if subIndex >= len(self.subStackList) -1:
                return
            self.SwitchWidgetByIndex(self.subStackList[subIndex+1])

    def SwitchWidgetLast(self):
        index = self.subStackWidget.currentIndex()
        if index in self.subStackList:
            subIndex = self.subStackList.index(index)
            if subIndex <= 0:
                return
            self.SwitchWidgetByIndex(self.subStackList[subIndex-1])

    def SwitchWidget(self, widget, **kwargs):
        return self.SwitchWidgetByIndex(self.subStackWidget.indexOf(widget), **kwargs)

    def SwitchWidgetByIndex(self, index, **kwargs):
        if index == self.subStackWidget.currentIndex():
            self.subStackWidget.widget(index).SwitchCurrent(**kwargs)
            return
        if index not in self.subStackList:
            # 需要清除後面的界面
            currrentListIndex = self.subStackList.index(self.subStackWidget.currentIndex())
            subStackList = self.subStackList[:currrentListIndex+1]

            self.ClearTabBar()
            self.subStackList = subStackList
            self.subStackList.append(index)
            self.UpdateTabBar()
        self.subStackWidget.SwitchWidgetByIndex(index, **kwargs)
        # self.toolButtonGroup.id()
        for button in self.toolButtons:
            if self.toolButtonGroup.id(button) == index:
                button.setChecked(True)
                button.setText(self.subStackWidget.widget(index).windowTitle())
        return

    def SwitchWidgetAndClear(self, index):
        self.ClearTabBar()
        self.subStackList = [index]
        kwargs = {"refresh": True}
        self.subStackWidget.SwitchWidgetByIndex(index, **kwargs)
        self.UpdateTabBar()
        return

    # def resizeEvent(self, e):
    #     super().resizeEvent(e)
    #     self.adjustWidgetGeometry()

    def closeEvent(self, a0) -> None:
        if self.totalStackWidget.currentIndex() == 1:
            self.readView.Close()
            a0.ignore()
            return
        if not self.isHidden():
            if Setting.ShowCloseType.value == 1 and QtOwner().closeType == 1:
                QtOwner().app.setQuitOnLastWindowClosed(False)
                self.myTrayIcon.show()
                self.hide()
                a0.ignore()
                return
            # if not Setting.IsNotShowCloseTip.value and QtOwner().closeType == 1:
                # log = ShowCloseDialog(QtOwner().owner)
                # log.show()
                # log.LoadSetting()
                # a0.ignore()
                # return

            # if  Setting.ShowCloseType.value == 2:
            #     self.myTrayIcon.show()
            #     self.hide()
            #     a0.ignore()
            #     return
        QtOwner().app.setQuitOnLastWindowClosed(True)
        super().closeEvent(a0)
        # reply = QtOwner().ShowMsgBox(QMessageBox.Question, self.tr('提示'), self.tr('确定要退出吗？'))
        self.GetExitScreen()

        # 点击关闭按钮或者点击退出事件会出现图标无法消失的bug，需要手动将图标内存清除
        # self.myTrayIcon = None
        a0.accept()

    def GetExitScreen(self):
        screens = QGuiApplication.screens()
        # print(self.pos())
        # for screen in screens:
        #     print(screen.geometry())
        screen = QGuiApplication.screenAt(self.pos()+QPoint(self.width()//2, self.height()//2))
        if screen in screens:
            index = screens.index(screen)
            Setting.ScreenIndex.SetValue(index)
            Log.Info("Exit screen index:{}".format(str(index)))

    def CheckShowMenu(self):
        if self.navigationWidget.isHidden():
            self.navigationWidget.aniShow()
        else:
            self.navigationWidget.aniHide()
        return

    def keyReleaseEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.SwitchWidgetLast()
        return super(self.__class__, self).keyReleaseEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.ForwardButton:
            self.SwitchWidgetNext()
        elif event.button() == Qt.BackButton:
            self.SwitchWidgetLast()
        self.searchView.lineEdit.CheckClick(event.pos())
        return super(self.__class__, self).mousePressEvent(event)


    #
    # def changeEvent(self, ev):
    #     if sys.platform == 'darwin':
    #         OSX_LIGHT_MODE = 236
    #         OSX_DARK_MODE = 50
    #         if ev.type() == QEvent.PaletteChange:
    #             bg = self.palette().color(QPalette.Active, QPalette.Window)
    #             if bg.lightness() == OSX_LIGHT_MODE:
    #                 print("MacOS light theme")
    #                 return
    #             elif bg.lightness() == OSX_DARK_MODE:
    #                 print("MacOS dark theme")
    #                 return
    #     return super(self.__class__, self).changeEvent(ev)

    def nativeEvent(self, eventType, message):
        # print(eventType, message)
        if eventType == "windows_generic_MSG":
            try:
                from ctypes.wintypes import POINT
                import ctypes.wintypes
            except Exception as es:
                return super(self.__class__, self).nativeEvent(eventType, message)

            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            # print(msg.message, self.GetWinSysColor())
            if msg.message == 26 and Setting.ThemeIndex.value == 0:
                self.settingView.SetTheme()

        return super(self.__class__, self).nativeEvent(eventType, message)

    def Close(self):
        # TODO 停止所有的定时器以及线程
        self.loadingDialog.close()
        self.downloadView.Close()
        self.chatView.Stop()
        self.nasView.Close()
        self.readView.Stop()
        self.batchSrView.Stop()
        TaskWaifu2x().Stop()
        TaskQImage().Stop()
        Server().Stop()
        SqlServer().Stop()
        # QtTask().Stop()

    def OnNewConnection(self):
        socket = QtOwner().localServer.nextPendingConnection()
        socket.readyRead.connect(self.OnReadConnection)
        return

    def OnReadConnection(self):
        conn = self.sender()
        if not conn:
            return
        data = conn.readAll()
        if data == b"restart":
            self.show()
            self.showNormal()