import numpy as np
import torch
import os
import cv2
import Unet
import torchvision.transforms as transform
transformer1 = transform.Compose([
    transform.ToTensor()
]
)
if __name__ == '__main__':
    net = Unet.UnetModel(inchannel=3,outchannel=1)
    net.load_state_dict(torch.load('best_model.pth'))
    net.eval()
    test_path = 'C:/Users/ASUS/Desktop/dachuang/roadtest/data/test/'
    img = cv2.imread(os.path.join(test_path, '10078675_15_2_1_sat.png'))
    cv2.imshow("orignal", img)
    img_tensor = transformer1(img)
    img_tensor = torch.unsqueeze(img_tensor,0)
   # img_tensor = img_tensor.permute(0,1,3,2)


    pred = net(img_tensor)

    pred = torch.squeeze(pred,0)
    pred = pred.permute(1,2,0)

    pred[pred>=0.5]=255
    pred[pred<0.5]=0

    pred = np.array(pred.data.cpu())



    cv2.namedWindow("pred")
    cv2.imshow("pred",pred)
    cv2.waitKey()
    cv2.destroyAllWindows()