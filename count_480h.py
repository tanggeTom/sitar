# encoding=gbk
import copy
import math
import time
import re
import pandas as pd

commits_id = []
postpone = []
above_48h = 0
within_24h = 0
within_48h_above_24h = 0
total_commit_file = 0
total_tests = 0
total_same_commit = 0
total_production = []
times_list = dict()
production_by_time = []

for i in range(0, 21):
    times_list["within_" + str((i + 1) * 24) + "_above_" + str(i * 24)] = 0
print(times_list)


def open_file(filename):
    global above_48h
    global total_tests
    global total_commit_file
    global total_same_commit
    global within_24h
    global within_48h_above_24h
    with open(filename, encoding='utf-8') as f:
        content = f.read()
        split = content.split("\n\n")  # 空行分割
        print(type(split))
        list.reverse(split)
        for i in range(len(split)):
            date, productions = get_all_file(split[i].split('\n'), 3)
            # if date.tm_year == 2019 and date.tm_mon == 7:
            #     break
            print('productions' + str(productions))
            date3, tests2 = get_all_file(split[i].split('\n'), 2)
            print('tests2' + str(tests2))
            total_commit_file += len(productions)
            total_tests += len(tests2)
            pre_num = len(productions)
            # 先排除自己的test
            for test in tests2:
                #     print('11111'+str(productions[0].split('.java')))
                productions = [i for i in productions if
                               not re.search(i.split('.java')[0] + 'Test', test, re.IGNORECASE)]
            total_same_commit += pre_num - len(productions)  # 计算在commit中相同时间更新

            pre_num_notsame = len(productions)
            j = i + 1
            time_index = 24  # 时间节点
            pre_left_nums = pre_num_notsame
            while j < len(split):
                date2, tests = get_all_file(split[j].split('\n'), 2)  # test文件
                for test in tests:
                    productions = [i for i in productions if
                                   not re.search(i.split('.java')[0] + 'Test', test, re.IGNORECASE)]
                interval = (time.mktime(date2) - time.mktime(date)) / 3600  # h
                print(interval)
                interval = math.ceil(interval / 24)
                if len(productions) == 0 or interval > 21:
                    break
                j += 1
                if interval <= 0:
                    print('负数')
                    continue
                times_list["within_" + str(interval * 24) + "_above_" + str(interval * 24 - 24)] += pre_left_nums - len(
                    productions)
                # if interval > time_index:
                #     times_list["within_" + str(time_index) + "_above_" + str(time_index - 24)] += pre_left_nums - len(
                #         productions)
                #     time_index += 24
                pre_left_nums = len(productions)




# 获取时间
def format_data(line: str):
    split = line.split('*')
    commits_id.append(split[0])
    date = time.strptime(split[1][:len(split[1]) - 6])
    print(time.asctime(date))
    return date


# 寻找每次commit所有java
def get_all_file(split: list, choice):
    global list_dir
    index = 0
    productions = []
    tests = []
    date = time.localtime()
    for line in split:
        if index == 0:
            date = format_data(line)
        else:
            path = line.split("|")[0]
            path = transfer_path(path)  # 路径更改替换
            for i in list_dir:
                if path.find(i) != -1 and path.find('src/') != -1 and path.find(
                        'java/') != -1:  # 如果存在src/test的前缀，并且是src目录下的
                    file = line.split("|")[0].split("/")[len(line.split("|")[0].split("/")) - 1].split(' ')[0]
                    # print('file',file)
                    if file.endswith('.java'):  # java文件
                        if not re.search('test', file, re.IGNORECASE) and path.find(
                                'src/main') != -1:  # path中必须含有src/main
                            # 下面三行增加存在对应test判断
                            for test in list_test_file:  # 存在对应的test
                                # if file.split('.java')[0] + 'Test'== test:
                                if str(path.split(" ")[1]).replace("main/", "test/").split(".java")[0] + 'Test' == test:
                                    # 改变路径比较src/main->src/test
                                    if choice == 3:
                                        total_production.append(path)
                                    # productions.append(file)
                                    productions.append(
                                        path.split(" ")[1].replace("main/", "test/"))  # 直接修改路径src/main->src/test
                                    break
                        if re.search('test', file, re.IGNORECASE):  # 如果file中含有test，肯定是测试文件
                            # tests.append(file)
                            tests.append(path.split(" ")[1])
                    break
        index += 1
    if choice == 2:
        return date, tests
    else:
        return date, productions


