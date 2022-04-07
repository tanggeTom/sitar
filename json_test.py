import json
import os


def read_json(filename):
    prod_paths = []
    prod_sha1s = []
    # for per_json in os.listdir(filename):
    with open(filename, 'r+', encoding='utf8') as fp:
        json_data = json.load(fp)
        fp.seek(0, 0)
        fp.truncate()
        prod_paths.append(json_data["prod_path"])
        prod_sha1s.append(json_data["prod_sha1"])
        json_data["delete"] = 1
        json_data["update"] = 1
        json_data["insert"] = 1
        json_data["move"] = 1
        print(json_data)
        print(type(json_data))
        fp.seek(0, 0)
        # fp.write()
        fp.writelines(json.dumps(json_data).splitlines())
        fp.close()


read_json("1.json")
