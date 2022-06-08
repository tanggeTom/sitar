import json
import os

import sklearn
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
    # print(filename)
    with open(filename, 'r', encoding='utf8') as fp:
        # print(fp.name)
        # print("count")
        try:
            json_data = json.load(fp)
        except:
            print(fp.name)
        # json_data = json.load(fp)
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
        prod_typ = json_data['prod_typ']
        print(filename)
        pre_cyclomatic_complexity = 0 if not json_data.get('pre_cyclomatic_complexity') else json_data["pre_cyclomatic_complexity"]
        last_cyclomatic_complexity = 0 if not json_data.get('last_cyclomatic_complexity') else json_data["last_cyclomatic_complexity"]
        pre_cyclomatic_complexity = str(pre_cyclomatic_complexity).replace(",","") # 存在1,234过千的数字
        last_cyclomatic_complexity = str(last_cyclomatic_complexity).replace(",","")
        cyclomatic_complexity_diff = int(last_cyclomatic_complexity)-int(pre_cyclomatic_complexity)
        json_data.get('insert')
        # if not json_data.get('insert'):
        #     print("noinsert")
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
        # add_total = add_annotation_line + add_call_line + add_classname_line + add_condition_line + add_field_line + add_import_line + add_packageid_line + add_parameter_line + add_return_line
        # del_total = del_call_line + del_annotation_line + del_classname_line + del_condition_line + del_field_line + del_import_line + del_packageid_line + del_parameter_line + del_return_line
        # create_delete =
        # print(type(del_return_line))
        feature = [ add_annotation_line, add_call_line, add_classname_line, add_condition_line, add_field_line,
                   add_import_line, add_packageid_line, add_parameter_line, add_return_line, del_annotation_line,
                   del_call_line, del_classname_line, del_condition_line, del_field_line, del_import_line,
                   del_packageid_line, del_parameter_line, del_return_line,insert_num, update_num, move_num,
                   delete_num, clusters_num, actions_num,pre_cyclomatic_complexity,last_cyclomatic_complexity,cyclomatic_complexity_diff]

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
project_f1s = []
# feature_name = ["add_annotation_line", "add_call_line", "add_classname_line", "add_condition_line", "add_field_line",
#                    "add_import_line", "add_packageid_line", "add_parameter_line", "add_return_line", "del_annotation_line",
#                    "del_call_line", "del_classname_line", "del_condition_line", "del_field_line", "del_import_line",
#                    "del_packageid_line", "del_parameter_line", "del_return_line"]
feature_name = ["add_annotation_line", "add_call_line", "add_classname_line", "add_condition_line", "add_field_line",
                "add_import_line", "add_packageid_line", "add_parameter_line", "add_return_line", "del_annotation_line",
                "del_call_line", "del_classname_line", "del_condition_line", "del_field_line", "del_import_line",
                "del_packageid_line", "del_parameter_line", "del_return_line", "insert_num", "update_num", "move_num",
                "delete_num", "clusters_num", "actions_num","pre_cyclomatic_complexity","last_cyclomatic_complexity","cyclomatic_complexity_diff"]
# projects = ['activemq', 'cloudstack', 'commons-math', 'flink', 'geode', 'james-project', 'logging-log4j2', 'storm',
#        'usergrid', 'zeppelin',
#        'jpacman-framework', 'gson', 'pmd', 'biojava', 'izpack', 'joda-time', 'dnsjava', 'jackson-core',
#        'jruby', 'jsoup']
# projects = ['activemq', 'cloudstack', 'commons-math', 'flink', 'geode', 'james-project', 'logging-log4j2', 'storm','usergrid', 'zeppelin']
projects = ['activemq', 'commons-math','zeppelin','flink','cloudstack', 'logging-log4j2','storm','usergrid','james-project','geode']
# projects = [ 'pmd', 'biojava','jsoup','jruby']
for project in projects:
    positive_num = 0
    negative_num = 0
    features = []
    target = []
    for dir in os.listdir('../experiment_data'):
        if dir == project:
            for file in os.listdir('../experiment_data/' + dir):
                read_json('../experiment_data/' + dir + '/' + file)
    # print(features)
    print('positive', positive_num)  # 打印正负样本数量
    print('negative', negative_num)

    features_np = np.asarray(features, dtype=float)
    target_np = np.asarray(target, dtype=float)
    # 下采样处理
    rus = RandomUnderSampler(random_state=1)
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
    kf = KFold(n_splits=10, shuffle=True, random_state=1)

    # print('seed',sklearn.utils.check_random_state(1))
    # 十折交叉验证
    first = True
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
        per_f1 = []
        gbdt = RandomForestClassifier(random_state=1)
        # 特征重要度
        gbdt2 = gbdt.fit(train, train_target)
        importances = gbdt.feature_importances_
        indices = np.argsort(importances)[::-1]
        predict = gbdt2.predict(test)
        if first:
            for i in indices:
                print("{0} - {1:.3f}".format(feature_name[i], importances[i]))
        first = False
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
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        per_acc.append((TP + TN) / len(predict))
        per_pre.append(precision)
        per_recall.append(recall)
        per_f1.append(2 * precision * recall / (precision + recall))
    project_accs.append(mean(per_acc))
    project_precs.append(mean(per_pre))
    project_recalls.append(mean(per_recall))
    project_f1s.append(mean(per_f1))
    print('mean_recall', mean(per_recall))
    print('mean_pre', mean(per_pre))
    print('mean_acc', mean(per_acc))
    print('mean_f1', mean(per_f1))
    print(classification_report(test_target, predict))
projects.append('Avg')
project_accs.append(mean(project_accs))
project_recalls.append(mean(project_recalls))
project_precs.append(mean(project_precs))
project_f1s.append(mean(project_f1s))
dict = {'Project': projects, 'Acc': project_accs, 'Prec': project_precs, 'Rec': project_recalls,'F1':project_f1s}
df = pd.DataFrame(dict)
print(df)
