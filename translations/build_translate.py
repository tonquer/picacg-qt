import os
# import subprocess

for root, dirs, filenames in os.walk("./"):
    for name in filenames:
        if name[-2:] != "ts":
            continue
        outName = name[:-6]
        tcName = outName + "_tc"
        filename = ".ts".format(tcName)
        sts = os.system("PySide6-lupdate -verbose ..\\ui\\{}.ui -ts {}.ts".format(outName, tcName))
        # sts = os.system("..\env\Scripts\PySide6-uic.exe {}.ui -o {}.py".format(outName, outName))
        # proc = subprocess.Popen(["PySide6-uic.exe {}.ui -o {}.py".format(outName, outName)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # while True:
        #     buff = proc.stdout.readline()
        #     buff = buff.decode("gbk", "ignore")
        #     if buff == '' and proc.poll() != None :
        #         break
        #     elif buff != '':
        #         print(buff)
        pass

print('Finished!')