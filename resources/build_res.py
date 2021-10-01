import base64
import os

fw = open("resources.py", "w+")
fw.write("import base64\n\n\n")
fw.write("class DataMgr(object):\n")

files = []
for root, dirs, filenames in os.walk("../resources2/"):
    for name in filenames:
        if name[-3:] != "png" and name[-3:] != "gif":
            continue
        if len(name.split(".")) >= 3:
            continue
        if not os.path.isfile(root+name):
            continue
        f = open(root+name, "rb")
        # fw.write("def get():\r\n    return )
        i = 0
        data = base64.b64encode(f.read())
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
fw.write("      return base64.b64decode(data.encode('utf-8'))\n")
fw.close()
