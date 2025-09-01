import json


def parse(data):
    return json.dumps(data, ensure_ascii=True).encode('UTF-8').decode('unicode_escape')
