#-*-coding:gb2312-*-
import json
import os
from numpy import *
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from mixedMLP import *
import torch.utils.data as Data  # ����pytorch�����ݴ���ģ��


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
    dataset=train_dataset,  # ���ݼ�
    batch_size=64  # ����С
)
test_dataloader = Data.DataLoader(
    dataset=test_dataset,  # ���ݼ�
    batch_size=64  # ����С
)
# ����ѵ�������һЩ����
total_train_step = 0  # ��¼ѵ���Ĵ���
total_test_step = 0  # ��¼���ԵĴ���
epoch = 10  # ѵ��������
# ������ʧ����
loss_fn = nn.CrossEntropyLoss()
# �Ż���
learning_rate = 1e-2  # 1e-2 = 1 * (10)^(-2) = 1 / 100 = 0.01
optimizer = torch.optim.SGD(mlp.parameters(), lr=learning_rate)

for i in range(epoch):
    print("------�� {} ��ѵ����ʼ------".format(i + 1))

    # ѵ�����迪ʼ
    for data in train_dataloader:
        imgs, targets = data
        outputs = mlp(imgs)  # ��ѵ�������ݷ���
        loss = loss_fn(outputs, targets)  # �õ���ʧֵ

        optimizer.zero_grad()  # �Ż�����������Ҫʹ���Ż��������ݶ�����
        loss.backward()  # ���õõ�����ʧ�����÷��򴫲����õ�ÿһ�������ڵ���ݶ�
        optimizer.step()  # �Բ��������Ż�
        total_train_step += 1  # ������ǽ�����һ��ѵ����ѵ������ +1

        # ֻ��ѵ��������100 ������ʱ��Ŵ�ӡ���ݣ����Լ���һЩû���õ����ݣ����������ҵ���������
        if total_train_step % 100 == 0:
            print("ѵ������: {}, Loss: {}".format(total_train_step, loss))

    # ���֪��ģ����û��ѵ���ã��������дﵽ�Լ���Ҫ������
    # ���ǿ�����ÿ��ѵ����һ�ֺ󣬽���һ�β��ԣ��ڲ������ݼ�����һ�飬�Բ������ݼ��ϵ���ʧ����ȷ���������ǵ�ģ����û��ѵ����

    # ����˼�壬����Ĵ���û���ݶȣ������ǲ�����е���
    total_test_loss = 0
    with torch.no_grad():
        for data in test_dataloader:
            imgs, targets = data
            outputs = mlp(imgs)
            loss = loss_fn(outputs, targets)  # ����� loss ֻ��һ��������(data) ������ģ���ϵ���ʧ
            total_test_loss = total_test_loss + loss  # �������Լ���loss

    print("������Լ��ϵ�loss: {}".format(total_test_loss))
    # writer.add_scalar("test_loss", total_test_loss)
    total_test_loss += 1  # ��������֮��Ҫ +1

    # torch.save(model, "model_{}.pth".format(i))
    # print("ģ���ѱ���")
