from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_short_url


router = APIRouter(prefix="/urls", tags=["URLs"])


@router.post("/", response_model=URLResponse, status_code=201)
def create_url(
    payload: URLCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        original_url = str(payload.original_url)

        url = create_short_url(
            db=db,
            original_url=original_url
        )

        return URLResponse(
            id=url.id,
            original_url=url.original_url,
            short_code=url.short_code,
            short_url=f"{request.base_url}{url.short_code}",
            click_count=url.click_count,
            created_at=url.created_at
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
