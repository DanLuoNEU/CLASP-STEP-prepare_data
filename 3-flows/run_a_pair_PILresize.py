import warnings
warnings.filterwarnings("ignore")

import os
import torch
import numpy as np
import argparse

from models import FlowNet2  # the path is depended on where you create this module
from utils.frame_utils import read_gen, read_gen_PIL  # the path is depended on where you create this module
from utils import flow_utils

path_model= "/home/dan/ws/Backup/2019-Flownet2/flownet2-pytorch-CLASP/pretrained/FlowNet2_checkpoint.pth.tar"
path_img1 = "/home/dan/ws/Backup/2019-Flownet2/flownet2-pytorch-CLASP/exp/frames/0000001.jpg"
path_img2 = "/home/dan/ws/Backup/2019-Flownet2/flownet2-pytorch-CLASP/exp/frames/0000002.jpg"
path_flo = "/home/dan/ws/Backup/2019-Flownet2/flownet2-pytorch-CLASP/exp/of/0000000.flo"
dir_flo = os.path.dirname(path_flo)


if __name__ == '__main__':
    # obtain the necessary args for construct the flownet framework
    parser = argparse.ArgumentParser()
    parser.add_argument('--fp16', action='store_true', help='Run model in pseudo-fp16 mode (fp16 storage fp32 math).')
    # fp16 not supported for FlowNet2 and FlowNet2C
    parser.add_argument("--rgb_max", type=float, default=255.)
    
    args = parser.parse_args()

    # initial a Net
    net = FlowNet2(args).cuda()
    # load the state_dict
    dict = torch.load(path_model)
    net.load_state_dict(dict["state_dict"])

    # load the image pair, you can find this operation in dataset.py
    pim1 = read_gen_PIL(path_img1)
    pim2 = read_gen_PIL(path_img2)
    
    size_norm = (256,256) # Must be multiple of 
    pim1 = np.asarray(pim1.resize(size_norm))
    pim2 = np.asarray(pim2.resize(size_norm))
    images = [pim1, pim2]
    images = np.array(images).transpose(3, 0, 1, 2)
    im = torch.from_numpy(images.astype(np.float32)).unsqueeze(0).cuda()

    # process the image pair to obtian the flow
    result = net(im).squeeze()


    # save flow, I reference the code in scripts/run-flownet.py in flownet2-caffe project
    def writeFlow(name, flow):
        f = open(name, 'wb')
        f.write('PIEH'.encode('utf-8'))
        np.array([flow.shape[1], flow.shape[0]], dtype=np.int32).tofile(f)
        flow = flow.astype(np.float32)
        flow.tofile(f)
        f.flush()
        f.close()


    data = result.data.cpu().numpy().transpose(1, 2, 0)

    writeFlow(path_flo, data)
    flow_utils.visulize_flow_file(path_flo,dir_flo)