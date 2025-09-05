import orjson

def save_json(data, file_path: str):
    with open(file_path, "wb") as f:
        f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))

def load_json(file_path: str):
    with open(file_path, "rb") as f:
        return orjson.loads(f.read())
