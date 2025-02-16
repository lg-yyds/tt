import json

def get_spider_value(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if "spider" in data:
                return data["spider"]
            return None
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def update_spider_value(file_path, spider_value):
    try:
        with open(file_path, 'r+') as f:
            data = json.load(f)
            if "spider" in data:
                data["spider"] = spider_value
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
    except (json.JSONDecodeError, FileNotFoundError):
        pass

def main():
    # 修正路径字符串中的引号错误
    lem_spider = get_spider_value('lem.json')
    if lem_spider:
        update_spider_value('tv.json', lem_spider)
        update_spider_value('tvy.json', lem_spider)

if __name__ == "__main__":
    main()
