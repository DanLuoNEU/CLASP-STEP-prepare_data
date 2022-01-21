Prepare Optical Flow file Folders listed in Annotations
This should be done after the frames folders had been generated


https://github.com/NVIDIA/flownet2-pytorch
# Prepared files
1. environment flow.yml
* possible bugs  
    (1) ImportError: cannot import name 'imread'  
    ```from scipy.misc import imread```  
    It happens when imread is depreciated after version 1.2.0, just install version 1.1.0(@mahbubcseju https://stackoverflow.com/questions/15345790/scipy-misc-module-has-no-attribute-imread)  
    ```pip install scipy==1.1.0```  
2. Generated frames folders
3. Annotation file including all the annotations from train and val annotation files, name with xxx.txt

# Prepare flow file folders
1. Login to Trupprs account
2. activate anaconda env flow
3. Go to path /data/CLASP-DATA/CVML-Tools/flownet, check of_generate file, run code
```
python of_generate.py path_to_annotations_file
```

# Visualize Flow Files
/home/truppr/sandbox/clasp/flownet