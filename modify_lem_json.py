import json
import os
import re

# JSON 文件路径
json_file = "JN/lem.json"

# 确保 JSON 文件存在
if not os.path.exists(json_file):
    print(f"错误：文件 {json_file} 不存在！")
    exit(1)

def fix_json(content):
    """ 尝试修复并解析 JSON 文件 """
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        print("尝试修复 JSON 格式...")
        # 修复多余的逗号和不匹配的括号
        content = re.sub(r",\s*([\]}])", r"\1", content)
        try:
            return json.loads(content)
        except json.JSONDecodeError as e2:
            print(f"修复失败: {e2}")
            # 直接返回空字典，防止中断后续处理
            return {}

try:
    # 读取 JSON 文件
    with open(json_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # 尝试修复 JSON 格式并解析
    data = fix_json(content)

    # **1. 删除 `wallpaper` 和 `notice`**
    if "wallpaper" in data:
        del data["wallpaper"]
    if "notice" in data:
        del data["notice"]

    # **2. 过滤掉包含 "雷蒙影视" 的项**
    if isinstance(data, list):
        data = [item for item in data if "雷蒙影视" not in str(item)]
    elif isinstance(data, dict):
        data = {k: v for k, v in data.items() if "雷蒙影视" not in str(v)}

    # **3. 替换 "YY轮播" 的 `name` 和 `url`**
    for item in data.get("channels", []):
        if item.get("name") == "YY轮播":
            item["name"] = "直播"
            item["url"] = "https://raw.githubusercontent.com/lg-yyds/gytvapi/refs/heads/master/output/user_result.txt"

    # **4. 只保留 `lives` 里的 `{"name": "YY轮播", ...}`**
    if "lives" in data and isinstance(data["lives"], list):
        data["lives"] = [item for item in data["lives"] if item.get("name") == "YY轮播"]

    # **5. 保存修复后的 JSON**
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("JSON 修复并修改成功！")

except Exception as e:
    print(f"发生错误: {e}")
    exit(1)
