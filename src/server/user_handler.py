import json
import os
import pickle
import re
import time

from config import config
from task.qt_task import TaskBase
from tools.log import Log
from tools.status import Status
from tools.tool import ToolUtil
from tools.user import User
from . import req
from .server import handler, Server

SpacePic = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xe2\x01\xd8ICC_PROFILE\x00\x01\x01\x00\x00\x01\xc8\x00\x00\x00\x00\x040\x00\x00mntrRGB XYZ \x07\xe0\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00acsp\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\xf6\xd6\x00\x01\x00\x00\x00\x00\xd3-\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\tdesc\x00\x00\x00\xf0\x00\x00\x00$rXYZ\x00\x00\x01\x14\x00\x00\x00\x14gXYZ\x00\x00\x01(\x00\x00\x00\x14bXYZ\x00\x00\x01<\x00\x00\x00\x14wtpt\x00\x00\x01P\x00\x00\x00\x14rTRC\x00\x00\x01d\x00\x00\x00(gTRC\x00\x00\x01d\x00\x00\x00(bTRC\x00\x00\x01d\x00\x00\x00(cprt\x00\x00\x01\x8c\x00\x00\x00<mluc\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x0cenUS\x00\x00\x00\x08\x00\x00\x00\x1c\x00s\x00R\x00G\x00BXYZ \x00\x00\x00\x00\x00\x00o\xa2\x00\x008\xf5\x00\x00\x03\x90XYZ \x00\x00\x00\x00\x00\x00b\x99\x00\x00\xb7\x85\x00\x00\x18\xdaXYZ \x00\x00\x00\x00\x00\x00$\xa0\x00\x00\x0f\x84\x00\x00\xb6\xcfXYZ \x00\x00\x00\x00\x00\x00\xf6\xd6\x00\x01\x00\x00\x00\x00\xd3-para\x00\x00\x00\x00\x00\x04\x00\x00\x00\x02ff\x00\x00\xf2\xa7\x00\x00\rY\x00\x00\x13\xd0\x00\x00\n[\x00\x00\x00\x00\x00\x00\x00\x00mluc\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x0cenUS\x00\x00\x00 \x00\x00\x00\x1c\x00G\x00o\x00o\x00g\x00l\x00e\x00 \x00I\x00n\x00c\x00.\x00 \x002\x000\x001\x006\xff\xdb\x00C\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\xff\xdb\x00C\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\xff\xc0\x00\x11\x08\x00]\x00\x9c\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1d\x00\x01\x01\x01\x00\x02\x03\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x07\x08\t\x03\x04\x05\n\x02\xff\xc4\x006\x10\x00\x00\x05\x04\x00\x03\x05\x07\x03\x04\x03\x01\x00\x00\x00\x00\x02\x03\x04\x05\x06\x00\x01\x07\x08\tV\x96\x12\x14\x17\xd4\xd7\x1167uv\xb5\xb6\x13\x15!\x16\x181A"2BQ\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xfd\xd4F\xa3L\xb2\xf6V\xc9\\\xad\xb1\x04\x91\xc2H\x81\x1b\xc9e\xbc\xa3!\xc1\x0bB\x17\x02\x02\xb1\xbd\xad\xad\xbd`T$DZ$\x8a\x00Q\xe7\x94\x0b\xaaZ\xaa\xeaT\xaaRp\x8e\xb5\x82\x1fw\xc3\x8cy\xc8p\xce\x97c\xf24\x0f\x0e1\xe7!\xc3:]\x8f\xc8\xd0<8\xc7\x9c\x87\x0c\xe9v?#@\xf0\xe3\x1er\x1c3\xa5\xd8\xfc\x8d\x03\xc3\x8cy\xc8p\xce\x97c\xf24\x0f\x0e1\xe7!\xc3:]\x8f\xc8\xd0<8\xc7\x9c\x87\x0c\xe9v?#@\xf0\xe3\x1er\x1c3\xa5\xd8\xfc\x8d\x03\xc3\x8cy\xc8p\xce\x97c\xf24\x0f\x0e1\xe7!\xc3:]\x8f\xc8\xd0<8\xc7\x9c\x87\x0c\xe9v?#@\xf0\xe3\x1er\x1c3\xa5\xd8\xfc\x8d\x03\xc3\x8cy\xc8p\xce\x97c\xf24\x0f\x0e1\xe7!\xc3:]\x8f\xc8\xd0<8\xc7\x9c\x87\x0c\xe9v?#@\xf0\xe3\x1er\x1c3\xa5\xd8\xfc\x8d\x03\xc3\x8cy\xc8p\xce\x97c\xf24\x0f\x0e`\x16\xfeJ\x85\xc5\xd2\x8f\xff\x00\'\xa1cn@\xa4\x17\xff\x00\xe9J\x91\'!IB\xb7\xf9\xb0\x8b4\x02\xb5\xedk\xda\xf6\xbd\xad{\x07\xa4\xce\xf8&\xa3\x9e\xd8\xd7\xa8=m\x98\xdd\xfb\x92\x05\x8a\xcd4\xe5g7)jkwHZ\xa3\xee\x03\xcdPr\x1b9\x89\xb7\xbd\xa94\xc5\x8b\x0bDZ\xb5\x86\x1a\xa4\xf3M\x18{\xb8\xe3\xe1\xe4\x0f\xe8\xc8\xbf\xd8\xd0\xd0Y\xd0(\x14\n\x05\x02\x81@\xa0P(\x14\n\x05\x02\x81@\xa0P(1\x85\xde\xf3K\xfer\x83\xf1H\xdd\x05\xa68\xf8y\x03\xfa2/\xf644\x16t\n\x05\x02\x81@\xa0P(\x14\n\x05\x02\x81@\xa0P(\x14\n\x0caw\xbc\xd2\xff\x00\x9c\xa0\xfcR7Ai\x8e>\x1e@\xfe\x8c\x8b\xfd\x8d\r\x05\x9d\x02\x81@\xa0P(\x14\n\x05\x02\x81@\xa0P(?\x93\x0c\x01@\x19\xa6\x8c\x05\x96X\x04a\x86\x18+\x00\x05\x80\x16\xb8\x861\x8cW\xb0B\x00\x86\xd7\x10\x84+\xda\xc1\xb5\xaf{\xde\xd6\xb5\x04\x9c\x17 \xc0\xb2\x8ca\xbeo\x8c\xe6\xf1\x0c\x8b\x0cw\x1a\xd2\xda\xa5\xd0Y+4\xba0\xe66\xe5\xca\x1b\x1c\x00\xde\xff\x00\x1fZ\xe0\xd4\xb4h\x1c\x91\xaboZ\x14\xca\xcd\xbaU\xc9T$>\xc5\x9eA\xa5\x84+\xa8\x14\x18\xc2\xefy\xa5\xff\x009A\xf8\xa4n\x82\xd3\x1c|<\x81\xfd\x19\x17\xfb\x1a\x1a\x0b:\x05\x07\xe4\x8e<\xa2\x7f\xad[\xdf\xc4\x9b\x88\x94\x00\xc9\x13\xf4K\x05\xed\xd3^;\xda\xfc^\xca\x15K\x8c\x99\xeb\x1c\xc3\x1c\xc3\xd6:MYZ\x8b\xb1\xa4\x9b*\xc1\xf2[\x15\x90\x08\xb5\x89$\xe7\x08\xd7\xf5*\x11\xb9"N\x13\x00\xa8;4\xdf\xd9\\nw\xb1\xdc\x17\xa6\xd0\xd7\xb6\xe9$J]\xb6.2H\xcc\x85\xa1H\x15\xb5\xbd\xb0\xbdaW\xe7\x16\xa7V\xf5E\xde\xe0=\x1a\xf4*\x08R\x9c\xd0\xff\x00\xd8\xb3\x03{\xda\xd7\xf6\xda\xc1\xc9=\xa5\xe2g\x83\xb5\x87\'6\xe0\xa4X\xefb6s>\xaac*\\\xef\x83u#\x12+\xcc\xf9*\x1d\x07<"\xb2y\xac\xcd\xb4\x0e\xf1\xe6\x96\x163\xd4\x89\nR\x889\xe8\xd7\xf1\xfe\xee\xd0\xbe\xcc\x9f\xb3\xaf%\xca\xe1\xe1\xc3\xbcN\xb0vv\xc3\xb9\xb7%c\x8cm\xb1\xce\xb9\x1b]\x82i9{RUb\x05\x8d\xfbq\x15y\xba\xb5i\xdb\xa3\x9e\x12)w\nGw\xb7\xa2Q\x9e\xb5\xb0\x96YK\x82+\x16Y\xc8\\\x177\xbd\xa3^\xd4\x908\x99\xc2#\x89VX\xdc\x14\x92\xe8>d\xc2\xdbR99Y\x1f:;\xb5\xe7)V\x03\x8f\xc1p\x0b\x1c:?8\x02(\x9e\x1bW7\x8e-D\x909N"\xd0\xbc\x96Gh\xfa\xe6%\xcf7\\\xd2\xebgi\x1b\xa2\xc4\xa6,<5\x0e<%\xa4;\x85\xbe\xc7\x94\xbe\xe5\xd9\x01\xaa\xb1\x19kni\xb7 \xab$\x1eg\x80\x05M\xcc:\xc3.\xe4\x97bn;\x8c\xdb\x18\x0b\x96\x1fh\xec0\xfb;V\x0coN4\xcf\x80\xecO8c\t\xb6\xa4>ks\xf6\xc9E\x82\xad\xfa\x0e\x8b\x1e\xee\x8c\xaf)\xcb\x88^\x18\xe2\xf4\xaf\xcbRc\xf3s\xcc\xb5+\xb0\x12\xb3-u\x12\xe2\xd5\xc6\xd7&@\x9e\xe6\xab\x11d\t8\x0e(7\xcc\xb5\xc6\x1b\x03\xc0\xb2n@\xc5\xb8\xab\x01n~\xe2\xba\xe2%\xa2d\xcb\xb2]<\xd7\xd5Y~\x07\x8c%\x85\xf7\xa1\x9f\x0e\x96\xcb\x95\xc9\xa2\x8d\xa5\xc8R&Fz\x85\xa0g\x13\xbbR1\x12\xb1\xbdK\xa9O\rn\xed\xad\xe1\xae:q:\xd5\x82\xf4\xa9\xc3}a\xef\x12\xbc\x9b\x83ZV\xb349\xa5\x84\xb0\xa4*|\xdb u\x972\xc2UF\xdc\xe2\xd3G\x88qmo\x8c\x0fo\xa8\xc4\xf0\x91\xc9\xd1 \x04\xd9\xecwf=\xe1\xb9kR\x87\x10\xdb\xf6\x97kq\xde\xa3\xe1\xa2s\x8eHf\x9a=\xc4\xce\x96c\xb8p\x1b\xa1\r\xccnR+9\xe4\xc9CLM\x84\xf1$~\x91\xc6\x9bl\x81#\x8b\xc2c\x9d\xcd\xb3\xbd\xd4\x10\x88\xb3\xccF\x95y\xe1-1\xa1\x8fl\xb7\x11\xfc\x05\xaa\x99\xae+\x80rS.Vv\xc8\x93\xccR\xf5\x94`\rx\xf2\x12L\xe5d\xf5Kd\x98\x88\x93n.\x85F\xd9\xde\x858\x93\xe5iS\xc1\xf6\xfe\x9d\x8e\xb3\xc4\xd54\xdd\xb5:\xf7\x87\xc9\x0b#Sc\x8a\xc4\xa0\xd3\xae#\x18gr\xe5\x19G\x1c0\xc0\xb3\xb6\x08\xcc\x98p\x0c\xeb\xe7\x98Cf\xf1\xc01VVk\x8d\xc8\x12&T\xcb.\xb4l\xa7\xe9\x1aqGW\xddQD\x04\xd3\\\xc9sJ3\x12(^\xd6\x95\xbd\xdd\x91k\x98qns\xc6\xdbX\xdb\xdc\xf2*H\xa6\x15\xdc\xdc\xb3\x861\xeb\xc3\xc4?!m\xc6%\xd7\'\x99\xa6\xacB\\\x1a\n,\x99\x82\xf7\xcc\x8c\x9d\xf13\xc8\xd9`\xe2ScdnM\x11\x07B\xceF]\x9cc`\x90\xb7+mT\xb8)x\x11)!o\x0b\xcdtX\x98\x7f\xa8\x99Z\xdc\xbe\xa59\x9d\x91\x83\xf5\x08?4\xe4\x03J\x1f`\xc0\x80\xc0v\xcb\x18E\xd9\x18B0\xfb}\x82\r\xafk\xda\xc1\xdb\xdd\x02\x83\x18]\xef4\xbf\xe7(?\x14\x8d\xd0Zc\x8f\x87\x90?\xa3"\xff\x00cCAg@\xa0\xe9\xab\x87Ck{\xce\xd2\xf1\x8ehvB\x91\xcd\xa9\xd7o\xd9[\\\xdbW\xa7)R\x17\x06\xf5\xd8n>\x95j\x15\x89O\x08\xc9R\x91ZcL!Bs\x802\x8e$\xc1\x96`D\x01^\xd7\x0e\xa6\xa50<\xb1\xa8<K\xb8}\xe8s\xc2\x07G\xdde\x8e\xed\xd4\x93>\xe9\xdc\xf5\xc0\xe1\x1adw\x1c\xcd\xe1\x92\xd4\xd3L\x0c\xa4\xce\xc8\xc0\xa4\xbc_/q\x00\x98\x04#\x80\xb0\x86\x07t\xc6\xa8 \x08\x9c\x1aS\xa3\x0em\x7fr\xf8\xa3\x85\xcf\x10m\xe6\x97\xee\xabl\xbf\x1fc=\xc3\x7f\xc5\x99\x1b\tm\x02\\o2\x9d\xc1\x9d\x92\xc4 `\x8c\xbb\xe1\x07\x87x\x14z@\xf6\xd5(\x8e8\'\\\xec\xcf\x1f)\x8c\xf2\x84\xd1\xdf\x1e\x1eV\xa6-c\x12\xa7p\xd8\xf4I\xf7\xfb\xb2\xe2\x0f\xb2\xfcA\xb1d>g\x18\xd5\xb9N\x05\xc6\xb8\x0b\x19Oe\xb1\xa7\xc8%\xb6BC\x14\x92\xb8><eX\xec^B\x95\x03\xcb\x845\x85\x15\x93\xc4\x98$\x8f\r\x8d\xaa\x94X&\xb7\x84\x92V\xa0yjh\x0c\xf3\x82\xe6\xca\xe1\xf8\xd1\xb9\xc7C\xe4\xef\xefQ\xad\xb0\x89l\xbe\xd6dg\xccD\xfd\x06\x9d\xb5\xafK\x06_\x93B\xe6\x86Ii"\xa8\xd8!\x82J\xb1\x1b\xfbY\xe8\xd1\xdeF\x17ei\xd4\x96\xb5+y\xcd\xe6\x90\xac\xd0\xe4O\x1d\x82\x8a?\x86\x06\xc3\x92qe\x9cI\xce8t\xa3J4\x010\xa3J35\xe3\xe0\x18Y\x85\x8e\xd7\x00\xcb\x18/p\x8c\x02\xb5\xc2 \xde\xe1\x15\xafk\xde\xd4\x1c\xcd\xc5:e\xa8\x98\xa5k\x14\xef\x13j\xce\xb8b\xb9\xfaF1\'n\x9e\xe3\xac\x19\x8b\xe1\x93\x16\xc0\xbb5]\x13\x85\xd0\xc9#\xb1v\xd7\x84\xfd\xf12\x83\x88X\x02\x96\x00\n\xc84\xc2TX\xc2\x8c\x18n\x1d\x1f\xe9\x1e\xff\x00\xeb\'\n\xfc[1\xd2\xed\xeb\x14\xcf]\xb3~<\xca\xd9ZN\x95\xdd~ \xc9Rx\xfe\xc9\xc7\xa7\x13\xd93\xcc{,\xc0$\xd0\x18\x84\x89$\x81;\x9byh\xa3\xca\xdc\x9e\xcb`NZ\xd6\xd4\xedI\r7\xf6\xc7$\xed\x01\x0c\xf1\xac\xdb\x01\x91\xf8R\xf16\x9f\xb3\xe19\xf4\x12A\xb5\xbb-&\xda\xfc=\xae\xaf\xec\xaa\x92dV\xdcv\xc76\xc7\xcf\xe9\xc8s\x81\x92a\xca\xd8fS\x06\xe8c\xcc\x81De5\xd59\xaa\xfdTWFJ\xc3\x96\xa1$\xe0\x9b\xe2\t\xc5\x1b]\xb7{E\xa10\xfdl\x04\xfez\xf4\x8b0j{\xc6uRv6\x98EcX\x0f\xb3\x92\xe2\x06\xa1`\x9aJ\xe5\xa8\x19#\x8e\xb2\xa7\xf9p\x01\x1c\x8f3c\xe79\xe0\xdc\x08l\x92\xbd\x88\xe2\x18\x99\xccw\x10vk\x93\x11\xa4S\xc7cX\x8eR\x95:\x83\x9b\xf8|\xe6\xd5\x88\r<\x82\x8d5\n\xb1\xe5\x86\x84\x03T\x90\xc3\x02!&P4+V\xa2\x11\xe4\xdc\x06\x89"\xb5I\xae+\x92\xa0\xd0\x0c"\xe5QU\xb2\xfe2[%\x15aWfg\xe9\x97\nDq\xc6\xf7\x92\x02QJ\x11:<\xe5I\x0bCc\x88\x8d\x11FXF7\x9e\xa4\x93\x8a\x19\xc04%\xd8\xa0\xdb\xb0 [\xb1p\xe2~\x8c\xf10\xd7\x1dW\xd3\xd8\x96\x82d\xdc_\x96\x987\x83\x08\xc6ex\x89\xc7Oc\x98J|\xfb2\xcb\x93t\x80tu\xbb\xe4M\xd9\x9a4\xe7\x03R\xc5\x90\xd1\xb8\x9b-[$\x93\xc8\xd9\xd2\x89\xb4\xc7\xa9 \x88U\x1c\x13S\x8b\xb0s\xe3\x80\xf5\x84\x1e\x16\xfa\xe0\x11\xa3-\xbcvU\x97,$\x05\x08\xa1\x94\x84V\xcc\xf3\xfb\t\x19c$!$e\xa6\xbf\xb4\x90\x08\xa0\x84\xa1\x04\x16\xb9a\xb0/kX;~\xa0Pc\x0b\xbd\xe6\x97\xfc\xe5\x07\xe2\x91\xba\x0bLq\xf0\xf2\x07\xf4d_\xechh,\xe8\x14\n\x05\x02\x81@\xa0P(\x14\n\x05\x02\x81@\xa0P(\x14\x18\xc2\xefy\xa5\xff\x009A\xf8\xa4n\x82\xd3\x1c|<\x81\xfd\x19\x17\xfb\x1a\x1a\x0b:\x05\x02\x81@\xa0P(\x14\n\x05\x02\x81@\xa0P(\x14\n\x05\x060\xbb\xdei\x7f\xceP~)\x1b\xa0\xb4\xc7\x1f\x0f \x7fFE\xfe\xc6\x86\x82\xce\x81@\xa0P(\x14\n\x05\x02\x81@\xa0P(\x14\n\x05\x02\x81A\x8c.\xf7\x9a_\xf3\x94\x1f\x8aF\xe8-1\xc7\xc3\xc8\x1f\xd1\x91\x7f\xb1\xa1\xa0\xb3\xa0P(\x14\n\x05\x02\x81@\xa0P(\x14\n\x05\x02\x81@\xa0Pc\x0b\xbd\xe6\x97\xfc\xe5\x07\xe2\x91\xba\x0bLs\xfcc\xf88/\xfc\x0c\x98\x94y9\xa1\xff\x00e\x9e\x99\xa5"u\x05\n\xdf\xe8d\x9eY\x85\x18\x1f\xf2\x11\x80A\xbf\xf3j\x0b:\x05\x02\x81@\xa0P(\x14\n\x05\x02\x81@\xa0P(\x14\n\x05\x06>ze*d\x93!&Nz\x80\x96\xf8\x80\xa3\x04AF\x1bb\xcc\xfe\x91\x8c\x19\xfac\xb9a\x15\x82?\xd30\xb3;\x02\xf6\x0b\xb0`\x05\xec\xec\x887\xb8T\x02.\xf2\xd0j\x9bE$\t[\x1b\xd5(=_\xec\xcf,\x82}lB\xa5Y\xe6\xa8X&\xbb$w`^\x8c\x85\'\x9a#\xae\x88k\xd4\xa2N`\x87\xdc\xd3\xa7,w*\xc1\xe5\xee9\x0f\x9a!\x9d\x06\xf9\xea=\x03\xb8\xe4>h\x86t\x1b\xe7\xa8\xf4\x0e\xe3\x90\xf9\xa2\x19\xd0o\x9e\xa3\xd0;\x8eC\xe6\x88gA\xbez\x8f@\xee9\x0f\x9a!\x9d\x06\xf9\xea=\x03\xb8\xe4>h\x86t\x1b\xe7\xa8\xf4\x0e\xe3\x90\xf9\xa2\x19\xd0o\x9e\xa3\xd0;\x8eC\xe6\x88gA\xbez\x8f@\xee9\x0f\x9a!\x9d\x06\xf9\xea=\x03\xb8\xe4>h\x86t\x1b\xe7\xa8\xf4\x0e\xe3\x90\xf9\xa2\x19\xd0o\x9e\xa3\xd0;\x8eC\xe6\x88gA\xbez\x8f@\xee9\x0f\x9a!\x9d\x06\xf9\xea=\x03\xb8\xe4>h\x86t\x1b\xe7\xa8\xf4\x0e\xe3\x90\xf9\xa2\x19\xd0o\x9e\xa3\xd0;\x8eC\xe6\x88gA\xbez\x8f@\xee9\x0f\x9a!\x9d\x06\xf9\xea=\x03\xf6\xe9\xf8\xff\x00\xe2d\xae*X/\xfc\x08h\xe0\xeee(\r\xaf\xfc^\xe5\x18\xaev\xbd8Gk^\xf7\x05\xcdHp,e\x82!\x96`,"\xc6\x1fu\x95\x99+\x1a;\xa4L3\x94\x0c\xd5\x07\xacZ\xb9_\xe8\x89s\x8a\xe5C\xed\xa8Z\xb8\xd2\tNQ\xaa\x0c\xbfd\x16\xb8\t(\xb2\x88(\x94\xc4\x16Rr\t(\x01\xff\xd9'

@handler(req.InitReq)
class InitHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().InitBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.InitAndroidReq)
class InitAndroidHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().InitImageServer(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.LoginReq)
class LoginHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st, token = User().LoginBack(task)
            data["st"] = st
            data["token"] = token
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))

@handler(req.RegisterReq)
class RegisterHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().RegisterBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetUserInfo)
class GetUserInfoHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().UpdateUserInfoBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.SetAvatarInfoReq)
class SetAvatarInfoHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.res.code != 200:
                data["st"] = Status.SetHeadError
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.PunchIn)
class PunchInHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            st = User().PunchedBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CategoryReq)
class CategoryHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            from tools.category import CateGoryMgr
            CateGoryMgr().UpdateCateGoryBack(task)
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetComicsBookEpsReq)
class GetComicsBookEpsHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status == Status.Ok:
                from tools.book import BookMgr
                st = BookMgr().AddBookEpsInfoBack(task)
                if st == Status.WaitLoad:
                    return
                data["st"] = st
        except Exception as es:
            Log.Error(es)
        if task.bakParam:
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetComicsBookOrderReq)
class GetComicsBookOrderHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status == Status.Ok:
                from tools.book import BookMgr
                st = BookMgr().AddBookEpsPicInfoBack(task)
                if st == Status.WaitLoad:
                    return
                data["st"] = st
        except Exception as es:
            Log.Error(es)
        if task.bakParam:
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetComicsBookReq)
class GetComicsBookHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            from tools.book import BookMgr
            st = BookMgr().AddBookByIdBack(task)
            data["st"] = st
        except Exception as es:
            Log.Error(es)
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.SpeedTestPingReq)
class SpeedTestPingHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        if hasattr(task.res.raw, "elapsed"):
            if task.res.raw.status_code == 401 or task.res.raw.status_code == 200:
                data["data"] = str(task.res.raw.elapsed.total_seconds()*1000//4)
            else:
                data["st"] = Status.Error
                data["data"] = "0"
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
        else:
            data["data"] = "0"
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.DownloadBookReq)
class DownloadBookHandler(object):
    def __call__(self, backData):
        if backData.status != Status.Ok:
            if backData.bakParam:
                TaskBase.taskObj.downloadBack.emit(backData.bakParam, -backData.status, b"")
        else:
            r = backData.res
                # if r.status_code != 200:
                #     if backData.bakParam:
                #         TaskBase.taskObj.downloadBack.emit(backData.bakParam, -Status.Error, b"")
                #     return
            request = backData.req
            index = backData.index
            try:
                with Server().downloadSession[index].stream("GET", request.url, follow_redirects=True, headers=request.headers,
                                    timeout=backData.timeout, extensions=request.extend) as r:

                    fileSize = int(r.headers.get('Content-Length', 0))
                    getSize = 0
                    data = b""

                    now = time.time()
                    isAlreadySend = False
                    isSpacePic = True
                    # 网速快，太卡了，优化成最多100ms一次
                    try:
                        # from tqdm import tqdm
                        # with tqdm(total=fileSize, unit_scale=True, unit_divisor=1024, unit="B") as progress:
                        #     num_bytes_downloaded = r.num_bytes_downloaded
                        for chunk in r.iter_bytes(chunk_size=1024):
                            cur = time.time()
                            tick = cur - now
                            getSize += len(chunk)
                            data += chunk
                            isSpacePic = False
                            if tick >= 0.1:
                                isAlreadySend = True
                                if backData.bakParam and fileSize - getSize > 0:
                                    TaskBase.taskObj.downloadBack.emit(backData.bakParam, fileSize - getSize, b"")
                                now = cur

                        if not isAlreadySend:
                            if backData.bakParam:
                                TaskBase.taskObj.downloadBack.emit(backData.bakParam, getSize, b"")

                    except Exception as es:
                        Log.Error(es)
                        if backData.req.resetCnt > 0:
                            backData.req.isReset = True
                            Server().ReDownload(backData)
                            return

                    # Log.Info("size:{}, url:{}".format(ToolUtil.GetDownloadSize(fileSize), backData.req.url))
                    if config.IsUseCache and len(data) > 0:
                        try:
                            for path in [backData.req.cachePath, backData.req.savePath]:
                                filePath = path
                                if not path:
                                    continue
                                fileDir = os.path.dirname(filePath)
                                if not os.path.isdir(fileDir):
                                    os.makedirs(fileDir)

                                with open(filePath, "wb+") as f:
                                    f.write(data)
                                Log.Debug("add download cache, cachePath:{}".format(filePath))
                        except Exception as es:
                            Log.Error(es)
                            # 保存失败了
                            if backData.bakParam:
                                TaskBase.taskObj.downloadBack.emit(backData.bakParam, -2, b"")

                    if backData.bakParam:
                        if isSpacePic:
                            TaskBase.taskObj.downloadBack.emit(backData.bakParam, 0, SpacePic)
                        else:
                            TaskBase.taskObj.downloadBack.emit(backData.bakParam, 0, data)

            except Exception as es:
                backData.status = Status.DownloadFail
                Log.Error(es)
                if backData.bakParam:
                    TaskBase.taskObj.downloadBack.emit(backData.bakParam, -backData.status, b"")


