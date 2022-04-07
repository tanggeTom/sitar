import os
import git
from shutil import copyfile

repo_name = 'D:\\BaiduNetdiskDownload\\commit\\activemq'
repo = git.Repo(repo_name)
commits = repo.iter_commits('main')
# 读取版本列表
commits_list = list(commits)
num = len(commits_list)
print(commits_list)
print(num)
# 开始版本号
start = 10967

new_path = '{0}_git'.format(repo_name)
# os.makedirs(new_path)
# new为新的一个版本
new = commits_list[2643]
print(new)
repo.index.reset(commit=new.hexsha, working_tree=True)
for index in range(2644,num):
    print('index',index)
    # 当前版本路径
    # version = num - index
    cur_path = '{0}/{1}'.format(new_path, commits_list[index-1])
    os.makedirs(cur_path)
    # 较新文件的路径
    new_file_path = '{0}/new'.format(cur_path)
    os.makedirs(new_file_path)
    # 较旧文件的路径
    old_file_path = '{0}/old'.format(cur_path)
    os.makedirs(old_file_path)

    old = commits_list[index]
    # 创建文件，记录当前版本信息
    with open('{0}/{1}'.format(cur_path, '0.txt'), 'w+', encoding='UTF-8') as f:
        f.write('修订版本号: {0}\n'.format(commits_list[index-1]))
        f.write('提交者: {0}\n'.format(new.author))
        f.write('日期: {0}\n'.format(new.committed_datetime.strftime('%a %b %d %H:%M:%S CST %Y')))
        f.write('注释信息: {0}\n'.format(new.summary))
    # # 创建文件，记录较早版本的信息
    # with open('{0}/{1}'.format(old_file_path, '0.txt'), 'w+') as f:
    #     f.write('修订版本号: {0}\n'.format(version - 1))
    #     f.write('提交者: {0}\n'.format(old.author))
    #     f.write('日期: {0}\n'.format(old.committed_datetime.strftime('%a %b %d %H:%M:%S CST %Y')))
    #     f.write('注释信息: {0}\n'.format(old.summary))

    # 记录新版本的文件
    diffs = new.diff(old)
    for diff in diffs:
        if diff.a_blob and diff.a_blob.path.endswith('java'):
            path, filename = os.path.split(diff.a_blob.path)
            copyfile('{0}/{1}'.format(repo_name, diff.a_blob.path), '{0}/{1}'.format(new_file_path, filename))

    # 记录旧版本的文件
    print(old, commits_list[index], index)
    repo.index.reset(commit=old.hexsha, working_tree=True)
    for diff in diffs:
        if diff.b_blob:
            if diff.a_blob and diff.a_blob.path.endswith('java'):
                path, filename = os.path.split(diff.a_blob.path)
                copyfile('{0}/{1}'.format(repo_name, diff.b_blob.path), '{0}/{1}'.format(old_file_path, filename))
            if not diff.a_blob and diff.b_blob.path.endswith('java'):
                path, filename = os.path.split(diff.b_blob.path)
                copyfile('{0}/{1}'.format(repo_name, diff.b_blob.path), '{0}/{1}'.format(old_file_path, filename))
    # 进入下一个版本
    new = old

# 返回最初版本
repo.index.reset(working_tree=True)
