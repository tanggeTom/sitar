#-*-coding:gb2312-*-
import json
import os
from numpy import *
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from mixedMLP import *
import torch.utils.data as Data  # 导入pytorch的数据处理模块


def read_json(filename):
    global positive_num, negative_num
    # print(filename)
    with open(filename, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        add_annotation_line = json_data['add_annotation_line']
        add_call_line = json_data['add_call_line']
        add_classname_line = json_data['add_classname_line']
        add_condition_line = json_data['add_condition_line']
        add_field_line = json_data['add_field_line']
        add_import_line = json_data['add_import_line']
        add_packageid_line = json_data['add_packageid_line']
        add_parameter_line = json_data['add_parameter_line']
        add_return_line = json_data['add_return_line']
        del_annotation_line = json_data['del_annotation_line']
        del_call_line = json_data['del_call_line']
        del_classname_line = json_data['del_classname_line']
        del_condition_line = json_data['del_condition_line']
        del_field_line = json_data['del_field_line']
        del_import_line = json_data['del_import_line']
        del_packageid_line = json_data['del_packageid_line']
        del_parameter_line = json_data['del_parameter_line']
        del_return_line = json_data['del_return_line']
        insert_num = 0 if not json_data.get('insert') else json_data["insert"]
        update_num = 0 if not json_data.get('update') else json_data["update"]
        move_num = 0 if not json_data.get('move') else json_data["move"]
        delete_num = 0 if not json_data.get('delete') else json_data["delete"]
        clusters_num = 0
        if insert_num != 0:
            clusters_num += 1
        if update_num != 0:
            clusters_num += 1
        if move_num != 0:
            clusters_num += 1
        if delete_num != 0:
            clusters_num += 1
        actions_num = delete_num + move_num + update_num + insert_num

    feature = [add_annotation_line, add_call_line, add_classname_line, add_condition_line, add_field_line,
               add_import_line, add_packageid_line, add_parameter_line, add_return_line, del_annotation_line,
               del_call_line, del_classname_line, del_condition_line, del_field_line, del_import_line,
               del_packageid_line, del_parameter_line, del_return_line, insert_num, update_num, move_num,
               delete_num, clusters_num, actions_num]
    features.append(feature)
    if json_data['sample_type'] == "POSITIVE":
        positive_num += 1
        target.append(1)
    else:
        negative_num += 1
        target.append(0)
    # target.append(1 if json_data['sample_type'] == "POSITIVE" else 0)
    return features


features = []
target = []
positive_num = 0
negative_num = 0
for dir in os.listdir('../experiment_data'):
    for file in os.listdir('../experiment_data/' + dir):
        read_json('../experiment_data/' + dir + '/' + file)
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.1, random_state=1)
train_dataset = Data.TensorDataset(X_train, y_train)
test_dataset = Data.TensorDataset(X_test, y_test)
train_dataloader = Data.DataLoader(
    dataset=train_dataset,  # 数据集
    batch_size=64  # 批大小
)
test_dataloader = Data.DataLoader(
    dataset=test_dataset,  # 数据集
    batch_size=64  # 批大小
)
# 设置训练网络的一些参数
total_train_step = 0  # 记录训练的次数
total_test_step = 0  # 记录测试的次数
epoch = 10  # 训练的轮数
# 创建损失函数
loss_fn = nn.CrossEntropyLoss()
# 优化器
learning_rate = 1e-2  # 1e-2 = 1 * (10)^(-2) = 1 / 100 = 0.01
optimizer = torch.optim.SGD(mlp.parameters(), lr=learning_rate)

for i in range(epoch):
    print("------第 {} 轮训练开始------".format(i + 1))

    # 训练步骤开始
    for data in train_dataloader:
        imgs, targets = data
        outputs = mlp(imgs)  # 将训练的数据放入
        loss = loss_fn(outputs, targets)  # 得到损失值

        optimizer.zero_grad()  # 优化过程中首先要使用优化器进行梯度清零
        loss.backward()  # 调用得到的损失，利用反向传播，得到每一个参数节点的梯度
        optimizer.step()  # 对参数进行优化
        total_train_step += 1  # 上面就是进行了一次训练，训练次数 +1

        # 只有训练步骤是100 倍数的时候才打印数据，可以减少一些没有用的数据，方便我们找到其他数据
        if total_train_step % 100 == 0:
            print("训练次数: {}, Loss: {}".format(total_train_step, loss))

    # 如何知道模型有没有训练好，即有咩有达到自己想要的需求
    # 我们可以在每次训练完一轮后，进行一次测试，在测试数据集上跑一遍，以测试数据集上的损失或正确率评估我们的模型有没有训练好

    # 顾名思义，下面的代码没有梯度，即我们不会进行调优
    total_test_loss = 0
    with torch.no_grad():
        for data in test_dataloader:
            imgs, targets = data
            outputs = mlp(imgs)
            loss = loss_fn(outputs, targets)  # 这里的 loss 只是一部分数据(data) 在网络模型上的损失
            total_test_loss = total_test_loss + loss  # 整个测试集的loss

    print("整体测试集上的loss: {}".format(total_test_loss))
    # writer.add_scalar("test_loss", total_test_loss)
    total_test_loss += 1  # 测试完了之后要 +1

    # torch.save(model, "model_{}.pth".format(i))
    # print("模型已保存")
