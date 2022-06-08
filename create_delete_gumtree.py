import os

project_name = "biojava"
path = "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\" + project_name
new = os.listdir(path + "\\new")
old = os.listdir(path + "\\old")
res = os.listdir(path + "\\res")
data = os.listdir("experiment_data\\" + project_name)
res = [i.split(".txt")[0] for i in res]
print(res)
data = [i.split(".json")[0] for i in data]
data_less = set(data).difference(res)
new_more = set(new).difference(old)
old_more = set(old).difference(new)
print('add', len(new_more))
print('delete', len(old_more))
print('data', data_less)
# print(new_more)

# print(len(old_more))
# print(set(data).difference(set(res)))

already_json = os.listdir("D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\" + project_name + "\\res")
# create
for i in new_more:
    if i.split(".java")[0] + ".txt" in already_json:
        print('skip', i)
        continue
    print(i)
    per_json = i.split(".java")[0]
    second = '.\gumtree textdiff ' + project_name + '\\' + 'new\\' + per_json + ".java " + project_name + '\\' + "blank.java > " + project_name + "\\" + "res\\" + per_json + ".txt"
    print(second)
    content = str(
        os.system('cd "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin" && ' + second))

# delete
for i in old_more:
    if i.split(".java")[0] + ".txt" in already_json:
        print('skip', i)
        continue
    print(i)
    per_json = i.split(".java")[0]
    second = '.\gumtree textdiff ' + project_name + '\\' + "blank.java " + project_name + '\\' + 'old//' + per_json + ".java > " + project_name + "\\" + "res\\" + per_json + ".txt"
    print(second)
    content = str(
        os.system('cd "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin" && ' + second))
