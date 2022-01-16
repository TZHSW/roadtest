import torch
import torch.utils.data as data
from torch.autograd import Variable as V
import torchvision
import torchvision.transforms as transform
import cv2
import numpy as np
import os
import torch.nn as nn


class Double_conv(nn):
    # 双层卷积
    # conv2d(kernelsize =3,padding=1)->Batch_Norm->ReLU->conv2d(kernelsize =3,padding=1)->Batch_Norm-<ReLU
    def __init__(self, inchannel, outchannel):  # 进入512*512，出512*512
        super(Double_conv, self).__init()
        self.conv = nn.Sequential(
            nn.Conv2d(inchannel, outchannel, 3, padding=1),
            nn.BatchNorm2d(outchannel),
            nn.ReLU(inplace=True),  # inplace是否直接修改源

            nn.Conv2d(outchannel, outchannel, 3, padding=1),
            nn.BatchNorm2d(outchannel),
            nn.ReLU(inplace=True),  # inplace是否直接修改源

        )

    def forward(self, x):
        x = self.conv(x)
        return x


class InConv(nn.Module):  #

    def __init__(self, inchannel, outchannel):
        super(InConv, self).__init__()
        self.conv = Double_conv(inchannel, outchannel)

    def forward(self, x):
        x = self.conv(x)
        return x


class Down(nn.Module):

    def __init__(self, inchannel, outchannel):
        super(Down, self).__init__()
        self.Max_Conv = nn.Sequential(
            nn.MaxPool2d(2),  # 最大池化
            Double_conv(inchannel, outchannel)  # 双层卷积
        )

    def forward(self, x):
        return self.Max_Conv(x)

class UP(nn.Module):

    def