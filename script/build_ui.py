import os
# import subprocess

for root, dirs, filenames in os.walk("../ui/"):
    for name in filenames:
        if name[-2:] != "ui":
            continue
        outName = name[:-3]
        sts = os.system("pyside6-uic.exe {}.ui -o {}.py".format(os.path.join(root, outName), os.path.join(
            "../src/interface/", outName)))
        # sts = os.system("..\env\Scripts\PySide6-uic.exe {}.interface -o {}.py".format(outName, outName))
        # proc = subprocess.Popen(["PySide6-uic.exe {}.interface -o {}.py".format(outName, outName)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # while True:
        #     buff = proc.stdout.readline()
        #     buff = buff.decode("gbk", "ignore")
        #     if buff == '' and proc.poll() != None :
        #         break
        #     elif buff != '':
        #         print(buff)
        pass

print('Finished!')
