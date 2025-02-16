import json
import os

def update_spider(file_path, spider_value):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            data[0]['spider'] = spider_value
        else:
            print(f"Invalid JSON format in {file_path}")
            return
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading {file_path}: {e}")

def main():
    # 获取 lem.json 文件中的 spider 值
    lem_file_path = './JN/lem.json'
    spider_value = None
    try:
        with open(lem_file_path, 'r') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            spider_value = data[0].get("spider")
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading {lem_file_path}: {e}")
        return

    if spider_value:
        # 更新 tv.json 和 tvy.json 文件
        update_spider('./JN/tv.json', spider_value)
        update_spider('./JN/tvy.json', spider_value)
    else:
        print("Spider value not found in lem.json")

if __name__ == '__main__':
    main()
