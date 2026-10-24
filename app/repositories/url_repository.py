from sqlalchemy.orm import Session

from app.models.url import URL


def get_by_original_url(db: Session, original_url: str):
    return (
        db.query(URL)
        .filter(URL.original_url == original_url)
        .first()
    )


def get_by_short_code(db: Session, short_code: str):
    return (
        db.query(URL)
        .filter(URL.short_code == short_code)
        .first()
    )


def create_url(db: Session, original_url: str, short_code: str):
    url = URL(
        original_url=original_url,
        short_code=short_code
    )

    db.add(url)

    try:
        db.commit()
        db.refresh(url)
        return url
    except Exception:
        db.rollback()
        raise
