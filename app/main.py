from fastapi import FastAPI

app = FastAPI(
    title="URL Shortener API",
    description="A simple API to convert long URLs into short links.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "URL Shortener API is running"}
