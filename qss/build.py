import base64
import os

fw = open("qss.py", "w+")
fw.write("import base64\n\n\n")
fw.write("class QssDataMgr(object):\n")

files = []
for root, dirs, filenames in os.walk("./"):
    for name in filenames:
        if name[-3:] != "qss":
            continue
        if len(name.split(".")) >= 3:
            continue
        f = open(name, "r", encoding="utf-8")
        # fw.write("def get():\r\n    return )
        i = 0
        data = base64.b64encode(f.read().encode("utf-8"))
        # if i % 2 == 0:
        #     fw.write("\\x")
        fw.write("  {}".format(name[:-4]))
        files.append(name[:-4])
        fw.write(" = \"")
        fw.write(data.decode("utf-8"))
        fw.write("\"\n\n")
        f.close()

fw.write("  files = {}\n\n".format(files))
fw.write("  @classmethod\n")
fw.write("  def GetData(cls, name):\n")
fw.write("      data = getattr(cls, name)\n")
fw.write("      return base64.b64decode(data.encode('utf-8')).decode('utf-8')\n")
fw.close()
