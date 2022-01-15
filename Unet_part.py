import torch
import torch.utils.data as data
from torch.autograd import Variable as V
import torchvision
import torchvision.transforms as transform
import cv2
import numpy as np
import os
import torch.nn as nn
import torch.nn.functional as F


class Double_conv(nn.Module):
    # 双层卷积
    # conv2d(kernelsize =3,padding=1)->Batch_Norm->ReLU->conv2d(kernelsize =3,padding=1)->Batch_Norm-<ReLU
    def __init__(self, inchannel, outchannel):  # 进入512*512，出512*512
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(inchannel, outchannel, 3, padding=1),  # N= floor((M-ksize+2*padding)/stride)+1
            nn.BatchNorm2d(outchannel),
            nn.ReLU(inplace=True),  # inplace是否直接修改源

            nn.Conv2d(outchannel, outchannel, 3, padding=1),
            nn.BatchNorm2d(outchannel),
            nn.ReLU(inplace=True),  # inplace是否直接修改源

        )

    def forward(self, x):
        x = self.conv(x)
        return x


class InConv(nn.Module):  # 就是一层双层卷积

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
            nn.MaxPool2d(2),  # 最大池化N=floor(（M+2*padding-kernelsize)/stride)
            Double_conv(inchannel, outchannel)  # 双层卷积
        )

    def forward(self, x):
        return self.Max_Conv(x)


class UP(nn.Module):
    # 上采样-》拼接-》双卷积
    def __init__(self, inchannel, outchannel, Transpose=False):
        super(UP, self).__init__()
        if Transpose:
            self.up = nn.ConvTranspose2d(inchannel, inchannel // 2, kernel_size=2,
                                         stride=2)  # N=(M-1)*stride-2*padding+ksize+output_padding
        else:
            self.up = nn.Sequential(
                nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
                nn.Conv2d(inchannel, inchannel // 2, kernel_size=2, padding=0),
                nn.ReLU(inplace=True)
            )
        self.conv = Double_conv(inchannel, outchannel)

    def forward(self, x1, x2):
        x1 = self.conv(x1)  # x1接受上采样的数据
        diffY = x2.size()[2] - x1.size()[2]
        diffX = x2.size()[3] - x1.size()[3]  # 跳步连接需要调整一下尺寸
        F.pad(x1, [diffX // 2, diffX - diffX // 2, diffY // 2, diffY - diffY // 2])  # 尽可能均匀的将两侧填充
        x = torch.cat([x1, x2], dim=1)  # 按channels相加
        return self.conv(x)
