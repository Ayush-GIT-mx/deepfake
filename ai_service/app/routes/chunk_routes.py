from fastapi import APIRouter, UploadFile
from app.services.chunk_service import chunk_text_from_json
from app.utils.file_utils import save_file

router = APIRouter()

@router.post("/chunk")
async def chunk_file(file: UploadFile, max_words: int = 450):
    """
    Takes a JSON file (from PDF or DOCX extraction) and splits text into chunks.
    Returns text chunks with associated images.
    """
    file_path = await save_file(file)
    chunks = chunk_text_from_json(file_path, max_words=max_words)
    return chunks
