from sklearn.datasets import fetch_20newsgroups  # 从sklearn.datasets里导入新闻数据抓取器 fetch_20newsgroups
from sklearn.model_selection import  train_test_split
from sklearn.feature_extraction.text import CountVectorizer  # 从sklearn.feature_extraction.text里导入文本特征向量化模块
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB  # 从sklean.naive_bayes里导入朴素贝叶斯模型
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from numpy import *
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
# 计算指标
features = []
target = []
positive_num = 0
negative_num = 0

for dir in os.listdir('../experiment_data'):
    for file in os.listdir('../experiment_data/' + dir):
        read_json('../experiment_data/' + dir + '/' + file)
    # 打印正负样本数量
print('positive', positive_num)
print('negative', negative_num)
# 测试集和训练集 0.1-0.9
features_np = np.asarray(features, dtype=float)
target_np = np.asarray(target, dtype=float)
is_train = np.random.uniform(0, 1, len(target)) <= .9
# print(is_train)
train = features_np[is_train == True]
train_target = target_np[is_train == True]
test = features_np[is_train == False]
test_target = target_np[is_train == False]

for num in range(0, 80):
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    threshold = num / 79
    print('======', threshold)
    for i in range(1):
        per_pre = []
        per_recall = []
        mnb = BernoulliNB()   # 使用默认配置初始化朴素贝叶斯
        mnb = mnb.fit(train, train_target)
        predict = mnb.predict_proba(test)
        print(predict)
        predict = predict[:,1]
        # predict = mnb.predict(test)
        print(predict)
        print('max', max(predict))
        print('min', min(predict))
        min_pre = min(predict)
        max_pre = max(predict)
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

        print('max', max(predict))
        print('min', min(predict))
        print('TP', TP)
        print('FP', FP)
        print('FN', FN)
        print('TN', TN)
        print('Precision', TP / (TP + FP))
        print('Recall', TP / (TP + FN))
        per_pre.append(TP / (TP + FP))
        per_recall.append(TP / (TP + FN))
    pres.append(mean(per_pre))
    recalls.append(mean(per_recall))
print(recalls)
print(pres)
plt.plot(recalls, pres)
plt.show()
#4.获取结果报告
# print('The Accuracy of Naive Bayes Classifier is:', mnb.score(X_test,y_test))
# print(classification_report(y_test, y_predict, target_names = news.target_names))