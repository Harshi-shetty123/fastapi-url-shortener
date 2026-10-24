from fastapi import FastAPI

from app.api.routes.urls import router as urls_router
from app.db.database import Base, engine
from app.models.url import URL


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A simple API to convert long URLs into short links.",
    version="1.0.0"
)

app.include_router(urls_router)


@app.get("/")
def home():
    return {"message": "URL Shortener API is running"}
