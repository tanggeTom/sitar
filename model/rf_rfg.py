import json
import os
from numpy import *
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt


# 读取json，并获取特征
from sklearn.feature_selection import RFE


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
        feature = [add_annotation_line, add_call_line, add_classname_line, add_condition_line, add_field_line,
                   add_import_line, add_packageid_line, add_parameter_line, add_return_line, del_annotation_line,
                   del_call_line, del_classname_line, del_condition_line, del_field_line, del_import_line,
                   del_packageid_line, del_parameter_line, del_return_line]
        features.append(feature)
        if json_data['sample_type'] == "POSITIVE":
            positive_num += 1
            target.append(1)
        else:
            negative_num += 1
            target.append(0)
        return features


# 计算指标
positive_num = 0
negative_num = 0
project_recalls = []
project_accs = []
project_precs = []
projects = ['cloudstack', 'flink', 'geode', 'storm', 'usergrid', 'jpacman-framework', 'biojava', 'dnsjava']
positive_num = 0
negative_num = 0
first = True
features = []
target = []
for project in projects:
    for dir in os.listdir('../experiment_data'):
        if dir == project:
            for file in os.listdir('../experiment_data/' + dir):
                read_json('../experiment_data/' + dir + '/' + file)

features_np = np.asarray(features, dtype=float)
target_np = np.asarray(target, dtype=float)
#     is_train = np.random.uniform(0, 1, len(target)) <= .9
#     if first:
#         train = np.array(features_np)[is_train == True]
#         train_target = np.array(target)[is_train == True]
#         test = np.array(features_np)[is_train == False]
#         test_target = np.array(target)[is_train == False]
#         first = False
#     else:
#         train = np.append(train, np.array(features_np)[is_train == True], axis=0)
#         train_target = np.append(train_target, np.array(target)[is_train == True], axis=0)
#         test = np.append(test, np.array(features_np)[is_train == False], axis=0)
#         test_target = np.append(test_target, np.array(target)[is_train == False], axis=0)
# print('positive', positive_num)  # 打印正负样本数量
# print('negative', negative_num)
rfc = RandomForestClassifier()
# 递归特征消除
rfe = RFE(estimator=rfc, n_features_to_select=1, step=1)
rfe.fit(features_np, target_np)
print(rfe.ranking_)
# #下采样处理
# rus = RandomUnderSampler(random_state=0)
# features_np, target_np = rus.fit_resample(features_np, target_np)
# positive_num = 0
# negative_num = 0
# for i in target_np:
#     if i == 1:
#         positive_num += 1
#     else:
#         negative_num += 1
# print("====undersample====")
# print('positive', positive_num)  # 打印欠采样后的样本数量
# print('negative', negative_num)
# kf = KFold(n_splits=10, shuffle=True)
#
# for i in range(18):
#     RandomForestC
#     train[:][:i]
