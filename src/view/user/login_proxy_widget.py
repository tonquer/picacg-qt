from PySide6 import QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from config import config
from interface.ui_login_proxy_widget import Ui_LoginProxyWidget
from qt_owner import QtOwner
from server import req, Log
from server.server import Server
from task.qt_task import QtTaskBase
from tools.str import Str


class LoginProxyWidget(QtWidgets.QWidget, Ui_LoginProxyWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginProxyWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.speedTest = []
        self.speedIndex = 0
        self.speedPingNum = 0
        self.buttonGroup.setId(self.radioButton_1, 1)
        self.buttonGroup.setId(self.radioButton_2, 2)
        self.buttonGroup.setId(self.radioButton_3, 3)
        self.buttonGroup.setId(self.radioButton_4, 4)
        self.LoadSetting()
        self.UpdateServer()
        self.commandLinkButton.clicked.connect(self.OpenUrl)

    def Init(self):
        self.LoadSetting()

    def ClickButton(self):
        self.SaveSetting()

    def SetEnabled(self, enabled):
        self.testSpeedButton.setEnabled(enabled)
        self.proxyBox.setEnabled(enabled)
        self.httpLine.setEnabled(enabled)
        self.cdnIp.setEnabled(enabled)
        self.radioButton_1.setEnabled(enabled)
        self.radioButton_2.setEnabled(enabled)
        self.radioButton_3.setEnabled(enabled)
        self.radioButton_4.setEnabled(enabled)
        self.cdnIp.setEnabled(enabled)
        self.httpsBox.setEnabled(enabled)

    def SpeedTest(self):
        self.speedIndex = 0
        self.speedPingNum = 0
        self.speedTest = []

        for i in range(1, 9):
            label = getattr(self, "label" + str(i))
            label.setText("")

        self.speedTest = [("", "", False, 1), ("", "", True, 2)]
        i = 3
        for address in config.Address:
            self.speedTest.append((address, config.ImageServer, False, i))
            i += 1
            self.speedTest.append((address, config.ImageServer, True, i))
            i += 1

        PreferCDNIP = self.cdnIp.text()
        if PreferCDNIP:
            self.speedTest.append((PreferCDNIP, PreferCDNIP, False, i))
            i += 1
            self.speedTest.append((PreferCDNIP, PreferCDNIP, True, i))
            i += 1

        self.SetEnabled(False)
        config.IsUseHttps = int(self.httpsBox.isChecked())
        self.StartSpeedPing()

    def StartSpeedPing(self):
        if len(self.speedTest) <= self.speedPingNum:
            self.StartSpeedTest()
            return
        address, imageProxy, isHttpProxy, i = self.speedTest[self.speedPingNum]
        httpProxy = self.httpLine.text()
        if isHttpProxy and not httpProxy:
            label = getattr(self, "label"+str(i))
            label.setText(Str.GetStr(Str.NoProxy))
            self.speedPingNum += 1
            self.StartSpeedPing()
            return

        request = req.SpeedTestPingReq()
        if isHttpProxy:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        else:
            request.proxy = ""
        Server().UpdateDns(address, imageProxy)
        self.AddHttpTask(lambda x: Server().TestSpeedPing(request, x), self.SpeedTestPingBack, i)
        return

    def SpeedTestPingBack(self, raw, i):
        data = raw["data"]
        label = getattr(self, "label" + str(i))
        if float(data) > 0.0:
            label.setText("<font color=#7fb80e>{}</font>".format(str(int(float(data)*500)) + "ms") + "/")
        else:
            label.setText("<font color=#d71345>{}</font>".format("fail") + "/")
        self.speedPingNum += 1
        self.StartSpeedPing()
        return

    def StartSpeedTest(self):
        if len(self.speedTest) <= self.speedIndex:
            self.UpdateServer()
            self.SetEnabled(True)
            return

        address, imageProxy, isHttpProxy, i = self.speedTest[self.speedIndex]
        httpProxy = self.httpLine.text()
        if isHttpProxy and not httpProxy:
            label = getattr(self, "label" + str(i))
            label.setText(Str.GetStr(Str.NoProxy))
            self.speedIndex += 1
            self.StartSpeedTest()
            return

        request = req.SpeedTestReq()
        if isHttpProxy:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        else:
            request.proxy = ""
        Server().UpdateDns(address, imageProxy)
        self.AddHttpTask(lambda x: Server().TestSpeed(request, x), self.SpeedTestBack, i)
        return

    def SpeedTestBack(self, raw, i):
        data = raw["data"]
        if not data:
            data = "<font color=#d71345>fail</font>"
        else:
            data = "<font color=#7fb80e>{}</font>".format(data)
        label = getattr(self, "label" + str(i))
        label.setText(label.text()+data)
        self.speedIndex += 1
        self.StartSpeedTest()
        return

    def LoadSetting(self):
        config.PreferCDNIP = QtOwner().settingView.GetSettingV("Proxy/PreferCDNIP", config.PreferCDNIP)
        config.ProxySelectIndex = QtOwner().settingView.GetSettingV("Proxy/ProxySelectIndex", config.ProxySelectIndex)
        config.IsUseHttps = QtOwner().settingView.GetSettingV("Proxy/IsUseHttps", config.IsUseHttps)
        httpProxy = QtOwner().settingView.GetSettingV("Proxy/Http", config.HttpProxy)

        self.httpsBox.setChecked(config.IsUseHttps)
        self.proxyBox.setChecked(config.IsHttpProxy)
        self.httpLine.setText(httpProxy)
        button = getattr(self, "radioButton_{}".format(config.ProxySelectIndex))
        button.setChecked(True)
        self.cdnIp.setText(config.PreferCDNIP)

    def UpdateServer(self):
        if config.ProxySelectIndex == 1:
            imageServer = ""
            address = ""
        elif config.ProxySelectIndex == 2:
            imageServer = config.ImageServer
            address = config.Address[0]
        elif config.ProxySelectIndex == 3:
            imageServer = config.ImageServer
            address = config.Address[1]
        else:
            imageServer = config.PreferCDNIP
            address = config.PreferCDNIP
        Server().UpdateDns(address, imageServer)
        Log.Info("update proxy, setId:{}, image server:{}, address:{}".format(config.ProxySelectIndex, Server().imageServer, Server().address))

    def SaveSetting(self):
        config.PreferCDNIP = self.cdnIp.text()
        config.IsHttpProxy = int(self.proxyBox.isChecked())
        httpProxy = self.httpLine.text()
        config.ProxySelectIndex = self.buttonGroup.checkedId()
        config.IsUseHttps = int(self.httpsBox.isChecked())

        QtOwner().settingView.SetSettingV("Proxy/ProxySelectIndex", config.ProxySelectIndex)
        QtOwner().settingView.SetSettingV("Proxy/PreferCDNIP", config.PreferCDNIP)
        QtOwner().settingView.SetSettingV("Proxy/Http", httpProxy)
        QtOwner().settingView.SetSettingV("Proxy/IsHttp", config.IsHttpProxy)
        QtOwner().settingView.SetSettingV("Proxy/IsUseHttps", config.IsUseHttps)
        self.UpdateServer()
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        return

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl(config.ProxyUrl))
