# 01/31/2021, Dan
# Split all annotations to train/val .csv files
import os
import csv
import random

def main():
    # TODO: Modify the path to .csv files
    file_all = "/data/CLASP-DATA/CLASP2-STEP/data/annotations/logan/logan_part_20210426.csv"
    file_train = file_all.split('.')[0]+'_train.csv'
    file_val = file_all.split('.')[0]+'_val.csv'
    # file_train = '/data/CLASP-DATA/CLASP2-STEP/data/annotations/topdown/clasp_20210131_topdown_1000+_train.csv'
    # file_val = '/data/CLASP-DATA/CLASP2-STEP/data/annotations/topdown/clasp_20210131_topdown_1000+_val.csv'
    
    # Read all annotations and store with each action class
    print(file_all)
    annot_all={}
    with open(file_all, 'r') as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if row[6] not in annot_all.keys():
                annot_all[row[6]] = []
            annot_all[row[6]].append(row)
    # Spliting all annotations for each action class with train:val as 9:1
    annot_train, annot_val = {'all':[]}, {'all':[]}
    for act in annot_all.keys():
        annot_train[act], annot_val[act] = [], []
        num_val = int(0.05*len(annot_all[act])) #0.1
        
        annot_val[act] = random.choices(annot_all[act],k=num_val)
        
        for annot in annot_all[act]:
            if annot not in annot_val[act]:
                annot_train[act].append(annot)
        
        annot_train['all'] += annot_train[act]
        annot_val['all'] += annot_val[act]

        print(len(annot_train[act]), len(annot_val[act]))

    print('train: ', len(annot_train['all']))
    print('val: ', len(annot_val['all']))
    
    # Write train/val annotation files
    with open(file_train, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerows(annot_train['all'])
    with open(file_val, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerows(annot_val['all'])

    # Statistic of the folders to generate
    # folder_sec = []
    # for act in annot_all.keys():
    #     for annot in annot_all[act]:
    #         vid=annot[0]
    #         sid=int(annot[1])
    #         for i in range(4):
    #             sid_t = sid-2+i
    #             if vid+'-'+str(sid_t) not in folder_sec:
    #                 folder_sec.append(vid+'-'+str(sid_t))
    # print('Approximate Num of OF Folders to generate: ', len(folder_sec))

    print("Well Done!")

if __name__ == "__main__":
    main()