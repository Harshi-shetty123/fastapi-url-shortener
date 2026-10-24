
import secrets
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import url_repository


class URLExpiredError(Exception):
    pass


def create_short_url(db: Session, original_url: str, expires_at=None):
    existing_url = url_repository.get_by_original_url(
        db, original_url
    )

    if existing_url:
        return existing_url

    for _ in range(5):
        short_code = secrets.token_urlsafe(5)

        try:
            return url_repository.create_url(
                db,
                original_url,
                short_code,
                expires_at
            )
        except IntegrityError:
            existing_url = url_repository.get_by_original_url(
                db, original_url
            )

            if existing_url:
                return existing_url

    raise RuntimeError("Unable to generate a unique short code")


def is_expired(url):
    if url.expires_at is None:
        return False

    expiration = url.expires_at

    if expiration.tzinfo is None:
        expiration = expiration.replace(tzinfo=timezone.utc)

    return expiration <= datetime.now(timezone.utc)


def get_url_for_redirect(db: Session, short_code: str):
    url = url_repository.get_by_short_code(db, short_code)

    if url is None:
        return None

    if is_expired(url):
        raise URLExpiredError("This short URL has expired")

    url_repository.increment_click_count(db, url)

    return url


def get_url_details(db: Session, short_code: str):
    return url_repository.get_by_short_code(db, short_code)


def list_urls(db: Session, skip: int, limit: int):
    urls = url_repository.get_all_urls(db, skip, limit)
    total = url_repository.count_urls(db)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": urls
    }


def remove_url(db: Session, short_code: str):
    url = url_repository.get_by_short_code(db, short_code)

    if url is None:
        return False

    url_repository.delete_url(db, url)

    return True
