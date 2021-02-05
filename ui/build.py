import os
import subprocess

for root, dirs, filenames in os.walk("./"):
    for name in filenames:
        if name[-2:] != "ui":
            continue
        outName = name[:-3]
        proc = subprocess.Popen(["python.exe -mPyQt5.uic.pyuic {}.ui -o {}.py".format(outName, outName)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            buff = proc.stdout.readline()
            buff = buff.decode("gbk", "ignore")
            if buff == '' and proc.poll() != None :
                break
            elif buff != '':
                print(buff)
        pass