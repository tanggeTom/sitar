import json
import os
from numpy import *
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

delete = 0
create = 0
edit = 0


# 读取json，并获取特征
def read_json(filename):
    global delete, create, edit
    # print(filename)
    with open(filename, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        prod_typ = json_data["prod_typ"]
        print(json_data.get('insert'))
        if not json_data.get('insert'):
            print("noinsert")
        if not json_data.get('insert') and (prod_typ =="EDIT") :
            print(filename)
        if prod_typ == "DELETE":
            delete += 1
        elif prod_typ == "CREATE":
            create += 1
        elif prod_typ == "EDIT":
            edit += 1


def write_json(filename: str,project_name):
    print(filename)
    with open(filename, "r",encoding="utf8") as fp:
        content = fp.read()
        insert_num = content.count("insert")
        update_num = content.count("update")
        move_num = content.count("move")
        delete_num = content.count("delete")
        lastname = os.path.split(filename)[1]
        print('last',lastname)
        with open('experiment_data//'+project_name+'//'+lastname.split(".txt")[0] + '.json', "r+", encoding='utf8') as fp:
            print(fp.name)
            json_data = json.load(fp)
            json_data['insert'] = insert_num
            json_data['update'] = update_num
            json_data['move'] = move_num
            json_data['delete'] = delete_num
            if json_data['prod_typ']=="CREATE" or json_data['prod_typ']=="DELETE":
                print('create_delete',fp.name)
            fp.seek(0)
            fp.truncate()
            fp.seek(0)
            fp.write(json.dumps(json_data))

project_name = "geode"
path = "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\"+project_name+"\\res"
json_path = "experiment_data/"+project_name
for file in os.listdir(path):
    # read_json(json_path + '/' + file)
    write_json(path + '/' + file,project_name)

# print('create', create)
# print('delete', delete)
# print('edit', edit)
