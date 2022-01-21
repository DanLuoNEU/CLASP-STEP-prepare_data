import os
import csv
import random

def main():
    file_all = "/data/CLASP-DATA/CLASP2-STEP/data/annotations/topdown/clasp_20210131_topdown.csv"
    
    annot_all=[]
    with open(file_all, 'r') as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            annot_all.append(row)
    for i in range(9):
        annot_select=random.choices(annot_all, k=420)
        file_select = f"/data/CLASP-DATA/CLASP2-STEP/data/annotations/topdown/20210131_train_ft/clasp_20210131_topdown_300+_{i+1}.csv"
        with open(file_select, 'w') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerows(annot_select)

    pass

if __name__=="__main__":
    main()