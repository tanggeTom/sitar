import json

import numpy as np
import pandas as pd
from numpy import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os

# 读取json，并获取特征
def read_json(filename):
    positive_num = 0
    negative_num = 0
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
        # features_np = np.asarray(features, dtype=float)
        # print(json_data['prod_typ'])
        features.append(feature)
        if json_data['sample_type'] == "POSITIVE":
            positive_num += 1
            target.append(1)
        else:
            negative_num += 1
            target.append(0)
        # target.append(1 if json_data['sample_type'] == "POSITIVE" else 0)
        return positive_num, negative_num


pres = []  # 精度
recalls = []  # 回召

# 计算指标
features = []
target = []
# positive_num = 0
# negative_num = 0

# print('=======', num)
ASF = ['activemq', 'cloudstack', 'flink', 'geode', 'james-project', 'logging-log4j2', 'storm', 'usergrid', 'zeppelin',
       'commons-math']
train_pos = 0
train_neg = 0
for dir in os.listdir('../experiment_data'):
    if dir in ASF:
        for file in os.listdir('../experiment_data/' + dir):
            positive_num, negative_num = read_json('../experiment_data/' + dir + '/' + file)
            train_pos += positive_num
            train_neg += negative_num
features_train = np.asarray(features, dtype=float)
target_train = np.asarray(target, dtype=float)
# print(features)
print('len_train', len(features))
print('positive', train_pos)  # 打印正负样本数量
print('negative', train_neg)
# 收集预测数据
project_recalls = []
project_accs = []
project_precs = []
test_project = ['jpacman-framework', 'gson', 'pmd', 'biojava', 'izpack', 'joda-time', 'dnsjava', 'jackson-core',
                'jruby', 'jsoup']
for project in test_project:
    print('project',project)
    pred_pos = 0
    pred_neg = 0
    features = []
    target = []
    for dir in os.listdir('../experiment_data'):
        if dir == project:
            for file in os.listdir('../experiment_data/' + dir):
                positive_num, negative_num = read_json('../experiment_data/' + dir + '/' + file)
                pred_pos += positive_num
                pred_neg += negative_num
    print('positive', pred_pos)  # 打印正负样本数量
    print('negative', pred_neg)
    # print(features)
    print('len_pred', len(features))
    features_pred = np.asarray(features, dtype=float)
    target_pred = np.asarray(target, dtype=float)

    # 取十次平均值
    for i in range(10):
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        per_pre = []
        per_recall = []
        per_acc = []
        gbdt = RandomForestClassifier()
        gbdt = gbdt.fit(features_train, target_train)
        predict = gbdt.predict(features_pred)
        # print(predict)
        # print(len(predict))
        # print('max', max(predict))
        # print('min', min(predict))
        min_pre = min(predict)
        max_pre = max(predict)
        for i in range(len(predict)):
            # # 归一化处理
            # predict[i] = (predict[i] - min_pre) / (max_pre - min_pre)
            if predict[i] == 1:
                if target_pred[i] == 1:
                    TP += 1
                else:
                    FP += 1
            else:
                if target_pred[i] == 1:
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
    # print(recalls)
    # print(pres)
    print(classification_report(target_pred, predict))
test_project.append('Avg')
project_accs.append(mean(project_accs))
project_recalls.append(mean(project_recalls))
project_precs.append(mean(project_precs))
dict = {'Project': test_project, 'Acc': project_accs, 'Prec': project_precs, 'Rec': project_recalls}
df = pd.DataFrame(dict)
print(df)
