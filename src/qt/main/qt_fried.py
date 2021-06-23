import json

from PySide2 import QtWidgets
from PySide2.QtCore import QPoint
from PySide2.QtGui import Qt

from qss.qss import QssDataMgr
from src.qt.com.qt_fried_msg import QtFriedMsg
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import Server, req, Log, Status, config, ToolUtil
from ui.fried import Ui_Ui_Fried


class QtFried(QtWidgets.QWidget, Ui_Ui_Fried, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Ui_Fried.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.page = 1
        self.maxPage = 1
        self.msgInfo = {}
        self.indexMsgId = 0
        self.mousePressed = False
        self.pressPos = QPoint(0, 0)
        self.limit = 10
        self.scrollArea.verticalScrollBar().setStyleSheet(QssDataMgr().GetData('qt_list_scrollbar'))

    def GetName(self):
        return self.__class__.__name__

    def Clear(self):
        for info in self.msgInfo.values():
            info.setParent(None)
        self.msgInfo.clear()
        self.indexMsgId = 0

    def SwitchCurrent(self):
        self.LoadPageInfo(self.page)
        return

    def LoadPageInfo(self, page):
        QtOwner().owner.loadingForm.show()
        self.Clear()
        self.AddHttpTask(req.AppInfoReq(Server().token, (page-1)*self.limit), self.LoadPageBack, page)
        return

    def LoadPageBack(self, data, page):
        QtOwner().owner.loadingForm.close()
        errMsg = ""
        try:
            info = json.loads(data)
            errMsg = info.get("error", {}).get("message", "")
            self.maxPage = info.get("data").get('total')
            self.limit = info.get("data").get("limit")

            self.page = page
            self.maxPage = self.maxPage // self.limit + 1
            self.spinBox.setMaximum(self.maxPage)
            self.pageLabel.setText(str(self.page) + "\\" + str(self.maxPage))
            for v in info.get("data").get("posts"):
                self.AddInfo(v)
                pass
        except Exception as es:
            Log.Error(es)
            QtOwner().owner.msgForm.ShowMsg(Status.UnKnowError + errMsg)
        return

    def JumpPage(self):
        page = int(self.spinBox.text())
        self.Clear()
        self.LoadPageInfo(page)

    def AddInfo(self, v):
        info = QtFriedMsg(self)
        msg = v.get("content", "")
        name = v.get("_user", {}).get("name", "")
        level = v.get("_user", {}).get("level", "")
        title = v.get("_user", {}).get("title", "")
        character = v.get("_user", {}).get("character", "")
        avatar = v.get("_user", {}).get("avatar", "")
        medias = v.get("medias", [])
        info.id = v.get("_id")
        totalComment = v.get("totalComments")
        liked = v.get("liked")
        createdTime = v.get("createdAt")
        totalLikes = v.get('totalLikes')

        if createdTime:
            timeArray, day = ToolUtil.GetDateStr(createdTime)
            strTime = "{}年{}月{}日 {}:{}:{}   ".format(timeArray.tm_year, timeArray.tm_mon, timeArray.tm_mday, timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)
            info.infoLabel.setText("{}".format(strTime))

        info.likeButton.setText("({})".format(str(totalLikes)))
        info.commentButton.setText("({})".format(str(totalComment)))
        self.msgInfo[self.indexMsgId] = info
        info.commentLabel.setText(msg)
        info.nameLabel.setText(name)
        info.levelLabel.setText(" LV"+str(level)+" ")
        info.titleLabel.setText(" " + title + " ")
        info.indexLabel.setText("")
        info.replayLabel.setVisible(False)

        if medias and config.IsLoadingPicture:
            self.AddDownloadTask(medias[0], "", None, self.LoadingPictureComplete, True, self.indexMsgId, True)

        if avatar and config.IsLoadingPicture:
            self.AddDownloadTask(avatar, "", None, self.LoadingTitleComplete, True, self.indexMsgId, True)

        if "pica-web.wakamoment.tk" not in character and config.IsLoadingPicture:
            self.AddDownloadTask(character, "", None, self.LoadingHeadComplete, True, self.indexMsgId, True)

        self.indexMsgId += 1
        self.verticalLayout_4.addWidget(info)

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            widget = self.msgInfo.get(index)
            if not widget:
                return
            widget.SetPictureComment(data)

    def LoadingTitleComplete(self, data, status, index):
        if status == Status.Ok:
            widget = self.msgInfo.get(index)
            if not widget:
                return
            widget.SetPicture(data)

    def LoadingHeadComplete(self, data, status, index):
        if status == Status.Ok:
            widget = self.msgInfo.get(index)
            if not widget:
                return
            widget.SetHeadPicture(data)

    def mouseMoveEvent(self, ev):
        if not self.mousePressed:
            return
        curretPot = ev.pos()
        dist = self.pressPos.y() - curretPot.y()
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value()+dist)
        self.pressPos = curretPot

    def mousePressEvent(self, ev):
        self.mousePressed = True
        self.pressPos = ev.pos()

    def mouseReleaseEvent(self, ev):
        self.mousePressed = False
        self.pressPos = QPoint(0, 0)