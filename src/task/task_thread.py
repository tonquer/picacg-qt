import socket
import threading
from tools.log import Log
from tools.tool import ToolUtil


class ThreadPrintDns(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.hostList = []

    def run(self):
        for h in self.hostList:
            self.resolve_ip(h)

    def resolve_ip(self, url):
        try:
            hostname = ToolUtil.GetUrlHost(url)
            ip_address = socket.gethostbyname(hostname)
            Log.Warn("dns_parse, host:{}, ip:{}".format(hostname, ip_address))
        except Exception as es:
            Log.Warn("dns_parse_error, host:{}, es:{}".format(url, es))