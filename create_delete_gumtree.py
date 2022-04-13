import os

project_name = "jruby"
path = "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin\\" + project_name
new = os.listdir(path + "\\new")
old = os.listdir(path + "\\old")
res = os.listdir(path + "\\res")
data = os.listdir("experiment_data\\" + project_name)
res = [i.split(".txt")[0] for i in res]
print(res)
data = [i.split(".json")[0] for i in data]
new_more = set(new).difference(old)
old_more = set(old).difference(new)
print('add', len(set(new).difference(old)))
print('delete', len(old_more))
# print(len(old_more))
# print(set(data).difference(set(res)))

# create
for i in new_more:
    print(i)
    per_json = i.split(".java")[0]
    second = '.\gumtree textdiff ' + project_name + '\\' + 'new\\' + per_json + ".java " + project_name + '\\' + "blank.java > " + project_name + "\\" + "res\\" + per_json + ".txt"
    print(second)
    content = str(
        os.system('cd "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin" && ' + second))

# delete
for i in old_more:
    print(i)
    per_json = i.split(".java")[0]
    second = '.\gumtree textdiff ' + project_name + '\\' + "blank.java " + project_name + '\\' + 'old//' + per_json+".java > " + project_name + "\\" + "res\\" + per_json + ".txt"
    print(second)
    content = str(
        os.system('cd "D:\\google download\\gumtree-3.0.0\\gumtree-3.0.0\\bin" && ' + second))
