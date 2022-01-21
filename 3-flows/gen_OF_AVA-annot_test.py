# 01/14/2022, Dan
# This file is used to generate needed Optical Flow files from AVA format annotations
# Multi GPU and Multi-processing uses 0-4 GPU for default, check line 66
import warnings
warnings.filterwarnings("ignore")

import os
from ast import parse
import csv
import time
import numpy as np
import torch
import argparse
from multiprocessing import Process, Lock, Queue
# from utils import flow_utils

from models import FlowNet2  # the path is depended on where you create this module
from utils.frame_utils import read_gen_PIL  # the path is depended on where you create this module

def gen_of_vid(avail_GPU, name_vid, list_sid, lock):
  gpu_id=avail_GPU.get()
  # Use Lock to avoid print multi-processing bug
  lock.acquire()
  try: 
    print(f"GPU {gpu_id} | Generating Optical Flows for {name_vid}({len(list_sid)})")
  finally:
    lock.release()
  ### Change this part for what you want ###
  time.sleep(10)
  ##################
  avail_GPU.put(gpu_id)


if __name__ == '__main__':
    # obtain the necessary args for construct the flownet framework
    parser = argparse.ArgumentParser()
    parser.add_argument('--fp16', action='store_true', help='Run model in pseudo-fp16 mode (fp16 storage fp32 math).')
    parser.add_argument("--rgb_max", type=float, default=255.)
    parser.add_argument("--path_annot", help="Path to the AVA format annotation file",
                        default="/data/CLASP-DATA/CLASP2-STEP/prepare_data/2_2-annotations/KRI/mixed/2cls/KRI-20220114-train_val_test-4of_gen.csv")
    parser.add_argument("--dir_frames", default='/data/CLASP-DATA/CLASP2-STEP/data/frames')
    parser.add_argument("--dir_flows",  default='/data/CLASP-DATA/CLASP2-STEP/data/flows')
    args = parser.parse_args()

    # Read CSV file and make data list
    dict_vid = {}
    amount_of = 0
    with open(args.path_annot) as file_csv:
      spamreader=csv.reader(file_csv, delimiter=',')
      for row in spamreader:
        name_vid = row[0]
        id_sec = int(row[1])
        if name_vid not in dict_vid:
          dict_vid[name_vid]=[]
        if id_sec not in dict_vid[name_vid]:
          dict_vid[name_vid].append(id_sec)
          
          amount_of += 1
    
    # Multi-processing
    ## One subprocess for one video
    lock=Lock()
    avail_GPU=Queue()
    for i in range(4): avail_GPU.put(i)

    for name_vid in dict_vid:
      while(avail_GPU.empty()): time.sleep(5)
      Process(target=gen_of_vid,args=( avail_GPU, name_vid, dict_vid[name_vid], lock)).start()