
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.url import URLCreate, URLResponse, URLListResponse
from app.services.url_service import (
    create_short_url,
    get_url_for_redirect,
    get_url_details,
    list_urls,
    remove_url,
    URLExpiredError
)

router = APIRouter(prefix="/urls", tags=["URLs"])


def format_url(url, request):
    return URLResponse(
        id=url.id,
        original_url=url.original_url,
        short_code=url.short_code,
        short_url=f"{request.base_url}urls/{url.short_code}",
        click_count=url.click_count,
        created_at=url.created_at,
        expires_at=url.expires_at
    )


@router.post("/", response_model=URLResponse, status_code=201)
def create_url(
    payload: URLCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        url = create_short_url(
            db,
            str(payload.original_url),
            payload.expires_at
        )

        return format_url(url, request)

    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/", response_model=URLListResponse)
def get_all_urls(
    request: Request,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    result = list_urls(db, skip, limit)

    result["items"] = [
        format_url(url, request) for url in result["items"]
    ]

    return result


@router.get("/{short_code}/details", response_model=URLResponse)
def get_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    url = get_url_details(db, short_code)

    if url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return format_url(url, request)


@router.get("/{short_code}")
def redirect_short_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    try:
        url = get_url_for_redirect(db, short_code)

        if url is None:
            raise HTTPException(
                status_code=404,
                detail="Short URL not found"
            )

        return RedirectResponse(
            url=url.original_url,
            status_code=307
        )

    except URLExpiredError as error:
        raise HTTPException(status_code=410, detail=str(error))


@router.delete("/{short_code}", status_code=204)
def delete_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    deleted = remove_url(db, short_code)

    if not deleted:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return None
