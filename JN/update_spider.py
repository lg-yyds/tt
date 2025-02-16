import json
import re

def load_json_ignore_errors(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # 用正则表达式修正单引号问题，将单引号替换为双引号
        content = re.sub(r"(\w+):", r'"\1":', content)  # 修正无引号的字段名
        content = content.replace("'", '"')  # 修正单引号为双引号

        try:
            # 尝试加载修复后的 JSON 内容
            return json.loads(content)
        except json.JSONDecodeError:
            print(f"Warning: Unable to fully decode {filename}. Continuing with available data.")
            return {}

def update_spider_value(file_path, spider_value):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = load_json_ignore_errors(file_path)

    # 如果数据有效且包含 'spider' 字段，则进行更新
    if isinstance(data, list) and len(data) > 0 and 'spider' in data[0]:
        data[0]['spider'] = spider_value

    # 保存更新后的内容到文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # 读取 lem.json 文件中的第一个 spider 值
    lem_data = load_json_ignore_errors('./JN/lem.json')

    if isinstance(lem_data, list) and len(lem_data) > 0 and 'spider' in lem_data[0]:
        spider_value = lem_data[0]['spider']
    else:
        print("Warning: lem.json does not contain a valid 'spider' field.")
        return

    # 更新 tv.json 和 tvy.json 文件中的 spider 值
    update_spider_value('./JN/tv.json', spider_value)
    update_spider_value('./JN/tvy.json', spider_value)
    print(f"Updated 'spider' value to: {spider_value}")

if __name__ == "__main__":
    main()
