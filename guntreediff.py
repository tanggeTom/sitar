import _thread
import os
import threading

import git
from shutil import copyfile
import json

project_name = 'biojava'  # 只需要修改此处
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
        if per_json.split(".json")[0] + ".txt" in already_json:
            print('skip', per_json)
            continue
        with open(filename + '/' + per_json, 'r', encoding='utf8') as fp:
            per_json = per_json.split(".json")[0]
            print(per_json)
            json_data = json.load(fp)
            prod_path = json_data["prod_path"]
            prod_sha1 = json_data["prod_sha1"]

            for i in range(num):  # 遍历所有commit
                if i == num - 1:  # 第一个commit，肯定没有old文件
                    # new_commit = commits_list[i]
                    # repo.index.reset(commit=new_commit.hexsha, working_tree=True)
                    try:
                        copyfile('{0}/{1}'.format(repo_name, prod_path),
                                 save_path + '\\' + 'new\\' + per_json + ".java")#只保存new文件
                    except:
                        print("文件不存在")
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
    new_commit = commits_list[new_index]
    print(new_commit)
    try:
        repo.index.reset(commit=new_commit.hexsha, working_tree=True)
    except BaseException as e:
        print("except", e)
        return False, False
    old_commit = commits_list[new_index + 1]

    # 记录新版本的文件
    try:
        diffs = new_commit.diff(old_commit)
    except BaseException as e:
        print("except", e)
        return False, False
    # print(diffs)
    find_new = False
    find_old = False
    for perdiff in diffs:
        if perdiff.a_blob and perdiff.a_blob.path.endswith('java') and perdiff.a_blob.path == prod_path:
            path, filename = os.path.split(perdiff.a_blob.path)
            print('yes', filename)
            copyfile('{0}/{1}'.format(repo_name, perdiff.a_blob.path),
                     save_path + '\\' + 'new\\' + per_json + ".java")
            find_new = True
            break

    print(old_commit, commits_list[new_index])
    try:
        repo.index.reset(commit=old_commit.hexsha, working_tree=True)  # 目前聚焦old版本的commit，输出的文件也是旧版的
    except BaseException as e:
        print("except", e)
        return False, False
    # print(output)
    # 记录旧版本的文件
    for perdiff in diffs:
        # print('diff', diff)
        if perdiff.b_blob:
            if perdiff.a_blob and perdiff.a_blob.path.endswith('java') and perdiff.a_blob.path == prod_path:
                path, filename = os.path.split(perdiff.a_blob.path)
                print('yes', filename)
                copyfile('{0}/{1}'.format(repo_name, perdiff.b_blob.path),
                         save_path + '\\' + 'old\\' + per_json + ".java")
                find_old = True
                break
            if not perdiff.a_blob and perdiff.b_blob.path.endswith('java') and perdiff.b_blob.path == prod_path:  # 修改之后文件被删除
                path, filename = os.path.split(perdiff.b_blob.path)
                print('no', filename)
                copyfile('{0}/{1}'.format(repo_name, perdiff.b_blob.path),
                         save_path + '\\' + 'old\\' + per_json + ".java")
                find_old = True
                break
    if not find_new and not find_old:  # 都没找到
        print("all not find")
        second = 'git diff ' + str(new_commit) + "^ " + str(new_commit) + " -- " + prod_path + " > "  "diff\\" + per_json + ".txt"
        print(second)
        with open("D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\"+project_name+"\\diff.txt","a") as f:
            f.write(second+"\n")

    return find_new, find_old


project_list = os.listdir("experiment_data//" + project_name)

read_json(project_list, "experiment_data//" + project_name)
