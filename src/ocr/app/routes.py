from fastapi import APIRouter, Depends

from app.auth import verify_api_key

public_router = APIRouter()


@public_router.get("/health")
def health():
    return {"status": "healthy"}


protected_router = APIRouter(dependencies=[Depends(verify_api_key)])


@protected_router.get("/welcome")
def welcome():
    return {"status": "you're authenticated"}
