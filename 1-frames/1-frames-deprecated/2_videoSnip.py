import os
import sys
import glob
import math
import numpy as np
import urllib.request
import subprocess


def get_chunk(filename, second, targetDir):
    ffmpeg_command = 'ffmpeg -i %(videopath)s \
            -ss %(timestamp)f -t %(timestamp_to)f \
            %(outpath)s' % {
                    'videopath': filename,
                    'timestamp': second,
                    'timestamp_to': 1,
                    'outpath' : targetDir}
    print(ffmpeg_command)
    try:
        subprocess.call(ffmpeg_command, shell=True)

        return True
    except:
        return False

def get_frames(filename, second, targetDir):
    # outdir_folder = os.path.join(outdir_keyframes, video_id)
    # mkdir_p(outdir_folder)
    # outpath = os.path.join(outdir_folder, '%d.jpg' % (int(time_id)))
    targetDir = targetDir + "/%02d.jpg"
    ffmpeg_command = 'ffmpeg -i %(videopath)s -vf "select=not(mod(n\,1))" -q:v 2 %(outpath)s'  % {
                          'videopath': filename,
                          'outpath': targetDir}
    print(ffmpeg_command)
    try:
        subprocess.call(ffmpeg_command, shell=True)

        return True
    except:
        return False


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

videoDir = sys.argv[2]
saveDir = "dataset"
chunkStagingDir = "temp"

str_padding = 5

dataset_file = sys.argv[1].replace("./", '')
dataset = open(dataset_file, 'r').readlines()

for line in dataset:
    video = line.replace('\n','')

    if not os.path.exists(saveDir + "/" + video.replace('.mp4', '')):
        os.mkdir(saveDir + "/" + video.replace('.mp4', ''))

    video_length = math.floor(get_length(videoDir + "/" + video))
    print("video: ", video, " is length ", video_length)

    # Snip video
    for second in range(0, video_length + 1):
        if not os.path.exists(saveDir + "/" + video.replace('.mp4', '') + "/" + str(second).zfill(str_padding)):
            os.mkdir(saveDir + "/" + video.replace('.mp4', '') + "/" + str(second).zfill(str_padding))
        # else:
        #     continue
        outDir = saveDir + "/" + video.replace('.mp4', '') + "/" + str(second).zfill(str_padding)
        tempDir = chunkStagingDir + "/" + str(second).zfill(str_padding) + "_" + video
        get_chunk(videoDir + "/" + video, second, tempDir)
        get_frames(tempDir, second, outDir)


