import torch
import torch.utils.data as data
from torch.autograd import Variable as V
import torchvision
import torchvision.transforms as transform
import cv2
import numpy as np
import os

train_transform = transform.Compose([
    transform.ToTensor()
]
)


def default_loader(id, root):
    img = cv2.imread(os.path.join(root, '{}_sat.png'.format(id)))
    mask = cv2.imread(os.path.join(root, '{}_mask.png'.format(id)),cv2.IMREAD_GRAYSCALE)
    # print(img.shape)
    # mask = cv2.imread(os.path.join(root+'{}_field_mask.png').format(id), cv2.IMREAD_GRAYSCALE)
    # print(mask.shape)
    # mask = cv2.imread(os.path.join(root, '{}_mask.png').format(id))
    # img = np.array(img)
    # mask = np.array(mask,np.float32)
    #img = train_transform(img)
    #mask = train_transform(mask)
    mask = torch.tensor(mask)
    img = torch.tensor(img)
    #mask增加channel
    mask = torch.unsqueeze(mask,dim=2)

    img = torch.permute(img,(2,0,1))/255.0*3.2-1.6
    mask = torch.permute(mask, (2, 0, 1))/255.0



    mask[mask>0.5]=1
    mask[mask<0.5]=0
    return img, mask


class Imgdataset(data.Dataset):

    def __init__(self, trainlist, root):
        self.root = root
        self.ids = trainlist
        self.loader = default_loader

    def __getitem__(self, index):
        id = self.ids[index]
        img, mask = self.loader(id, self.root)
        # img = torch.Tensor(img)/255.0
        # mask = torch.Tensor(mask)

        return img, mask

    def __len__(self):
        return len(self.ids)


if __name__ == '__main__':
    ROOT = "C:/Users/ASUS/Desktop/dachuang/road512/"

    imagelist = filter(lambda x: x.find('sat') != -1, os.listdir(ROOT))

    trainlist = list(map(lambda x: x[:-8], imagelist))

    dataset = Imgdataset(trainlist, ROOT)

    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=1,
        shuffle=True)
    for img,mask in data_loader:
        print(img.shape)
        print(mask.shape)
        mask = mask*255.0
        mask= mask.squeeze(dim=0)
        mask= mask.permute((1,2,0)).numpy()

        cv2.imshow("mask",mask)
        cv2.waitKey()
"""


for i, mask in enumerate(data_loader):
    print("第{}个batch，{}".format(i, mask))
dataset[0]
"""
