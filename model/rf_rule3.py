import json
import os
from numpy import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import KFold


# 读取json，并获取特征
def read_json(filename):
    global positive_num, negative_num
    # print(filename)
    with open(filename, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        # add_annotation_line = json_data['add_annotation_line']
        # add_call_line = json_data['add_call_line']
        # add_classname_line = json_data['add_classname_line']
        # add_condition_line = json_data['add_condition_line']
        add_field_line = json_data['add_field_line']
        # add_import_line = json_data['add_import_line']
        # add_packageid_line = json_data['add_packageid_line']
        # add_parameter_line = json_data['add_parameter_line']
        # add_return_line = json_data['add_return_line']
        # del_annotation_line = json_data['del_annotation_line']
        # del_call_line = json_data['del_call_line']
        # del_classname_line = json_data['del_classname_line']
        # del_condition_line = json_data['del_condition_line']
        del_field_line = json_data['del_field_line']
        # del_import_line = json_data['del_import_line']
        # del_packageid_line = json_data['del_packageid_line']
        # del_parameter_line = json_data['del_parameter_line']
        # del_return_line = json_data['del_return_line']
        # print(type(del_return_line))
        prod_typ = json_data['prod_typ']
        test_typ = json_data['test_typ']
        # print(test_typ)
        # if prod_typ == "CREATE" or prod_typ == "DELETE":
        #     feature = [1]
        # else:
        #     feature = [0]
        feature = [add_field_line,del_field_line]
        features.append(feature)
        if json_data['sample_type'] == "POSITIVE":
            target.append(1)
            positive_num += 1
        else:
            target.append(0)
            negative_num += 1
        #     if test_typ == "DELETE":
        #         target.append(0)
        #     elif test_typ == "CREATE":
        #         target.append(1)


# print(1)
# 计算指标
positive_num = 0
negative_num = 0
project_recalls = []
project_accs = []
project_precs = []
projects = ['activemq', 'cloudstack', 'commons-math', 'flink', 'geode', 'james-project', 'logging-log4j2', 'storm',
            'usergrid', 'zeppelin', ]
for project in projects:
    positive_num = 0
    negative_num = 0
    features = []
    target = []
    for dir in os.listdir('../experiment_data'):
        if dir == project:
            print(dir)
            for file in os.listdir('../experiment_data/' + dir):
                read_json('../experiment_data/' + dir + '/' + file)

    print('positive', positive_num)  # 打印正负样本数量
    print('negative', negative_num)
    print(features)
    features_np = np.asarray(features, dtype=float)
    target_np = np.asarray(target, dtype=float)
    # 下采样处理
    rus = RandomUnderSampler(random_state=0)
    features_np, target_np = rus.fit_resample(features_np, target_np)
    positive_num = 0
    negative_num = 0
    for i in target_np:
        if i == 1:
            positive_num += 1
        else:
            negative_num += 1
    print("====undersample====")
    print('positive', positive_num)  # 打印欠采样后的样本数量
    print('negative', negative_num)
    kf = KFold(n_splits=10, shuffle=True)

    # 十折交叉验证
    for train_index, test_index in kf.split(features_np):
        train = features_np[train_index]
        train_target = target_np[train_index]
        test = features_np[test_index]
        test_target = target_np[test_index]
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        per_pre = []
        per_recall = []
        per_acc = []
        gbdt = RandomForestClassifier()
        gbdt = gbdt.fit(train, train_target)
        predict = gbdt.predict(test)
        print(predict)
        print(len(predict))
        print('max', max(predict))
        print('min', min(predict))
        min_pre = min(predict)
        max_pre = max(predict)
        for i in range(len(predict)):
            # # 归一化处理
            # predict[i] = (predict[i] - min_pre) / (max_pre - min_pre)
            if predict[i] == 1:
                if test_target[i] == 1:
                    TP += 1
                else:
                    FP += 1
            else:
                if test_target[i] == 1:
                    FN += 1
                else:
                    TN += 1

        # print('max', max(predict))
        # print('min', min(predict))
        # print('TP', TP)
        # print('FP', FP)
        # print('FN', FN)
        # print('TN', TN)
        # print('Precision', TP / (TP + FP))
        # print('Recall', TP / (TP + FN))
        # print('Acc', (TP + TN) / len(predict))
        per_acc.append((TP + TN) / len(predict))
        per_pre.append(TP / (TP + FP))
        per_recall.append(TP / (TP + FN))
    project_accs.append(mean(per_acc))
    project_precs.append(mean(per_pre))
    project_recalls.append(mean(per_recall))
    print('mean_recall', mean(per_recall))
    print('mean_pre', mean(per_pre))
    print('mean_acc', mean(per_acc))
    print(classification_report(test_target, predict))
projects.append('Avg')
project_accs.append(mean(project_accs))
project_recalls.append(mean(project_recalls))
project_precs.append(mean(project_precs))
dict = {'Project': projects, 'Acc': project_accs, 'Prec': project_precs, 'Rec': project_recalls}
df = pd.DataFrame(dict)
print(df)
