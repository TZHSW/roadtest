from unet_model import UNet
from data import ImageLoader
from torch import optim
import torch.nn as nn
import torch

def train_net(net, device, data_path, epochs=40, batch_size=1, lr=0.00001):
    # 加载训练集


    imagedataset = ImageLoader(data_path)

    train_loader = torch.utils.data.DataLoader(dataset=imagedataset,
                                               batch_size=batch_size,
                                               shuffle=True)
    # 定义RMSprop算法
    optimizer = optim.Adam(net.parameters(), lr=lr)
    # 定义Loss算法
    criterion = nn.BCEWithLogitsLoss()
    # best_loss统计，初始化为正无穷
    best_loss = float('inf')
    # 训练epochs次
    for epoch in range(epochs):
        # 训练模式
        net.train()
        # 按照batch_size开始训练
        for image, label in train_loader:
            optimizer.zero_grad()
            # 将数据拷贝到device中
            image = image.to(device=device, dtype=torch.float32)
            label = label.to(device=device, dtype=torch.float32)
            # 使用网络参数，输出预测结果
            pred = net(image)
            # 计算loss
            loss = criterion(pred, label)
            print('Loss/train', loss.item())
            # 保存loss值最小的网络参数
            if loss < best_loss:
                best_loss = loss
                torch.save(net.state_dict(), r'C:\Users\ASUS\Desktop\dachuang\roadtest\newtry\best_model.pth')
            # 更新参数
            loss.backward()
            optimizer.step()

if __name__ == "__main__":
    # 选择设备，有cuda用cuda，没有就用cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # 加载网络，图片单通道1，分类为1。
    net = UNet(n_channels=3, n_classes=1)
    # 将网络拷贝到deivce中
    net.to(device=device)
    # 指定训练集地址，开始训练
    data_path = r"C:\Users\ASUS\Desktop\dachuang\roadtest\datanew\train"
    train_net(net, device, data_path,batch_size=2)