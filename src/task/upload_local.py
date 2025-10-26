import os
import shutil

from task.task_upload import UpLoadBase

from tools.log import Log
from tools.status import Status
from tools.str import Str
from view.nas.nas_item import NasInfoItem


class LocalClient(UpLoadBase):
    AllLink = {}

    def __init__(self):
        UpLoadBase.__init__(self)
        self.path = ""
        pass

    def Init(self, nasInfo):
        self.path = nasInfo.path

    def Connect(self):
        try:
            isDir = os.path.isdir(self.path)
            if isDir:
                return Status.Ok
            else:
                return Str.DirNotFound
        except Exception as es:
            Log.Error(es)
            return Str.Error

    def TestConnect(self):
        try:
            isDir = os.path.isdir(self.path)
            if isDir:
                return Status.Ok
            else:
                return Str.DirNotFound
        except Exception as es:
            Log.Error(es)
            return Str.Error

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
            if not os.path.isfile(localPath):
                return Str.FileError
            if not os.path.isdir(remotePath):
                os.makedirs(remotePath)
            fileName = os.path.basename(localPath)
            destPath = os.path.join(remotePath, fileName)
            if os.path.isfile(destPath):
                os.remove(destPath)
            shutil.copy(localPath, destPath)
            os.remove(localPath)
        except Exception as es:
            Log.Error(es)
            return Str.Error
        return Str.Ok

