import os
import orjson

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_json(data, filename: str) -> str:
    name, ext = os.path.splitext(filename)
    if not ext:
        ext = ".json"  # default extension
    file_path = os.path.join(OUTPUT_DIR, name + ext)

    # If file already exists, add duplicate count
    i = 1
    while os.path.exists(file_path):
        new_filename = f"{name}_duplicate_{i}{ext}"
        file_path = os.path.join(OUTPUT_DIR, new_filename)
        i += 1

    with open(file_path, "wb") as f:
        f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))

    return file_path

def load_json(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, "rb") as f:
        return orjson.loads(f.read())