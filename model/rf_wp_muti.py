import json
import os
from numpy import *
import numpy as np
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
    global SSC, SSE, SSD
    # print(filename)
    with open(filename, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        prod_typ = json_data['prod_typ']
        test_typ = json_data['test_typ']
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
        create_delete = 0
        actions_num = delete_num + move_num + update_num + insert_num
        # print(type(del_return_line))
        feature = [add_annotation_line, add_call_line, add_classname_line, add_condition_line, add_field_line,
                   add_import_line, add_packageid_line, add_parameter_line, add_return_line, del_annotation_line,
                   del_call_line, del_classname_line, del_condition_line, del_field_line, del_import_line,
                   del_packageid_line, del_parameter_line, del_return_line,insert_num,update_num,move_num,delete_num,clusters_num,actions_num]

        features.append(feature)
        if json_data['sample_type'] == "POSITIVE":
            if test_typ == 'EDIT':
                SSE += 1
                target.append('SSE')
            if test_typ == 'CREATE':
                SSC += 1
                target.append('SSC')
            if test_typ == 'DELETE':
                target.append('SSD')
                SSD += 1
            positive_num += 1
            # target.append(1)
        else:
            negative_num += 1
            target.append('NC')
        return features


# 计算指标
positive_num = 0
negative_num = 0

project_recalls = []
project_accs = []
project_precs = []
projects = ['storm','usergrid','flink']
for project in projects:
    # positive_num = 0
    # negative_num = 0
    SSC = 0
    SSE = 0
    SSD = 0
    print('project', project)
    features = []
    target = []
    for dir in os.listdir('../experiment_data'):
        if dir == project:
            for file in os.listdir('../experiment_data/' + dir):
                read_json('../experiment_data/' + dir + '/' + file)

    print('positive', positive_num)  # 打印正负样本数量
    print('negative', negative_num)
    print('SSE', SSE)
    print('SSC', SSC)
    print('SSD', SSD)
    features_np = np.asarray(features, dtype=str)
    target_np = np.asarray(target, dtype=str)
    # 下采样处理
    # rus = RandomUnderSampler(random_state=0)
    # features_np, target_np = rus.fit_resample(features_np, target_np)
    # # positive_num = 0
    # negative_num = 0
    # SSC = 0
    # SSE = 0
    # SSD = 0
    # for i in target_np:
    #     if i == 1:
    #         SSE += 1
    #     if i == 2:
    #         SSC += 1
    #     if i == 3:
    #         SSD += 1
    #     else:
    #         negative_num += 1
    # print("====undersample====")  # 打印欠采样后的样本数量
    # print('SSE', SSE)
    # print('SSC', SSC)
    # print('SSD', SSD)
    # print('negative', negative_num)
    kf = KFold(n_splits=10, shuffle=True,random_state=1)
    dict_res = {}
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
        # SSC_SSC=0
        # SSC_SSE=0
        # SSC_SSD=0
        # SSC_NC=0
        # SSD_SSC =0
        # SSD_SSD=0
        # SSD_SSE=0
        # SSD_NC=0
        # SSD

        right = 0
        wrong = 0
        per_pre = []
        per_recall = []
        per_acc = []
        gbdt = RandomForestClassifier(random_state=1)
        gbdt = gbdt.fit(train, train_target)
        predict = gbdt.predict(test)
        min_pre = min(predict)
        max_pre = max(predict)
        for i in range(len(predict)):
            # if predict[i] =='SSC':
            #     if test_target[i]=='SSC':
            #
            res = predict[i] + "_" + test_target[i]
            if res not in dict_res.keys():
                dict_res[res] = 1
            else:
                dict_res[res] += 1

            if predict[i] == test_target[i]:
                right += 1
            else:
                wrong += 1
        # print('max', max(predict))
        # print('min', min(predict))
        # print('TP', TP)
        # print('FP', FP)
        # print('FN', FN)
        # print('TN', TN)
        # print('Precision', TP / (TP + FP))
        # print('Recall', TP / (TP + FN))
        # print('Acc', (TP + TN) / len(predict))
        per_acc.append((right) / len(predict))
        # per_pre.append(TP / (TP + FP))
        # per_recall.append(TP / (TP + FN))
    project_accs.append(mean(per_acc))
    # project_precs.append(mean(per_pre))
    # project_recalls.append(mean(per_recall))
    # print('mean_recall', mean(per_recall))
    # print('mean_pre', mean(per_pre))
    print('mean_acc', mean(per_acc))
    print(classification_report(test_target, predict))
    print(dict_res)
projects.append('Avg')
project_accs.append(mean(project_accs))
# project_recalls.append(mean(project_recalls))
# project_precs.append(mean(project_precs))
dict = {'Project': projects, 'Acc': project_accs}
df = pd.DataFrame(dict)
print(df)
