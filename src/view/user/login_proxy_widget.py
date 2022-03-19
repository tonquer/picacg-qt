from PySide6 import QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from config import config
from config.setting import Setting
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

        self.buttonGroup_2.setId(self.proxy_0, 0)
        self.buttonGroup_2.setId(self.proxy_1, 1)
        self.buttonGroup_2.setId(self.proxy_2, 2)

    def Init(self):
        self.LoadSetting()

    def ClickButton(self):
        self.SaveSetting()

    def SetEnabled(self, enabled):
        self.testSpeedButton.setEnabled(enabled)
        self.proxy_0.setEnabled(enabled)
        self.proxy_1.setEnabled(enabled)
        self.proxy_2.setEnabled(enabled)
        self.httpLine.setEnabled(enabled)
        self.sockEdit.setEnabled(enabled)
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
        self.speedTest.append((config.Address[0], config.ImageServer2, False, i))
        i += 1
        self.speedTest.append((config.Address[0], config.ImageServer2, True, i))
        i += 1
        self.speedTest.append((config.Address[1], config.ImageServer3, False, i))
        i += 1
        self.speedTest.append((config.Address[1], config.ImageServer3, True, i))
        i += 1

        PreferCDNIP = self.cdnIp.text()
        if PreferCDNIP:
            self.speedTest.append((PreferCDNIP, PreferCDNIP, False, i))
            i += 1
            self.speedTest.append((PreferCDNIP, PreferCDNIP, True, i))
            i += 1

        self.SetEnabled(False)
        self.StartSpeedPing()

    def StartSpeedPing(self):
        if len(self.speedTest) <= self.speedPingNum:
            self.StartSpeedTest()
            return
        address, imageProxy, isHttpProxy, i = self.speedTest[self.speedPingNum]
        httpProxy = self.httpLine.text()
        if isHttpProxy and (self.buttonGroup_2.checkedId() == 0 or
                            (self.buttonGroup_2.checkedId() == 1 and not self.httpLine.text()) or
                            (self.buttonGroup_2.checkedId() == 2 and not self.sockEdit.text())):
            label = getattr(self, "label"+str(i))
            label.setText(Str.GetStr(Str.NoProxy))
            self.speedPingNum += 1
            self.StartSpeedPing()
            return

        request = req.SpeedTestPingReq()
        request.isUseHttps = self.httpsBox.isChecked()
        if isHttpProxy and self.buttonGroup_2.checkedId() == 1:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        else:
            request.proxy = ""

        if isHttpProxy and self.buttonGroup_2.checkedId() == 2:
            self.SetSock5Proxy(True)
        else:
            self.SetSock5Proxy(False)

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
        if isHttpProxy and (self.buttonGroup_2.checkedId() == 0 or
                            (self.buttonGroup_2.checkedId() == 1 and not self.httpLine.text()) or
                            (self.buttonGroup_2.checkedId() == 2 and not self.sockEdit.text())):
            label = getattr(self, "label" + str(i))
            label.setText(Str.GetStr(Str.NoProxy))
            self.speedIndex += 1
            self.StartSpeedTest()
            return

        request = req.SpeedTestReq()
        request.isUseHttps = self.httpsBox.isChecked()
        if isHttpProxy and self.buttonGroup_2.checkedId() == 1:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        else:
            request.proxy = ""

        if isHttpProxy and self.buttonGroup_2.checkedId() == 2:
            self.SetSock5Proxy(True)
        else:
            self.SetSock5Proxy(False)

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
        # config.PreferCDNIP = QtOwner().settingView.GetSettingV("Proxy/PreferCDNIP", config.PreferCDNIP)
        # config.ProxySelectIndex = QtOwner().settingView.GetSettingV("Proxy/ProxySelectIndex", config.ProxySelectIndex)
        # config.IsUseHttps = QtOwner().settingView.GetSettingV("Proxy/IsUseHttps", config.IsUseHttps)
        # httpProxy = QtOwner().settingView.GetSettingV("Proxy/Http", config.HttpProxy)

        self.httpsBox.setChecked(Setting.IsUseHttps.value)
        self.httpLine.setText(Setting.HttpProxy.value)
        self.sockEdit.setText(Setting.Sock5Proxy.value)
        button = getattr(self, "radioButton_{}".format(Setting.ProxySelectIndex.value))
        button.setChecked(True)
        button = getattr(self, "proxy_{}".format(int(Setting.IsHttpProxy.value)))
        button.setChecked(True)
        self.cdnIp.setText(Setting.PreferCDNIP.value)

    def UpdateServer(self):
        if Setting.ProxySelectIndex.value == 1:
            imageServer = ""
            address = ""
        elif Setting.ProxySelectIndex.value == 2:
            imageServer = config.ImageServer2
            address = config.Address[0]
        elif Setting.ProxySelectIndex.value == 3:
            imageServer = config.ImageServer3
            address = config.Address[1]
        else:
            imageServer = Setting.PreferCDNIP.value
            address = Setting.PreferCDNIP.value
        QtOwner().settingView.SetSock5Proxy()
        Server().UpdateDns(address, imageServer)
        Log.Info("update proxy, setId:{}, image server:{}, address:{}".format(Setting.ProxySelectIndex.value, Server().imageServer, Server().address))

    def SaveSetting(self):
        Setting.PreferCDNIP.SetValue(self.cdnIp.text())
        Setting.IsHttpProxy.SetValue(int(self.buttonGroup_2.checkedId()))
        Setting.Sock5Proxy.SetValue(self.sockEdit.text())
        Setting.HttpProxy.SetValue(self.httpLine.text())
        Setting.ProxySelectIndex.SetValue(self.buttonGroup.checkedId())
        Setting.IsUseHttps.SetValue(int(self.httpsBox.isChecked()))

        # QtOwner().settingView.SetSettingV("Proxy/ProxySelectIndex", config.ProxySelectIndex)
        # QtOwner().settingView.SetSettingV("Proxy/PreferCDNIP", config.PreferCDNIP)
        # QtOwner().settingView.SetSettingV("Proxy/Http", httpProxy)
        # QtOwner().settingView.SetSettingV("Proxy/IsHttp", config.IsHttpProxy)
        # QtOwner().settingView.SetSettingV("Proxy/IsUseHttps", config.IsUseHttps)

        self.UpdateServer()
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        return

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl(config.ProxyUrl))

    def SetSock5Proxy(self, isProxy):
        import socket
        import socks
        if not QtOwner().backSock:
            QtOwner().backSock = socket.socket
        if isProxy:
            data = self.sockEdit.text().replace("http://", "").replace("https://", "").replace("sock5://", "")
            data = data.split(":")
            if len(data) == 2:
                host = data[0]
                port = data[1]
                socks.set_default_proxy(socks.SOCKS5, host, int(port))
                socket.socket = socks.socksocket
        else:
            socks.set_default_proxy()
            socket.socket = QtOwner().backSock