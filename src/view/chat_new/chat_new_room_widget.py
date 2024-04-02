import base64
import json
import os
import random
import time

from PySide6.QtCore import Signal, QTimer, Qt, QEvent, QSize
from PySide6.QtGui import QFont, QTextCursor, QAction, QGuiApplication, QIcon
from PySide6.QtWidgets import QMenu, QWidget, QLabel, QListWidgetItem, QScroller, QFileDialog, QFrame, QListView

from component.dialog.loading_dialog import LoadingDialog
from component.label.msg_label import MsgLabel
from config import config
from config.setting import Setting
from interface.ui_chat_room import Ui_ChatRoom
from qt_owner import QtOwner
from server import req
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.tool import time_me, ToolUtil
from tools.user import User
from view.chat_new.chat_new_msg_widget import ChatNewMsgWidget
from view.chat_new.chat_new_websocket import ChatNewWebSocket

class MsgData:
    def __init__(self):
        self.id = ""
        self.referenceId = ""
        self.type = "TEXT_MESSAGE"
        self.createdAt = ""
        self.isBlocked = False
        self.data = {}

    def ParseData(self, text):
        ToolUtil.ParseFromData(self, text)

class ChatNewRoomWidget(QWidget, Ui_ChatRoom, QtTaskBase):
    websocket = Signal(int, str)

    Enter = 1
    Leave = 2
    Msg = 3
    ErrorMsg = 4
    SendImg = 5
    SendMsg2 = 6

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_ChatRoom.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("PicACG")
        self.setWindowIcon(QIcon(":/png/icon/logo_round.png"))
        # self.titleBar = Ui_TitleBar()
        # self.titleBar.setupUi(self.widget)
        # self.titleBar.closeButton.clicked.connect(self.close)
        # self.titleBar.minButton.clicked.connect(self.showMinimized)
        # self.titleBar.menuButton.hide()

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.url = ""
        self.token = ""
        self.roleProfile = ""

        self.socket = ChatNewWebSocket(self)
        self.websocket.connect(self.HandlerInfo)
        # self.timer = QTimer(self)
        self.resize(200, 200)
        self.move(500, 500)
        # self.timer.setInterval(15000)
        # self.timer.timeout.connect(self.SendPing)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.SliderScroll)
        self.maxScrollArea = self.scrollArea.verticalScrollBar().value()

        self.msgInfo = {}
        self.msgIdInfo = {}
        self.removeMsgId = 0
        self.indexMsgId = 0
        self.maxMsgInfo = 1000
        self.loadingDialog = LoadingDialog(self)
        self.replyName = ""
        self.reply = ""
        self.atRoleId = ""
        self.atRoleName = ""

        self.listWidget.setFrameShape(QListView.NoFrame)  # 无边框
        self.listWidget.setFlow(QListView.LeftToRight)  # 从左到右
        self.listWidget.setWrapping(True)
        self.listWidget.setResizeMode(QListView.Adjust)
        self.listWidget.itemClicked.connect(self.IconSelect)
        # self.listWidget.setMinimumHeight(200)
        self.cachePath = "."
        f = QFont()
        f.setPointSize(14)
        for icon in Str.IconList:
            item = QListWidgetItem(icon)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(f)
            item.setSizeHint(QSize(60, 60))
            self.listWidget.addItem(item)
        self.listWidget.setVisible(False)
        # ToolUtil.SetIcon(self)

        self.toolMenu = QMenu(self.toolButton)
        self.action1 = QAction(Str.GetStr(Str.PressEnter), self.toolMenu, triggered=self.CheckAction1)
        self.action1.setCheckable(True)
        self.action2 = QAction(Str.GetStr(Str.PressCtrlEnter), self.toolMenu, triggered=self.CheckAction2)
        self.action2.setCheckable(True)
        self.toolMenu.addAction(self.action1)
        self.toolMenu.addAction(self.action2)
        self.toolButton.setMenu(self.toolMenu)
        if Setting.ChatSendAction.value == 0:
            self.action2.setChecked(True)
        else:
            self.action1.setChecked(True)
        self.textEdit.installEventFilter(self)
        self.isAutoScroll = True

        desktop = QGuiApplication.primaryScreen().geometry()
        self.resize(desktop.width() // 4 * 1, desktop.height() // 4 * 3)
        self.move(desktop.width() // 2, desktop.height() // 8)
        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)

    def Stop(self):
        self.socket.Stop()

    def CheckAction1(self):
        self.action2.setChecked(not self.action1.isChecked())
        Setting.ChatSendAction.SetValue(1)

    def CheckAction2(self):
        self.action1.setChecked(not self.action2.isChecked())
        Setting.ChatSendAction.SetValue(0)

    def eventFilter(self, obj, event):
        if obj == self.textEdit and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                # print(event.modifiers() == Qt.ControlModifier)
                if (Setting.ChatSendAction.value == 0 and event.modifiers() != Qt.ControlModifier) or (Setting.ChatSendAction.value == 1 and (event.modifiers() == Qt.ControlModifier)):
                    cursor = self.textEdit.textCursor()
                    textCursor = QTextCursor(self.textEdit.document())
                    textCursor.setPosition(cursor.position())
                    self.textEdit.setUndoRedoEnabled(False)
                    textCursor.insertBlock()
                    self.textEdit.setUndoRedoEnabled(True)
                    return True
                else:
                    self.SendMsg()
                    return True
            return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Return:
            if (Setting.ChatSendAction.value == 0 and event.modifiers() != Qt.ControlModifier) or (
                    Setting.ChatSendAction.value == 1 and (event.modifiers() == Qt.ControlModifier)):
                return
            else:
                self.SendMsg()
                return
        else:
            return super(self.__class__, self).keyPressEvent(event)

    def closeEvent(self, event) -> None:
        self.socket.Close()
        return super(self.__class__, self).closeEvent(event)

    def GetName(self):
        return self.__class__.__name__

    def Error(self, error):
        return

    def JoinRoom(self):
        Log.Info("join room, Url:{}".format(self.url))
        # self.LoginRoom()
        # self.timer.start()
        self.loadingDialog.close()
        return

    # def LoginRoom(self):
    #     data = ["init", User().userInfo]
    #     msg = "42{}".format(json.dumps(data))
    #     self.socket.Send(msg)
    #     Log.Info("send websocket info: {}".format(msg))

    # def SendPing(self):
    #     msg = "2"
    #     self.socket.Send(msg)
    #     Log.Debug("send websocket info: ping")

    # def RecvPong(self):
    #     Log.Debug("recv websocket info: pong")
    #     return

    def LeaveRoom(self):
        Log.Info("level room, Url:{}".format(self.url))
        # self.timer.stop()
        self.close()
        self.url = ""
        for info in self.msgInfo.values():
            self.verticalLayout_2.removeWidget(info)
            info.setParent(None)
        self.msgInfo.clear()
        self.msgIdInfo.clear()
        self.indexMsgId = 0
        self.removeMsgId = 0
        return

    def ReceviveMsg(self, msg):
        Log.Debug("recv websocket info: " + msg)
        try:
            data = json.loads(msg)
            msg = MsgData()
            msg.ParseData(data)
            if msg.type == "TEXT_MESSAGE":
                self._RecvBroadcastMsg(msg)
            elif msg.type == "IMAGE_MESSAGE":
                self._RecvImageMsg(msg)
            elif msg.type == "CONNECTED":
                pass
            elif msg.type == "INITIAL_MESSAGES":
                self._RecvBroadcastInitMsgs(msg)
            elif msg.type == "DELETE_MESSAGE_ACTION":
                "删除消息"
                pass
            elif msg.type == "UPDATE_ROOM_ONLINE_USERS_COUNT_ACTION":
                onlineCount = msg.data.get("onlineCount", 0)
                self.onlineNum.setText(str(onlineCount))
                pass
            elif msg.type == "PODCAST_IS_LIVE_ACTION":
                pass
            # if len(data) < 2:
            #     return
            # elif data[0] == "new_connection":
            #     self._UpdateOnline(data[1])
            # elif data[0] == "broadcast_message":
            #     self._RecvBroadcastMsg(data[1])
            # elif data[0] == "broadcast_ads":
            #     self._RecvAdsMsg(data[1])
            # elif data[0] == "broadcast_image":
            #     self._RecvBroadcastMsg(data[1])
            # elif data[0] == "receive_notification":
            #     self._RecvNoticeMsg(data[1])
            # elif data[0] == "broadcast_audio":
            #     self._RecvBroadcastMsg(data[1])
            # elif data[0] == "send_image":
            #     self._RecvBroadcastMsg(data[1])
            # elif data[0] == "send_message":
            #     self._RecvBroadcastMsg(data[1])
            # else:
            #     a = data[1]
        except Exception as es:
            Log.Warn(msg)
            Log.Error(es)
        return

    def _UpdateOnline(self, data):
        num = data.get("connections")
        self.numLabel.setText(Str.GetStr(Str.OnlineNum) + ": "+str(num))
        return

    @time_me
    def _RecvBroadcastInitMsgs(self, rawMsg):
        for v in rawMsg.data.get("messages", []):
            msg = MsgData()
            msg.ParseData(v)
            if msg.type == "TEXT_MESSAGE":
                self._RecvBroadcastMsg(msg)
            elif msg.type == "IMAGE_MESSAGE":
                self._RecvImageMsg(msg)
            else:
                pass
        pass

    @time_me
    def _RecvBroadcastMsg(self, rawMsg):
        data = rawMsg.data
        msg = data.get("message", "")

        userMentions = data.get("userMentions", [])
        reply = data.get("reply", {})

        createdTime = rawMsg.createdAt
        timeArray, _ = ToolUtil.GetDateStr(createdTime)
        strTime = "{}:{}:{}   ".format(timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)

        name = data.get("profile", {}).get("name", "")
        level = data.get("profile", {}).get("level", "")
        title = data.get("profile", {}).get("title", "")
        characters = data.get("profile", {}).get("characters", [])
        info = ChatNewMsgWidget(self)
        info.vipIcon.hide()
        info.managerIcon.hide()
        info.nvIcon.hide()
        info.officialIcon.hide()
        info.rawMsg = rawMsg
        for i in characters:
            if i == "vip":
                info.vipIcon.setVisible(True)
            elif i == "girl":
                info.nvIcon.setVisible(True)
            elif i == "manager":
                info.managerIcon.setVisible(True)
            elif i == "official":
                info.officialIcon.setVisible(True)
            elif i == "anchor":
                pass
        for at in userMentions:
            atName = at.get("name", "")
            msg = "<font color=#1661ab>@{}</font>".format(atName) + "\n" + msg

        # info.commentLabel.setText("<font color=#130c0e>{}</font>".format(msg))
        info.commentLabel.setText("{}".format(msg.replace("\n", "<br/>")))
        info.nameLabel.setText(name)
        info.levelLabel.setText("<font color=#130c0e>{}</font>".format(" LV"+str(level))+" ")
        info.titleLabel.setText("<font color=#130c0e>{}</font>".format(" " + title + " "))
        # info.indexLabel.setText("{}".format(str(self.indexMsgId + 1))+ Str.GetStr(Str.Floor))
        # date = time.strftime("%H:%M:%S")
        info.indexLabel.setText(strTime)
        # info.numLabel.setText("{}楼".format(str(self.indexMsgId+1)))
        info.infoLabel.setText(data.get("platform", "")+" ")
        if reply:
            replayId = reply.get("id")
            replyType = reply.get("type", "")

            replyData = reply.get("data", {})
            replyMsg = str(replyData.get("message", ""))
            if replyMsg == "null" or replyMsg == "None":
                replyMsg = ""

            index = self.msgIdInfo.get(replayId)
            oldWiget = self.msgInfo.get(index)
            if oldWiget:
                assert isinstance(oldWiget, ChatNewMsgWidget)
                replyData = oldWiget.rawMsg.data

            replyName = replyData.get("name", "")
            info.replayLabel.setText("<font color=#1661ab>@{}</font>{}".format(replyName, "<br/>" + replyMsg))
            info.replayWidget.setVisible(True)
            if replyType == "TEXT_MESSAGE":
                # replyMsg = replyData.get("message", {}).get("message", "")
                # replyDate = replyData.get("message", {}).get("date", "")
                info.replyPic.hide()
                info.replayWidget.setVisible(True)
            elif replyType == "IMAGE_MESSAGE":
                ## 回复图片
                info.SetReplyPictureDefault()
                replayImage = reply.get("data", {}).get("media")
                replyName = reply.get("data", {}).get("name", "")
                info.replayLabel.setText("<font color=#1661ab>@{}</font>{}".format(replyName, "<br/>" + replyMsg))
                if replayImage:
                    path = ToolUtil.GetMd5RealPath(replayImage, "chat2/img")
                    self.AddDownloadTask(replayImage, path, completeCallBack=self.LoadingReplyMsgImgComplete, backParam=self.indexMsgId)
                # replyMsg = replyData.get("message", {}).get("message", "")
                # replyDate = replyData.get("message", {}).get("date", "")
                # replyName = replyData.get("profile", {}).get("name", "")
                # info.replayLabel.setText("<font color=#1661ab>@{}</font>{}".format(replyName, "<br/>" + replyMsg))
                # info.replayWidget.setVisible(True)
                pass
            else:
                info.replayWidget.setVisible(False)
        else:
            info.replayWidget.setVisible(False)
        userId = data.get("user_id", "")
        info.userId = userId
        profile = data.get("profile", {})
        if profile and config.IsLoadingPicture:
            url = profile.get("avatarUrl")
            path = ToolUtil.GetMd5RealPath(url, "chat2/user")
            self.AddDownloadTask(url, path, completeCallBack=self.LoadingPictureComplete, backParam=self.indexMsgId)

        self.verticalLayout_2.addWidget(info)
        self.msgInfo[self.indexMsgId] = info
        self.msgIdInfo[rawMsg.id] = self.indexMsgId
        self.indexMsgId += 1
        if len(self.msgInfo) > self.maxMsgInfo:
            removeInfo = self.msgInfo.get(self.removeMsgId)
            if removeInfo:
                self.verticalLayout_2.removeWidget(removeInfo)
                removeInfo.setParent(None)
                self.msgInfo.pop(self.removeMsgId)
            self.removeMsgId += 1
        return

    @time_me
    def _RecvImageMsg(self, rawMsg):
        data = rawMsg.data
        msg = data.get("caption", "")
        if msg == "null" or msg == "None" or not msg:
            msg = ""
        userMentions = data.get("userMentions", [])
        reply = data.get("reply", {})

        createdTime = rawMsg.createdAt
        timeArray, _ = ToolUtil.GetDateStr(createdTime)
        strTime = "{}:{}:{}   ".format(timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)

        name = data.get("profile", {}).get("name", "")
        level = data.get("profile", {}).get("level", "")
        title = data.get("profile", {}).get("title", "")
        info = ChatNewMsgWidget(self)
        info.rawMsg = rawMsg

        for at in userMentions:
            name = at.get("name", "")
            msg = "<font color=#1661ab>{}</font>".format(name) + "\n" + msg

        # info.commentLabel.setText("<font color=#130c0e>{}</font>".format(msg))
        info.commentLabel.setText("{}".format(msg.replace("\n", "<br/>")))
        info.nameLabel.setText(name)
        info.levelLabel.setText("<font color=#130c0e>{}</font>".format(" LV"+str(level))+" ")
        info.titleLabel.setText("<font color=#130c0e>{}</font>".format(" " + title + " "))
        # info.indexLabel.setText("{}".format(str(self.indexMsgId + 1))+ Str.GetStr(Str.Floor))
        info.indexLabel.setText(strTime)
        info.replayWidget.setVisible(False)
        # info.numLabel.setText("{}楼".format(str(self.indexMsgId+1)))
        info.infoLabel.setText(data.get("platform", "")+" ")

        imageData = None
        userId = data.get("user_id", "")
        info.userId = userId
        profile = data.get("profile", {})
        info.SetPictureDefault()
        if profile and config.IsLoadingPicture:
            url = profile.get("avatarUrl")
            path = ToolUtil.GetMd5RealPath(url, "chat2/user")
            self.AddDownloadTask(url, path, completeCallBack=self.LoadingPictureComplete, backParam=self.indexMsgId)

        medias = data.get("medias", [])
        if medias and config.IsLoadingPicture:
            ## 这里目前只有一张
            url = medias[0]
            path = ToolUtil.GetMd5RealPath(url, "chat2/img")
            self.AddDownloadTask(url, path, completeCallBack=self.LoadingMsgImgComplete, backParam=self.indexMsgId)

        self.verticalLayout_2.addWidget(info)
        self.msgInfo[self.indexMsgId] = info
        self.msgIdInfo[rawMsg.id] = self.indexMsgId
        self.indexMsgId += 1
        if len(self.msgInfo) > self.maxMsgInfo:
            removeInfo = self.msgInfo.get(self.removeMsgId)
            if removeInfo:
                self.verticalLayout_2.removeWidget(removeInfo)
                removeInfo.setParent(None)
                self.msgInfo.pop(self.removeMsgId)
            self.removeMsgId += 1
        return

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            widget = self.msgInfo.get(index)
            if not widget:
                return
            widget.SetPicture(data)

    def LoadingReplyMsgImgComplete(self, data, status, index):
        if status == Status.Ok:
            widget = self.msgInfo.get(index)
            if not widget:
                return
            widget.SetReplyPictureComment(data)
        return

    def LoadingMsgImgComplete(self, data, status, index):
        if status == Status.Ok:
            widget = self.msgInfo.get(index)
            if not widget:
                return
            widget.SetPictureComment(data)
        return

    def LoadingHeadComplete(self, data, status, index):
        if status == Status.Ok:
            widget = self.msgInfo.get(index)
            if not widget:
                return
            widget.SetHeadPicture(data)

    def _RecvAdsMsg(self, data):
        return

    def _RecvNoticeMsg(self, data):
        msg = data.get("message", "")
        info = QLabel(msg)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        info.setFont(font)
        self.verticalLayout_2.addWidget(info, alignment=Qt.AlignCenter)
        self.msgInfo[self.indexMsgId] = info
        self.indexMsgId += 1
        return

    def OpenChat(self, token, roleProfile, roomId, name):
        if self.url:
            return
        self.token = token
        self.roleProfile = roleProfile
        self.show()
        self.atLabel.setVisible(False)
        self.replyLabel.setVisible(False)
        self.url = roomId
        self.nameLabel.setText(name)
        self.loadingDialog.show()
        self.socket.Start(self.url, token)
        return

    def HandlerInfo(self, taskType, data):
        if taskType == self.Leave:
            self.LeaveRoom()
        elif taskType == self.Msg:
            self.ReceviveMsg(data)
        elif taskType == self.Enter:
            self.JoinRoom()
        elif taskType == self.ErrorMsg:
            QtOwner().CloseLoading()
            MsgLabel().ShowErrorEx(self, Str.GetStr(Str.DownError) + "," + data)
            pass
        elif taskType == self.SendImg:
            self.picButton.setEnabled(True)
            self.picButton.setText(Str.GetStr(Str.Picture))
            self.ReceviveMsg(data)
        elif taskType == self.SendMsg2:
            self.ReceviveMsg(data)

    def SliderScroll(self):
        # print(self.scrollArea.verticalScrollBar().value(), self.maxScrollArea,
        #       self.scrollArea.verticalScrollBar().maximum())
        # print(self.scrollArea.verticalScrollBar().value(), self.scrollArea.verticalScrollBar().maximum(), self.maxScrollArea)
        # 自动滚动
        if abs(self.scrollArea.verticalScrollBar().value() - self.maxScrollArea) <= 200:
            self.scrollArea.vScrollBar.ScrollValue(self.scrollArea.verticalScrollBar().maximum())
        self.maxScrollArea = self.scrollArea.verticalScrollBar().maximum()

    def SendMsg(self, imageData=None):
        msg = self.textEdit.toPlainText()
        if not msg and not imageData:
            return
        userMentions = []
        replyId = ""
        if self.atLabel.isVisible() and self.atRoleId:
            userMentions = [self.atRoleId]
        if self.replyLabel.isVisible() and self.reply:
            replyId = self.reply.get("id", "")
        data = req.SendNewChatMsgReq(self.token, self.url, msg, userMentions, replyId)
        self.AddHttpTask(data, callBack=self.SendMsgBack)
        self.textEdit.setText("")
        self.replyLabel.setVisible(False)
        self.atLabel.setVisible(False)

    def SendMsgBack(self, raw):
        st = raw["st"]
        Log.Debug(raw)

    def OpenPicture(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Open Image", self.cachePath, "Image Files(*.jpg *.png *.webp *.gif)")
            if filename and len(filename) > 1:
                name = filename[0]
                if not name:
                    return
                self.cachePath = os.path.dirname(name)
                msg = self.textEdit.toPlainText()
                data = req.SendNewChatImgMsgReq(self.token, self.url, msg, name)
                self.AddHttpTask(data, callBack=self.SendMsgBack)
                self.textEdit.setText("")
                self.replyLabel.setVisible(False)
                self.atLabel.setVisible(False)
        except Exception as ex:
            Log.Error(ex)
        return

    def Test(self):
        pass

    def SetAtLabel(self, widget):
        assert isinstance(widget, ChatNewMsgWidget)
        assert isinstance(widget.rawMsg, MsgData)

        self.atRoleId = widget.rawMsg.data.get("profile", {}).get("id", "")
        self.atRoleName = widget.rawMsg.data.get("profile", {}).get("name", "")
        self.atLabel.setText("@" + self.atRoleName + ":")
        self.atLabel.setVisible(True)

    def SetAtPrivateLabel(self, widget):
        assert isinstance(widget, ChatNewMsgWidget)
        assert isinstance(widget.rawMsg, MsgData)

        self.atRoleId = widget.rawMsg.data.get("profile", {}).get("id", "")
        self.atRoleName = widget.rawMsg.data.get("profile", {}).get("name", "")
        self.atLabel.setText("@" + self.atRoleName + ":")
        self.atLabel.setVisible(True)

    def SetReplyLabel(self, widget):
        assert isinstance(widget, ChatNewMsgWidget)
        assert isinstance(widget.rawMsg, MsgData)
        name = widget.rawMsg.data.get("profile", {}).get("name", "")
        text = widget.rawMsg.data.get("message", "")
        self.reply = {
            "id": widget.rawMsg.id,
            "name": name,
            "type": "TEXT_MESSAGE",
            "images": "null",
            "message": text,
        }
        self.replyLabel.setText(name + ":" + text)
        self.replyLabel.setVisible(True)

    def SetEnable1(self):
        self.atLabel.setVisible(False)
        return

    def SetEnable2(self):
        self.replyLabel.setVisible(False)
        return

    def OpenIcon(self):
        self.listWidget.setVisible(not self.listWidget.isVisible())
        return

    def IconSelect(self, item):
        data = item.text()
        text = self.textEdit.toPlainText()
        self.textEdit.setText(text + data)
        self.listWidget.setVisible(False)
