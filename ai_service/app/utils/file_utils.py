import os
from fastapi import UploadFile

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_file(file: UploadFile) -> str:
    filename = file.filename
    name, ext = os.path.splitext(filename)
    file_path = os.path.join(UPLOAD_DIR, filename)

    # If file already exists, add duplicate count
    i = 1
    while os.path.exists(file_path):
        new_filename = f"{name}_duplicate_{i}{ext}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)
        i += 1

    # Save the file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return file_path