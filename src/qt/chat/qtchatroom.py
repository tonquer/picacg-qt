import base64
import json

from PySide2 import QtWidgets, QtWebSockets
from PySide2.QtCore import Signal, QTimer
from PySide2.QtGui import QPixmap

from conf import config
from src.qt.chat.chat_ws import ChatWebSocket
from src.qt.chat.qtchatroommsg import QtChatRoomMsg
from src.qt.com.qtloading import QtLoading
from src.qt.util.qttask import QtTask
from src.user.user import User
from src.util import Log
from src.util.status import Status
from ui.chatroom import Ui_ChatRoom, Qt, QUrl


class QtChatRoom(QtWidgets.QWidget, Ui_ChatRoom):
    websocket = Signal(int, str)

    Enter = 1
    Leave = 2
    Msg = 3

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_ChatRoom.__init__(self)
        self.setupUi(self)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWindowTitle("聊天室")
        self.url = ""
        self.socket = ChatWebSocket(self)
        self.websocket.connect(self.HandlerInfo)
        self.timer = QTimer(self)
        self.resize(800, 1000)
        self.timer.setInterval(15000)
        self.timer.timeout.connect(self.SendPing)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.SliderScroll)

        self.msgInfo = {}
        self.removeMsgId = 0
        self.indexMsgId = 0
        self.maxMsgInfo = 100
        self.loadingForm = QtLoading(self)

    def closeEvent(self, event) -> None:
        self.socket.Stop()
        return super(self.__class__, self).closeEvent(event)

    def GetName(self):
        return self.__class__.__name__

    def Error(self, error):
        return

    def JoinRoom(self):
        Log.Debug("join room, Url:{}".format(self.url))
        self.LoginRoom()
        self.timer.start()
        self.loadingForm.close()
        return

    def LoginRoom(self):
        data = ["init", User().userInfo]
        msg = "42{}".format(json.dumps(data))
        self.socket.Send(msg)

    def SendPing(self):
        msg = "2"
        self.socket.Send(msg)
        Log.Debug("send ping")

    def RecvPong(self):
        return

    def LeaveRoom(self):
        Log.Debug("level room, Url:{}".format(self.url))
        self.timer.stop()
        self.close()
        self.url = ""
        for info in self.msgInfo.values():
            info.setParent(None)
        self.msgInfo.clear()
        self.indexMsgId = 0
        self.removeMsgId = 0
        return

    def ReceviveMsg(self, msg):
        Log.Debug(msg)
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
        return

    def _UpdateOnline(self, data):
        num = data.get("connections")
        self.numLabel.setText("在线人数："+str(num))
        return

    def _RecvBroadcastMsg(self, data):
        msg = data.get("message", "")
        name = data.get("name", "")
        info = QtChatRoomMsg()
        info.commentLabel.setText(msg)
        info.nameLabel.setText(name)
        info.numLabel.setText("{}楼".format(str(self.indexMsgId+1)))

        imageData = data.get("image")
        if not imageData:
            replay = data.get("reply", "")
            replayName = data.get("reply_name", "")
            if replay and replayName:
                info.replayLabel.setText(replayName + "\n" + replay)
                info.replayLabel.setVisible(True)
            else:
                info.replayLabel.setVisible(False)
        else:
            info.replayLabel.setVisible(False)
            image = QPixmap()
            imageData = imageData.split(",", 1)
            if len(imageData) >= 2:
                byte = base64.b64decode(imageData[1])
                image.loadFromData(byte)
            width = info.commentLabel.width()
            height = info.commentLabel.height()
            image.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            info.commentLabel.setPixmap(image)

        url = data.get("avatar")
        if url and config.IsLoadingPicture:
            if isinstance(url, dict):
                QtTask().AddDownloadTask(url.get("fileServer"), url.get("path"), None, self.LoadingPictureComplete, True, self.indexMsgId, True, self.GetName())
            else:
                QtTask().AddDownloadTask(url, "", None, self.LoadingPictureComplete, True, self.indexMsgId, True,
                                         self.GetName())
        self.verticalLayout_2.addWidget(info)
        self.msgInfo[self.indexMsgId] = info
        self.indexMsgId += 1
        if len(self.msgInfo) > self.maxMsgInfo:
            removeInfo = self.msgInfo.get(self.removeMsgId)
            if removeInfo:
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

    def _RecvAdsMsg(self, data):
        return

    def OpenChat(self, url, name):
        if self.url:
            return
        self.show()
        self.url = url
        self.nameLabel.setText(name)
        self.loadingForm.show()
        self.socket.Start(self.url)
        return

    def HandlerInfo(self, taskType, data):
        if taskType == self.Leave:
            self.LeaveRoom()
        elif taskType == self.Msg:
            self.ReceviveMsg(data)
        elif taskType == self.Enter:
            self.JoinRoom()

    def SliderScroll(self):
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximumHeight())

    def SendMsg(self):
        msg = self.lineEdit.text()
        if not msg:
            return
        info = dict(User().userInfo)
        if User().avatar:
            info['avatar'] = "https://storage.wikawika.xyz" + "/static/" + User().avatar.get("path")
        info['at'] = ""
        info['audio'] = ""
        info['message'] = msg
        info['reply'] = ""
        info['reply_name'] = ""
        info['image'] = ""
        info['block_user_id'] = ""
        data = "42" + json.dumps(["send_message", info])
        self.socket.Send(data)
        self._RecvBroadcastMsg(info)

    def Test(self):
        pass