@handler(req.CheckUpdateDatabaseReq)
@handler(req.DownloadDatabaseReq)
@handler(req.DownloadDatabaseWeekReq)
class DownloadDatabaseReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        if not task.res.GetText() or task.status == Status.NetError:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
            return
        if task.bakParam:
            data["data"] = task.res.GetText()
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CheckUpdateReq)
class CheckUpdateHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return
            verData = task.res.GetText()
            info = verData.replace("v", "").split(".")
            version = int(info[0]) * 100 + int(info[1]) * 10 + int(info[2]) * 1
            
            info2 = re.findall(r"\d+\d*", os.path.basename(config.UpdateVersion))
            curversion = int(info2[0]) * 100 + int(info2[1]) * 10 + int(info2[2]) * 1
            
            if version > curversion:
                data["data"] = verData.replace("\r\n", "").replace("\n", "")
            else:
                data["data"] = "no"
        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CheckUpdateInfoReq)
class CheckUpdateInfoHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return

            data["data"] =  task.res.GetText()
        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CheckUpdateConfigReq)
class CheckUpdateConfigHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return

            data["data"] = task.res.GetText()
        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.SpeedTestReq)
class SpeedTestHandler(object):
    def __call__(self, backData):
        data = {"st": backData.status, "data": ""}
        if backData.status != Status.Ok:
            if backData.bakParam:
                TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))
        else:
            request = backData.req
            index = backData.index
            try:
                with Server().downloadSession[index].stream("GET", request.url, follow_redirects=True, headers=request.headers,
                                    timeout=backData.timeout, extensions=request.extend) as r:

                    fileSize = int(r.headers.get('Content-Length', 0))
                    getSize = 0
                    now = time.time()
                    # 网速快，太卡了，优化成最多100ms一次
                    try:
                        for chunk in r.iter_bytes(chunk_size=1024):
                            getSize += len(chunk)
                            consume = time.time() - now
                            if consume >= 3.0:
                                break

                    except Exception as es:
                        Log.Error(es)

                consume = time.time() - now
                downloadSize = getSize / consume
                speed = ToolUtil.GetDownloadSize(downloadSize)
                if backData.bakParam:
                    data["data"] = speed
                    TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))

            except Exception as es:
                Log.Error(es)
                data["st"] = Status.DownloadFail
                if backData.bakParam:
                    TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))


