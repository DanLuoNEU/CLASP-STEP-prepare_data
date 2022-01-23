Prepare Optical Flow file Folders listed in Annotations. Optical Flow files are generated based on [FlowNet2](https://github.com/NVIDIA/flownet2-pytorch).

# Prerequisite
1. environment py36pt110-FlowNet2.yml 
    - (*py36pt110* would be the name of conda environment)
2. Generated frames folders

    This should be done **AFTER** the frames folders had been generated

3. Annotation file (.csv or .txt)

    Includes all the annotations from train and val annotation files 

# Prepare flow file folders
1. Set up FlowNet2 environment, go to FlowNet2 root(cloned from git link)
2. Activate anaconda env py36pt110, follow the official installation guide
3. Get pretrained FlowNet2 model under pretrained folder under FlowNet2 root
4. Copy the 3-flows/gen_OF_AVA-annot.py to FlowNet2 root and run
```
    python gen_OF_AVA-annot.py \
    --path_annot /path/to/annotation_file \
    --path_model /path/to/pretrained/FlowNet2 \
    --dir_frames /path/to/frames \
    --dir_flows /path/to/flows \
    --num_proc number_of_subprocesses(also the GPUs utilized from GPU 0)
```
# Visualize Flow Files
Check utils.flow_utils.visulize_flow_file(path_flow, /path/to/output/folder) for more details, also mentioned in 3-flows/gen_OF_AVA-annot.py line 130

\*  You can also copy run_a_pair_PILresize.py and gen_OF_AVA-annot_test.py and play with them, Good Luck!