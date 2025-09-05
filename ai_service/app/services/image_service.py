import os
from PIL import Image
from io import BytesIO

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)


def save_image(image_bytes: bytes, page: int, image_id: str, ext: str = "png") -> str:
    """
    Save image bytes to disk and return the saved path.
    """
    img_name = f"page_{page}_img_{image_id}.{ext}"
    img_path = os.path.join(IMAGE_DIR, img_name)

    # Save the image
    with open(img_path, "wb") as f:
        f.write(image_bytes)

    # Validate with Pillow
    Image.open(BytesIO(image_bytes)).verify()

    return img_path


def make_image_record(image_bytes: bytes, page: int, image_id: str, ext: str = "png") -> dict:
    """
    Create a consistent image record for JSON output.
    """
    img_path = save_image(image_bytes, page, image_id, ext)
    return {
        "id": image_id,
        "page": page,
        "path": img_path
    }
