import _thread
import os
import threading

import git
from shutil import copyfile
import json

project_name = 'logging-log4j2'  # 只需要修改此处
repo_name = 'D:\\BaiduNetdiskDownload\\commit\\' + project_name
repo = git.Repo(repo_name)
commits = repo.iter_commits('release-2.x')
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
# new_path = '{0}_git'.format(save_path)


# 获取所有json中的prod_path和sha
def read_json(project_list, filename):
    # print(os.listdir(filename))
    #已经生产的java,二次执行
    project_list = ["5f64679ad3d6800b57857641.json"]
    already_json = os.listdir("D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\"+project_name+"\\new")
    for per_json in project_list:
        if per_json.split(".json")[0]+".java" in already_json:
            print('skip',per_json)
            continue

        with open(filename + '/' + per_json, 'r', encoding='utf8') as fp:
            per_json = per_json.split(".json")[0]
            print(per_json)
            json_data = json.load(fp)
            prod_path = json_data["prod_path"]
            prod_sha1 = json_data["prod_sha1"]
            for i in range(num):  # 遍历所有commit
                if i == num - 1:  # 第一个commit，肯定没有old文件
                    break
                if str(commits_list[i]) == prod_sha1:
                    find_new, find_old = compare_file(i, prod_path, per_json)
                    if find_new and find_old:
                        print("all find")
                        second = '.\gumtree textdiff ' + project_name + '//' + 'new//' + per_json + ".java " + project_name + '//' + "old//" + per_json + ".java >" + project_name + "\\" + "res\\" + per_json + ".txt"
                        # print(second)
                        content = str(
                            os.system('cd "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin" && ' + second))
                        # print(content)
                    break


# 使用gumtree比较两个文件
def compare_file(new_index, prod_path, per_json):
    new = commits_list[new_index]
    print(new)
    print('tree',new.tree.blobs)
    try:
        repo.index.reset(commit=new.hexsha, working_tree=True)
    except:
        print("except")
        return False, False
    old = commits_list[new_index + 1]

    # new.
    # 记录新版本的文件
    diffs = new.diff(old)
    print(diffs)
    # print(diffs)
    find_new = False
    find_old = False
    for diff in diffs:
        print(diff.a_blob.name)
        if diff.a_blob and diff.a_blob.path.endswith('java') and diff.a_blob.path == prod_path:
            path, filename = os.path.split(diff.a_blob.path)
            print('yes', filename)
            copyfile('{0}/{1}'.format(repo_name, diff.a_blob.path),
                     save_path + '\\' + 'new\\' + per_json + ".java")
            find_new = True
            break

    print(old, commits_list[new_index])
    try:
        repo.index.reset(commit=old.hexsha, working_tree=True)  # 目前聚焦old版本的commit，输出的文件也是旧版的
    except:
        print("except")
        return False, False
    # print(output)
    # 记录旧版本的文件
    for diff in diffs:
        # print('diff', diff)
        if diff.b_blob:
            if diff.a_blob and diff.a_blob.path.endswith('java') and diff.a_blob.path == prod_path:
                path, filename = os.path.split(diff.a_blob.path)
                print('yes', filename)
                copyfile('{0}/{1}'.format(repo_name, diff.b_blob.path),
                         save_path + '\\' + 'old\\' + per_json + ".java")
                find_old = True
                break
            if not diff.a_blob and diff.b_blob.path.endswith('java') and diff.b_blob.path == prod_path:  # 修改之后文件被删除
                path, filename = os.path.split(diff.b_blob.path)
                print('no', filename)
                copyfile('{0}/{1}'.format(repo_name, diff.b_blob.path),
                         save_path + '\\' + 'old\\' + per_json + ".java")
                find_old = True
                break
    return find_new, find_old


project_list = os.listdir("experiment_data//" + project_name)

read_json(project_list, "experiment_data//" + project_name)
