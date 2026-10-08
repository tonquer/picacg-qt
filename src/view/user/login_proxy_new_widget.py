import json
import re
import urllib
from functools import partial

from PySide6 import QtCore
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QAbstractItemView, QCheckBox, QButtonGroup, QLabel

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from qt_owner import QtOwner
from server import req, Server
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil


class IpItem(object):
    def __init__(self, index, j, ip, isProxy=False, isSelf=False):
        self.index = index
        self.tableRow = index
        self.j = j
        if isProxy:
            self.name = f"ProxyIP分流{j}"
        elif isSelf:
            self.name = f"自定义分流{j}"
        else:
            self.name = f"CDN分流{j}"
        self.ip = ip
        self.isProxy = False
        self.tags = []
        self.country = ""
        self.asn = ""
        self.delay = 0
        self.download = 0
        self.downloadDelay = 0
        self.isFail = False
        self.downloadFail = False
        self.st = ""
        self.downloadSt = ""
        self.isSelect = False

    def Copy(self, other):
        assert isinstance(other, IpItem)
        self.country = other.country
        self.asn = other.asn

    def __lt__(self, other):
        assert isinstance(other, IpItem)
        if self.isSelect == other.isSelect:
            leIsFail = self.isFail or self.downloadFail
            rtIsFail = other.isFail or other.downloadFail
            if leIsFail == rtIsFail:
                return self.delay*0.8 + self.downloadDelay*0.2 < other.delay*0.8 + other.downloadDelay*0.2
            else:
                if leIsFail:
                    return False
                else:
                    return True
        else:
            if self.isSelect:
                return True
            else:
                return False

