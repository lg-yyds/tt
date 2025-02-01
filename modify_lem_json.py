import json
import re

# 读取文件
with open("JN/lem.json", "r", encoding="utf-8") as f:
    raw_data = f.read()

# 修复单引号为双引号
fixed_data = re.sub(r"(?<!\\)'(.*?)'(?!:)", r'"\1"', raw_data)

# 解析修复后的 JSON 数据
try:
    data = json.loads(fixed_data)
except json.decoder.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
    exit(1)

# 删除指定的条目
keys_to_delete = ["wallpaper", "notice"]
for key in keys_to_delete:
    if key in data:
        del data[key]

# 删除含有特定字段的条目
delete_items = [
    {"name": "雷蒙影视电视直播"},
    {"name": "雷蒙影视轻量直播"},
    {"name": "雷蒙影视宣传片"},
    {"name": "国内直播[合并版]"}
]

data = [item for item in data if not any(item.get(key) == value for key, value in delete_items.items())]

# 替换 name 和 url
for item in data:
    if item.get("name") == "YY轮播":
        item["name"] = "直播"
        item["url"] = "https://raw.githubusercontent.com/lg-yyds/gytvapi/refs/heads/master/output/user_result.txt"

# 删除文件中的 "雷蒙影视 | "
for item in data:
    if isinstance(item.get("name"), str):
        item["name"] = item["name"].replace("雷蒙影视 | ", "")

# 写回文件
with open("JN/lem.json", "w", encoding="utf-8") as f_out:
    json.dump(data, f_out, ensure_ascii=False, indent=2)

print("文件修改完成。")
