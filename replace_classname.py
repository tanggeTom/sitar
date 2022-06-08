# coding=gbk
import os
import re

pattern_classname = "(abstract )?(final )? ((class)|(interface)|(enum)) .+{"  # 匹配类名
path = "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\"
projects = ['activemq', 'commons-math', 'zeppelin', 'flink', 'cloudstack', 'logging-log4j2', 'storm', 'usergrid',
            'james-project', 'geode', 'biojava', 'jruby', 'pmd', 'jsoup']
notfind = []
print(re.search(pattern_classname, "public interface Broker extends Region, Service {"))
for project in projects:
    # if i != 'activemq':
    #     break
    project_path = path + project
    project_path_new = project_path + "\\new"
    project_path_old = project_path + "\\old"
    for file in os.listdir(project_path_new):
        file_data = ""
        with open(project_path_new + "\\" + file, "r", encoding="utf8") as fp:
            print(file)
            # lines = fp.readlines()
            flat = False
            for line in fp:
                if line.find("*"):# 是注释
                    continue
                if re.search(pattern_classname, line) != None and not flat:
                    token = line.split(" ")
                    count = 0  # class关键字下标
                    for i in token:
                        if i == 'class' or i == 'enum' or i == 'interface':
                            break
                        count += 1
                    if count == len(token):  # 匹配上但是找不到关键字就跳过
                        notfind.append(project + "_new_" + file)
                        file_data += line
                        continue
                    line = line.replace(token[count + 1], project + "_new_" + file.split(".java")[0])  # 替换类名为 newXXXX
                    flat = True
                    print(line)
                file_data += line
            if not flat:
                notfind.append(project + "_new_" + file)
                print("errornotfind")
        with open(
                "D:\\google download\\NCL_CSC8016-main\\countCompacity\\src\\main\\java\\" + project + "\\new\\" + file,
                "w",
                encoding="utf-8") as f:
            f.write(file_data)
            # print(lines)

    for file in os.listdir(project_path_old):
        file_data = ""
        with open(project_path_old + "\\" + file, "r", encoding="utf8") as fp:
            print(file)
            # lines = fp.readlines()
            flat = False
            for line in fp:
                if re.search(pattern_classname, line) != None and not flat:
                    token = line.split(" ")
                    count = 0
                    for i in token:
                        if i == 'class' or i == 'enum' or i == 'interface':
                            break
                        count += 1
                    if count == len(token):  # 匹配但是找不到就跳过
                        file_data += line
                        continue
                    line = line.replace(token[count + 1], project + "_old_" + file.split(".java")[0])  # 替换类名为 newXXXX
                    flat = True
                    print(line)
                file_data += line
            if not flat:
                notfind.append(project + "_old_" + file)
                print("errornotfind")
        with open(
                "D:\\google download\\NCL_CSC8016-main\\countCompacity\\src\\main\\java\\" + project + "\\old\\" + file,
                "w",
                encoding="utf-8") as f:
            f.write(file_data)
            # print(lines)

print(notfind)
