import os

path_file_avakri = "/data/CLASP-DATA/CLASP2-STEP/data/annotations/KRI/mixed/AVA_KRI-20210629-mixedview-all.csv"
path_file_kri = "/data/CLASP-DATA/CLASP2-STEP/data/annotations/KRI/mixed/KRI-20210629-mixedview-all.csv"

def main():
    lines_kri = []
    
    with open(path_file_avakri,'r') as f:
        lines_all=f.readlines()
    lines_all.sort()
    for line in lines_all:
        if 'cam' in line:
            lines_kri.append(line)
    with open(path_file_kri,'w') as f:
        f.writelines(lines_kri)
        
    pass

if __name__ == "__main__":
    main()