Prepare frame(RGB) Folders listed in Annotations
This should be done after the frames folders had been generated

# Prepared files
original videos in original-data
./originalData.txt(with all video names under ./original-data/* in it, no .mp4/.mkv, just names)

# 1_downSample.sh
* Because we are saving .npy as the optical flow files, downsampled videos can save a lot of space
This bash script is used to generate downsampled videos under ./downsample-data from videos under ./original-data
```
    bash 1_downSample.sh 20191024-training-cam09exp2.mp4
```
# TODO: this can be improved by bash script reading names under ./originalData.txt

# 2_videoSnip.py
This script takes a text file (detailed below) listing filenames of .mp4 data in ./downsample-data/ subdirectory and chops it up into .jpg frames in the ./dataset/ subdirectory.

Here is the resulting directory tree structure:

	./datatset/->
		->/VIDEO_NAME/
			->/0000/-> ...
			->/0001/-> ...
			->/0002/-> ...
				->/01.jpg
				->/02.jpg
				    ...
				->/30.jpg 		# assuming 30 FPS

NOTE: some seconds have extra frames, or/and repeated frames in it's output. This can be the result of ffmpeg using an 'inconvenient keyframe' in determining the encoded time stamp, repeated frames in the original recorded data, or other because of other encoding flaws. These errors do not propogate into future seconds. As in, subdirectory ./datatset/VIDEO_NAME/2000/ will include events from the 2000th second of the video data. One does not need to account for these errors for future frames.

The only way to call the script, see originalData.txt for input file formatting

```
    python ./2_videoSnip.py ./originalData.txt downsample-data( or 'original-data', depending on if downsampling)
```

# 3. Move frame folders under ./dataset to the Dataset frames folder
```
	mv dataset/* /path-to-dataset-frames-folder(/data/CLASP-DATA/CLASP2-STEP/data/frames)
```