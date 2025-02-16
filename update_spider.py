import json
import os

def update_spider(file_path, spider_value):
    try:
        # 尝试加载文件内容
        with open(file_path, 'r') as f:
            data = f.read()  # 先读取文件内容为字符串
            
            # 忽略 JSON 解析错误，尽最大努力处理格式不完全正确的文件
            try:
                data = json.loads(data)  # 尝试解析为JSON格式
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON format in {file_path}, attempting to proceed anyway.")

        # 确保数据是列表且第一个元素存在
        if isinstance(data, list) and len(data) > 0:
            data[0]['spider'] = spider_value
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            print(f"Warning: Invalid JSON structure in {file_path}, skipping this file.")

    except FileNotFoundError:
        print(f"File not found: {file_path}")

def main():
    # 获取 lem.json 文件中的 spider 值
    lem_file_path = './JN/lem.json'  # 修改为相对路径
    spider_value = None
    try:
        with open(lem_file_path, 'r') as f:
            data = f.read()  # 先读取文件内容为字符串
            
            # 忽略 JSON 解析错误，尽最大努力处理格式不完全正确的文件
            try:
                data = json.loads(data)  # 尝试解析为JSON格式
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON format in {lem_file_path}, attempting to proceed anyway.")
                data = []  # 如果 JSON 无法解析，使用空列表，避免错误

        # 提取 spider 值
        if isinstance(data, list) and len(data) > 0:
            spider_value = data[0].get("spider")
        else:
            print("Warning: No valid spider field found in lem.json")

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
