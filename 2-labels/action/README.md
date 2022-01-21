# 1. Prepare CVAT

# 2. localhost:8080

# 3. Create Tasks(1 fps data)
## 3.1 Using CVAT frame step(recommended)
Use the downsample video, use frame step as **30**(30/29.97 fps) to get 1 annotation per sec
## 3.2 Chop the video into 1-fps images(Optional) 
MAKE SURE: # frames = # seconds in video
```
video_name=20191024-training-cam09exp2
mkdir -p frames_temp/$video_name
ffmpeg -i $video_name.mp4 -r 1 frames_temp/video_name/frame_%04d.jpg
```
# 4. Dump annotation in ***video*** mode and unzip

# 5. Generate .csv file with 1_create_ava_formated_gt.py
This script takes **an cvat annotation file** in the **CVAT csv video format (version 1.1)** and converts it into a groundtruth file using formatting used by the AVA dataset

** Annotation **coordinates** are **normalized** using **the width and height of the video**  
** Annotation **video_name** is **CVAT task name**   
** Annotation **second** is **CVAT frame step**  
** Annotation default action list: (p2p:1, xfr:2, background:3)  
now touch_move included: (background:1, xfr:2, touch_move:3)

- Print ground truth to screen
```
    python ./1_create_ava_formated_gt.py cam20-p2p-2.xml
```

- Create ground truth file named clasp_datatset_20200227.txt
```
    python ./1_create_ava_formated_gt.py cam20-p2p-2.xml > ./clasp_datatset_20200227.txt
    or
    python ./1_create_ava_formated_gt.py cam20-p2p-2.xml > ./clasp_datatset_20200227.csv
```

- Append to ground truth file names clasp_datatset_20200227.txt 
```bash
    python ./1_create_ava_formated_gt.py cam20-p2p-2.xml >> ./clasp_datatset_20200227.txt
    or
    python ./1_create_ava_formated_gt.py cam20-p2p-2.xml >> ./clasp_datatset_20200227.csv
```

# 6. Split All Annotations into Train and Val sets
For now all annotations are splitted into Train and Val with ratio of 9:1.
```bash
    python ./2_split_train-val.py path-to-annotations-all.csv
```

# (optional) 7. Add False Alarm Samples as Background

# (optional) 8. Remove False Alarm Backgrounds, which are Actions we need
When adding new annotations with new action label, its possible that those annotations are recorded in False Alarms as 'background' label
```bash
    python 4_clean_FA_with_IOU.py /full/path/to/annotations_with_False_Alarms.csv /full/path/to/annotations_with_new_annotations.csv
```
The new annotation file would contain clean combined annotations with all annotations in 2 files without corrupted background ones generated using false alarms.  
The path for the new annotation file would be  ***/full/path/to/annotations_with_False_Alarms-clean.csv***  
*Don't forget to split the annotations to Train and Val sets
