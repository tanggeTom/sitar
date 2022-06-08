import codecs
import csv
import json
import os
import re
import sys
from shutil import copyfile
from sys import exit
import pandas as pd
from pathlib import Path

# 读取csv文件，并完成compacity的赋值
with open('compacity_part4_class.csv', encoding='gbk') as f:
    notfind2 = []
    f_csv = csv.reader(f)
    headers = next(f_csv)
    count = 0
    for row in f_csv:
        print(row)
        filename = row[0].split(".")
        filename = filename[len(filename) - 1]
        print(row)
        # if row[3].find(",") != -1:
        #     sys.exit()
        if re.search("_(old)|(new)_", filename) is not None:  # 不是内部类
            file_list = filename.split("_")
            print(file_list)
            project_name = file_list[0]
            sequence = file_list[1]
            sha = file_list[2]
            if project_name=='jamesproject':
                project_name = 'james-project'
            if project_name=='commonsmath':
                project_name = 'commons-math'
            if project_name=='logginglog4j2':
                project_name = 'logging-log4j2'
            path = "experiment_data//" + project_name
            count+=1
            with open(path + '//' + sha + '.json', "r+", encoding='utf8') as fp:
                json_data = json.load(fp)
                if sequence == 'old':
                    json_data['pre_cyclomatic_complexity'] = row[3]
                if sequence == 'new':
                    json_data['last_cyclomatic_complexity'] = row[3]
                fp.seek(0)
                fp.truncate()
                fp.seek(0)
                fp.write(json.dumps(json_data))
        else:
            notfind2.append(filename)
            print("notfind")
    print('notfind2', notfind2)
    print('count',count)

# 将notfind list中的文件复制到指定位置,并完成类名的更改
# path = "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\"
# des_path = "D:\\google download\\NCL_CSC8016-main\\notfindCompacity\\src\\main\\java"
# notfind3 = []
# pattern_classname = "(abstract )?(final )? ((class)|(interface)|(enum)) .+"  # 匹配类名
# for notfind_file in notfind:
#     print(notfind_file)
#     file_list = notfind_file.split("_")
#     project_name = file_list[0]
#     sequence = file_list[1]
#     sha = file_list[2]
#     # copyfile(path + project_name + "\\" + sequence + "\\" + sha,
#     #          "D:\\google download\\NCL_CSC8016-main\\notfindCompacity\\src\\main\\java\\"+notfind_file)
#     file_data = ""
#     with open(path + project_name + "\\" + sequence + "\\" + sha, "r", encoding="utf8") as fp:
#         print(notfind_file)
#         # lines = fp.readlines()
#         flat = False
#         for line in fp:
#             # print(line)
#             if line.find("*")!=-1:  # 是注释
#                 file_data += line
#                 continue
#             if (re.search(pattern_classname, line) != None or line[0:5]=='class') and not flat:
#                 token = line.split(" ")
#                 count = 0  # class关键字下标
#                 for i in token:
#                     if i == 'class' or i == 'enum' or i == 'interface':
#                         break
#                     count += 1
#                 if count == len(token):  # 匹配上但是找不到关键字就跳过
#                     notfind3.append(notfind_file)
#                     file_data += line
#                     continue
#                 line = line.replace(token[count + 1], notfind_file.split(".java")[0]+" ")  # 替换类名为 newXXXX
#                 flat = True
#                 # print(line)
#             file_data += line
#         if not flat:
#             notfind3.append(notfind_file)
#             print("errornotfind")
#     with open(des_path + "\\" + notfind_file, "w", encoding="utf-8") as f:
#         # print(file_data)
#         f.write(file_data)

# 提取剩下的没有检测compacity的文件
# notfind = []
# path = "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\"
# projects = ['activemq', 'commons-math', 'zeppelin', 'flink', 'cloudstack', 'logging-log4j2', 'storm', 'usergrid',
#             'james-project', 'geode', 'biojava', 'jruby', 'pmd', 'jsoup']
# pattern_classname = "(abstract )?(final )? ((class)|(interface)|(enum)) .+"  # 匹配类名
# count_compacity_0 = 0
# for project in projects:
#     for sequence in ['new', 'old']:
#         for file in os.listdir(path + project + "\\" + sequence):
#             file_data = "" # 保存每一行的信息
#             with open("experiment_data\\" + project + "\\" + file.split('.java')[0] + ".json", "r",
#                       encoding="utf8") as fp:
#                 json_data = json.load(fp)
#                 pre_cyclomatic_complexity = 0 if not json_data.get('pre_cyclomatic_complexity') else json_data[
#                     "pre_cyclomatic_complexity"]
#                 last_cyclomatic_complexity = 0 if not json_data.get('last_cyclomatic_complexity') else json_data[
#                     "last_cyclomatic_complexity"]
#                 # print(type(pre_cyclomatic_complexity))
#                 # print(last_cyclomatic_complexity)
#                 if (sequence == 'new' and last_cyclomatic_complexity == 0) or (sequence == 'old' and pre_cyclomatic_complexity==0 ):  # 存在未提取compacity文件
#                     count_compacity_0+=1
#                     with open(path + project + "\\" + sequence + "\\" + file, "r", encoding="utf8") as fp:
#                         # print(last_cyclomatic_complexity)
#                         # print(pre_cyclomatic_complexity)
#                         print(file)
#                         flat = False
#                         for line in fp:
#                             # print(line)
#                             if line.find("*") != -1:  # 是注释
#                                 file_data += line
#                                 continue
#                             if (re.search(pattern_classname, line) != None or line[0:5] == 'class') and not flat:
#                                 token = line.split(" ")
#                                 count = 0  # class关键字下标
#                                 for i in token:
#                                     if i == 'class' or i == 'enum' or i == 'interface':
#                                         break
#                                     count += 1
#                                 if count == len(token):  # 匹配上但是找不到关键字就跳过
#                                     notfind.append(project + "_" + sequence + "_" + file)
#                                     file_data += line
#                                     continue
#                                 line = line.replace(token[count + 1],
#                                                     project.replace("-","") + "_" + sequence + "_" + file.split(".java")[0] + " ")  # 替换类名为 newXXXX
#                                 flat = True
#                                 # print(line)
#                             file_data += line
#                         if not flat:
#                             notfind.append(project + "_" + sequence + "_" + file)
#                             print("errornotfind")
#                     with open("D:\\google download\\NCL_CSC8016-main\\notfindcompacity_part4\\src\\main\\java\\" + project.replace("-","") + "_" + sequence + "_" + file, "w", encoding="utf-8") as f:
#                         # print(file_data)
#                         f.write(file_data)
# #
# #
# print(count_compacity_0)
# print(notfind)
# ['activemq_new_5f640b61d3d6800b577cf401.java', 'activemq_old_5f640b6ad3d6800b577cf4c1.java', 'james-project_new_5f64551ed3d6800b578395fd.java', 'james-project_new_5f645598d3d6800b5783a143.java']
