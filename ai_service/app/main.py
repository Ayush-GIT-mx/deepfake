from fastapi import FastAPI
from app.routes import pdf_routes, docx_routes, chunk_routes

app = FastAPI(title="AI Service Backend")

# Register routes
app.include_router(pdf_routes.router, prefix="/pdf", tags=["PDF"])
app.include_router(docx_routes.router, prefix="/docx", tags=["DOCX"])
app.include_router(chunk_routes.router, prefix="/chunks", tags=["Chunks"])
