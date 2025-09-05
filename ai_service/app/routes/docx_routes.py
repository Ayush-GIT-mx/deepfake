from fastapi import APIRouter, UploadFile
from app.services.docx_service import extract_docx_content
from app.utils.file_utils import save_file

router = APIRouter()

@router.post("/extract")
async def extract_docx(file: UploadFile):
    file_path = await save_file(file)
    output_path = extract_docx_content(file_path)
    return {"output_file": output_path}
