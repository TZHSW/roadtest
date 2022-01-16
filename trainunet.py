import torch
import torch.utils.data as data
import torch.nn as nn
from torch.autograd import Variable as V
import torchvision
import torchvision.transforms as transform
import cv2
import numpy as np
import os
import Unet
import data


def train_net(net, data_path, epochs=40, batch_size=1, lr=0.00001):
    # 加载训练集
    ROOT = data_path
    imagelist = filter(lambda x: x.find('sat') != -1, os.listdir(ROOT))
    trainlist = list(map(lambda x: x[:-8], imagelist))
    dataset = data.Imgdataset(trainlist, ROOT)

    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size,
        shuffle=True)

    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    loss_f = nn.BCEWithLogitsLoss()
    best_loss = float('inf')

    for e in range(epochs):
        print("epoch:",e)
        net.train()

        for image, mask in data_loader:

            optimizer.zero_grad()
            pred = net(image)

            loss = loss_f(pred, mask)

            if loss < best_loss:
                best_loss = loss
                torch.save(net.state_dict(), 'best_model.pth')

            loss.backward()
            optimizer.step()
    print (best_loss)
    return best_loss

if __name__ == "__main__":
    net = Unet.UnetModel(inchannel=3, outchannel=1)
    ROOT = "C://Users/ASUS/Desktop/dachuang/road512"

    loss = train_net(net, ROOT,10,4)
    print(loss)