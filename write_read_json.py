import json
import os
from numpy import *
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

delete = 0
create = 0
edit = 0
CC = 0
CD = 0
CE = 0
DC = 0
DD = 0
DE = 0
# CE = 0
EC = 0
ED = 0
EE = 0


# 读取json，并获取特征
def read_json(filename):
    global CC, CD, CE, DC, DD, DE, CE, EC, ED, EE
    # print(filename)CC，CD，CE，DC，DD，DE，CE，EC，ED，ED
    with open(filename, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        prod_typ = json_data["prod_typ"]
        test_typ = json_data["test_typ"]
        if prod_typ == "DELETE":
            if test_typ == "DELETE":
                DD += 1
            elif test_typ == "CREATE":
                DC += 1
            elif test_typ == "EDIT":
                DE += 1
        elif prod_typ == "CREATE":
            if test_typ == "DELETE":
                CD += 1
            elif test_typ == "CREATE":
                CC += 1
            elif test_typ == "EDIT":
                CE += 1
        elif prod_typ == "EDIT":
            if test_typ == "DELETE":
                ED += 1
            elif test_typ == "CREATE":
                EC += 1
            elif test_typ == "EDIT":
                EE += 1
    # print(json_data.get('insert'))
    # del_annotation_line = json_data['del_annotation_line']
    # del_call_line = json_data['del_call_line']
    # del_classname_line = json_data['del_classname_line']
    # del_condition_line = json_data['del_condition_line']
    # del_field_line = json_data['del_field_line']
    # del_import_line = json_data['del_import_line']
    # del_packageid_line = json_data['del_packageid_line']
    # del_parameter_line = json_data['del_parameter_line']
    # del_return_line = json_data['del_return_line']
    # if not json_data.get('insert'):
    #     print("noinsert")
    # if not json_data.get('insert') and (prod_typ =="EDIT") :
    # print(filename)
    # if prod_typ == "DELETE":
    #     delete += 1
    # elif prod_typ == "CREATE":
    #     print('create', filename)
    #     create += 1
    # elif prod_typ == "EDIT":
    #     if del_annotation_line == 0 and del_return_line == 0 and del_parameter_line == 0 and del_packageid_line == 0 and del_import_line == 0 and del_field_line == 0 and del_condition_line == 0 and del_call_line == 0 and del_classname_line == 0:
    #         print('edit',filename)
    #     edit += 1


def write_json(filename: str, project_name):
    print(filename)
    with open(filename, "r", encoding="utf8") as fp:
        content = fp.read()
        insert_num = content.count("insert")
        update_num = content.count("update")
        move_num = content.count("move")
        delete_num = content.count("delete")
        lastname = os.path.split(filename)[1]
        print('last', lastname)
        with open('experiment_data//' + project_name + '//' + lastname.split(".txt")[0] + '.json', "r+",
                  encoding='utf8') as fp:
            print(fp.name)
            json_data = json.load(fp)
            json_data['insert'] = insert_num
            json_data['update'] = update_num
            json_data['move'] = move_num
            json_data['delete'] = delete_num
            if json_data['prod_typ'] == "CREATE" or json_data['prod_typ'] == "DELETE":
                print('create_delete', fp.name)
            fp.seek(0)
            fp.truncate()
            fp.seek(0)
            fp.write(json.dumps(json_data))

projects = ['activemq', 'commons-math','zeppelin','flink','cloudstack', 'logging-log4j2','storm','usergrid','james-project','geode']
project_name = "zeppelin"
path = "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\" + project_name + "\\res"
for i in projects:
    print(i)
    json_path = "experiment_data/" + i
    for file in os.listdir(json_path):
        read_json(json_path + '/' + file)
        # write_json(path + '/' + file,project_name)

print('CC', CC)
print('CD', CD)
print('CE', CE)
print('DC', DC)
print('DD', DD)
print('DE', DE)
print('EC', EC)
print('ED', ED)
print('EE', EE)
