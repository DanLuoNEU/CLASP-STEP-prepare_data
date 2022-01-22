# Use IOU and timestamp to clean action from Background actions(Mainly from False Alarms for 1 Action Classification)
# 10/07/2021, Dan

import os
import csv
import sys
import numpy as np

def obj_overlap(box_a, boxes_b):
    """
    A n B / B = A n B / area(B)
    """
    b_a = np.asarray(box_a)[np.newaxis,:]
    b_b = np.asarray(boxes_b)
    num_a = b_a.shape[0]
    num_b = b_b.shape[0]
    min_xy_a = np.repeat(np.expand_dims(b_a[:,:2], 1),num_b,axis=1)
    min_xy_b = np.repeat(np.expand_dims(b_b[:,:2], 0),num_a,axis=0)
    max_xy_a = np.repeat(np.expand_dims(b_a[:,2:], 1),num_b,axis=1)
    max_xy_b = np.repeat(np.expand_dims(b_b[:,2:], 0),num_a,axis=0)
    min_xy = np.maximum(min_xy_a, min_xy_b) 
    max_xy = np.minimum(max_xy_a, max_xy_b)
    
    inter_xy = np.clip((max_xy - min_xy), 0, np.inf)
    inter = inter_xy[:,:,0] * inter_xy[:,:,1]
    area_a = np.repeat(np.expand_dims(((b_a[:, 2]-b_a[:, 0]) * (b_a[:, 3]-b_a[:, 1])), 1),num_b,axis=1)
    area_b = np.repeat(np.expand_dims(((b_b[:, 2]-b_b[:, 0]) * (b_b[:, 3]-b_b[:, 1])), 0),num_a,axis=0)

    return (inter/area_b)[0,:], min_xy[0,:], max_xy[0,:]

def main():
    path_with_FA=sys.argv[1]
    path_action=sys.argv[2]
    ########## TEST ##########
    # path_with_FA="/data/CLASP-DATA/CLASP2-STEP/data/annotations/PVD/20210830-2cls/PVD-exp1-04162021_08172020-2cls_with_false_alarms-all.csv" # TEST
    # path_action ="/data/CLASP-DATA/CLASP2-STEP/data/annotations/PVD/20211006-3cls-touch_move/20211007-touch_move-all.csv"                    # TEST
    ##########################

    # Read ALL files from Annotation_FA and Annotation_Action
    with open(path_with_FA, 'r') as f:
        lines_FA = f.readlines()
    with open(path_action, 'r') as f:
        lines_action = f.readlines()
    lines_FA_clean=lines_FA.copy()
    # Loop through Annotation_Action to remove records in Annotatio_FA
    for line_FA in lines_FA:
        words=line_FA.split(',')
        id_exp = words[0]
        id_t = words[1]
        bbox = np.fromstring(words[2]+','+words[3]+','+words[4]+','+words[5], dtype=float,sep=',')
        id_action=words[6]
        # Background Annotation
        if id_action=='1':
            # Loop through Action Annotations
            for line_action in lines_action:
                words_action=line_action.split(',')
                id_exp_action=words_action[0]
                id_t_action=words_action[1]
                # When Experiment Name and Second ID are the same
                if id_exp_action==id_exp and int(id_t)==int(id_t_action):
                    # Compute BBox IOU
                    bbox_action = np.fromstring(words_action[2]+','+words_action[3]+','+words_action[4]+','+words_action[5], dtype=float,sep=',')
                    IOUs,_, _ = obj_overlap(bbox, [bbox_action])
                    if IOUs[0]>0.5:
                        lines_FA_clean.remove(line_FA)
    # Save the Result
    path_save=path_with_FA.split('.')[0]+'-Clean.csv'
    with open(path_save,'w') as f:
        f.writelines(lines_FA_clean)
        f.write('\n')
        f.writelines(lines_action)

if __name__ == '__main__':
    main()