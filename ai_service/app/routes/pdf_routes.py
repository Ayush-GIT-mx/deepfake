from fastapi import APIRouter, UploadFile
from app.services.pdf_service import extract_pdf_content
from app.utils.file_utils import save_file

router = APIRouter()

@router.post("/extract")
async def extract_pdf(file: UploadFile):
    file_path = await save_file(file)
    output_path = extract_pdf_content(file_path)
    return {"output_file": output_path}
