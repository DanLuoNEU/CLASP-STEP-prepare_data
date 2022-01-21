# 01/14/2022, Dan
# This file is used to generate needed Optical Flow files from AVA format annotations
# Multi GPU and Multi-processing uses 0-4 GPU for default 
from socket import timeout
import warnings
warnings.filterwarnings("ignore")

import os
from ast import parse
import sys
import csv
import glob
import time
import numpy as np
import torch
import argparse
from multiprocessing import Process, Lock, Value, Queue

from models import FlowNet2  # the path is depended on where you create this module
from utils import flow_utils
from utils.frame_utils import read_gen_PIL  # the path is depended on where you create this module

'''
    Input:  Annotations
        * Files should be like this:
            -| frames
              -| vid01
                -| 01
                  -| 01.jpg
                  -| 02.jpg
                  -| ...
                -| 02
                  -| 01.jpg
                  -| 02.jpg
                  -| ...
                -| xx
            -| of
              -| vid01
                -| 01
                  -| 01.flo
                  -| 02.flo
                  -| ...
                -| 02
                  -| 01.flo
                  -| 02.flo
                  -| ...
                -| xx
    Output:  256x256 .flo files in folders organized as same as input folders
'''
# save flow, I reference the code in scripts/run-flownet.py in flownet2-caffe project
def writeFlow(name, flow):
    f = open(name, 'wb')
    f.write('PIEH'.encode('utf-8'))
    np.array([flow.shape[1], flow.shape[0]], dtype=np.int32).tofile(f)
    flow = flow.astype(np.float32)
    flow.tofile(f)
    f.flush()
    f.close()


def gen_of_vid(lock, num_processed, avail_GPU,
                name_vid, list_sid, args):
    # Get the available 
    gpu_id=avail_GPU.get()
    # Use Lock to avoid print multi-processing bug
    lock.acquire()
    try: 
        print(f"GPU {gpu_id} | Generating Optical Flows for {name_vid}({len(list_sid)})")
        # os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_id)
        # ## Initialize a Net
        # net = FlowNet2(args).cuda()
        # dict_net = torch.load(args.path_model,map_location=torch.device('cpu'))
        # net.load_state_dict(dict_net["state_dict"])

    finally:
        lock.release()
    # Process One Video Data Flows
    os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_id)
    ## Initialize a Net
    net = FlowNet2(args).cuda()
    dict_net = torch.load(args.path_model,map_location=torch.device('cpu'))
    net.load_state_dict(dict_net["state_dict"])
    ## Sort the List Sid
    list_sid.sort()
    id_temp = 0
    ## Loop over each annotation sid
    for sid in list_sid:
        ### Prepare 4 sec data for each annotation, (sid-2,sid-1,sid+0,sid+1)
        for step in range(4):
            #### Check if sid_temp < 0
            sid_temp = sid-2+step
            if sid_temp < 0: continue
            #### Check if Already Generated and Numbers are right
            dir_sid_temp = os.path.join(args.dir_flows, name_vid, f"{sid_temp:05d}")
            dir_sid_ori = os.path.join(args.dir_frames, name_vid, f"{sid_temp:05d}")
            if os.path.exists(dir_sid_temp): 
                number_flows = len(glob.glob(dir_sid_temp+'/*.flo'))
                number_frames= len(os.listdir(dir_sid_ori))
                if number_flows == number_frames-1:    continue
            else:
                os.makedirs(dir_sid_temp)

            #### Generate OF for name_vid/sid_temp
            list_frames = os.listdir(dir_sid_ori)
            list_frames.sort() # !!!CANNOT be used as return object!!!
            number_flows = len(list_frames)-1
            for i_frame in range(number_flows)[1:]:
                path_img1=os.path.join(dir_sid_ori,list_frames[i_frame])
                path_img2=os.path.join(dir_sid_ori,list_frames[i_frame+1])
                pim1=read_gen_PIL(path_img1)
                pim2=read_gen_PIL(path_img2)

                size_norm = (256,256) # One 256x256 .flo would take 512KB
                                      # *WIDTH and HEIGHT must be multiple of 64
 
                pim1 = np.asarray(pim1.resize(size_norm))
                pim2 = np.asarray(pim2.resize(size_norm))
                images = [pim1, pim2]
                images = np.array(images).transpose(3, 0, 1, 2)
                
                # lock.acquire()
                # os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_id)
                im = torch.from_numpy(images.astype(np.float32)).unsqueeze(0).cuda()
                # lock.release()

                result=net(im).squeeze()
                data_flow = result.data.cpu().numpy().transpose(1,2,0)
                path_flow=os.path.join(dir_sid_temp, f"{i_frame:02d}.flo")
                writeFlow(path_flow, data_flow)
                # flow_utils.visulize_flow_file(path_flow, dir_sid_temp)  
        id_temp += 1
        
        num_processed.value = num_processed.value + 1
        lock.acquire()
        try: 
            print(f"GPU {gpu_id} | Generating OF for {name_vid}({id_temp}/{len(list_sid)})| Processed {num_processed.value}({args.amount_of})... | {time.asctime(time.localtime(time.time()))}")
        finally:
            lock.release()
        
    del net
    # Release the GPU and put it back into available GPU Queue
    # # time.sleep(10) # Used to test MultiProcessing
    avail_GPU.put(gpu_id)


