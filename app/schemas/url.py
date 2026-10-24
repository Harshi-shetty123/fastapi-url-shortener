
from datetime import datetime, timezone
from typing import Optional, List

from pydantic import BaseModel, HttpUrl, ConfigDict, field_validator


class URLCreate(BaseModel):
    original_url: HttpUrl
    expires_at: Optional[datetime] = None

    @field_validator("expires_at")
    @classmethod
    def check_expiration(cls, value):
        if value is None:
            return value

        if value.tzinfo is None:
            raise ValueError("Expiration date must include a timezone")

        if value <= datetime.now(timezone.utc):
            raise ValueError("Expiration date must be in the future")

        return value


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    click_count: int
    created_at: datetime
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class URLListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[URLResponse]
