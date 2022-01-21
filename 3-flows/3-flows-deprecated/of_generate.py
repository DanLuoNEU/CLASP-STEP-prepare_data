# 01/31/2021, Created by Timothy, modified by Dan
# This file is used to create optical flow files

import os
import sys
import subprocess

rootDir = "/data/truppr/ava_v2_1/flipped_frames/"
saveDir = "/data/truppr/ava_v2_1/numpy_files/flip-flows/"
fileList = "/data/truppr/ava_v2_1/total_files4.txt"

dirs = open(fileList, 'r').readlines()

for dir in dirs:
    # print(saveDir + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5))
    targetDirRootArr = []
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")


    targetDirSaveArr = []
    targetDirSaveArr.append(saveDir + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirSaveArr.append(saveDir + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirSaveArr.append(saveDir + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")

    index = 0
    for targetDirRoot in targetDirRootArr:
        # print("checking... ", targetDirSave)
        targetDirSave = targetDirSaveArr[index]

        if os.path.exists(targetDirSave):
            print("Skipping... ",targetDirSave)
            index += 1
            continue
        else:
            if not os.path.exists(saveDir + "/" + dir.split(",")[0] + "/"):
                os.mkdir(saveDir + "/" + dir.split(",")[0] + "/")
            if not os.path.exists(targetDirSave):
                os.mkdir(targetDirSave)

        command = "python main.py --optical_weights flownet2-pytorch/models/FlowNet2_checkpoint.pth.tar --image_dir " + targetDirRoot + " --save_dir " + targetDirSave

        try:
            print(command)
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            print("\t[ OK ]")
        except subprocess.CalledProcessError as err:
            print("\t[ FAIL ]")
            print(err)
        index += 1
