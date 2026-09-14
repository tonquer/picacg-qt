import base64
import time

from PySide6 import QtWidgets
from PySide6.QtCore import QTimer

from component.dialog.base_mask_dialog import BaseMaskDialog
from component.label.gif_label import GifLabel
from config.global_config import GlobalConfig
from config.setting import Setting
from interface.ui_login_new import Ui_LoginNew
from qt_owner import QtOwner
from server import req
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.str import Str
from view.user.login_new_widget import LoginNewWidget
from view.user.login_proxy_new_widget import LoginProxyNewWidget
from view.user.register_new_widget import RegisterNewWidget
from view.user.change_password_new_widget import UserChangePasswordWidget


class LoginNewView(QtWidgets.QWidget, Ui_LoginNew, QtTaskBase):

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginNew.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.CheckInit)
        self.loginWidget = LoginNewWidget(self)
        self.proxyWidget = LoginProxyNewWidget(self)
        self.registerWidget = RegisterNewWidget(self)
        self.userManagerWidget = UserChangePasswordWidget(self)
        self.isInit = False
        self.echConfigIndex = 0
        self.dohDomainList = []
        # 每5分钟更新echconfig
        self.timer = QTimer(self)
        self.timer.setInterval(1000*(15*60))
        self.timer.timeout.connect(self.HourTimeOut)

    def retranslateUi(self, Nas):
        themId = Setting.ThemeIndex.autoValue
        if themId != 1:
            qss = """
                .QFrame
                {
                    background-color: rgb(253, 253, 253);

                    border:2px solid rgb(234,234,234);
                    border-radius:5px
                }        
                """
        else:
            qss = """
                .QFrame
                {
                    background-color: rgb(50, 50, 50);

                    border:2px solid rgb(35,35,35);
                    border-radius:5px
                }        
                """
        self.tab_4.setStyleSheet(qss)
        Ui_LoginNew.retranslateUi(self, self)

    def SwitchCurrent(self, **kwargs):
        if not self.isInit:
            self.isInit = True
            self.Init()
        refresh = kwargs.get("refresh")
        index = kwargs.get("page")
        if not refresh:
            return
        if index != None:
            self.tabWidget.setCurrentIndex(index)
        self.CheckInit()
        pass

    def CheckInit(self):
        if self.tabWidget.currentIndex() == 3:
            self.proxyWidget.Init()
        elif self.tabWidget.currentIndex() == 1:
            self.registerWidget.Init()
        elif self.tabWidget.currentIndex() == 0:
            self.loginWidget.Init()

    def Init(self):
        self.timer.start()
        self.InitEchConfig()

    def HourTimeOut(self):
        self.InitEchConfig()

    def InitEchConfig(self):
        # self.echConfigIndex = 0
        self.dohDomainList = GlobalConfig.DohUrlList.value[:]
        if Setting.DohAddress.value and Setting.DohAddress.value in self.dohDomainList:
            self.dohDomainList.remove(Setting.DohAddress.value)
        if Setting.DohAddress.value:
            self.dohDomainList.insert(0, Setting.DohAddress.value)
        if not self.dohDomainList:
            return
        request = req.GetEchConfigReq(GlobalConfig.EchDomain.value, self.dohDomainList)
        self.AddHttpTask(request, self.InitEchConfigBack)

    def InitEchConfigBack(self, raw):
        try:
            st = raw.get("st")
            data = raw.get('data')
            if st != Str.Ok or not data:
                self.echTick.setText("error")
                self.echTick.setStyleSheet("background-color:transparent;color:{}".format("#d71345"))
                Log.Warn("not fetch ech config")
                self.timer.stop()
                self.timer.setInterval(1000*(1*60))
                self.timer.start()
            else:
                QtOwner().echConfig = data
                day = time.strftime(Str.GetStr(Str.UpdateTime)+'：%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
                self.echTick.setText(day),
                self.echTick.setStyleSheet("background-color:transparent;color:{}".format("#ff4081"))
                Log.Info(f"update ech config, {data}")
                self.timer.stop()
                self.timer.setInterval(1000 * (15 * 60))
                self.timer.start()
        except Exception as es:
            Log.Error(es)

    def Stop(self):
        self.timer.stop()
