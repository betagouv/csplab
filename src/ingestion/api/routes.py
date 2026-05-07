from fastapi import APIRouter

public_router = APIRouter()


@public_router.get("/health")
def health():
    return {"status": "healthy"}
