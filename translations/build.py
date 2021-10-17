import os
# import subprocess
import subprocess

for root, dirs, filenames in os.walk("./"):
    for name in filenames:
        if name[-2:] != "ts":
            continue
        outName = name[:-6]
        tcName = outName + "_tc"
        filename = "{}.ts".format(tcName)
        f = open(filename, "r+", encoding="utf-8")
        data = ""
        for line in f.readlines():
            if "<message>" in line:
                data += line.replace("<message>", "<message encoding=\"UTF-8\">")
            else:
                data += line
        f.seek(0)
        f.write(data)
        f.close()
        sts = os.system("..\\env\\Scripts\\PySide6-lupdate.exe -verbose ..\\ui\\{}.ui -ts {}.ts".format(outName, tcName))
        # sts = os.system("..\env\Scripts\PySide6-uic.exe {}.ui -o {}.py".format(outName, outName))
        # proc = subprocess.Popen(["PySide6-lupdate", "..\\ui\\{}.ui".format(outName) + " -ts {}_tc.ts".format(outName)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        # proc = subprocess.Popen(["dir", "..\\ui\\{}.ui".format(outName)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        # while True:
        #     buff = proc.stdout.readline()
        #     buff = buff.decode("gbk", "ignore")
        #     if buff == '' and proc.poll() != None :
        #         break
        #     elif buff != '':
        #         print(buff)
        # pass

print('Finished!')
