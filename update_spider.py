import json
import os

def update_spider(file_path, spider_value):
    try:
        # 尝试加载文件并捕获格式错误
        with open(file_path, 'r') as f:
            data = f.read()  # 先读取文件内容为字符串
            try:
                data = json.loads(data)  # 尝试解析为JSON格式
            except json.JSONDecodeError:
                print(f"Invalid JSON format in {file_path}, skipping this file.")
                return  # 如果格式错误，跳过文件

        # 如果文件是列表，并且第一个元素存在
        if isinstance(data, list) and len(data) > 0:
            data[0]['spider'] = spider_value
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            print(f"Invalid JSON structure in {file_path}, skipping this file.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def main():
    # 获取 lem.json 文件中的 spider 值
    lem_file_path = './JN/lem.json'  # 修改为相对路径
    spider_value = None
    try:
        with open(lem_file_path, 'r') as f:
            data = f.read()  # 先读取文件内容为字符串
            try:
                data = json.loads(data)  # 尝试解析为JSON格式
            except json.JSONDecodeError:
                print(f"Invalid JSON format in {lem_file_path}, skipping this file.")
                return  # 如果格式错误，跳过文件
        if isinstance(data, list) and len(data) > 0:
            spider_value = data[0].get("spider")
        else:
            print("No valid spider field found in lem.json")

    except FileNotFoundError:
        print(f"File not found: {lem_file_path}")
        return

    if spider_value:
        # 更新 tv.json 和 tvy.json 文件
        update_spider('./JN/tv.json', spider_value)  # 修改为相对路径
        update_spider('./JN/tvy.json', spider_value)  # 修改为相对路径
    else:
        print("Spider value not found in lem.json")

if __name__ == '__main__':
    main()
