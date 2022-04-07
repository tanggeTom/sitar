import os
import subprocess

import chardet

project_name = "gson"
path = "D:\\BaiduNetdiskDownload\\commit\\" + project_name + "\\diff"
save_path ="D:\\BaiduNetdiskDownload\\commit\\"+project_name
# os.makedirs('{0}/old'.format(save_path))
# os.makedirs('{0}/new'.format(save_path))
os.chdir(save_path)
# per_json = "1"

for file in os.listdir(path):
    # print(per_json)
    per_json = file.split(".txt")[0]
    print(per_json)
    with open(path + "\\" + file, "r", encoding="UTF-16") as fp:
        content = fp.read()
        index = content.find("index ")
        sha = content[index + 6:index + 28]
        # sha = sha.split(" ")[0]
        print('sha',sha)
        file_sha = sha.split("..")
        if len(file_sha[0])==9:
            sha = content[index + 6:index + 26]
            file_sha = sha.split("..")
        if len(file_sha[0])==8:
            sha = content[index + 6:index + 24]
            file_sha = sha.split("..")
        print(file_sha)
        os.system("git show "+file_sha[0]+" > old/"+per_json+".java")
        os.system("git show "+file_sha[1]+" > new/"+per_json+".java")
        second = '.\gumtree textdiff ' + save_path + '//' + 'new//' + per_json + ".java " + save_path + '//' + "old//" + per_json + ".java > " + project_name + "\\" + "res\\" + per_json + ".txt"
        print(second)
        content = str(
            os.system('cd "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin" && ' + second))
        # print(content)