class LoginProxyNewWidget(object):
    def __init__(self, owner):
        from view.user.login_new_view import LoginNewView
        assert isinstance(owner, LoginNewView)
        self.owner = owner


        self.speedTest = []
        self.speedPingNum = 0
        self.speedDownNum = 0

        self.pingBackNumCnt = {}
        self.pingBackNumDict = {}
        self.needBackNum = 0

        self.owner.radioApiGroup.setId(self.owner.radioButton_1, 1)
        self.owner.radioApiGroup.setId(self.owner.radioButton_2, 2)
        self.owner.radioApiGroup.setId(self.owner.radioButton_3, 3)
        self.owner.radioApiGroup.setId(self.owner.radioButton_4, 4)
        self.owner.radioApiGroup.setId(self.owner.radioButton_5, 5)
        self.owner.radioApiGroup.setId(self.owner.radioButton_6, 6)
        # self.owner.radioApiGroup.setId(self.owner.radioButton_7, 7)

        self.owner.radioImgGroup.setId(self.owner.radio_img_1, 1)
        self.owner.radioImgGroup.setId(self.owner.radio_img_2, 2)
        self.owner.radioImgGroup.setId(self.owner.radio_img_3, 3)
        self.owner.radioImgGroup.setId(self.owner.radio_img_4, 4)
        self.owner.radioImgGroup.setId(self.owner.radio_img_5, 5)
        self.owner.radioImgGroup.setId(self.owner.radio_img_6, 6)
        # self.owner.radioImgGroup.setId(self.owner.radio_img_7, 7)
        # self.buttonGroup.setId(self.radioButton_5, 5)

        self.owner.radioProxyGroup.setId(self.owner.proxy_0, 0)
        self.owner.radioProxyGroup.setId(self.owner.proxy_1, 1)
        self.owner.radioProxyGroup.setId(self.owner.proxy_2, 2)
        self.owner.radioProxyGroup.setId(self.owner.proxy_3, 3)

        self.LoadSetting()

        # self.UpdateServer()
        self.owner.cdnLinkButton.clicked.connect(self.OpenUrl)
        self.maxNum = 7
        # self.loginProxy.hide()
        # self.uaRandom.clicked.connect(self.RandomUa)
        self.lastResult = {}
        # self.owner.host_img_domain.SetWordData(GlobalConfig.ImgAutoUrl.value[:])
        self.owner.dohLine.SetWordData(GlobalConfig.DohUrlList.value[:])
        self.allApiUrl = []
        self.checkDohUrl = ""
        self.checkResult = None
        self.owner.dohLine.editingFinished.connect(self.CheckDohReq)

        # self.flowLayout = FlowLayout(self.owner.ipWidget)
        self.owner.testSpeedButton.clicked.connect(self.SpeedTest)
        self.owner.testIpButton.clicked.connect(self.StartTestIp)
        self.allItems = {}
        self.maxSpeedIpCnt = 0
        self.maxSpeedImgCnt = 0
        self.isInitProxy = False
        self.owner.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.owner.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.owner.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.owner.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.owner.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.owner.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.owner.tableWidget.resizeColumnsToContents()
        self.owner.tableWidget.resizeRowsToContents()

        self.proxyIpGroup = QButtonGroup(self.owner)
        self.proxyIpGroup.setExclusive(True)
        self.otherProxyIps = Setting.ProxyIpLastList.value.split(",")
        if not self.otherProxyIps:
            self.otherProxyIps = GlobalConfig.ProxyIpList.value[:]

        self.otherCDNIps = Setting.BestCfIpLastList.value.split(",")
        if not self.otherCDNIps:
            self.otherCDNIps = GlobalConfig.BestCfIpList.value[:]

        self.ShowAllItem()
        self.LoadHistory()
        self.Sort()
        self.cdnIndex = 4
        self.owner.proxyIpEdit.SetWordData(["JP", "US", "HK", "SG", "KR", "GB", "FR", "NL"])
        pass

    def SetEnabled(self, enabled):
        self.owner.testSpeedButton.setEnabled(enabled)
        # self.dohBox.setEnabled(enabled)
        # self.dohEdit.setEnabled(enabled)
        self.owner.proxy_0.setEnabled(enabled)
        self.owner.proxy_1.setEnabled(enabled)
        self.owner.proxy_2.setEnabled(enabled)
        self.owner.proxy_3.setEnabled(enabled)
        self.owner.httpLine.setEnabled(enabled)
        self.owner.sockEdit.setEnabled(enabled)
        # self.owner.cdn_img_ip.setEnabled(enabled)
        # self.owner.cdn_api_ip.setEnabled(enabled)
        # self.owner.host_api_domain.setEnabled(enabled)
        # self.owner.host_img_domain.setEnabled(enabled)
        self.owner.radioButton_1.setEnabled(enabled)
        self.owner.radioButton_2.setEnabled(enabled)
        self.owner.radioButton_3.setEnabled(enabled)
        self.owner.radioButton_4.setEnabled(enabled)
        self.owner.radioButton_5.setEnabled(enabled)
        self.owner.radioButton_6.setEnabled(enabled)
        # self.owner.radioButton_7.setEnabled(enabled)
        self.owner.radio_img_1.setEnabled(enabled)
        self.owner.radio_img_2.setEnabled(enabled)
        self.owner.radio_img_3.setEnabled(enabled)
        self.owner.radio_img_4.setEnabled(enabled)
        self.owner.radio_img_5.setEnabled(enabled)
        self.owner.radio_img_6.setEnabled(enabled)
        # self.owner.radio_img_7.setEnabled(enabled)
        self.owner.echBox.setEnabled(enabled)
        # self.owner.http3Box.setEnabled(enabled)
        # self.owner.dohBox.setEnabled(enabled)
        self.owner.dohLine.setEnabled(enabled)
        # self.radioButton_5.setEnabled(enabled)

    def __InitSetting(self):
        self.owner.radioApiGroup.buttonClicked.connect(
            partial(QtOwner().settingView.ButtonClickEvent, Setting.ProxySelectIndex))
        self.owner.radioImgGroup.buttonClicked.connect(
            partial(QtOwner().settingView.ButtonClickEvent, Setting.ProxyImgSelectIndex))
        self.owner.radioProxyGroup.buttonClicked.connect(
            partial(QtOwner().settingView.ButtonClickEvent, Setting.IsHttpProxy))
        self.owner.httpLine.editingFinished.connect(
            partial(QtOwner().settingView.LineEditEvent, Setting.HttpProxy, self.owner.httpLine))
        self.owner.sockEdit.editingFinished.connect(
            partial(QtOwner().settingView.LineEditEvent, Setting.Sock5Proxy, self.owner.sockEdit))
        self.owner.echBox.clicked.connect(
            partial(QtOwner().settingView.CheckButtonEvent, Setting.EnableEch, self.owner.echBox))
        # self.owner.http3Box.clicked.connect(
        #     partial(QtOwner().settingView.CheckButtonEvent, Setting.IsOpenHTTP3, self.owner.http3Box))
        self.owner.ipListEdit.editingFinished.connect(
            partial(QtOwner().settingView.LineEditEvent, Setting.PreferCDNList, self.owner.ipListEdit))
        self.owner.proxyIpEdit.editingFinished.connect(
            partial(QtOwner().settingView.LineEditEvent, Setting.ProxyIpCountry, self.owner.proxyIpEdit))
        self.owner.dohLine.editingFinished.connect(
            partial(QtOwner().settingView.LineEditEvent, Setting.DohAddress, self.owner.dohLine))

        self.proxyIpGroup.buttonClicked.connect(self.SaveProxyIp)
        self.owner.radioApiGroup.buttonClicked.connect(QtOwner().UpdateProxyName)
        self.owner.radioImgGroup.buttonClicked.connect(QtOwner().UpdateProxyName)
        self.proxyIpGroup.buttonClicked.connect(QtOwner().UpdateProxyName)
        self.LoadHistory()

    def LoadHistory(self):
        try:
            if Setting.LastProxyResult.value:
                for k, v in Setting.LastProxyResult.value.items():
                    if hasattr(self.owner, k):
                        widget = getattr(self.owner, k, None)
                        if isinstance(widget, QLabel):
                            widget.setText(str(v))
            if Setting.LastIpResult.value:
                for item in self.allItems.values():
                    assert isinstance(item, IpItem)
                    if item.ip in Setting.LastIpResult.value:
                        item.country = Setting.LastIpResult.value[item.ip].get('country', "")
                        item.asn = Setting.LastIpResult.value[item.ip].get('asn', "")
                        item.delay = Setting.LastIpResult.value[item.ip].get('delay', 0)
                        item.downloadDelay = Setting.LastIpResult.value[item.ip].get('downloadDelay', 0)
                        item.isFail = Setting.LastIpResult.value[item.ip].get('isFail', "")
                        item.downloadFail = Setting.LastIpResult.value[item.ip].get('downloadFail', "")
                        item.st = Setting.LastIpResult.value[item.ip].get('st', "")
                        item.downloadSt = Setting.LastIpResult.value[item.ip].get('downloadSt', "")

        except Exception as es:
            Log.Error(es)

    def SaveHistory(self):
        Setting.LastProxyResult.SetValue(dict(self.lastResult))

    def Init(self):
        if not self.isInitProxy:
            self.isInitProxy = True
            self.__InitSetting()
        self.LoadSetting()
        proxy = urllib.request.getproxies()
        if isinstance(proxy, dict) and proxy.get("http"):
            self.owner.proxyLabel.setText(proxy.get("http", ""))
            self.owner.checkLabel.setVisible(False)
        else:
            self.owner.checkLabel.setVisible(True)
        # if not self.allApiUrl:
        #     self.InitJmServer()
        self.CheckDohReq()

    def LoadSetting(self):
        # self.dohBox.setChecked(Setting.IsOpenDoh.value)
        # self.dohEdit.setText(Setting.DohAddress.value)
        self.owner.httpLine.setText(Setting.HttpProxy.value)
        self.owner.sockEdit.setText(Setting.Sock5Proxy.value)
        button = getattr(self.owner, "radioButton_{}".format(Setting.ProxySelectIndex.value), None)
        if button:
            button.setChecked(True)
        button = getattr(self.owner, "proxy_{}".format(int(Setting.IsHttpProxy.value)), None)
        if button:
            button.setChecked(True)
        button = getattr(self.owner, "radio_img_{}".format(int(Setting.ProxyImgSelectIndex.value)), None)
        if button:
            button.setChecked(True)
        # self.owner.cdn_api_ip.setText(Setting.PreferCDNIP.value)
        # self.owner.cdn_img_ip.setText(Setting.PreferCDNIPImg.value)
        # self.uaEdit.setText(Setting.UerAgent.value)
        # self.loginProxy.setChecked(bool(Setting.IsLoginProxy.value))
        self.owner.apiTimeout.setCurrentIndex(Setting.ApiTimeOut.value)
        self.owner.imgTimeout.setCurrentIndex(Setting.ImgTimeOut.value)
        # self.owner.host_api_domain.setText(Setting.HostApiDomain.value)
        # self.owner.host_img_domain.setText(Setting.HostImgDomain.value)
        self.owner.echBox.setChecked(bool(Setting.EnableEch.value))
        # self.owner.dohBox.setChecked(bool(Setting.IsOpenDoh.value))
        self.owner.dohLine.setText(Setting.DohAddress.value)
        # self.owner.http3Box.setChecked(bool(Setting.IsOpenHTTP3.value))
        self.owner.ipListEdit.setText(Setting.PreferCDNList.value)
        self.owner.proxyIpEdit.setText(Setting.ProxyIpCountry.value)

    def SaveSetting(self):
        Setting.IsHttpProxy.SetValue(int(self.owner.radioProxyGroup.checkedId()))
        Setting.Sock5Proxy.SetValue(self.owner.sockEdit.text())
        Setting.HttpProxy.SetValue(self.owner.httpLine.text())
        Setting.ProxySelectIndex.SetValue(self.owner.radioApiGroup.checkedId())
        Setting.ProxyImgSelectIndex.SetValue(self.owner.radioImgGroup.checkedId())
        # Setting.IsLoginProxy.SetValue(int(self.loginProxy.isChecked()))
        # Setting.PreferCDNIPImg.SetValue(self.owner.cdn_img_ip.text())
        # Setting.PreferCDNIP.SetValue(self.owner.cdn_api_ip.text())
        # Setting.HostApiDomain.SetValue(self.owner.host_api_domain.text())
        # Setting.HostImgDomain.SetValue(self.owner.host_img_domain.text())
        # Setting.UerAgent.SetValue(self.uaEdit.text())
        Setting.ApiTimeOut.SetValue(self.owner.apiTimeout.currentIndex())
        Setting.ImgTimeOut.SetValue(self.owner.imgTimeout.currentIndex())
        # Setting.IsOpenDoh.SetValue(bool(self.owner.dohBox.isChecked()))
        Setting.EnableEch.SetValue(bool(self.owner.echBox.isChecked()))
        Setting.DohAddress.SetValue((self.owner.dohLine.text()))
        # Setting.IsOpenHTTP3.SetValue(bool(self.owner.http3Box.isChecked()))
        # Setting.DohAddress.SetValue(self.dohEdit.text())
        # Setting.IsOpenDoh.SetValue(int(self.dohBox.isChecked()))
        # self.UpdateServer()
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        return

    # def UpdateServer(self):
    #     index = Setting.ProxySelectIndex.value-1
    #     index2 = Setting.ProxyImgSelectIndex.value-1
    #     if Setting.ProxyImgSelectIndex.value == 5:
    #         imageServer = Setting.PreferCDNIPImg.value
    #     else:
    #         imageServer = ""
    #     if Setting.ProxySelectIndex.value == 5:
    #         address = Setting.PreferCDNIP.value
    #     else:
    #         address = ""
    #     # Server().UpdateDns(address, imageServer)
    #     # Server().UpdateProxy()
    #     # QtOwner().settingView.SetSock5Proxy()
    #     Log.Warn("update proxy, ver:{}, setId:{}:{}, address:{}, img:{}".format(config.UpdateVersion, Setting.ProxySelectIndex.value, Setting.ProxyImgSelectIndex.value, address, imageServer))

    def CheckDohReq(self):
        self.checkResult = None
        self.checkDohUrl = self.owner.dohLine.text()
        self.SetDohIcon()
        url = GlobalConfig.AllApiDomain.value[0]
        request = req.DnsOverHttpsReq(url, self.checkDohUrl)
        self.owner.AddHttpTask(request, self.CheckDohBack, self.checkDohUrl)

    def CheckDohBack(self, raw, url):
        data = raw["data"]
        st = raw["st"]
        Log.Warn(f"check_doh, {url}, st:{st}, data:{data}")
        if url != self.checkDohUrl:
            return
        if st == Str.Ok and raw.get("Answer"):
            self.checkResult = True
        else:
            self.checkResult = False
        self.SetDohIcon()

    def SetDohIcon(self):
        icon2 = QIcon()
        if self.checkResult == True:
            icon2.addFile(u":/png/icon/right.svg", QSize(), QIcon.Normal, QIcon.Off)
        elif self.checkResult == False:
            icon2.addFile(u":/png/icon/error.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.owner.dohTool.setStyleSheet(u"background-color:transparent;")
        self.owner.dohTool.setMinimumSize(QSize(0, 40))
        self.owner.dohTool.setFocusPolicy(Qt.NoFocus)
        self.owner.dohTool.setIcon(icon2)
        self.owner.dohTool.setIconSize(QSize(20, 20))

    def OpenUrl(self):
        QtOwner().owner.helpView.OpenProxyUrl()

    # def InitJmServer(self):
    #     self.owner.AddHttpTask(req.GetJmServerReq(), self.InitJmServerBack)
    #     return
    #
    # def InitJmServerBack(self, raw):
    #     if raw.get("st") == Str.Ok:
    #         for server in raw.get('data', {}).get("jm3_Server"):
    #             if not server:
    #                 continue
    #             url = server[0]
    #             self.allApiUrl.append(url)
    #         self.owner.host_api_domain.SetWordData(self.allApiUrl)
    #     return

    def StartTestIp(self):
        self.owner.testIpButton.setEnabled(False)
        self.StartGetProxyIp()
    
    def StartGetProxyIp(self):
        request = req.GetProxyIpInfoReq(self.owner.proxyIpEdit.text())
        self.owner.AddHttpTask(request, self.GetProxyIpBack)
    
    def GetProxyIpBack(self, raw):
        st = raw["st"]
        if st == Str.Ok:
            ipList = raw.get("list", [])    
            self.otherProxyIps = ipList
            self.owner.proxyIpLabel.setText(f"<font color=#d71345>成功获取{len(ipList)}个proxyip节点</font>")
            Setting.ProxyIpLastList.SetValue(",".join(self.otherProxyIps))
        else:

            self.owner.proxyIpLabel.setText("<font color=#d71345>{}</font>".format(Str.GetStr(st)))
            Setting.ProxyIpLastList.SetValue("")
        if not self.otherProxyIps:
            self.otherProxyIps = GlobalConfig.ProxyIpList.value[:]
        self.GetBestCfIp()       
        
    def GetBestCfIp(self, raw):
        request = req.GetBestCfIpReq()
        self.owner.AddHttpTask(request, self.GetBestCfIpBack)
    
    def GetBestCfIpBack(self, raw):
        st = raw["st"]
        if st == Str.Ok:
            ipList = raw.get("list", [])    
            self.otherCDNIps = ipList
            self.owner.proxyIpLabel.setText(self.owner.proxyIpLabel.text() + f" <font color=#d71345>成功获取{len(ipList)}个CDN节点</font>")
            Setting.BestCfIpLastList.SetValue(",".join(self.otherCDNIps))
        else:
            self.owner.proxyIpLabel.setText(self.owner.proxyIpLabel.text() + " <font color=#d71345>{}</font>".format(Str.GetStr(st)))
            Setting.BestCfIpLastList.SetValue("")
        if not self.otherCDNIps:
            self.otherCDNIps = GlobalConfig.BestCfIpList.value[:]
        self.StartTestIp2()       

    def StartTestIp2(self):
        self.ShowAllItem()
        # url = GlobalConfig.CdnApiUrl.value
        self.maxSpeedIpCnt = len(self.allItems)
        for item in self.allItems.values():
            request = req.SpeedTestPingReq()
            request.SetProxy(0, "", "")
            request.SetIndex(0, 0, GlobalConfig.CdnImgUrl.value)
            request.SetCurlOpt(self.owner.echBox.isChecked, QtOwner().echConfig, item.ip)
            self.owner.AddHttpTask(request, self.StartTestIpBack, backParam=item.index)

            if not item.country or not item.asn:
                request = req.GetIpInfoReq(item.ip)
                request.SetProxy(0, "", "")
                request.SetIndex(0, 0)
                request.SetCurlOpt(False, "")
                self.owner.AddHttpTask(request, self.GetIpInfo, backParam=item.index)
        return

    def CheckSelectBox(self):
        if not self.allItems:
            return
        isHave = False
        selectIp = Setting.ProxyIpValue.value
        for item in self.allItems.values():
            assert isinstance(item, IpItem)
            if item.ip == selectIp:
                isHave = True
                item.isSelect = True
            else:
                item.isSelect = False
            self.UpdateRow(item)
        if not isHave:
            firstItem = sorted(self.allItems.values())[0]
            firstItem.isSelect = True
            Setting.ProxyIpValue.SetValue(firstItem.ip)
            self.UpdateRow(firstItem)

    def StartTestImgIp(self):
        url = GlobalConfig.CdnImgUrl.value
        self.maxSpeedImgCnt = 0
        for item in self.allItems.values():
            if item.isFail:
                continue
            self.maxSpeedImgCnt += 1
            request = req.SpeedTestPing2Req(url)
            request.SetProxy(0, "", "")
            request.SetIndex(0, 0,  GlobalConfig.CdnImgUrl.value)
            request.SetCurlOpt(self.owner.echBox.isChecked, QtOwner().echConfig, item.ip)
            self.owner.AddHttpTask(request, self.StartTestImgBack, backParam=item.index)
        return

    def GetIpInfo(self, raw, v):
        index = v
        data = raw.get("data", "")
        st = raw["st"]
        item = self.allItems.get(index)
        if not item:
            return
        assert isinstance(item, IpItem)
        if st == Str.Ok:
            try:
                data2 = json.loads(data)
                if data2.get("code") == 200:
                    country = data2.get('data',{}).get("country", "")
                    province = data2.get('data', {}).get("province", "")
                    isp = data2.get('data', {}).get("isp", "")
                    item.country = f"{country}·{province}"
                    item.asn = isp
                    self.UpdateRow(item)
                    # v = self.flowLayout.itemAt(item.index)
                    # if v:
                    #     w = v.widget()
                    #     assert isinstance(w, ProxyIpWidget)
                    #     w.Update(item)
            except Exception as es:
                Log.Error(es)
    #
    # def GetRawCountry(self, data):
    #     if data.get("country", {}).get("names"):
    #         names = data.get("country", {}).get("names")
    #     elif data.get("registered_country", {}).get("names"):
    #         names = data.get("country", {}).get("names")
    #     else:
    #         names = {}
    #     return self.GetCnName(names)
    #
    # def GetCnName(self, names):
    #     if "zh-CN" in names:
    #         return names['zh-CN']
    #     return names.get("en", "")

    def StartTestIpBack(self, raw, v):
        index = v
        data = raw["data"]
        st = raw["st"]
        item = self.allItems.get(index)
        if not item:
            return

        self.maxSpeedIpCnt -= 1
        assert isinstance(item, IpItem)
        if float(data) > 0.0:
            item.delay = int(float(data))
            # self.pingBackNumDict[i][backNum] = int(float(data))
            # label.setText("<font color=#7fb80e>{}</font>".format(str(int(float(data))) + "ms"))
        else:
            item.delay = 0
            item.isFail = True
            item.st = st
            # label.setText("<font color=#d71345>{}</font>".format(Str.GetStr(st)))
        self.UpdateRow(item)
        if self.maxSpeedIpCnt == 0:
            self.Sort()
            self.StartTestImgIp()

    def StartTestImgBack(self, raw, v):
        index = v
        data = raw["data"]
        st = raw["st"]
        item = self.allItems.get(index)
        if not item:
            return

        self.maxSpeedImgCnt -= 1
        assert isinstance(item, IpItem)
        if float(data) > 0.0:
            item.downloadDelay = int(float(data))
        else:
            item.downloadDelay = 0
            item.downloadFail = True
            item.downloadSt = st
        self.UpdateRow(item)
        if self.maxSpeedImgCnt <= 0:
            self.Sort()
            self.owner.testIpButton.setEnabled(True)
            self.CheckSelectBox()
            history = {}
            for item in self.allItems.values():
                assert isinstance(item, IpItem)
                history[item.ip] = {}
                history[item.ip]['country'] = item.country
                history[item.ip]['asn'] = item.asn
                history[item.ip]['delay'] = item.delay
                history[item.ip]['downloadDelay'] = item.downloadDelay
                history[item.ip]['isFail'] = item.isFail
                history[item.ip]['downloadFail'] = item.downloadFail
                history[item.ip]['st'] = item.st
                history[item.ip]['downloadSt'] = item.downloadSt
            Setting.LastIpResult.SetValue(history)

    def SaveProxyIp(self):
        tabRow = self.proxyIpGroup.checkedId()
        for item in self.allItems.values():
            if item.tableRow == tabRow:
                item.isSelect = True
                Setting.ProxyIpValue.SetValue(item.ip)
            else:
                item.isSelect = False

    def ShowAllItem(self):
        self.ClearAllItem()
        oldItems = {}
        for v in self.allItems.values():
            oldItems[v.ip] = v
        self.allItems = {}
        index = 0
        allips = set()

        for j, ip in enumerate(self.otherProxyIps):
            if not ip:
                continue

            if ip in allips:
                continue
            allips.add(ip)

            item = IpItem(index, j + 1, ip, True, False)
            item.isSelect = ip == Setting.ProxyIpValue.value
            self.allItems[index] = item
            if ip in oldItems:
                item.Copy(oldItems[ip])
            self.AddRow(index)
            self.UpdateRow(item)
            index += 1

        for j, ip in enumerate(ToolUtil.ExportIpsByStr(Setting.PreferCDNList.value)):
            if not ip:
                continue
            if ip in allips:
                continue
            allips.add(ip)
            item = IpItem(index, j+1, ip,False, True)
            item.isSelect = ip == Setting.ProxyIpValue.value
            self.allItems[index] = item
            if ip in oldItems:
                item.Copy(oldItems[ip])
            self.AddRow(index)
            self.UpdateRow(item)
            index += 1
        for j, ip in enumerate(self.otherCDNIps):
            if not ip:
                continue
            
            if ip in allips:
                continue
            allips.add(ip)
            
            item = IpItem(index, j+1, ip,False, False)
            item.isSelect = ip == Setting.ProxyIpValue.value
            self.allItems[index] = item
            if ip in oldItems:
                item.Copy(oldItems[ip])
            self.AddRow(index)
            self.UpdateRow(item)
            index += 1

        # self.owner.tableWidget.resizeColumnsToContents()
        # self.owner.tableWidget.resizeRowsToContents()

    def AddRow(self, index):
        rowCont = self.owner.tableWidget.rowCount()
        self.owner.tableWidget.insertRow(rowCont)
        checkBox = QCheckBox()
        self.owner.tableWidget.setCellWidget(rowCont, 0, checkBox)
        self.proxyIpGroup.addButton(checkBox)
        self.proxyIpGroup.setId(checkBox, index)

    def UpdateRow(self, info):
        assert isinstance(info, IpItem)
        if info.tableRow < 0:
            return
        widget = self.owner.tableWidget.cellWidget(info.tableRow, 0)
        if isinstance(widget, QCheckBox):
            widget.setText(info.name)
            widget.setChecked(info.isSelect)
        # self.owner.tableWidget.setItem(info.tableRow, 0, QTableWidgetItem(info.name))
        self.owner.tableWidget.setItem(info.tableRow, 1, QTableWidgetItem(info.ip))
        speed = ""
        if info.delay:
            speed = str(int(float(info.delay))) + "ms"
        if info.isFail:
            speed = Str.GetStr(info.st)
        if info.downloadDelay:
             speed += "/" + str(int(float(info.downloadDelay))) + "ms"
        if info.downloadFail:
            speed += "/" + Str.GetStr(info.downloadSt)

            # speed = ""
        # if info.delay:
        #     speed = "<font color=#7fb80e>{}</font>".format(str(int(float(info.delay))) + "ms")
        # if info.isFail:
        #     speed = "<font color=#d71345>{}</font>".format(Str.GetStr(info.st))
        self.owner.tableWidget.setItem(info.tableRow, 4, QTableWidgetItem(speed))
        self.owner.tableWidget.setItem(info.tableRow, 2, QTableWidgetItem(info.country))
        self.owner.tableWidget.setItem(info.tableRow, 3, QTableWidgetItem(info.asn))

    def GetProxyName(self):
        for item in self.allItems.values():
            if item.isSelect:
                return item.name
        return Setting.ProxyIpValue.value

    def ClearAllItem(self):
        for i in range(self.owner.tableWidget.rowCount()-1, -1, -1):
            widget = self.owner.tableWidget.cellWidget(i, 0)
            if isinstance(widget, QCheckBox):
                self.proxyIpGroup.removeButton(widget)
            self.owner.tableWidget.removeRow(i)

        # while 1:
            # child = self.flowLayout.takeAt(0)
            # if not child:
            #     break
            # if child.widget():
            #     child.widget().setParent(None)
            # del child
        return

    def Sort(self):
        sortItems = sorted(self.allItems.values())
        for i, item in enumerate(sortItems):
            assert isinstance(item, IpItem)
            item.tableRow = i
            self.UpdateRow(item)

        # order = self.order.get(col, 1)
        # if order == 1:
        #     self.tableWidget.sortItems(col, Qt.AscendingOrder)
        #     self.order[col] = 0
        # else:
        #     self.tableWidget.sortItems(col, Qt.DescendingOrder)
        #     self.order[col] = 1

    def SpeedTest(self):
        self.speedPingNum = 0
        self.speedTest = []
        self.SetEnabled(False)
        for i in range(1, self.maxNum):
            label = getattr(self.owner, "label_api_" + str(i))
            label.setText("")
            label = getattr(self.owner, "label_img_" + str(i))
            label.setText("")
            if i == self.cdnIndex:
                continue
            request = req.SpeedTestPingReq()
            request.SetIndex(i, i)
            address = GlobalConfig.GetAddress(i)
            request.SetCurlOpt(Setting.EnableEch.value, QtOwner().echConfig, address)
            self.speedPingNum += 1
            self.owner.AddHttpTask(request, self.SpeedTestPingBack, backParam=i)

    def SpeedTestPingBack(self, raw, v):
        i = v
        data = raw.get("data", "")
        st = raw["st"]
        label = getattr(self.owner, "label_api_" + str(i))
        if float(data) > 0.0:
            text = "<font color=#7fb80e>{}</font>".format(str(int(float(data))) + "ms")
            label.setText(text)
        else:
            text = "<font color=#d71345>{}</font>".format(Str.GetStr(st))
            label.setText(text)
        objectName = "label_api_" + str(i)
        self.lastResult[objectName] = text
        self.speedPingNum -= 1
        if self.speedPingNum == 0:
            self.speedDownNum = 0
            self.StartSpeedTest()

    def StartSpeedTest(self):
        self.speedDownNum += 1
        if self.speedDownNum >= self.maxNum:
            self.SetEnabled(True)
            self.SaveHistory()
            return
        if self.speedDownNum == self.cdnIndex:
            # 跳过ip分流
            self.StartSpeedTest()
            return
        i = self.speedDownNum
        label = getattr(self.owner, "label_img_" + str(i))
        label.setText("")
        request = req.SpeedTestReq()
        address = GlobalConfig.GetImageAdress(i)
        request.SetIndex(i, i)
        request.SetCurlOpt(Setting.EnableEch.value, QtOwner().echConfig, address)
        self.owner.AddHttpTask(lambda x: Server().TestSpeed(request, x), self.SpeedTestBack, i)
        return

    def SpeedTestBack(self, raw, i):
        data = raw["data"]
        st = raw["st"]
        if not data:
            data = "<font color=#d71345>{}</font>".format(Str.GetStr(st))
        else:
            data = "<font color=#7fb80e>{}</font>".format(data)
        objectName = "label_img_" + str(i)
        label = getattr(self.owner, "label_img_" + str(i))
        label.setText(data)
        self.lastResult[objectName] = data
        self.StartSpeedTest()
        return