# 寻找存在src/test 的路径
def find_test_dir(filename):
    list_dir = set()
    with open(filename, encoding='utf-8') as f:
        content = f.read()
        split = content.split("\n\n")  # 空行分割
        print(type(split))
        list.reverse(split)
        for commit in split:
            for line in commit.split('\n'):
                # if line.find('{') != -1 or line.find('...') != -1 or line.find('=') != -1:  # 改变文件路径, 存在缩写,
                #     continue
                path = line.split("|")[0]
                path = transfer_path(path)
                if str(path).find('src/test') != -1:
                    list_dir.add(str(path).split('src/test')[0])
    return list_dir


# 寻找src/test路径下所有test
def find_test_file(filename):
    list_dir = set()
    with open(filename, encoding='utf-8') as f:
        content = f.read()
        split = content.split("\n\n")  # 空行分割
        print(type(split))
        list.reverse(split)
        for commit in split:
            for line in commit.split('\n'):
                line = transfer_path(line)  # 更改路径
                if str(line).find('src/test') == -1 or line.find('...') != -1:
                    continue
                file = line.split("|")[0].split("/")[len(line.split("|")[0].split("/")) - 1].split(' ')[0]
                # print('test',file[len(file)-10:])
                if file.endswith('.java'):  # java文件
                    if re.search('test', file[len(file) - 10:], re.IGNORECASE):  # 最后几个字符test匹配
                        list_dir.add(line.split("|")[0].split('.java')[0].split(' ')[1])  # 保留文件路径

    return list_dir


# 改变路径到更改的地方
# {dubbo-metadata-report/dubbo-metadata-report-api/src/test/java/org/apache/dubbo/metadata/store => dubbo-metadata/dubbo-metadata-api/src/test/java/org/apache/dubbo/metadata}/test/JTestMetadataReport4Test.java
def transfer_path(path: str):
    if path.find('=') != -1:
        pre = path.find('{')
        last = path.find('}')
        # print('pre :',path)
        # print('aft :',path[0:pre]+path.split(' => ')[1].split('}')[0]+path[last+1:len(path)])
        # print(path)
        if last != len(path) - 1:
            try:
                return path[0:pre] + path.split(' => ')[1].split('}')[0]
            except:
                print('error_path', path)
        else:
            return path[0:pre] + path.split(' => ')[1].split('}')[0] + path[last + 1:len(path)]
    else:
        return path


# git logs --stat=500 --pretty=format:"%H*%cd*%ar" --date-order > logs_dubbo.txt
# dir_set = set()
# dir_list = ['dubbo-cluster','dubbo-common','dubbo-remoting','dubbo-rpc','dubbo-registry','dubbo-cluster','dubbo-compatible','dubbo-config','dubbo-configcenter','dubbo-container-spring','']
name = "logs/logs_zeppelin.txt"
list_dir = (find_test_dir(name))
list_test_file = find_test_file(name)
df = pd.DataFrame(list_test_file)
df.to_csv('tests.csv')
# for i in list_test_file:
#     print(i)
print(len(list_test_file))
print(list_dir)
open_file(name)
print(total_commit_file)
print('above_48', above_48h)
print('same', total_same_commit)
print('within_24h', times_list["within_24_above_0"]/total_commit_file)
print('within_48h_above_24h', times_list["within_48_above_24"]/total_commit_file)
print('above', above_48h / total_commit_file)
print('0-24', within_24h / total_commit_file)
print('24-48', within_48h_above_24h / total_commit_file)
print('same', total_same_commit / total_commit_file)
print('times_list', times_list)
print(total_tests)
df = pd.DataFrame(total_production)
df.to_csv('production.csv')
