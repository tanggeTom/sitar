#-*-coding:gb2312-*-
import torch
from torch import nn
class MLP (nn.Module):
    def __init__(self):
        super (MLP,self).__init__()
        self.linear1 = nn.Linear(18,1024)
        self.linear2 = nn.Linear(6,1024)
        self.linear3 = nn.Linear(2048,2)
        self.dropout1 = nn.Dropout()
        self.dropout2 = nn.Dropout()
        self.dropout3 = nn.Dropout()
        self.dropout4 = nn.Dropout()
        self.activate = torch.relu


    def forward(self,input1,input2):
        output1 = self.linear1(input1)
        output1 = self.activate(output1)
        output1 = self.dropout1(output1)
        output2 = self.linear2(input2)
        output2 = self.activate(output2)
        output2 = self.dropout2(output2)
        output = torch.cat((output1,output2),1)
        output = self.dropout3(output)
        output = self.linear3(output)
        output = self.activate(output)
        output = self.dropout4(output)
        return output

if __name__ == '__main__':
    test1 = torch.ones((64,1,18))
    test2 = torch.ones((64,1,6))

    mlp = MLP()
    print(mlp)
    print(mlp(test1,test2).shape)