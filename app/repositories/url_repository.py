from sqlalchemy.orm import Session
from app.models.url import URL

def get_by_original_url(db: Session, original_url: str):
    return db.query(URL).filter(
        URL.original_url == original_url
    ).first()

def get_by_short_code(db: Session, short_code: str):
    return db.query(URL).filter(
        URL.short_code == short_code
    ).first()

def create_url(db: Session, original_url: str, short_code: str, expires_at=None):
    url = URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at
    )

    db.add(url)

    try:
        db.commit()
        db.refresh(url)
        return url
    except Exception:
        db.rollback()
        raise

def increment_click_count(db: Session, url: URL):
    url.click_count += 1
    db.commit()
    db.refresh(url)
    return url

def get_all_urls(db: Session, skip: int, limit: int):
    return (
        db.query(URL)
        .order_by(URL.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def count_urls(db: Session):
    return db.query(URL).count()


def delete_url(db: Session, url: URL):
    db.delete(url)
    db.commit()
