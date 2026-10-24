import secrets
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import url_repository


def create_short_url(db: Session, original_url: str):
    existing_url = url_repository.get_by_original_url(
        db, original_url
    )

    if existing_url:
        return existing_url

    for _ in range(5):
        short_code = secrets.token_urlsafe(5)

        try:
            return url_repository.create_url(
                db=db,
                original_url=original_url,
                short_code=short_code
            )
        except IntegrityError:
            # Another request may have saved this URL already.
            existing_url = url_repository.get_by_original_url(
                db, original_url
            )

            if existing_url:
                return existing_url

            # Otherwise, retry with another random short code.

    raise RuntimeError("Unable to generate a unique short code")
