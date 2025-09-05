import os, orjson
from docx import Document
from docx.enum.text import WD_BREAK
from app.services.image_service import make_image_record


def extract_docx_content(file_path: str) -> str:
    if not file_path.endswith(".docx"):
        raise ValueError("File is not a DOCX")

    doc = Document(file_path)
    pages_data = []
    current_page = {"page": 1, "text": [], "images": []}
    page_number = 1
    image_counter = 1

    # --- Iterate through paragraphs and detect page breaks ---
    for para in doc.paragraphs:
        # Handle manual page breaks
        if para.runs:
            for run in para.runs:
                for br in run._element.findall(".//w:br", run._element.nsmap):
                    if br.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type") == "page":
                        # Save current page
                        pages_data.append({
                            "page": page_number,
                            "text": "\n".join(current_page["text"]).strip(),
                            "images": current_page["images"]
                        })
                        # Start new page
                        page_number += 1
                        current_page = {"page": page_number, "text": [], "images": []}

        # Add text
        if para.text.strip():
            current_page["text"].append(para.text.strip())

        # Add images tied to this paragraph
        for run in para.runs:
            if run._element.xpath(".//a:blip"):
                for blip in run._element.xpath(".//a:blip"):
                    rId = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                    image_part = doc.part.related_parts[rId]
                    image_bytes = image_part.blob
                    image_id = f"{page_number}_{image_counter}"
                    image_record = make_image_record(image_bytes, page=page_number, image_id=image_id, ext="png")
                    current_page["images"].append(image_record)
                    image_counter += 1

    # Save last page
    if current_page["text"] or current_page["images"]:
        pages_data.append({
            "page": page_number,
            "text": "\n".join(current_page["text"]).strip(),
            "images": current_page["images"]
        })

    # --- Write JSON output ---
    output_file = os.path.splitext(file_path)[0] + ".json"
    with open(output_file, "wb") as f:
        f.write(orjson.dumps(pages_data, option=orjson.OPT_INDENT_2))

    return output_file


