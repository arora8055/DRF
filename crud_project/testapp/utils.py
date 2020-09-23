import json


def valid_json(data):
    try:
        data = json.loads(data)
        value = True
    except ValueError:
        value = False
    return value
