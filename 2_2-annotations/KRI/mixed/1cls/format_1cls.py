import os

path_file_2cls = "/data/CLASP-DATA/CLASP2-STEP/data/annotations/KRI/mixed/1cls/KRI-20210716-train_val-ori.csv"
path_file_1cls = "/data/CLASP-DATA/CLASP2-STEP/data/annotations/KRI/mixed/1cls/KRI-20210716-train_val.csv"

def main():
    lines_1cls = []
    
    with open(path_file_2cls,'r') as f:
        lines_all=f.readlines()
    lines_all.sort()
    for line in lines_all:
        words=line.split(',')
        if words[6]=='2':
            words[6]='1'
            line_new = ''
            for word in words:
                line_new += word+','
            line_new = line_new[:-1]
            lines_1cls.append(line_new)
    with open(path_file_1cls,'w') as f:
        f.writelines(lines_1cls)
        
    pass

if __name__ == "__main__":
    main()