import json
import os
from numpy import *
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt


# 读取json，并获取特征
from sklearn.model_selection import train_test_split


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
        # print(type(del_return_line))
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
                   del_packageid_line, del_parameter_line, del_return_line,insert_num,update_num,move_num,delete_num,clusters_num,actions_num]
        features.append(feature)
        if json_data['sample_type'] == "POSITIVE":
            positive_num += 1
            target.append(1)
        else:
            negative_num += 1
            target.append(0)
        # target.append(1 if json_data['sample_type'] == "POSITIVE" else 0)
        return features


pres = []  # 精度
recalls = []  # 回召
features = []
target = []
positive_num = 0
negative_num = 0
# print('=======', num)
for dir in os.listdir('../experiment_data'):
    for file in os.listdir('../experiment_data/' + dir):
        read_json('../experiment_data/' + dir + '/' + file)
# 打印正负样本数量
print('positive', positive_num)
print('negative', negative_num)
# 测试集和训练集 0.1-0.9
features_np = np.asarray(features, dtype=float)
target = np.asarray(target, dtype=float)
x_train, x_test, y_train, y_test = train_test_split(features_np, target, test_size = 0.1,random_state=1)

for num in range(0, 50):
    threshold = num / 49
    print('======', threshold)
    # 计算指标
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    rgs = RandomForestRegressor()  ##随机森林模型
    rgs = rgs.fit(x_train,y_train)
    predict = rgs.predict(x_test)
    for i in range(len(predict)):
        if predict[i] >= threshold:
            if y_test[i] == 1:
                TP += 1
            else:
                FP += 1
        else:
            if y_test[i] == 1:
                FN += 1
            else:
                TN += 1
    print('TP', TP)
    print('FP', FP)
    print('FN', FN)
    print('TN', TN)
    print('Precision', TP / (TP + FP))
    print('Recall', TP / (TP + FN))
    pres.append(TP / (TP + FP))
    recalls.append(TP / (TP + FN))
    print('max', max(predict))
    print('min', min(predict))
print(recalls)
print(pres)
plt.plot(recalls, pres)
plt.show()
