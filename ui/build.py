import os
# import subprocess

for root, dirs, filenames in os.walk("./"):
    for name in filenames:
        if name[-2:] != "ui":
            continue
        outName = name[:-3]
        sts = os.system("pyside2-uic.exe {}.ui -o {}.py".format(outName, outName))
        # sts = os.system("..\env\Scripts\pyside2-uic.exe {}.ui -o {}.py".format(outName, outName))
        # proc = subprocess.Popen(["pyside2-uic.exe {}.ui -o {}.py".format(outName, outName)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # while True:
        #     buff = proc.stdout.readline()
        #     buff = buff.decode("gbk", "ignore")
        #     if buff == '' and proc.poll() != None :
        #         break
        #     elif buff != '':
        #         print(buff)
        pass

print('Finished!')