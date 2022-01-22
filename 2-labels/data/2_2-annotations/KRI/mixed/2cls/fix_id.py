# Fix pid problem
# 07/01/2021, Dan

import os

def main():
    with open('/data/CLASP-DATA/CLASP2-STEP/data/annotations/KRI/mixed/2cls/KRI-20210701-train_val copy.csv') as f:
        lines=f.readlines()

    vid_last = ''
    pid = 0
    for i, line in enumerate(lines):
        vid = line.split(',')[0]
        if vid == vid_last:
            pid += 1
        else:
            pid = 0
        vid_last = vid
        words = line.split(',')
        words[-1] = str(pid)+'\n'
        line_new = words[0]
        for word in words[1:]:
            line_new = line_new + ',' + word
        lines[i]=line_new

    with open('/data/CLASP-DATA/CLASP2-STEP/data/annotations/KRI/mixed/2cls/KRI-20210701-train_val copy.csv','w') as f:
        f.writelines(lines)
    
    
    pass

if __name__ == "__main__":
    main()