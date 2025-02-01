import json
import re

# 读取JSON文件内容
with open('JN/lem.json', 'r', encoding='utf-8') as f:
    content = f.read()

# **1. 预处理：尝试修复JSON格式问题**
content = content.replace("'", '"')  # 替换单引号为双引号
content = re.sub(r',\s*}', '}', content)  # 删除对象末尾的逗号
content = re.sub(r',\s*]', ']', content)  # 删除数组末尾的逗号
content = re.sub(r'//.*', '', content)  # 删除单行注释
content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # 删除多行注释

# **2. 尝试解析JSON**
try:
    data = json.loads(content)
except json.JSONDecodeError as e:
    print(f"❌ JSON解析失败: {e}")
    with open("JN/lem_debug.json", "w", encoding="utf-8") as debug_file:
        debug_file.write(content)  # 保存调试文件
    exit(1)

# **3. 处理 "lives" 条目**
for live in data.get('lives', []):
    live['name'] = '直播'
    live['url'] = 'https://raw.githubusercontent.com/lg-yyds/gdtvapi/refs/heads/master/output/user_result.txt'

# **4. 删除不需要的条目**
keys_to_remove = [
    "wallpaper",
    "notice",
    {"key": "csp_Notice"},
    {"key": "公告1"},
    {"key": "csp_Market"},
    {"key": "csp_FirstAid"},
]

# **函数：删除指定的键**
def remove_key(data, key):
    if isinstance(key, str):
        if key in data:
            del data[key]
    elif isinstance(key, dict):
        if isinstance(data, list):
            data[:] = [item for item in data if not all(item.get(k) == v for k, v in key.items())]

# **应用删除规则**
for key in keys_to_remove:
    remove_key(data, key)
    if 'lives' in data:
        remove_key(data['lives'], key)

# **5. 保存修改后的JSON**
with open('JN/lem_modified.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ 处理完成，保存为 lem_modified.json")
