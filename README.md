# FastAPI URL Shortener

A simple URL Shortener API built using Python, FastAPI, and SQLite.

This project converts long URLs into short, shareable links. When someone accesses a shortened link, the application redirects them to the original URL.

The project is being developed to understand REST API development, database operations, URL redirection, and backend application design.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Uvicorn

## Features

- Create short URLs from original URLs.
- Generate unique short codes.
- Reuse existing short codes for duplicate original URLs.
- Redirect users to the original URLs.
- Track the number of clicks.
- Validate incoming URLs.
- Handle invalid or non-existent short codes.

## Project Structure

```text
fastapi-url-shortener/
│
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
├── README.md
├── requirements.txt
└── .gitignore
```

## How It Works

1. The user submits an original URL through the API.
2. The application checks whether the URL already exists.
3. If it exists, the existing short code is returned.
4. Otherwise, the application generates a unique short code.
5. The original URL and short code are stored in SQLite.
6. When someone opens the short URL, the application looks up the short code.
7. The user is redirected to the original URL.
8. The click count is updated.

## Design Decisions

### 1. Why URL Shortening?

- Long URLs are difficult to share and remember.
- Short URLs make links more compact and convenient.
- Users can access the original destination through a short link.

### 2. Why Store Both URLs?

- The original URL is required for redirection.
- The short code identifies the original URL.
- Both are stored in the database.

### 3. Handling Duplicate URLs

- The application reuses an existing short code when the same original URL is submitted.
- This avoids duplicate records for identical URLs.
- Click counts are shared for the same shortened URL.

### 4. Why SQLite?

- Lightweight and easy to configure.
- Suitable for a small backend application.
- Does not require a separate database server.

### 5. Why SQLAlchemy?

- Provides an ORM to interact with the database using Python.
- Helps organize database operations.
- Reduces the need to write raw SQL for common operations.

### 6. Why FastAPI?

- Provides a simple way to build REST APIs.
- Supports request validation using Pydantic.
- Automatically generates interactive API documentation.

## Setup Instructions

### 1. Clone the repository

```bash
git clone git@github-personal:Harshi-shetty123/fastapi-url-shortener.git
cd fastapi-url-shortener
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
uvicorn app.main:app --reload --port 8765
```

## API Documentation

Once the application is running, open:

- Swagger UI: http://127.0.0.1:8765/docs
- ReDoc: http://127.0.0.1:8765/redoc

## Future Improvements

- Custom short codes.
- URL expiration.
- Separate click analytics.
- User-specific URL management.
- Docker support.

## Learning Outcomes

This project focuses on understanding:

- REST API development using FastAPI.
- Database design and SQLAlchemy ORM.
- Pydantic request and response validation.
- Separation of API, service, repository, and model layers.
- URL redirection and HTTP status codes.
- Error handling and input validation.

---

**Project Status:** Under Development
