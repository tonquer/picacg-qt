import base64
import json
import os
import random
import time

from PySide6.QtCore import Signal, QTimer, Qt, QEvent, QSize
from PySide6.QtGui import QFont, QTextCursor, QAction, QGuiApplication, QIcon
from PySide6.QtWidgets import QMenu, QWidget, QLabel, QListWidgetItem, QScroller, QListView

from component.dialog.loading_dialog import LoadingDialog
from component.label.msg_label import MsgLabel
from config import config
from config.setting import Setting
from interface.ui_chat_room import Ui_ChatRoom
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.tool import time_me, ToolUtil
from tools.user import User
from view.chat.chat_msg_widget import ChatMsgWidget
from view.chat.chat_websocket import ChatWebSocket


class ChatRoomWidget(QWidget, Ui_ChatRoom, QtTaskBase):
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
        self.socket = ChatWebSocket(self)
        self.websocket.connect(self.HandlerInfo)
        self.timer = QTimer(self)
        self.resize(200, 200)
        self.move(500, 500)
        self.timer.setInterval(15000)
        self.timer.timeout.connect(self.SendPing)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.SliderScroll)
        self.maxScrollArea = self.scrollArea.verticalScrollBar().value()

        self.msgInfo = {}
        self.removeMsgId = 0
        self.indexMsgId = 0
        self.maxMsgInfo = 1000
        self.loadingDialog = LoadingDialog(self)
        self.replyName = ""
        self.reply = ""
        self.atName = ""
        self.atUserId = ""
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
        self.LoginRoom()
        self.timer.start()
        self.loadingDialog.close()
        return

    def LoginRoom(self):
        data = ["init", User().userInfo]
        msg = "42{}".format(json.dumps(data))
        self.socket.Send(msg)
        Log.Info("send websocket info: {}".format(msg))

    def SendPing(self):
        msg = "2"
        self.socket.Send(msg)
        Log.Debug("send websocket info: ping")

    def RecvPong(self):
        Log.Debug("recv websocket info: pong")
        return

    def LeaveRoom(self):
        Log.Info("level room, Url:{}".format(self.url))
        self.timer.stop()
        self.close()
        self.url = ""
        for info in self.msgInfo.values():
            self.verticalLayout_2.removeWidget(info)
            info.setParent(None)
        self.msgInfo.clear()
        self.indexMsgId = 0
        self.removeMsgId = 0
        return

    def ReceviveMsg(self, msg):
        Log.Debug("recv websocket info: " + msg)
        if msg == "3":
            self.RecvPong()
        elif msg[:2] == "42":
            data = json.loads(msg[2:])
            if len(data) < 2:
                return
            elif data[0] == "new_connection":
               self._UpdateOnline(data[1])
            elif data[0] == "broadcast_message":
               self._RecvBroadcastMsg(data[1])
            elif data[0] == "broadcast_ads":
                self._RecvAdsMsg(data[1])
            elif data[0] == "broadcast_image":
                self._RecvBroadcastMsg(data[1])
            elif data[0] == "receive_notification":
                self._RecvNoticeMsg(data[1])
            elif data[0] == "broadcast_audio":
                self._RecvBroadcastMsg(data[1])
            elif data[0] == "send_image":
                self._RecvBroadcastMsg(data[1])
            elif data[0] == "send_message":
                self._RecvBroadcastMsg(data[1])
            else:
                a = data[1]
        return

    def _UpdateOnline(self, data):
        num = data.get("connections")
        self.numLabel.setText(Str.GetStr(Str.OnlineNum) + ": "+str(num))
        return

    @time_me
    def _RecvBroadcastMsg(self, data):
        msg = data.get("message", "")
        name = data.get("name", "")
        level = data.get("level")
        title = data.get("title")
        info = ChatMsgWidget(self)
        at = data.get('at')
        if at:
            if "@悄悄话" in msg:
                msg = "<font color=#1661ab>{}</font>".format("@悄悄话 " + at.replace("嗶咔_", "@")) + "\n" + msg.replace("@悄悄话", "")
            else:
                msg = "<font color=#1661ab>{}</font>".format(at.replace("嗶咔_", "@")) + "\n" + msg
        # info.commentLabel.setText("<font color=#130c0e>{}</font>".format(msg))
        info.commentLabel.setText("{}".format(msg.replace("\n", "<br/>")))
        info.nameLabel.setText(name)
        info.levelLabel.setText("<font color=#130c0e>{}</font>".format(" LV"+str(level))+" ")
        info.titleLabel.setText("<font color=#130c0e>{}</font>".format(" " + title + " "))
        # info.indexLabel.setText("{}".format(str(self.indexMsgId + 1))+ Str.GetStr(Str.Floor))
        date = time.strftime("%H:%M:%S")
        info.indexLabel.setText(date)
        # info.numLabel.setText("{}楼".format(str(self.indexMsgId+1)))
        info.infoLabel.setText(data.get("platform", "")+" ")
        imageData = data.get("image")
        if not imageData:
            replay = data.get("reply", "").replace("\n", "<br/>")
            replayName = data.get("reply_name", "")
            if replay and replayName:
                info.replayLabel.setText("<font color=#1661ab>@{}</font>{}".format(replayName, "<br/>" + replay))
                info.replayWidget.setVisible(True)
            else:
                info.replayWidget.setVisible(False)
        else:
            info.replayWidget.setVisible(False)
            imageData = imageData.split(",", 1)
            if len(imageData) >= 2:
                byte = base64.b64decode(imageData[1])
                date = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
                if Setting.SavePath.value:
                    path = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), "chat/picture/{}_{}.jpg".format(date, random.randint(1, 999)))
                    ToolUtil.SaveFile(byte, path)
                info.SetPictureComment(byte)

        audio = data.get("audio")
        if audio:
            info.replayWidget.setVisible(False)
            info.commentLabel.setVisible(False)
            info.toolButton.setVisible(True)
            try:
                saveName = str(int(time.time())) + "_" + str(random.randint(1, 1000)) + ".3gp"
                info.toolButton.setText(saveName)
                if Setting.SavePath.value:
                    path = os.path.join(Setting.SavePath.value, config.ChatSavePath)
                    saveName = os.path.join(path, saveName)
                    info.audioData = saveName
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    f = open(saveName, "wb")
                    f.write(audio.encode("utf-8"))
                    f.close()
            except Exception as es:
                Log.Error(es)
        else:
            info.toolButton.setVisible(False)
        userId = data.get("user_id", "")
        info.userId = userId
        url = data.get("avatar")
        if url and config.IsLoadingPicture:
            if isinstance(url, dict):
                url = ToolUtil.GetRealUrl(url.get("fileServer"), url.get("path"))
                path = ToolUtil.GetMd5RealPath(url, "chat/user")
                self.AddDownloadTask(url, path, completeCallBack=self.LoadingPictureComplete, backParam=self.indexMsgId)
            else:
                path = ToolUtil.GetMd5RealPath(url, "chat/user")
                self.AddDownloadTask(url, path, completeCallBack=self.LoadingPictureComplete, backParam=self.indexMsgId)
        character = data.get("character", "")
        if "pica-web.wakamoment.tk" not in character and character and config.IsLoadingPicture:
            self.AddDownloadTask(character, "", completeCallBack=self.LoadingHeadComplete, backParam=self.indexMsgId)
        self.verticalLayout_2.addWidget(info)
        self.msgInfo[self.indexMsgId] = info
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

    def OpenChat(self, url, name):
        if self.url:
            return
        self.show()
        self.atLabel.setVisible(False)
        self.replyLabel.setVisible(False)
        self.url = url
        self.nameLabel.setText(name)
        self.loadingDialog.show()
        self.socket.Start(self.url)
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
        info = dict(User().userInfo)
        if User().avatar:
            info['avatar'] = "https://storage.wikawika.xyz" + "/static/" + User().avatar.get("path")
        info['audio'] = ""
        info['block_user_id'] = ""
        info['platform'] = "android"
        info['message'] = ""
        if not imageData:
            info['reply_name'] = ""
            info['at'] = ""
            info['reply'] = ""
            if self.atLabel.isVisible() and self.atName:
                info['at'] = "嗶咔_" + self.atName
                if "@悄悄话" in self.atLabel.text():
                    info['message'] += "@悄悄话"
                    info["block_user_id"] = self.atUserId

            if self.replyLabel.isVisible() and self.replyName:
                info['reply'] = self.reply
                info['reply_name'] = self.replyName
            info['message'] += msg
            sendType = "send_message"
            data = "42" + json.dumps([sendType, info])
            self.textEdit.setText("")
            self.replyLabel.setVisible(False)
            self.atLabel.setVisible(False)
        else:
            info['image'] = imageData
            sendType = "send_image"
            data = "42" + json.dumps([sendType, info])
            self.picButton.setEnabled(False)
            self.picButton.setText(Str.GetStr(Str.Sending))

        self.socket.Send(data)

    def OpenPicture(self):
        try:
            data, name, picFormat = MsgLabel.OpenPicture(self, self.cachePath)
            if data:
                self.cachePath = os.path.dirname(name)
                imgData = base64.b64encode(data).decode("utf-8")
                imgData = "data:image/" + picFormat + ";base64," + imgData
                self.SendMsg(imgData)
        except Exception as ex:
            Log.Error(ex)
        return

    def Test(self):
        pass

    def SetAtLabel(self, name):

        self.atName = name
        self.atLabel.setText("@" + name + ":")
        self.atLabel.setVisible(True)

    def SetAtPrivateLabel(self, name, userId):
        self.atUserId = userId
        self.atName = name
        self.atLabel.setText("@悄悄话" + "_@" + name + ":")
        self.atLabel.setVisible(True)

    def SetReplyLabel(self, name, text):
        self.replyName = name
        self.reply = text
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
