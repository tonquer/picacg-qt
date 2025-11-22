import hashlib
import hmac
import io
import json
import os
import re
import time
import uuid
from hashlib import sha256
from urllib.parse import quote

from lxml import etree

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
        data = ToolUtil.GetModelByIndex(Setting.LookModelName.value, Setting.LookScale.value, mat)
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
        return ToolUtil.GetModelByIndex(Setting.DownloadModelName.value, Setting.DownloadScale.value, mat)

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

    # @staticmethod
    # def GetLookModel(category):
    #     if Setting.LookModel.value == 0:
    #         if "Cosplay" in category or "cosplay" in category or "CosPlay" in category or "COSPLAY" in category:
    #             return 2
    #         return 3
    #     else:
    #         return Setting.LookModel.value

    # @staticmethod
    # def GetModelAndScale(model):
    #     if not model:
    #         return "cunet", 1, 1
    #     index = model.get('index', 0)
    #     scale = model.get('scale', 0)
    #     noise = model.get('noise', 0)
    #     if index == 0:
    #         model = "anime_style_art_rgb"
    #     elif index == 1:
    #         model = "cunet"
    #     elif index == 2:
    #         model = "photo"
    #     else:
    #         model = "anime_style_art_rgb"
    #     return model, noise, scale

    @staticmethod
    def GetModelByIndex(modelName, scale, mat="jpg"):
        if not config.CanWaifu2x:
            return {}
        data = {"scale": scale}
        from sr_vulkan import sr_vulkan as sr
        data["model"] = getattr(sr, modelName, 0)
        data["model_name"] = modelName
        return data
    
    @staticmethod
    def GetShowModelName(name):
        if "WAIFU2X_CUNET" in name:
            return "Waifu2x(cunet)"
        elif "WAIFU2X_ANIME" in name:
            return "Waifu2x(anime)"
        elif "WAIFU2X_PHOTO" in name:
            return "Waifu2x(photo)"
        elif "REALCUGAN_PRO" in name:
            return "Realcugan(pro)"
        elif "REALCUGAN_SE" in name:
            return "Realcugan(se)"
        elif "REALSR" in name:
            return "RealSR"
        elif "REALESRGAN_X4PLUSANIME" in name:
            return "X4plusAnime"
        elif "REALESRGAN_X4PLUS" in name:
            return "X4Plus"
        elif "REALESRGAN_ANIMAVIDEOV3" in name:
            return "AnimaVideoV3"
        return name
    
    @staticmethod
    def GetCanSaveName(name):
        # 限制文件夹名称为255/3的长度
        return (str(re.sub('[\\\/:*?"<>|\0\t\r\n]', '', name))[:254//3-1]).rstrip(".").strip(" ")

    @staticmethod
    def LoadCachePicture(filePath):
        """
        加载图片文件（带内存缓存）

        优化说明：
        1. 先查内存缓存，命中则直接返回（速度提升5-10倍）
        2. 未命中则从磁盘读取并加入缓存
        3. 使用LRU策略自动管理缓存
        """
        try:
            # 先查内存缓存
            from tools.image_cache import get_image_cache
            cache = get_image_cache()

            cached_data = cache.get(filePath)
            if cached_data is not None:
                # 缓存命中，直接返回
                return cached_data

            # 缓存未命中，从磁盘读取
            c = CTime()
            if not os.path.isfile(filePath):
                return None

            with open(filePath, "rb") as f:
                data = f.read()
                c.Refresh("LoadCache", filePath)

                # 加入内存缓存
                cache.put(filePath, data)

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

    @staticmethod
    def GetComicInfoXml(epsId, picNum, bookInfo):
        from lxml import etree
        from tools.book import Book
        assert isinstance(bookInfo, Book)
        root = etree.Element("ComicInfo")

        title = etree.SubElement(root, "Title")  # 标题
        title.text = bookInfo.title

        publish = etree.SubElement(root, "Publisher")  # 标题
        publish.text = config.ProjectName

        writer = etree.SubElement(root, "Writer")  # 作者
        writer.text = bookInfo.author

        desc = etree.SubElement(root, "Summary")  # 摘要
        desc.text = bookInfo.description

        bookId = etree.SubElement(root, "BookId")  # 当前章节
        bookId.text = str(bookInfo.id)

        series = etree.SubElement(root, "Series")  # 当前章节
        series.text = str(bookInfo.title)

        number = etree.SubElement(root, "Number")  # 当前章节
        number.text = str(epsId+1)

        count = etree.SubElement(root, "Count")  # 总章节
        count.text = str(bookInfo.epsCount)
        if bookInfo.created_at:
            timeArray = time.strptime(bookInfo.created_at, "%Y-%m-%dT%H:%M:%S.%f%z")
            year = etree.SubElement(root, "Year")  # 年
            year.text = str(timeArray.tm_year)
            month = etree.SubElement(root, "Month")  # 月
            month.text = str(timeArray.tm_mon)
            day = etree.SubElement(root, "Day")  # 日
            day.text = str(timeArray.tm_mday)

        genre = etree.SubElement(root, "Genre")  # 分类
        genre.text = ",".join(bookInfo.categories)

        tags = etree.SubElement(root, "Tags")
        tags.text = ",".join(bookInfo.tags)

        everyoneTags = ["无h", "無h"]
        isNotH = ToolUtil.IsHaveAssignTag(tags, everyoneTags)
        ageRating = etree.SubElement(root, "AgeRating")  # R18+  Everyone
        if isNotH:
            ageRating.text = "Everyone"
        else:
            ageRating.text = "R18+"

        pageCount = etree.SubElement(root, "PageCount")  # ue
        pageCount.text = str(picNum)

        blackAndWhite = etree.SubElement(root, "BlackAndWhite")  # Yes No
        everyoneTags = ["全彩", "cosplay"]
        isColor = ToolUtil.IsHaveAssignTag(bookInfo.tags, everyoneTags)
        if isColor:
            blackAndWhite.text = "No"
        else:
            blackAndWhite.text = "Yes"

        manga = etree.SubElement(root, "Manga")  # Yes No
        everyoneTags = ["cosplay"]
        isCos = ToolUtil.IsHaveAssignTag(bookInfo.tags, everyoneTags)
        if isCos:
            manga.text = "No"
        else:
            manga.text = "Yes"

        tree = etree.ElementTree(root)
        buffer = io.BytesIO()
        tree.write(buffer, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        data = buffer.getvalue()
        buffer.close()
        return data

    @staticmethod
    def IsHaveAssignTag(tagList, assignList):
        isHave = False
        for tag in tagList:
            for noHtag in assignList:
                if noHtag.lower() in tag.lower():
                    isHave = True
                    break
        return  isHave

    @staticmethod
    def IsipAddress(hostname) -> bool:
        if isinstance(hostname, bytes):
            # IDN A-label bytes are ASCII compatible.
            hostname = hostname.decode("ascii")
        _IPV4_PAT = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
        _IPV4_RE = re.compile("^" + _IPV4_PAT + "$")
        _HEX_PAT = "[0-9A-Fa-f]{1,4}"
        _LS32_PAT = "(?:{hex}:{hex}|{ipv4})".format(hex=_HEX_PAT, ipv4=_IPV4_PAT)
        _subs = {"hex": _HEX_PAT, "ls32": _LS32_PAT}
        _variations = [
            #                            6( h16 ":" ) ls32
            "(?:%(hex)s:){6}%(ls32)s",
            #                       "::" 5( h16 ":" ) ls32
            "::(?:%(hex)s:){5}%(ls32)s",
            # [               h16 ] "::" 4( h16 ":" ) ls32
            "(?:%(hex)s)?::(?:%(hex)s:){4}%(ls32)s",
            # [ *1( h16 ":" ) h16 ] "::" 3( h16 ":" ) ls32
            "(?:(?:%(hex)s:)?%(hex)s)?::(?:%(hex)s:){3}%(ls32)s",
            # [ *2( h16 ":" ) h16 ] "::" 2( h16 ":" ) ls32
            "(?:(?:%(hex)s:){0,2}%(hex)s)?::(?:%(hex)s:){2}%(ls32)s",
            # [ *3( h16 ":" ) h16 ] "::"    h16 ":"   ls32
            "(?:(?:%(hex)s:){0,3}%(hex)s)?::%(hex)s:%(ls32)s",
            # [ *4( h16 ":" ) h16 ] "::"              ls32
            "(?:(?:%(hex)s:){0,4}%(hex)s)?::%(ls32)s",
            # [ *5( h16 ":" ) h16 ] "::"              h16
            "(?:(?:%(hex)s:){0,5}%(hex)s)?::%(hex)s",
            # [ *6( h16 ":" ) h16 ] "::"
            "(?:(?:%(hex)s:){0,6}%(hex)s)?::",
        ]
        _IPV6_PAT = "(?:" + "|".join([x % _subs for x in _variations]) + ")"
        _UNRESERVED_PAT = r"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._\-~"
        _ZONE_ID_PAT = "(?:%25|%)(?:[" + _UNRESERVED_PAT + "]|%[a-fA-F0-9]{2})+"
        _IPV6_ADDRZ_PAT = r"\[" + _IPV6_PAT + r"(?:" + _ZONE_ID_PAT + r")?\]"
        _BRACELESS_IPV6_ADDRZ_RE = re.compile("^" + _IPV6_ADDRZ_PAT[2:-2] + "$")
        return bool(_IPV4_RE.match(hostname) or _BRACELESS_IPV6_ADDRZ_RE.match(hostname))

    @staticmethod
    def HasIpv6() -> bool:
        """Returns True if the system can bind an IPv6 address."""
        host = "::1"
        sock = None
        has_ipv6 = False
        import socket
        if socket.has_ipv6:
            # has_ipv6 returns true if cPython was compiled with IPv6 support.
            # It does not tell us if the system has IPv6 support enabled. To
            # determine that we must bind to an IPv6 address.
            # https://github.com/urllib3/urllib3/pull/611
            # https://bugs.python.org/issue658327
            try:
                sock = socket.socket(socket.AF_INET6)
                sock.bind((host, 0))
                has_ipv6 = True
            except Exception:
                pass

        if sock:
            sock.close()
        return has_ipv6