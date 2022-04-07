import json
import os
from numpy import *
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import matplotlib.pyplot as plt


# 读取json，并获取特征
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
is_train = np.random.uniform(0, 1, len(target)) <= .9
# print(is_train)
train = features_np[is_train == True]
train_target = target[is_train == True]
test = features_np[is_train == False]
test_target = target[is_train == False]
# print(len(train))
# print(len(train_target))
# print(len(test))
# print(len(test_target))

svmm = svm.SVC(probability=True)
svmm = svmm.fit(train, train_target)
predict = svmm.predict_proba(test)
print(predict)
predict = predict[:, 1]
# predict = mnb.predict(test)
print(predict)
print('max', max(predict))
print('min', min(predict))
min_pre = min(predict)
max_pre = max(predict)
for num in range(0, 50):
    threshold = num / 49
    print('======', threshold)
    # 计算指标
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    for i in range(len(predict)):
        # 归一化处理
        predict[i] = (predict[i] - min_pre) / (max_pre - min_pre)
        if predict[i] >= threshold:
            if test_target[i] == 1:
                TP += 1
            else:
                FP += 1
        else:
            if test_target[i] == 1:
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
    # print('max', max(predict))
    # print('min', min(predict))
# print("===pres===")
# print('mean', mean(pres))
# print('max', max(pres))
# print('min', min(pres))
# print("===recalls===")
# print('mean', mean(recalls))
# print('max', max(recalls))
# print('min', min(recalls))
print(recalls)
print(pres)
plt.plot(recalls, pres)
plt.show()
