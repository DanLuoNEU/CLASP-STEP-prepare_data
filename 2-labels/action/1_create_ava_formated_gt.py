import sys
import xml.etree.ElementTree as etree

action_list = {"bkgd" : '1',
               "xfr" : '2',
               "touch_move": '3'}
# action_list = {"p2p" : '1',
#                 "xfr" : '2',
#                 "background": '3'}
# action_list = {"background": '3',
                # "human" : '4', 
                # "bin": '5'}

cvat_file = sys.argv[1]
# cvat_file = 'CLASP-DATA/CVML-Tools/make_dataset/ava-format/20191024-exp2cam9-training_video.xml'
tree = etree.parse(cvat_file)
root = tree.getroot()
# Get indexes of the root
width, height,FRAME_RATE = 0, 0, 0
video_data = None

width = int(root.find('meta').find('task').find('original_size').find('width').text)
height = int(root.find('meta').find('task').find('original_size').find('height').text)
video_data = root.find('meta').find('task').find('name').text
FRAME_RATE = int(root.find('meta').find('task').find('frame_filter').text.split('=')[1])

# wONG7Vh87B4,1555,0.142,0.024,0.408,0.978,2,404

# width = int(sys.argv[1]) #root[1][0][-1][0].text
# height = int(sys.argv[2]) #root[1][0][-1][1].text
# video_data = root[1][0][1].text

# TODO: CHECK FRAME RATE:
# ffmpeg -i ./original-data/cam20-p2p-1.mp4 2>&1 | sed -n "s/.*, \(.*\) fp.*/\1/p"
# FRAME_RATE = int(sys.argv[3])

for index, entry in enumerate(root.findall('track')):
  
    person_id = str(index) # '0'
    action = entry.attrib['label']
    frame = entry[0].attrib['frame']
    bb = [entry[0].attrib['xtl'], entry[0].attrib['ytl'], entry[0].attrib['xbr'], entry[0].attrib['ybr']]
    for i in range(0, len(bb)):
        if i in [0, 2]:
            bb[i] = "%.3f" % (float(bb[i]) / float(width))
        elif i in [1, 3]:
            bb[i] = "%.3f" % (float(bb[i]) / float(height))

    second = str(int((float(frame) ) / FRAME_RATE)).zfill(5)
    # second = str(int(frame) - 1).zfill(5) # because video starts from 00000 sec

    if action in action_list.keys():
        line = [video_data,second,bb[0],bb[1],bb[2],bb[3],action_list[action], person_id]
        print(",".join(line))
    else:
        line = [video_data,second,bb[0],bb[1],bb[2],bb[3],'-1', person_id]


