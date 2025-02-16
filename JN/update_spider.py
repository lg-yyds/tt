import json

def update_spider_value(file_path, spider_value):
    # 读取现有的 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 更新第一个 spider 的值
    if isinstance(data, list) and len(data) > 0 and 'spider' in data[0]:
        data[0]['spider'] = spider_value

    # 保存更新后的内容到文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # 读取 lem.json 文件中的第一个 spider 值
    with open('./JN/lem.json', 'r', encoding='utf-8') as f:
        lem_data = json.load(f)

    if isinstance(lem_data, list) and len(lem_data) > 0 and 'spider' in lem_data[0]:
        spider_value = lem_data[0]['spider']
    else:
        print("Error: lem.json does not contain a valid 'spider' field.")
        return

    # 更新 tv.json 和 tvy.json 文件中的 spider 值
    update_spider_value('./JN/tv.json', spider_value)
    update_spider_value('./JN/tvy.json', spider_value)
    print(f"Updated 'spider' value to: {spider_value}")

if __name__ == "__main__":
    main()
