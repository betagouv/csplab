from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from api.config import get_settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)


def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    settings = get_settings()
    if api_key != settings.ocr_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key"
        )
    return api_key
