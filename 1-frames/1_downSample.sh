#!/bin/bash

video=$1

if [ -z "$video" ]; then
	exit -1
fi

vid_name=$(basename "$video" .mp4)
echo "down sampling $video ..."

echo "	ffmpeg -i original-data/$video -vf "scale=iw/4:ih/4" downsample-data/$video"
yes | ffmpeg -i original-data/$video -vf "scale=iw/4:ih/4" downsample-data/$video > /dev/null 2>&1 || exit -1

# # BELOW are original
# echo "	ffmpeg -i original-data/$video -vf "scale=iw/4:ih/4" downsample-data/${vid_name}.mp4"
# yes | ffmpeg -i original-data/$video -vf "scale=iw/4:ih/4" downsample-data/${vid_name}.mp4 > /dev/null 2>&1 || exit -1

# if [ ! -d ./downsampled-${vid_name} ]; then
# 	mkdir ./downsampled-${vid_name}
# elif [ -z "$vid_name" ]; then
# 	echo "	deleting old directory..."
# 	# rm -rf ./downsampled-${vid_name}
# 	mkdir ./downsampled-${vid_name}
# fi

# echo "	ffmpeg -i ${vid_name}-quartersized.mp4  -vf \"select=not(mod(n\,10))\" -vsync vfr -q:v 2 ./downsampled-${vid_name}/%09d.jpg"
# yes | ffmpeg -i ${vid_name}-quartersized.mp4  -vf "select=not(mod(n\,10))" -vsync vfr -q:v 2 ./downsampled-${vid_name}/%09d.jpg > /dev/null 2>&1 || exit -1

# echo "	ffmpeg -i ./downsampled-${vid_name}/%09d.jpg sampled_{$vid_name}.mp4"
# yes | ffmpeg -i ./downsampled-${vid_name}/%09d.jpg sampled_${vid_name}.mp4 > /dev/null 2>&1 || exit -1

# if [ -d ./downsampled-${vid_name} ]; then
#         echo "	cleaning..."
# 	# rm -rf ./downsampled-${vid_name}
# fi

# if [ -f ${vid_name}-quartersized.mp4 ]; then
# 	echo "	cleaning..."
# 	rm ${vid_name}-quartersized.mp4
# fi

# echo
# echo "... [ OK ]"
# exit 0
