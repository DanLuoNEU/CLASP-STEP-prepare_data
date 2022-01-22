# 01/21/2022, Dan
# Because CVAT is using Projects now, a file would deal with one Project .xml should follow
# If dealing with one task .xml, check the earlier version of this file in github
import sys
import xml.etree.ElementTree as etree


# action_list = {"bkgd" : '1',
#                "xfr" : '2',
#                "touch_move": '3'}
# action_list = {"p2p" : '1',
#                 "xfr" : '2',
#                 "background": '3'}
# action_list = {"background": '3',
                # "human" : '4', 
                # "bin": '5'}
action_list = {"tc_mv": '3'}

cvat_file = sys.argv[1]
# cvat_file = '/data/CLASP-DATA/CLASP2-STEP/prepare_data/2-labels/data/2_1-cvat_files/action/KRI/20220120-1cls-tc_mv/20220118-KRI tc_mv-2cls_cvat_files.xml'
tree = etree.parse(cvat_file)
root = tree.getroot()
# Get indexes of the root
dict_tasks={}
start_fid_task = 0
for info_task in root.find('meta').find('project').find('tasks').findall('task'):
    id_task, width, height,FRAME_RATE = 0, 0, 0, 0
    video_data = None

    id_task = int(info_task.find('id').text)
    width = int(info_task.find('original_size').find('width').text)
    height = int(info_task.find('original_size').find('height').text)
    video_data = info_task.find('name').text
    FRAME_RATE = int(info_task.find('frame_filter').text.split('=')[1])

    dict_tasks[id_task]={'start_fid': start_fid_task,
                        'width': width, 'height': height,
                        'name': video_data, 'FRAME_RATE': FRAME_RATE}

    start_fid_task += int(info_task.find('stop_frame').text)
# wONG7Vh87B4,1555,0.142,0.024,0.408,0.978,2,404

# TODO: CHECK FRAME RATE:
# ffmpeg -i ./original-data/cam20-p2p-1.mp4 2>&1 | sed -n "s/.*, \(.*\) fp.*/\1/p"
# FRAME_RATE = int(sys.argv[3])

for index, entry in enumerate(root.findall('track')):
    
    
    person_id = str(index) # '0'
    action = entry.attrib['label']
    id_task = int(entry.attrib['task_id'])
    
    width, height = dict_tasks[id_task]['width'],dict_tasks[id_task]['height']
    video_data = dict_tasks[id_task]['name']
    FRAME_RATE=dict_tasks[id_task]['FRAME_RATE']
    start_fid_task = dict_tasks[id_task]['start_fid']
    frame = str(int(entry[0].attrib['frame'])-start_fid_task)
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


