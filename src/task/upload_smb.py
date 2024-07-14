import os

import requests

from task.task_upload import UpLoadBase
from smb.SMBConnection import SMBConnection, NotReadyError

from tools.log import Log
from tools.status import Status
from tools.str import Str
from view.nas.nas_item import NasInfoItem


class SmbClient(UpLoadBase):
    AllLink = {}

    def __init__(self):
        UpLoadBase.__init__(self)
        pass

    def Init(self, nasInfo):
        assert isinstance(nasInfo, NasInfoItem)
        self.address = nasInfo.address
        self.port = nasInfo.port
        self.password = nasInfo.passwd
        self.username = nasInfo.user
        datas = nasInfo.path.strip("/").split("/")

        self.service_name = datas[0]

        self.client = SMBConnection(self.username, self.password, '', '', use_ntlm_v2=True)
        self.isLink = False

    def Connect(self):
        try:
            if self.port:
                result = self.client.connect(self.address, self.port, timeout=5)
            else:
                result = self.client.connect(self.address, timeout=5)
            self.isLink = True
            if not result:
                return Str.CvAuthError
        except Exception as es:
            Log.Error(es)
            return self.GetExceptionSt(es)
        return Str.Ok

    def DisConnect(self):
        try:
            self.client.close()
        except Exception as es:
            Log.Error(es)
        return Str.Ok

    def IsHaveDir(self, remote_directory):
        filelist = self.client.listPath(self.service_name, os.path.dirname(remote_directory))
        for file in filelist:
            if file.isDirectory and file.filename == os.path.split(remote_directory)[-1]:
                return True
        return False

    def Create(self, path):
        current_dir = ""
        dirs = path.split("/")
        for directory in dirs:
            if not directory:
                continue
            current_dir += directory
            if not self.IsHaveDir(current_dir):
                self.client.createDirectory(self.service_name, current_dir)
            current_dir  += "/"
        return Str.Ok

    def Upload(self, localPath, remotePath):
        try:
            if not self.isLink:
                self.Connect()

            remotePath  = remotePath.replace("/{}/".format(self.service_name), "")
            if not os.path.isfile(localPath):
                return Str.FileError
            self.Create(remotePath)
            fileName = os.path.basename(localPath)
            with open(localPath, "rb") as local_file:
                self.client.storeFile(self.service_name, remotePath + "/" + fileName, local_file)
            os.remove(localPath)
        except Exception as es:
            Log.Error(es)
            return self.GetExceptionSt(es)
        return Str.Ok

    def GetExceptionSt(self, es):
        if isinstance(es, NotReadyError):
            return Str.CvAuthError
        return Str.Error
