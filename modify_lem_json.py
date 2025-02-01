import json

# 加载JSON文件
with open('JN/lem.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 处理 "lives" 条目
for live in data.get('lives', []):
    live['name'] = '直播'
    live['url'] = 'https://raw.githubusercontent.com/lg-yyds/gdtvapi/refs/heads/master/output/user_result.txt'

# 删除指定条目
keys_to_remove = [
    "wallpaper",
    "notice",
    {"key": "csp_Notice", "name": "📢【Lem声明】公告", "type": 3, "api": "csp_Notice", "ext": "雷蒙影视独家资源，私享即可，请勿传播！"},
    {"key": "公告1", "name": "📢【Lem声明】勿传播本线路", "type": 3, "api": "csp_Bili", "searchable": 0, "quickSearch": 0, "filterable": 0, "ext": {"json": "https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/EXT/XB/ANNOUNCEMENT.json"}},
    {"key": "csp_Market", "name": "雷蒙影视 | 🏪应用商店", "jar": "./N3RD/J/market.jar", "type": 3, "api": "csp_Market", "searchable": 0, "changeable": 0, "ext": "./N3RD/T/market.json"},
    {"key": "csp_FirstAid", "name": "雷蒙影视 | 🚑急救教学(SP)", "type": 3, "api": "csp_FirstAid", "searchable": 0, "quickSearch": 0, "changeable": 0, "style": {"type": "rect", "ratio": 3.8}},
]

def remove_key(data, key):
    if isinstance(key, str):
        if key in data:
            del data[key]
    elif isinstance(key, dict):
        for item in data:
            if isinstance(item, dict) and all(item.get(k) == v for k, v in key.items()):
                data.remove(item)

# 删除指定的字段和条目
for key in keys_to_remove:
    if isinstance(key, str):
        remove_key(data, key)
    else:
        remove_key(data.get('lives', []), key)

# 保存修改后的数据
with open('JN/lem_modified.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("文件已处理并保存为 lem_modified.json")
