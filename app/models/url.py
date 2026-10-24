
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True, nullable=False)
    short_code = Column(String(20), unique=True, index=True, nullable=False)
    click_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
