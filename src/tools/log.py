import logging
import os
import time

from config import config
from config.setting import Setting


class Log(object):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = None
    fh = None

    @staticmethod
    def UpdateLoggingLevel():
        if Setting.LogIndex.value == 0:
            Log.ch.setLevel(logging.WARN)
            Log.fh.setLevel(logging.WARN)
            # Log.logger.setLevel(logging.WARN)
        elif Setting.LogIndex.value == 1:
            Log.ch.setLevel(logging.INFO)
            Log.fh.setLevel(logging.INFO)
            # Log.logger.setLevel(logging.INFO)
        elif Setting.LogIndex.value == 2:
            Log.ch.setLevel(logging.DEBUG)
            Log.fh.setLevel(logging.DEBUG)
            # Log.logger.setLevel(logging.DEBUG)
        return

    @staticmethod
    def Init():
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        ch.setFormatter(formatter)
        Log.ch = ch
        Log.logger.addHandler(ch)

        logPath = Setting.GetLogPath()
        if not os.path.isdir(logPath):
            os.makedirs(logPath)
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        logfile = os.path.join(logPath, day+".log")
        fh = logging.FileHandler(logfile, mode='a', encoding="utf-8")
        Log.fh = fh
        fh.setLevel(logging.INFO)
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

    @staticmethod
    def InstallFilter(stream2):
        class Stream2Handler(logging.StreamHandler):
            def __init__(self, stream=None):
                logging.StreamHandler.__init__(self, stream)

            def emit(self, record):
                """
                Emit a record.

                If a formatter is specified, it is used to format the record.
                The record is then written to the stream with a trailing newline.  If
                exception information is present, it is formatted using
                traceback.print_exception and appended to the stream.  If the stream
                has an 'encoding' attribute, it is used to determine how to do the
                output to the stream.
                """
                try:
                    msg = self.format(record)
                    stream = self.stream
                    # issue 35046: merged two stream.writes into one.
                    stream.write(record.levelno, msg + self.terminator)
                    self.flush()
                except RecursionError:  # See issue 36272
                    raise
                except Exception:
                    self.handleError(record)

        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", datefmt=logging.Formatter.default_time_format)
        ch = Stream2Handler(stream2)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        Log.logger.addHandler(ch)
