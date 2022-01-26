import numpy as np
import torch
import os
import cv2
import Unet
import torchvision.transforms as transform
import glob
import data

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

if __name__ == '__main__':
    net = Unet.UnetModel(inchannel=3,outchannel=1).to(device)

    net.load_state_dict(torch.load('net_model.pth',map_location=device))


    net.eval()
    test_path = 'C:/Users/ASUS/Desktop/dachuang/roadtest/data/test/'


    ROOT = test_path
    imagelist = filter(lambda x: x.find('sat') != -1, os.listdir(ROOT))
    trainlist = list(map(lambda x: x[:-8], imagelist))
    dataset = data.Imgdataset(trainlist, ROOT)

    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=1,
        shuffle=True)
    iter = 0
    for image,mask in data_loader:

        img= image.to(device,dtype=torch.float32)
        pred = net(img)
        pred = np.array(pred.data.cpu()[0])[0]

        pred[pred<=0.5]=0
        pred[pred>0.5]=255

        save_path = str(iter)+'.png'
        cv2.imwrite(save_path, pred)
        iter+=1

    #pred = pred.cpu().detach().numpy()






    #cv2.namedWindow("pred")
    #cv2.imshow("pred",pred)
    #cv2.waitKey()
    #cv2.destroyAllWindows()