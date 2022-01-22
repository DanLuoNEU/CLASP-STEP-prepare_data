# README
README file for Preparing all files needed for STEP-variant Action Detection Finetuning

NOTE: Both **CVAT annotations** and the **described scripts** are needed to parse original data into an ava formatted dataset

## 1. RGB Frames in AVA sec format
check ./1-frames/README.md

## 2. Action Annotations
check ./2-labels/action/README.md

## 3. Optical Flow files in sec format
check ./flows/README.md
This is a plain textfile. Each line is the name of a mp4 file in the ./original-data subdirectory.

Below is the output of my call to cat on the originalData.txt file. 
The resulting files are in my ./original-data subdirectory directory.
```
(base) truppr@server:~$ cat ./originalData.txt
cam20-p2p-1.mp4
cam20-p2p-2.mp4
cam20-xfr-1.mp4
cam20-xfr-2.mp4
```

## 4. create_multibb_gt.py
Files needed:
1) xxx.xml - action annotations with action and objects
2) xxx.csv - output normal ava formated ground truth with just action bounding boxes
3) xxx-objects.json - output objects for p2p("give"&"to"), xfr("bin"/"human") BB associated with each sample in the xxx.csv
NOTE: As seen in the sample code provided, there are 28 samples that do not have corresponding "give" and "take" or "bin" and "human" BB associated with it, and will return a KeyError if you querry the json file as a python dictionary for that sample. Each sample is called with the BB for the entire action as a string. See the sample code for examples of both a xfr and p2p action.

```
	python ./create_ava_formated_gt-v3.py --cvat_file=./cvat-files/clasp_cvat_files_v3/cam20-xfr-1.xml --json_file=./yuexi_dataset_20200717-objects.json --csv_file=./yuexi_dataset_20200717.csv
```