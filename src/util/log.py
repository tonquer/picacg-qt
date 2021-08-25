import logging
import os
import time
import traceback

from conf import config


class Log(object):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    @staticmethod
    def UpdateLoggingLevel():
        if config.LogIndex == 0:
            Log.logger.setLevel(logging.WARN)
        elif config.LogIndex == 1:
            Log.logger.setLevel(logging.INFO)
        elif config.LogIndex == 2:
            Log.logger.setLevel(logging.DEBUG)
        return

    @staticmethod
    def Init():
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)

        Log.logger.addHandler(ch)

        if not os.path.isdir("logs"):
            os.mkdir("logs")
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        logfile = os.path.join("logs", day+".log")
        fh = logging.FileHandler(logfile, mode='a', encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        Log.logger.addHandler(fh)
        Log.Debug = Log.logger.debug
        Log.Info = Log.logger.info
        Log.Warn = Log.logger.warning
        Log.Error = Log.logger.exception
        return

    @staticmethod
    def Debug(es):
        Log.logger.debug(es)

    @staticmethod
    def Info(es):
        Log.logger.info(es, exc_info=True)

    @staticmethod
    def Warn(es):
        Log.logger.warning(es, exc_info=True)

    @staticmethod
    def Error(es):
        Log.logger.error(es, exc_info=True)