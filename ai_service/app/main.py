from fastapi import FastAPI
from app.routes import document_routes

app = FastAPI(title="AI Service Backend")

# Register routes
app.include_router(document_routes.router)