@handler(req.GetUserCommentReq)
@handler(req.FavoritesAdd)
@handler(req.FavoritesReq)
@handler(req.AdvancedSearchReq)
@handler(req.CategoriesSearchReq)
@handler(req.RankReq)
@handler(req.KnightRankReq)
@handler(req.GetCommentsReq)
@handler(req.GetComicsRecommendation)
@handler(req.BookLikeReq)
@handler(req.CommentsLikeReq)
@handler(req.CommentsReportReq)
@handler(req.GetKeywords)
@handler(req.SendCommentReq)
@handler(req.SendCommentChildrenReq)
@handler(req.GetCommentsChildrenReq)
@handler(req.GetChatReq)
@handler(req.GetCollectionsReq)
@handler(req.GetRandomReq)
@handler(req.GetAPPsReq)
@handler(req.LoginAPPReq)
@handler(req.AppInfoReq)
@handler(req.AppCommentInfoReq)
@handler(req.GetGameReq)
@handler(req.GetGameInfoReq)
@handler(req.GetGameCommentsReq)
@handler(req.SendGameCommentsReq)
@handler(req.GameCommentsLikeReq)
@handler(req.ForgotPasswordReq)
@handler(req.ResetPasswordReq)
@handler(req.ChangePasswordReq)
@handler(req.GetNewChatReq)
@handler(req.GetNewChatProfileReq)
@handler(req.GetNewChatLoginReq)
@handler(req.SendNewChatMsgReq)
@handler(req.SendNewChatImgMsgReq)
class MsgHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        if task.bakParam:
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
