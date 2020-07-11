import json

with open("usr_lib/api_keys.json") as f:
    data = json.load(f)

def get_api_key(database = "quandl"):
    return data[database]
