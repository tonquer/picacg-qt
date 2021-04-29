import json
import os
import time
import uuid

import hmac
from hashlib import sha256

from src.util import Log
from conf import config




class CTime(object):
    def __init__(self):
        self._t1 = time.time()

    def Refresh(self, clsName, des='', checkTime=100):
        t2 = time.time()
        diff = int((t2 - self._t1) * 1000)
        if diff >= checkTime:
            text = 'CTime2 consume:{} ms, {}.{}'.format(diff, clsName, des)
            Log.Warn(text)
            # 超过0.5秒超时写入数据库
        self._t1 = t2
        return diff


def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        rt = fn(*args, **kwargs)
        diff = int((time.time() - start) * 1000)
        if diff >= 100:
            clsName = args[0]
            strLog = 'time_me consume,{} ms, {}.{}'.format(diff, clsName, fn.__name__)
            # Log.w(strLog)
            Log.Warn(strLog)
        return rt
    return _wrapper


class ToolUtil(object):
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
        }
        return header

    @staticmethod
    def __ConFromNative(datas):
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
            if isinstance(src, str):
                src = json.loads(src)
            for k, v in src.items():
                setattr(desc, k, v)
        except Exception as es:
            Log.Error(es)

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
    def GetScaleAndNoise(w, h):
        dot = w * h
        # 条漫不放大
        if max(w, h) >= 2561:
            return 1, 3
        if dot >= 1920 * 1440:
            return 2, 3
        if dot >= 1920 * 1080:
            return 2, 3
        elif dot >= 720 * 1080:
            return 2, 3
        elif dot >= 240 * 720:
            return 2, 3
        else:
            return 2, 3

    @staticmethod
    def GetLookScaleModel(w, h, category):
        dot = w * h
        # 条漫不放大

        if max(w, h) >= 2561:
            return ToolUtil.GetModelByIndex(0)
        return ToolUtil.GetModelByIndex(ToolUtil.GetLookModel(category))

    @staticmethod
    def GetDownloadScaleModel(w, h):
        dot = w * h
        # 条漫不放大
        if not config.CanWaifu2x:
            return {}
        import waifu2x
        if max(w, h) >= 2561:
            return {"model": waifu2x.MODEL_ANIME_STYLE_ART_RGB_NOISE3, "scale": 1, "index": 0}
        return ToolUtil.GetModelByIndex(config.DownloadModel)

    @staticmethod
    def GetPictureFormat(data):
        if data[:8] == b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a":
            return "png"
        elif data[:2] == b"\xff\xd8":
            return "jpg"
        return "jpg"

    @staticmethod
    def GetPictureSize(data):
        from PIL import Image
        from io import BytesIO
        a = BytesIO(data)
        img = Image.open(a)
        a.close()
        return img.width, img.height
        # picFormat = ToolUtil.GetPictureFormat(data)
        # weight, height = 1, 1
        # if picFormat == "png":
        #     # head = 8 + 4 + 4
        #     data2 = data[16:24]
        #     weight = int.from_bytes(data2[:4], byteorder='big', signed=False)
        #     height = int.from_bytes(data2[5:], byteorder='big', signed=False)
        # elif picFormat == "jpg":
        #     size = min(1000, len(data))
        #
        #     index = 0
        #     while index < size:
        #         if data[index] == 255:
        #             index += 1
        #             if 192 <= data[index] <= 206:
        #                 index += 4
        #                 if index + 4 >= size:
        #                     continue
        #                 height = int.from_bytes(data[index:index + 2], byteorder='big', signed=False)
        #                 weight = int.from_bytes(data[index + 2:index + 4], byteorder='big', signed=False)
        #                 break
        #             else:
        #                 continue
        #         index += 1
        # return weight, height

    @staticmethod
    def GetDataModel(data):
        picFormat = ToolUtil.GetPictureFormat(data)
        if picFormat == "png":
            IDATEnd = 8 + 25
            dataSize = int.from_bytes(data[IDATEnd:IDATEnd + 4], byteorder="big", signed=False)
            if dataSize >= 10:
                return ""
            dataType = data[IDATEnd + 4:IDATEnd + 8]
            if dataType == b"tEXt":
                return data[IDATEnd + 8:IDATEnd + 8 + dataSize].decode("utf-8")
            return ""
        elif picFormat == "jpg":
            if data[:4] != b"\xff\xd8\xff\xe0":
                return ""
            size = int.from_bytes(data[4:6], byteorder="big", signed=False)
            if size >= 100:
                return ""
            if data[4 + size:4 + size + 2] != b"\xff\xfe":
                return
            size2 = int.from_bytes(data[4 + size + 2:4 + size + 2 + 2], byteorder="big", signed=False) - 2
            if size2 >= 100:
                return
            return data[4 + size2 + 2 + 2:4 + size2 + 2 + 2 + size2].decode("utf-8")
        return ""

    @staticmethod
    def GetLookModel(category):
        if config.LookModel == 0:
            if "Cosplay" in category or "cosplay" in category or "CosPlay" in category or "COSPLAY" in category:
                return 2
            return 3
        else:
            return config.LookModel

    @staticmethod
    def GetDownloadModel():
        if config.DownloadModel == 0:
            return config.Model1
        return getattr(config, "Model"+str(config.DownloadModel), config.Model1)

    @staticmethod
    def GetModelAndScale(model):
        if not model:
            return 0, 1, 1
        model = model.get('index', 0)
        if model == 0:
            return 0, 3, 1
        elif model == 1:
            return 1, 3, 2
        elif model == 2:
            return 2, 3, 2
        elif model == 3:
            return 3, 3, 2
        return 0, 1, 1

    @staticmethod
    def GetModelByIndex(index):
        if not config.CanWaifu2x:
            return {}
        import waifu2x
        if index == 0:
            return {"model": waifu2x.MODEL_CUNET_NO_SCALE_NOISE3, "scale": 1, "index": index}
        elif index == 1:
            return {"model": waifu2x.MODEL_CUNET_NOISE3, "scale": 2, "index": index}
        elif index == 2:
            return {"model": waifu2x.MODEL_PHOTO_NOISE3, "scale": 2, "index": index}
        elif index == 3:
            return {"model": waifu2x.MODEL_ANIME_STYLE_ART_RGB_NOISE3, "scale": 2, "index": index}
        return {"model": waifu2x.MODEL_CUNET_NOISE3, "scale": 2, "index": index}

    @staticmethod
    def GetCanSaveName(name):
        return name.replace("/", "").replace("|", "").replace("*", "").\
            replace("\\", "").replace("?", "").replace(":", "").replace("*", "").\
            replace("<", "").replace(">", "").replace("\"", "").replace(" ", "")

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
