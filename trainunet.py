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
import wandb
from tqdm.notebook import tqdm

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

config = dict(
    epochs=10,
    batch_size = 4,
    learning_rate = 0.00001,

)
def train_net(net, data_path,config):
    wandb.init(project="roadtest",config=config)
    config = wandb.config


    # 加载训练集
    ROOT = data_path
    imagelist = filter(lambda x: x.find('sat') != -1, os.listdir(ROOT))
    trainlist = list(map(lambda x: x[:-8], imagelist))
    dataset = data.Imgdataset(trainlist, ROOT)

    data_loader = torch.utils.data.DataLoader(
        dataset,
        config.batch_size,
        shuffle=True)

    net = net.to(device)



    optimizer = torch.optim.Adam(net.parameters(), lr=config.learning_rate)
    criterion = nn.BCEWithLogitsLoss()
    wandb.watch(net, criterion, log="all", log_freq=10)
    best_loss = float('inf')
    total_batches = len(data_loader) * config.epochs
    example_ct = 0  # number of examples seen
    batch_ct = 0

    for e in tqdm(range(config.epochs)):
        print("epoch:",e)
        net.train()

        for image, mask in data_loader:

            optimizer.zero_grad()
            image = image.to(device,dtype=torch.float32)
            mask = mask.to(device,dtype=torch.float32)
            pred = net(image)

            loss = criterion(pred, mask)
            loss.backward()
            optimizer.step()
            example_ct += len(image)
            batch_ct += 1

            if((batch_ct+1)%25)==0:
                wandb.log({"epoch": e, "loss": loss}, step=example_ct)
                print(f"Loss after " + str(example_ct).zfill(5) + f" examples: {loss:.3f}")

    torch.save(net.state_dict(),'net_model.pth')
    wandb.save('net_model.pth')


if __name__ == "__main__":
    net = Unet.UnetModel(inchannel=3, outchannel=1)
    ROOT = "C://Users/ASUS/Desktop/dachuang/roadtest/data/train"

    train_net(net, ROOT,config)
