import threading
import weakref
from queue import Queue

import websocket

from config import config
from config.setting import Setting
from tools.log import Log


class ChatNewWebSocket:
    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        self.ws = None
        self._inQueue = Queue()
        self.sendThread = threading.Thread(target=self.SendDataRun)
        self.sendThread.setName("ChatSendThread")
        self.sendThread.setDaemon(True)
        self.sendThread.start()
        pass

    @property
    def parent(self):
        return self._parent()

    def Stop(self):
        self._inQueue.put("")
        return

    def SendDataRun(self):
        while True:
            task = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                if task == "":
                    break
                self._SendData(task)
            except Exception as es:
                Log.Error(es)
        pass

    def _SendData(self, data):
        # Log.Info("ws: send img data")
        self._Send(data)
        if "send_image" in data:
            Log.Info("ws: send img success")
            self.parent.websocket.emit(self.parent.SendImg, data)
        else:
            self.parent.websocket.emit(self.parent.SendMsg2, data)
        return

    def _Send(self, msg):
        try:
            if self.ws:
                self.ws.send(msg)
        except Exception as es:
            Log.Error(es)

    def Send(self, data):
        self._inQueue.put(data)
        return

    def on_message(self, ws, message):
        self.parent.websocket.emit(self.parent.Msg, message)

    def on_error(self, ws, error):
        self.parent.websocket.emit(self.parent.ErrorMsg, str(error))
        Log.Warn(error)

    def on_close(self, ws):
        self.parent.websocket.emit(self.parent.Leave, "")
        Log.Warn("close ws:{}".format(ws.url))

    def on_open(self, ws):
        self.parent.websocket.emit(self.parent.Enter, "")
        pass

    def Start(self, roomId, token):
        url = config.NewChatUrl
        url = url.replace("https", "wss")
        url = url.replace("http", "ws")
        url = url + "?token={}&room={}".format(token, roomId)
        def Run():
            # websocket.enableTrace(True)
            ws = websocket.WebSocketApp(url,
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
            self.ws = ws
            if Setting.HttpProxy.value and Setting.ChatProxy.value:
                data = Setting.HttpProxy.value.split(":")
                if len(data) == 3:
                    port = data[2]
                    host = data[1].replace("//", "")
                else:
                    host = data
                    port = 80

                ws.run_forever(ping_interval=30, http_proxy_host=host, http_proxy_port=port)
            else:
                ws.run_forever(ping_interval=30)

        thread = threading.Thread(target=Run)
        thread.setDaemon(True)
        thread.start()

    def Close(self):
        if self.ws:
            self.ws.close()
            self.ws = None
