import fitz  # PyMuPDF
import os, orjson
from app.services.image_service import make_image_record

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_pdf_content(file_path: str) -> str:
    doc = fitz.open(file_path)
    pages_data = []
    filename = os.path.basename(file_path)  # base filename for images

    for i, page in enumerate(doc):
        page_text = page.get_text("text")
        images = []

        for _, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_ext = base_image["ext"]

            image_record = make_image_record(img_bytes, filename=filename, ext=img_ext)
            images.append(image_record)

        pages_data.append({
            "page": i + 1,
            "text": page_text.strip(),
            "images": images
        })

    # --- Write JSON output into output/ ---
    json_filename = os.path.splitext(os.path.basename(file_path))[0] + ".json"
    output_file = os.path.join(OUTPUT_DIR, json_filename)
    with open(output_file, "wb") as f:
        f.write(orjson.dumps(pages_data, option=orjson.OPT_INDENT_2))

    return output_file