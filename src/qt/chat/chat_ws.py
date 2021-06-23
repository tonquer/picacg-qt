import weakref
from queue import Queue

import websocket

from conf import config
from src.util import Log

try:
    import thread
except ImportError:
    import _thread as thread
import threading


class ChatWebSocket(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self._parent = weakref.ref(parent)
        self.ws = None
        self.sendThread = threading.Thread(target=self.SendDataRun)
        self.sendThread.setDaemon(True)
        self.sendThread.start()
        self._inQueue = Queue()
        pass

    @property
    def parent(self):
        return self._parent()

    def SendDataRun(self):
        while True:
            try:
                task = self._inQueue.get(True)
            except Exception as es:
                continue
                pass
            self._inQueue.task_done()
            try:
                self._SendData(task)
            except Exception as es:
                Log.Error(es)
        pass

    def _SendData(self, data):
        Log.Info("ws: send img data")
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
        print(error)

    def on_close(self, ws, code, msg):
        self.parent.websocket.emit(self.parent.Leave, "")
        print("### closed ###, code:{}, msg:{}".format(code, msg))

    def on_open(self, ws):
        self.parent.websocket.emit(self.parent.Enter, "")
        pass

    def Start(self, url):
        url = url.replace("https", "wss")
        url = url.replace("http", "ws")
        url = url + "/socket.io/?EIO=3&transport=websocket"
        def Run():
            # websocket.enableTrace(True)
            ws = websocket.WebSocketApp(url,
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
            self.ws = ws
            if config.HttpProxy and config.ChatProxy:
                data = config.HttpProxy.split(":")
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

    def Stop(self):
        if self.ws:
            self.ws.close()
            self.ws = None
