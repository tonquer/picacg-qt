# 目录管理
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
