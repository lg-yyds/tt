import json
import os
import re

# JSON 文件路径
json_file = "JN/lem.json"

# 确保 JSON 文件存在
if not os.path.exists(json_file):
    print(f"错误：文件 {json_file} 不存在！")
    exit(1)

try:
    # 读取 JSON 文件
    with open(json_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # **尝试自动修复 JSON 格式**
    def fix_json(content):
        # 1. **去除 JSON 末尾多余的逗号**（避免 "Expecting property name" 错误）
        content = re.sub(r",\s*([\]}])", r"\1", content)

        # 2. **尝试补全 JSON**
        try:
            return json.loads(content)  # 如果能解析，直接返回
        except json.JSONDecodeError:
            pass  # 继续尝试修复

        # 3. **逐行解析，跳过有问题的行**
        fixed_lines = []
        for line in content.splitlines():
            try:
                json.loads(f"[{line}]")  # 尝试解析该行
                fixed_lines.append(line)
            except json.JSONDecodeError:
                print(f"跳过错误行: {line}")

        fixed_json = "\n".join(fixed_lines)
        return json.loads(fixed_json)  # 最后尝试解析

    # 解析并修复 JSON
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
        data["lives"] = [item for item in data["lives"] if item.get("name") == "直播"]

    # **5. 保存修复后的 JSON**
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("JSON 修复并修改成功！")

except json.JSONDecodeError as e:
    print(f"JSON 解析失败: {e}")
    print("请手动检查 JN/lem.json 文件格式！")
    exit(1)

except Exception as e:
    print(f"发生错误: {e}")
    exit(1)
