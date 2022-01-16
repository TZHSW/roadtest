import torch
import torch.nn as nn
import Unet_part as U


class UnetModel(nn.Module):
    def __init__(self, inchannel, outchannel):
        super(UnetModel, self).__init__()
        self.In = U.InConv(inchannel, 32)
        self.down1 = U.Down(32, 64)
        self.down2 = U.Down(64, 128)
        self.down3 = U.Down(128, 256)
        self.down4 = U.Down(256, 512)

        self.up1 = U.UP(512, 256, Transpose=True)
        self.up2 = U.UP(256, 128, Transpose=True)
        self.up3 = U.UP(128, 64, Transpose=True)
        self.up4 = U.UP(64, 32, Transpose=True)

        self.Out = nn.Conv2d(32, outchannel, kernel_size=1)

    def forward(self, x):
        x1 = self.In(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)

        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        x = self.Out(x)

        return x


if __name__ == '__main__':
    net = UnetModel(inchannel=3, outchannel=3)
    print(net)
