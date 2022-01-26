import torch
import cv2
import os
import glob
from torch.utils.data import Dataset
import random


class ImageLoader(Dataset):
    def __init__(self, ROOT):
        # 初始化函数，读取所有data_path下的图片
        self.data_path = ROOT
        imagelist = filter(lambda x: x.find('sat') != -1, os.listdir(ROOT))

        trainlist = list(map(lambda x: x[:-8], imagelist))
        self.ids = trainlist

    def augment(self, image, flipCode):
        # 使用cv2.flip进行数据增强，filpCode为1水平翻转，0垂直翻转，-1水平+垂直翻转
        flip = cv2.flip(image, flipCode)
        return flip

    def __getitem__(self, index):
        id = self.ids[index]

        # 读取训练图片和标签图片
        image = cv2.imread(os.path.join(self.data_path, '{}_sat.png'.format(id)))
        label = cv2.imread(os.path.join(self.data_path, '{}_mask.png'.format(id)))
        # 将数据转为单通道的图片
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        label = cv2.cvtColor(label, cv2.COLOR_BGR2GRAY)
        image = image.reshape(3, image.shape[0], image.shape[1])
        label = label.reshape(1, label.shape[0], label.shape[1])
        # 处理标签，将像素值为255的改为1
        if label.max() > 1:
            label = label / 255
        # 随机进行数据增强，为2时不做处理
        flipCode = random.choice([-1, 0, 1, 2])
        if flipCode != 2:
            image = self.augment(image, flipCode)
            label = self.augment(label, flipCode)
        return image, label

    def __len__(self):
        # 返回训练集大小
        return len(self.ids)


if __name__ == "__main__":
    ROOT = r"C:\Users\ASUS\Desktop\dachuang\roadtest\datanew\train"

    imagedataset = ImageLoader(ROOT)
    print("数据个数：", len(imagedataset))
    train_loader = torch.utils.data.DataLoader(dataset=imagedataset,
                                               batch_size=2,
                                               shuffle=True)
    for image, label in train_loader:
        print(image.shape)