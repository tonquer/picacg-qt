import os
from tools.langconv import Converter
os.system("chcp 65001")
sts = os.system("pyside6-lupdate.exe -no-obsolete -source-language zh_CN -target-language zh_HK ../src/tools/str.py -ts ../translate/str_hk.ts")
sts = os.system("pyside6-lupdate.exe -no-obsolete -source-language zh_CN -target-language en_US ../src/tools/str.py -ts ../translate/str_en.ts")

sts = os.system("pyside6-lupdate.exe -no-obsolete -source-language zh_CN -target-language zh_HK ../ui -ts ../translate/ui_hk.ts")
sts = os.system("pyside6-lupdate.exe -no-obsolete -source-language zh_CN -target-language en_US ../ui -ts ../translate/ui_en.ts")
#
for tsFile in ["../translate/str_hk.ts", "../translate/ui_hk.ts"]:
    f = open(tsFile, "r", encoding="utf-8")
    data = ""
    nextName = ""
    for srcLine in f.readlines():
        line = srcLine.strip()
        if "<source>" in line:
            name = line.replace("<source>", "").replace("</source>", "")
            nextName = Converter('zh-hant').convert(name)
        if "<translation type=\"unfinished\"></translation>" in line:
            srcLine = srcLine.replace("<translation type=\"unfinished\"></translation>", "<translation>{}</translation>".format(nextName))
        elif "<translation>" in line:
            oldName = line.replace("<translation>", "").replace("</translation>", "").replace("\n", "")
            srcLine = srcLine.replace(oldName, nextName)
        elif "<translation type=\"vanished\">" in line:
            oldName = line.replace("<translation type=\"vanished\">", "").replace("</translation>", "").replace("\n", "")
            srcLine = srcLine.replace(" type=\"vanished\"", "").replace(oldName, nextName)
        data += srcLine

    f.close()
    f = open(tsFile, "w+", encoding="utf-8")
    f.write(data)
    f.close()

sts = os.system("pyside6-lrelease.exe ../translate/str_en.ts ../translate/ui_en.ts -qm ../res/tr/tr_en.qm")
sts = os.system("pyside6-lrelease.exe ../translate/str_hk.ts ../translate/ui_hk.ts -qm ../res/tr/tr_hk.qm")
