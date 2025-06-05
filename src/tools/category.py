# 目录管理
from tools.langconv import Converter
from tools.log import Log
from tools.singleton import Singleton
from tools.tool import ToolUtil


class CateGoryBase(object):
    def __init__(self):
        self._id = ""            # 标识
        self.title = ""         # 标题
        self.description = ""          # 描述
        self.thumb = ""  # (fileServer, path, originalName)

    @property
    def id(self):
        return self._id


class CateGoryMgr(Singleton):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.idToCateGoryBase = []    # id: CateGoryBase
        self.allCategorise = \
            [
                    "嗶咔漢化",
                    "全彩",
                    "長篇",
                    "同人",
                    "短篇",
                    "圓神領域",
                    "碧藍幻想",
                    "CG雜圖",
                    "英語 ENG",
                    "生肉",
                    "純愛",
                    "百合花園",
                    "耽美花園",
                    "偽娘哲學",
                    "後宮閃光",
                    "扶他樂園",
                    "單行本",
                    "姐姐系",
                    "妹妹系",
                    "SM",
                    "性轉換",
                    "足の恋",
                    "人妻",
                    "NTR",
                    "強暴",
                    "非人類",
                    "艦隊收藏",
                    "Love Live",
                    "SAO 刀劍神域",
                    "Fate",
                    "東方",
                    "WEBTOON",
                    "禁書目錄",
                    "歐美",
                    "Cosplay",
                    "重口地帶",
        ]
        self.categoriseIndex = {}
        self.indexCategories = {}
        for index, v in enumerate(self.allCategorise):
            name = Converter('zh-hans').convert(v)
            self.categoriseIndex[name] = index+1
            self.indexCategories[index+1] = name

    @property
    def server(self):
        from server.server import Server
        return Server()

    def UpdateCateGoryBack(self, backData):
        for info in backData.res.data.get("categories", {}):
            if info.get("isWeb"):
                continue
            # 兼容下图片加载失败
            if info.get("thumb").get('fileServer') == "https://wikawika.xyz/static/":
                info["thumb"]["fileServer"] = 'https://storage1.picacomic.com'
            newInfo = CateGoryBase()
            ToolUtil.ParseFromData(newInfo, info)
            self.idToCateGoryBase.append(newInfo)
            # print("\""+newInfo.title+"\",", )
        Log.Info("初始化目录成功。。。")
        return
