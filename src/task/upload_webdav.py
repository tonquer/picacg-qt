import os

import requests

from task.task_upload import UpLoadBase
from webdav3.client import Client
import webdav3.exceptions as WebdavEx

from tools.log import Log
from tools.status import Status
from tools.str import Str


class Unauthorized(WebdavEx.WebDavException):
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return "User '{name}' unauthorized".format(name=self.user)


def execute_request2(self, action, path, data=None, headers_ext=None):
    """Generate request to WebDAV server for specified action and path and execute it.

    :param action: the action for WebDAV server which should be executed.
    :param path: the path to resource for action
    :param data: (optional) Dictionary or list of tuples ``[(key, value)]`` (will be form-encoded), bytes,
                 or file-like object to send in the body of the :class:`Request`.
    :param headers_ext: (optional) the addition headers list witch should be added to basic HTTP headers for
                        the specified action.
    :return: HTTP response of request.
    """
    response = self.session.request(
        method=self.requests[action],
        url=self.get_url(path),
        auth=(self.webdav.login, self.webdav.password) if (not self.webdav.token and not self.session.auth)
                                                          and (
                                                                  self.webdav.login and self.webdav.password) else None,
        headers=self.get_headers(action, headers_ext),
        timeout=self.timeout,
        cert=(self.webdav.cert_path, self.webdav.key_path) if (
                self.webdav.cert_path and self.webdav.key_path) else None,
        data=data,
        proxies = {"http":None, "https":None},
        stream=True,
        verify=self.verify
    )
    if response.status_code == 507:
        raise WebdavEx.NotEnoughSpace()
    if response.status_code == 404:
        raise WebdavEx.RemoteResourceNotFound(path=path)
    if response.status_code == 405:
        raise WebdavEx.MethodNotSupported(name=action, server=self.webdav.hostname)
    if response.status_code == 401:
        raise Unauthorized(user=self.webdav.login)
    if response.status_code >= 400:
        raise WebdavEx.ResponseErrorCode(url=self.get_url(path), code=response.status_code, message=response.content)
    return response


Client.execute_request = execute_request2


class WebdavClient(UpLoadBase):
    def __init__(self):
        UpLoadBase.__init__(self)
        pass

    def Init(self, nasInfo):
        from view.nas.nas_item import NasInfoItem
        assert isinstance(nasInfo, NasInfoItem)
        self.address = nasInfo.address + ":" + str(nasInfo.port)
        self.password = nasInfo.passwd
        self.username = nasInfo.user

        options = {
            'webdav_hostname': self.address,
            'webdav_login': self.username,
            'webdav_password': self.password,
            'webdav_timeout': 5,
            'disable_check': True,   # 有的网盘不支持check功能
        }
        self.client = Client(options)
        self.client.verify = False

    def Connect(self):
        try:
            self.client.list()
        except Exception as es:
            Log.Error(es)
            return self.GetExceptionSt(es)
        return Str.Ok

    def Upload(self, localPath, remotePath):
        try:
            if not os.path.isfile(localPath):
                return Str.FileError
            self.CheckAndCreateDir(remotePath)
            fileName = os.path.basename(localPath)
            self.client.upload(remotePath + "/" + fileName, localPath)
            os.remove(localPath)
        except Exception as es:
            Log.Error(es)
            return self.GetExceptionSt(es)
        return Str.Ok

    def CheckAndCreateDir(self, remotePath):
        # result = self.client.check(remotePath)
        try:
            result = self.client.mkdir(remotePath)
        except Exception as es:
            Log.Error(es)
            return Str.CvMkdirFail
        return Str.Ok

    def GetExceptionSt(self, es):
        if isinstance(es, WebdavEx.NotEnoughSpace):
            return Str.CvNotSpace
        elif isinstance(es, WebdavEx.NoConnection):
            return Str.CvNotConnect
        elif isinstance(es, WebdavEx.MethodNotSupported):
            return Str.CvNotSupport
        elif isinstance(es, Unauthorized):
            return Str.CvAuthError
        else:
            return Str.Error


if __name__ == "__main__":
    a = WebdavClient()
    a.address = "http://101.35.89.244:16000"
    a.username = "tonquer"
    a.password = "123"
    a.Init()
    a.Upload("qt-unified-windows-x64-4.7.0-online.exe", "test")