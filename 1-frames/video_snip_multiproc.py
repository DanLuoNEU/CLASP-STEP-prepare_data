# 01/20/2022, Dan
# This file is used to generate needed RGB frames with path to original videos
# Multiprocessing uses 8 subprocesses for default

import os
from ast import parse
from platform import release
import cv2
import sys
import glob
import time
import math
import numpy as np
import argparse
from multiprocessing import Process, Lock, Queue, Value


def gen_rgb_vid(lock, num_processed, name_vid, args):
    # OpenCV reads Video and info
    path_vid = os.path.join(args.dir_vid, name_vid)
    vidcap = cv2.VideoCapture(path_vid)
    num_secs = int(video.get(cv2.CAP_PROP_FRAME_COUNT)/video.get(cv2.CAP_PROP_FPS))
    if np.ceil(vidcap.get(cv2.CAP_PROP_FPS))-vidcap.get(cv2.CAP_PROP_FPS) < 0.1:
        fps_vid = np.ceil(vidcap.get(cv2.CAP_PROP_FPS))
    else:
        fps_vid=int(vidcap.get(cv2.CAP_PROP_FPS))
    
    # Lock to print 
    lock.acquire()
    try:
        print(f"Generating frames for {name_vid}({num_secs})...")
    finally:
        lock.release()
    
    # Subprocess
    id_sec = 0
    id_one_sec = 1
    success,image = vidcap.read()
    while success:
        dir_sec = os.path.join(args.dir_frames, name_vid, f"{id_sec:05d}")
        if not os.path.exists(dir_sec):
            os.makedirs(dir_sec)
        path_img = os.path.join(dir_sec,f"{id_one_sec:02d}.jpg")
        cv2.imwrite(path_img, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        id_one_sec+=1
        
        if id_one_sec == fps_vid+1:
            id_one_sec = 1
            num_processed.value += 1
            id_sec += 1
            lock.acquire()
            try:
                print(f"Generating frames for {name_vid}({num_processed.value}/{args.amount_data})...")
            finally:
                lock.release()


if __name__ == '__main__':
    
    # obtain the necessary args
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_vid", help="Path to video folder",
                        default="/data/CLASP-DATA/CLASP2-STEP/prepare_data/1-frames/videos")
    parser.add_argument("--dir_frames", help="Path to store frames",
                        default='./frames')
    parser.add_argument("--num_proc", type=int, default=8)
    args = parser.parse_args()

    # Get all video names and count sec folder amount
    list_vid = os.listdir(args.dir_vid)
    
    args.amount_data = 0
    for name_vid in list_vid:
        path_vid = os.path.join(args.dir_vid, name_vid)
        video = cv2.VideoCapture(path_vid)
        args.amount_data += int(video.get(cv2.CAP_PROP_FRAME_COUNT)/video.get(cv2.CAP_PROP_FPS))

    # Multiprocessing Frames Generation
    ## Shared Content
    lock=Lock()
    num_processed = Value('i', 0)

    procs=[]
    for name_vid in list_vid:
        if len(procs) < args.num_proc:
            p_temp=Process(target=gen_rgb_vid, args=(lock,num_processed, name_vid, args))
            procs.append(p_temp)
            p_temp.start()
        else:
            id_avail=-1
            while id_avail==-1:
                for i_proc in range(args.num_proc):
                    procs[i_proc].join(timeout=0)
                    if not procs[i_proc].is_alive():
                        id_avail=i_proc
                        break
                if id_avail==-1:
                    time.sleep(20)

            p_temp=Process(target=gen_rgb_vid,args=(lock, num_processed, name_vid, args))
            procs[id_avail] = p_temp
            procs[id_avail].start()