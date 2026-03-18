from fastapi import FastAPI

from app.routes import protected_router, public_router

app = FastAPI(title="OCR Microservice", version="0.1.0")

app.include_router(public_router)
app.include_router(protected_router)
