# -*-coding:gb2312-*-
import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.linear1 = nn.Linear(18, 32)
        self.linear2 = nn.Linear(6, 32)
        self.linear3 = nn.Linear(64, 2)
        self.dropout1 = nn.Dropout(p=0.1)
        self.dropout2 = nn.Dropout(p=0.1)
        self.dropout3 = nn.Dropout(p=0.1)
        self.dropout4 = nn.Dropout(p=0)
        self.activate = nn.Sigmoid()
        self.activate2 = nn.Softmax(dim=1)

    def forward(self, input):
        input1, input2 = torch.split(input, (18, 6), 1)
        output1 = self.linear1(input1)
        output1 = self.activate(output1)
        output1 = self.dropout1(output1)
        output2 = self.linear2(input2)
        output2 = self.activate(output2)
        output2 = self.dropout2(output2)
        output = torch.cat((output1, output2), 1)
        output = self.dropout3(output)
        output = self.linear3(output)
        output = self.activate2(output)
        # output = self.dropout4(output)
        return output


if __name__ == '__main__':
    test1 = torch.ones((64, 18))
    test24 = torch.ones((64, 24))
    test = torch.rand((1, 5))
    print(test)
    test2 = torch.ones((64, 6))
    b1, b2 = torch.split(test, (4, 1), 1)
    # print(b[0])
    # print(b[1])
    mlp = MLP()
    print(mlp)
    print(mlp(test24).shape)