if __name__ == '__main__':
    # obtain the necessary args for construct the flownet framework
    parser = argparse.ArgumentParser()
    parser.add_argument('--fp16', action='store_true', help='Run model in pseudo-fp16 mode (fp16 storage fp32 math).')
    parser.add_argument("--rgb_max", type=float, default=255.)
    parser.add_argument("--path_annot", help="Path to the AVA format annotation file",
                        default="/data/CLASP-DATA/CLASP2-STEP/prepare_data/2_2-annotations/KRI/mixed/2cls/KRI-20220114-train_val_test-4of_gen.csv")
    parser.add_argument("--path_model", help="Path to FlowNet2 Pretrained Model",
                        default="/home/dan/ws/Backup/2019-Flownet2/flownet2-pytorch-CLASP/pretrained/FlowNet2_checkpoint.pth.tar")
    parser.add_argument("--dir_frames", default='/data/CLASP-DATA/CLASP2-STEP/data/frames')
    parser.add_argument("--dir_flows",  default='/data/CLASP-DATA/CLASP2-STEP/data/flows')
    parser.add_argument("--num_proc", type=int, default=4)
    args = parser.parse_args()

    # Read CSV file and make data list
    dict_vid = {}
    args.amount_of = 0
    with open(args.path_annot) as file_csv:
        spamreader=csv.reader(file_csv, delimiter=',')
        for row in spamreader:
            name_vid = row[0]
            id_sec = int(row[1])
            if name_vid not in dict_vid:
                dict_vid[name_vid]=[]
            if id_sec not in dict_vid[name_vid]:
                dict_vid[name_vid].append(id_sec)
            
                args.amount_of += 1
    
    # Multi-processing: One subprocess for one video
    ## Prepare Lock and Exchanging objects between processes
    lock=Lock()
    num_processed = Value('i', 0)
    avail_GPU=Queue()
    for i in range(args.num_proc): avail_GPU.put(i) # test using range(1)

    procs=[]
    for name_vid in dict_vid:
        # Initilize all processes list
        if len(procs) < args.num_proc:
            p_temp=Process(target=gen_of_vid,args=(lock, num_processed, avail_GPU,
                                                    name_vid, dict_vid[name_vid], args))
            procs.append(p_temp)
            p_temp.start()
        else:
            # Make sure at least one GPU is available
            id_avail=-1
            while id_avail==-1:
                for i_proc in range(args.num_proc):
                    procs[i_proc].join(timeout=0)
                    if not procs[i_proc].is_alive():
                        id_avail=i_proc
                        break
                if id_avail==-1:
                    time.sleep(20)

            p_temp=Process(target=gen_of_vid,args=(lock, num_processed, avail_GPU,
                                                    name_vid, dict_vid[name_vid], args))
            procs[id_avail] = p_temp
            procs[id_avail].start()

        # Process(target=gen_of_vid,args=(lock, num_processed, avail_GPU,
        #                                 name_vid, dict_vid[name_vid], args)).start()