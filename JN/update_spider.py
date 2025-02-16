import json
import os

def update_spider(file_path, spider_value):
    try:
        # 读取文件内容，不管格式如何
        with open(file_path, 'r') as f:
            data = f.read()  # 读取文件内容为字符串
            try:
                # 尝试解析 JSON 数据
                data = json.loads(data)
            except json.JSONDecodeError:
                data = []  # 如果解析错误，设为一个空列表，避免崩溃

        # 无论格式如何，只要数据是列表，就更新第一个元素的 spider 值
        if isinstance(data, list):
            if len(data) > 0:
                data[0]['spider'] = spider_value
            else:
                data.append({'spider': spider_value})  # 如果列表为空，添加一个新的字典
        else:
            data = [{'spider': spider_value}]  # 如果数据格式不对，直接创建一个包含 spider 的字典

        # 将更新后的数据写回文件
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # 获取 lem.json 文件中的 spider 值
    lem_file_path = './lem.json'  # 修改为相对路径
    spider_value = None
    try:
        with open(lem_file_path, 'r') as f:
            data = f.read()  # 读取文件内容为字符串
            try:
                data = json.loads(data)  # 尝试解析 JSON 格式
            except json.JSONDecodeError:
                data = []  # 如果格式错误，设为空列表
        print(f"Data from lem.json: {data}")  # 打印读取的数据

        # 检查是否找到 spider 值
        if isinstance(data, list) and len(data) > 0:
            spider_value = data[0].get("spider")
            print(f"Found spider value: {spider_value}")  # 打印找到的 spider 值

    except FileNotFoundError:
        print(f"File not found: {lem_file_path}")
        return
    except Exception as e:
        print(f"Error reading {lem_file_path}: {e}")

    if spider_value:
        # 更新 tv.json 和 tvy.json 文件
        update_spider('./tv.json', spider_value)  # 修改为相对路径
        update_spider('./tvy.json', spider_value)  # 修改为相对路径
    else:
        print("Spider value not found in lem.json")

if __name__ == '__main__':
    main()
