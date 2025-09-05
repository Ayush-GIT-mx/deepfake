import fitz  # PyMuPDF
import os, orjson
from app.services.image_service import make_image_record


def extract_pdf_content(file_path: str) -> str:
    doc = fitz.open(file_path)
    pages_data = []

    for i, page in enumerate(doc):
        page_text = page.get_text("text")
        images = []

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_ext = base_image["ext"]

            image_id = f"{i+1}_{img_index+1}"
            image_record = make_image_record(img_bytes, page=i+1, image_id=image_id, ext=img_ext)
            images.append(image_record)

        pages_data.append({
            "page": i + 1,
            "text": page_text.strip(),
            "images": images
        })

    output_file = os.path.splitext(file_path)[0] + ".json"
    with open(output_file, "wb") as f:
        f.write(orjson.dumps(pages_data, option=orjson.OPT_INDENT_2))

    return output_file
