Prepare frame(RGB) Folders with Second(duration) Folder as unit

Prerequisite:
- Python Environment
	- Python >= 3.6
	- opencv-python
	- numpy
- Folder containing all videos needed


# video_snip_multiproc.py
This python script takes videos in a folder as input to get 'xx.jpg' files organized as AVA-format dataset.

Here is the resulting directory tree structure:

```
	./frames/->
		->/VIDEO_NAME/
			->/00000/-> ...
			->/00001/-> ...
			->/00002/-> ...
				->/01.jpg
				->/02.jpg
				    ...
				->/30.jpg 		# assuming 30 FPS
```

Run the python script like below under ***./1-frames*** as root:

```
    python video_snip_multiproc.py
```
- --dir_vid /path/to/videos-directory
	- default path: &emsp; './videos'
- --dir_frames /path/to/frames
	- default path: &emsp; ./frames
- --num_proc number_of_subprocesses
	- default number: &emsp; 8

# Move frame folders under ./frames to the Dataset frames folder
```
	mv frames/* /path-to-dataset-frames-folder(/data/CLASP-DATA/CLASP2-STEP/data/frames)
```