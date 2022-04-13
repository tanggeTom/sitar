import _thread
import os
import threading

import git
from shutil import copyfile
import json

project_name = 'jruby'  # 只需要修改此处
repo_name = 'D:\\BaiduNetdiskDownload\\commit\\' + project_name
repo = git.Repo(repo_name)
commits = repo.iter_commits('master')
# 读取版本列表
commits_list = list(commits)
num = len(commits_list)
print(commits_list)
# print(commits_list[0])
print(num)
save_path = "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\" + project_name


# 创建对应的文件夹
# os.makedirs('{0}/old'.format(save_path))
# os.makedirs('{0}/new'.format(save_path))
# os.makedirs('{0}/res'.format(save_path))

# os.makedirs('{0}/diff'.format(save_path))
# new_path = '{0}_git'.format(save_path)


# 获取所有json中的prod_path和sha
def read_json(project_list, filename):
    # print(os.listdir(filename))
    # 已经生产的java,二次执行
    already_json = os.listdir("D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\" + project_name + "\\res")
    for per_json in project_list:
        with open(filename + '/' + per_json, 'r', encoding='utf8') as fp:
            if per_json.split(".json")[0] + ".txt" in already_json:
                print('skip', per_json)
                continue
            per_json = per_json.split(".json")[0]
            print(per_json)
            json_data = json.load(fp)
            prod_path = json_data["prod_path"]
            prod_sha1 = json_data["prod_sha1"]
            for i in range(num):  # 遍历所有commit
                if str(commits_list[i]) == prod_sha1:
                    new = commits_list[i]
                    second = 'git diff ' + str(new) + "^ " + str(
                        new) + " -- " + prod_path + " > "  "diff\\" + per_json + ".txt"
                    print(second)
                    with open("D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\" + project_name + "\\diff.txt",
                              "a") as f:
                        f.write(second + "\n")




project_list = os.listdir("experiment_data//" + project_name)

read_json(project_list, "experiment_data//" + project_name)
