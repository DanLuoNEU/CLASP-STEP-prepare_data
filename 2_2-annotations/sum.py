# Summarize all statistics in one xml file
# 07/03/2021, Dan

import os
import sys

def main():
    path_annot = sys.argv[1]

    with open(path_annot, "r") as f:
        lines=f.readlines()

    dict_sum = {'all':[0,0,0],'CLASP':[0,0,0]}    
    for line in lines:
        words = line.split(',')
        vid, act = words[0], int(words[6])-1
        if 'cam' in vid:
            dict_sum['CLASP'][act] += 1
        if vid not in dict_sum.keys():
            dict_sum[vid]=[0,0,0]
        
        dict_sum[vid][act] += 1

        
        dict_sum['all'][act] += 1
    for vid in dict_sum:
        print(vid, dict_sum[vid])

    pass

if __name__ == "__main__":
    main()