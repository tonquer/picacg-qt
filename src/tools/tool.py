import hashlib
import hmac
import json
import os
import re
import time
import uuid
from hashlib import sha256
from urllib.parse import quote

from config import config
from config.setting import Setting
from tools.log import Log


class CTime(object):
    def __init__(self):
        self._t1 = time.time()

    def Refresh(self, clsName, des='', checkTime=100):
        t2 = time.time()
        diff = int((t2 - self._t1) * 1000)
        if diff >= checkTime:
            text = 'CTime2 consume:{} ms, {}.{}'.format(diff, clsName, des)
            Log.Warn(text)
        self._t1 = t2
        return diff


def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        rt = fn(*args, **kwargs)
        diff = int((time.time() - start) * 1000)
        if diff >= 50:
            clsName = args[0]
            strLog = 'time_me consume,{} ms, {}.{}'.format(diff, clsName, fn.__name__)
            Log.Warn(strLog)
        return rt
    return _wrapper


class ToolUtil(object):

    @staticmethod
    def DictToUrl(paramDict):
        assert isinstance(paramDict, dict)
        data = ''
        for k, v in paramDict.items():
            data += quote(str(k)) + '=' + quote(str(v))
            data += '&'
        return data.strip('&')
    
    @classmethod
    def GetHeader(cls, _url: str, method: str) -> dict:
        now = str(int(time.time()))
        nonce = str(uuid.uuid1()).replace("-", "")
        # nonce = "c74f6b365c8411eb97cf3c7c3f156854"

        datas = [
            config.Url, _url.replace(config.Url, ""),
            now,
            nonce,
            method,
            config.ApiKey,
            config.Version,
            config.BuildVersion
        ]
        _src = ToolUtil.__ConFromNative(datas)
        _key = ToolUtil.__SigFromNative()
        signature = ToolUtil.HashKey(_src, _key)

        header = {
            "api-key": config.ApiKey,
            "accept": config.Accept,
            "app-channel": config.AppChannel,
            "time": now,
            "app-uuid": config.Uuid,
            "nonce": nonce,
            "signature": signature,
            "app-version": config.Version,
            "image-quality": config.ImageQuality,
            "app-platform": config.Platform,
            "app-build-version": config.BuildVersion,
            "user-agent": config.Agent,
            "version": config.UpdateVersion,
        }
        if method.lower() in ["post", "put"]:
            header["Content-Type"] = "application/json; charset=UTF-8"

        return header

    @staticmethod
    def GetNewChatHeader():
        header = {
            "user-agent": "Dart/2.19 (dart:io)",
            "accept-encoding":"gzip",
            "api-version": "1.0.3",
            "content-type":"application/json; charset=UTF-8",
        }
        return header

    @staticmethod
    def __ConFromNative(datas):
        # 以下是IDA PRO反编译的混淆代码
        key = ""

        # v6 = datas[0]
        v37 = str(datas[1])
        v7 = str(datas[2])
        v35 = str(datas[3])
        v36 = str(datas[4])
        v8 = str(datas[5])
        # v9 = datas[6]
        # v10 = datas[7]
        # v33 = v9
        # v34 = v6

        key += v37
        key += v7
        key += v35
        key += v36
        key += v8
        return key

    @staticmethod
    def __SigFromNative():
        return '~d}$Q7$eIni=V)9\\RK/P.RM4;9[7|@/CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn'
        # 以下是IDA PRO反编译的混淆代码
        key = "~*}$#,$-\").=$)\",,#/-.'%(;$[,|@/&(#\"~%*!-?*\"-:*!!*,$\"%.&'*|%/*,*"
        key = list(key)
        # v5 = int[] 32bit
        # BYTE1(v5[0]) = 100;
        key[1] = chr(100)
        # LOWORD(v5[1]) = 14161;
        key[4:6] = list((14161).to_bytes(2, 'little').decode("utf-8"))
        # *(int *)((char *)&v5[1] + 3) = 1768835429;
        key[7:11] = list((1768835429).to_bytes(4, 'little').decode("utf-8"))
        # LOBYTE(v5[3]) = 86;
        key[12] = chr(86)
        # HIBYTE(v5[4]) = 80;
        key[20 - 1] = chr(80)
        # qmemcpy((char *)&v5[5] + 1, "RM4", 3);
        key[20 + 1:20 + 1 + 3] = list("RM4")
        # qmemcpy((char *)&v5[7] + 3, "CA}b", sizeof(int));
        key[28 + 3:28 + 3 + 4] = list("CA}b")
        # LOWORD(v5[9]) = 22351;
        key[36:38] = list((22351).to_bytes(2, 'little').decode("utf-8"))
        # qmemcpy((char *)&v5[10] + 1, "EV`", 3);
        key[40 + 1:40 + 1 + 3] = list("EV`")
        # qmemcpy((char *)&v5[11] + 1, "<>M7pddUBL5n", 12);
        key[44 + 1:44 + 1 + 12] = list("<>M7pddUBL5n")
        # *(_WORD *)((char *)&v5[15] + 1) = 28227;
        key[60 + 1:63] = list((28227).to_bytes(2, 'little').decode("utf-8"))
        # qmemcpy((char *)&v5[3] + 2, "9\\RK", sizeof(int))
        key[12 + 2:12 + 2 + 4] = list("9\\RK")
        # BYTE1(v5[6]) = 57;
        key[24 + 1] = chr(57)
        # HIBYTE(v5[6]) = 55;
        key[28 - 1] = chr(55)
        # HIBYTE(v5[9]) = 51;
        key[40 - 1] = chr(51)
        # BYTE2(v5[14]) = 48;
        key[56 + 2] = chr(48)
        return "".join(key)

    @staticmethod
    def HashKey(src, key):
        appsecret = key.encode('utf-8')  # 秘钥
        data = src.lower().encode('utf-8')  # 数据
        signature = hmac.new(appsecret, data, digestmod=sha256).hexdigest()
        return signature

    @staticmethod
    def ParseFromData(desc, src):
        try:
            if not src:
                return
            if isinstance(src, str):
                src = json.loads(src)
            for k, v in src.items():
                setattr(desc, k, v)
        except Exception as es:
            Log.Error(src)

    @staticmethod
    def GetCodeErrMsg(code):
        msg = ""
        if code == "1029":
            msg = "你所在的時間線與我們有所不同請你調整一下再嘗試吧！"
        if code == "1026":
            msg = "嗶咔娘認定你的是假冒電郵！！"
        elif code == "1025":
            msg = "嗶咔是註冊商標，不能用的。"
        elif code == "1024":
            msg = "我們不支授此郵箱...QQ和163電郵君不想跟我們做朋友，所以請你用其他電郵服務商吧。例如：Gmail, Yahoo 和 Outlook"
        elif code == "1023":
            msg = "吼！你的要求太多了！有問題你直接找團長吧！"
        elif code == "1019":
            msg = """小紳紳的等級不夠或者沒有認證帳戶！

認證了的帳戶等級2才能留言唷～

你可以打嗶卡和更換頭像升等級的～"""
        elif code == "1014":
            msg = "這個本子好像正在審核過程當中..？請待會再來吧！"
        elif code == "1010":
            msg = "你輸入的帳戶資料並不正確哦，請重新輸入！"
        elif code == "1009":
            msg = """這個匿稱已經屬於一位紳士
請使用別的匿稱！"""
        elif code == "1008":
            msg = """這個嗶咔帳號已經被註冊！

如果你忘記了密碼，請回上一頁按忘記密碼！"""
        elif code == "1007":
            msg = """欸...!?

404 找不到"""
        elif code == "1006":
            msg = """這個帳戶還沒有被激活！

請前往你註冊的郵箱並找尋【嗶咔邀請函】（有機會在垃圾郵件中）！

如找不到邀請函郵件，請按下方的重新發送邀請函！"""
        elif code == "1005":
            msg = ""
        elif code == "1004":
            msg = "你輸入的帳戶資料並不正確哦，請重新輸入！"
        elif code == "1002":
            msg = """欸...!?
為什麼呢？
認證好像有點問題...

再試試看吧"""
        return msg

    @staticmethod
    def GetUrlHost(url):
        host = url.replace("https://", "")
        host = host.replace("http://", "")
        host = host.split("/")[0]
        return host

    @staticmethod
    def GetDateStr(createdTime):
        timeArray = time.strptime(createdTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        tick = int(time.mktime(timeArray)-time.timezone)
        now = int(time.time())
        day = int((int(now - time.timezone) / 86400) - (int(tick - time.timezone) / 86400))
        return time.localtime(tick), day

    @staticmethod
    def GetUpdateStr(createdTime):
        if not createdTime:
            return ""
        timeArray = time.strptime(createdTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        tick = int(time.mktime(timeArray)-time.timezone)
        return ToolUtil.GetUpdateStrByTick(tick)

    @staticmethod
    def GetUpdateStrByTick(tick):
        now = int(time.time())
        day = (now - tick) // (24*3600)
        hour = (now - tick) // 3600
        minute = (now - tick) // 60
        second = (now - tick)

        from tools.str import Str
        if day > 0:
            return "{}".format(day) + Str.GetStr(Str.DayAgo)
        elif hour > 0:
            return "{}".format(hour) + Str.GetStr(Str.HourAgo)
        elif minute > 0:
            return "{}".format(minute) + Str.GetStr(Str.MinuteAgo)
        else:
            return "{}".format(second) + Str.GetStr(Str.SecondAgo)

    @staticmethod
    def GetDownloadSize(downloadLen):
        kb = downloadLen / 1024.0
        if kb <= 0.1:
            size = str(downloadLen) + "bytes"
        else:
            mb = kb / 1024.0
            if mb <= 0.1:
                size = str(round(kb, 2)) + "kb"
            else:
                size = str(round(mb, 2)) + "mb"
        return size

    @staticmethod
    def GetLookScaleModel(category, w, h, mat="jpg"):
        data = ToolUtil.GetModelByIndex(Setting.LookNoise.value, Setting.LookScale.value, ToolUtil.GetLookModel(category), mat)
        # 放大倍数不能过大，如果图片超过4k了，QImage无法显示出来，bug
        if min(w, h) > 3000:
            data["scale"] = 1
        elif min(w, h) > 2000:
            data["scale"] = 1.5
        return data

    @staticmethod
    def GetDownloadScaleModel(w, h, mat):
        dot = w * h
        # 条漫不放大
        if not config.CanWaifu2x:
            return {}
        return ToolUtil.GetModelByIndex(Setting.DownloadNoise.value, Setting.DownloadScale.value, Setting.DownloadModel.value, mat)

    @staticmethod
    def GetAnimationFormat(data):
        try:
            from PIL import Image
            from io import BytesIO
            a = BytesIO(data)
            img = Image.open(a)

            format = ""
            if getattr(img, "is_animated", ""):
                format = img.format
            a.close()
            return format
        except Exception as es:
            Log.Error(es)
        return ""

    @staticmethod
    def GetPictureSize(data):
        if not data:
            return 0, 0, "jpg", False
        try:
            from PIL import Image
            from io import BytesIO
            a = BytesIO(data)
            img = Image.open(a)
            isAnima = getattr(img, "is_animated", False)
            if img.format == "PNG":
                mat = "png"
            elif img.format == "GIF":
                mat = "gif"
            elif img.format == "WEBP":
                mat = "webp"
            else:
                mat = "jpg"
            a.close()
            return img.width, img.height, mat, isAnima
        except Exception as es:
            Log.Error(es)
        return 0, 0, "jpg", False

    @staticmethod
    def GetLookModel(category):
        if Setting.LookModel.value == 0:
            if "Cosplay" in category or "cosplay" in category or "CosPlay" in category or "COSPLAY" in category:
                return 2
            return 3
        else:
            return Setting.LookModel.value

    @staticmethod
    def GetModelAndScale(model):
        if not model:
            return "cunet", 1, 1
        index = model.get('index', 0)
        scale = model.get('scale', 0)
        noise = model.get('noise', 0)
        if index == 0:
            model = "anime_style_art_rgb"
        elif index == 1:
            model = "cunet"
        elif index == 2:
            model = "photo"
        else:
            model = "anime_style_art_rgb"
        return model, noise, scale

    @staticmethod
    def GetModelByIndex(noise, scale, index, mat="jpg"):
        if not config.CanWaifu2x:
            return {}
        if noise < 0:
            noise = 3
        data = {"format": mat, "noise": noise, "scale": scale, "index": index}
        from waifu2x_vulkan import waifu2x_vulkan
        if index == 0:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_ANIME_STYLE_ART_RGB_NOISE"+str(noise))
        elif index == 1:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_CUNET_NOISE"+str(noise))
        elif index == 2:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_PHOTO_NOISE" + str(noise))
        elif index == 3:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_ANIME_STYLE_ART_RGB_NOISE"+str(noise))
        else:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_CUNET_NOISE"+str(noise))
        return data

    @staticmethod
    def GetCanSaveName(name):
        return re.sub('[\\\/:*?"<>|\0\r\n]', '', name).rstrip(".").strip(" ")

    @staticmethod
    def LoadCachePicture(filePath):
        try:
            c = CTime()
            if not os.path.isfile(filePath):
                return None
            with open(filePath, "rb") as f:
                data = f.read()
                c.Refresh("LoadCache", filePath)
                return data
        except Exception as es:
            Log.Error(es)
        return None

    @staticmethod
    def IsHaveFile(filePath):
        try:
            if os.path.isfile(filePath):
                return True
            return False
        except Exception as es:
            Log.Error(es)
        return False

    @staticmethod
    def DiffDays(d1, d2):
        return (int(d1 - time.timezone) // 86400) - (int(d2 - time.timezone) // 86400)

    @staticmethod
    def GetCurZeroDatatime(tick):
        from datetime import timedelta
        from datetime import datetime
        now = datetime.fromtimestamp(tick)
        delta = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        zeroDatetime = now - delta
        return int(time.mktime(zeroDatetime.timetuple()))

    @staticmethod
    def GetTimeTickEx(strDatetime):
        if not strDatetime:
            return 0
        timeArray = time.strptime(strDatetime, "%Y-%m-%d %H:%M:%S")
        tick = int(time.mktime(timeArray))
        return tick

    @staticmethod
    def Escape(s):
        s = s.replace("&", "&amp;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
        s = s.replace('\n', '<br/>')
        s = s.replace('  ', '&nbsp;')
        s = s.replace(' ', '&emsp;')
        return s

    @staticmethod
    def GetPictureFormat(data):
        import imghdr
        mat = imghdr.what(None, data)
        if mat:
            return mat
        return "jpg"

    @staticmethod
    def GetStrMaxLen(str, maxLen=6):
        if len(str) > maxLen:
            return str[:maxLen] + "..."
        else:
            return str

    @staticmethod
    def GetRealUrl(url, path):
        if path:
            if url[-7:] != "static/":
                return url + "/static/" + path
            else:
                return url + path
        else:
            return url

    @staticmethod
    def GetRealPath(path, direction):
        if path:
            data = "{}/{}".format(direction, path)
            if ".jpg" not in data:
                return data + ".jpg"
            else:
                return data
        else:
            return path

    @staticmethod
    def GetMd5RealPath(path, direction):
        if path:
            a = hashlib.md5(path.encode("utf-8")).hexdigest()
            return "{}/{}.jpg".format(direction, a)
        else:
            return path

    @staticmethod
    def SaveFile(data, filePath):
        if not data:
            return
        if not filePath:
            return

        try:
            fileDir = os.path.dirname(filePath)

            if not os.path.isdir(fileDir):
                os.makedirs(fileDir)

            with open(filePath, "wb+") as f:
                f.write(data)

            Log.Debug("add chat cache, cachePath:{}".format(filePath))

        except Exception as es:
            Log.Error(es)