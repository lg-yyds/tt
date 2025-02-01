import re

json_file = "JN/lem.json"

try:
    # 读取文件内容
    with open(json_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 直接删除 wallpaper 字段
    content = re.sub(r'"wallpaper":\s*"[^"]*",\s*\n?', "", content)

    # 直接删除 notice 相关字段
    content = re.sub(r'"notice":\s*"[^"]*",\s*\n?', "", content)

    # 直接删除 JSON 里的 "雷蒙影视 |" 关键字
    content = content.replace("雷蒙影视 | ", "")

    # 修改 "YY轮播" 的 "name" 和 "url"
    content = re.sub(
        r'("name":\s*)"YY轮播"(,.*?)("url":\s*")([^"]+)"',
        r'\1"直播"\2\3"https://raw.githubusercontent.com/lg-yyds/gytvapi/refs/heads/master/output/user_result.txt"',
        content
    )

    # 重新写回 JSON 文件
    with open(json_file, "w", encoding="utf-8") as f:
        f.write(content)

    print("lem.json 修改完成！")

except Exception as e:
    print(f"发生错误: {e}")
