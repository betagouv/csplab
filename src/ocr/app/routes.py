from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.auth import verify_api_key
from application.usecases.extract_text_usecase import ExtractTextUsecase
from infrastructure.di.container import Container

public_router = APIRouter()


@public_router.get("/health")
def health():
    return {"status": "healthy"}


@public_router.post("/extract-text")
@inject
async def extract_text(
    file: UploadFile = File(...),
    usecase: ExtractTextUsecase = Depends(Provide[Container.extract_text_usecase]),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    content = await file.read()
    text = await usecase.execute(content)

    return {"text": text, "pages": 1}


protected_router = APIRouter(dependencies=[Depends(verify_api_key)])


@protected_router.get("/welcome")
def welcome():
    return {"status": "you're authenticated"}
