import os
import shutil

from PySide6.QtCore import QDir


class Setting:
    @staticmethod
    def Init():
        path = Setting.GetConfigPath()
        if not os.path.isdir(path):
            os.mkdir(path)
        Setting.CheckRepair()
        return

    @staticmethod
    def GetConfigPath():
        homePath = QDir.homePath()
        projectName = ".picacg"
        return os.path.join(homePath, projectName)

    @staticmethod
    def GetLogPath():
        return os.path.join(Setting.GetConfigPath(), "logs")

    @staticmethod
    def CheckRepair():
        try:
            fileList = ["download.db", "config.ini", "history.db"]
            for file in fileList:
                path = os.path.join(Setting.GetConfigPath(), file)
                if not os.path.isfile(path):
                    if os.path.isfile(file):
                        shutil.copyfile(file, path)
        except Exception as es:

            from tools.log import Log
            Log.Error(es)
