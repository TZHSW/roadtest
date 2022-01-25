import torch
import torch.utils.data as data
from torch.autograd import Variable as V
import torchvision
import torchvision.transforms as transform
import cv2
import numpy as np
import os
ROOT = "C://Users/ASUS/Desktop/dachuang/road512/"
id = 1
img = cv2.imread(os.path.join(ROOT, '10078675_15_0_0_sat.png'))

