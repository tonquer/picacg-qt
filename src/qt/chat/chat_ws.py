import weakref

import websocket

from conf import config

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
        pass

    @property
    def parent(self):
        return self._parent()

    def Send(self, msg):
        if self.ws:
            self.ws.send(msg)

    def on_message(self, ws, message):
        self.parent.websocket.emit(self.parent.Msg, message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        self.parent.websocket.emit(self.parent.Leave, "")
        print("### closed ###")

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
            if config.HttpProxy:
                data = config.HttpProxy.split(":")
                if len(data) == 3:
                    port = data[2]
                    host = data[1].replace("//", "")
                else:
                    host = data
                    port = 80

                ws.run_forever(http_proxy_host=host, http_proxy_port=port)
            else:
                ws.run_forever()

        thread = threading.Thread(target=Run)
        thread.setDaemon(True)
        thread.start()

    def Stop(self):
        if self.ws:
            self.ws.close()
            self.ws = None
