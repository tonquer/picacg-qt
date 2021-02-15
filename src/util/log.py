import os
import sys
import logging
import time


class Log(object):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    @staticmethod
    def Init():
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        Log.logger.addHandler(ch)

        if not os.path.isdir("logs"):
            os.mkdir("logs")
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        logfile = os.path.join("logs", day+".log")
        fh = logging.FileHandler(logfile, mode='a', encoding="utf-8")
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        Log.logger.addHandler(fh)

        return

    @staticmethod
    def Info(data):
        Log.logger.info(data)

    @staticmethod
    def Warn(data):
        Log.logger.warning(data)

    @staticmethod
    def Error(cur_tb, e):
        message = ''
        message += 'Exception: {}\n'.format(e)
        message += '  Traceback info: \n'
        while cur_tb is not None:
            frame = cur_tb.tb_frame
            code = frame.f_code
            message += '    File: {}, line: {}, in: {}\n'.format(code.co_filename, str(frame.f_lineno), code.co_name)
            message += '         local params:{}\n'.format(frame.f_locals)
            cur_tb = cur_tb.tb_next
        Log.logger.error(message)
