# FastAPI URL Shortener

A REST API built with **FastAPI** that converts long URLs into short links. It supports redirection, click tracking, URL management, pagination, and optional link expiration.

## Features

- Create short URLs with randomly generated short codes.
- Prevent duplicate entries for the same original URL.
- Redirect short URLs to their original destinations.
- Track the number of clicks.
- Retrieve URL details using a short code.
- List URLs with pagination.
- Delete existing URLs.
- Set optional expiration dates for short URLs.
- Validate URLs and reject expired or invalid expiration dates.

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Testing:** Pytest, FastAPI TestClient
- **CI:** GitHub Actions

## Project Structure

```text
app/
├── api/routes/       # API endpoints
├── core/             # Application configuration
├── db/               # Database connection
├── models/            # SQLAlchemy models
├── repositories/      # Database operations
├── schemas/           # Request and response validation
├── services/          # Business logic
└── main.py            # FastAPI application

tests/                 # Automated tests
.github/workflows/     # CI workflow
README.md
requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Harshi-shetty123/fastapi-url-shortener.git
cd fastapi-url-shortener
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python -m uvicorn app.main:app --reload --port 8765
```

The API will be available at:

`http://127.0.0.1:8765`

Interactive API documentation:

`http://127.0.0.1:8765/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/urls/` | Create a short URL |
| GET | `/urls/` | List URLs with pagination |
| GET | `/urls/{short_code}/details` | Retrieve URL details |
| GET | `/urls/{short_code}` | Redirect to original URL |
| DELETE | `/urls/{short_code}` | Delete a short URL |

### Create URL

**Request:**

```json
{
  "original_url": "https://www.wikipedia.org/",
  "expires_at": "2026-10-30T10:00:00Z"
}
```

`expires_at` is optional and must be a future timestamp with a timezone.

### Example Response

```json
{
  "id": 1,
  "original_url": "https://www.wikipedia.org/",
  "short_code": "abc123",
  "short_url": "http://127.0.0.1:8765/urls/abc123",
  "click_count": 0,
  "created_at": "2026-10-24T07:30:00",
  "expires_at": "2026-10-30T10:00:00"
}
```

### Pagination

```text
GET /urls/?skip=0&limit=10
```

## Running Tests

```bash
python -m pytest -q
```

The test suite covers URL creation, duplicate handling, validation, redirection, click tracking, pagination, deletion, and expiration.

## Design

The application follows a simple layered architecture:

- **Routes:** Handle HTTP requests and responses.
- **Schemas:** Validate incoming data and structure responses.
- **Services:** Contain business logic.
- **Repositories:** Handle database operations.
- **Models:** Define database tables.

## Future Improvements

- User authentication and URL ownership.
- Custom short codes.
- Rate limiting.
- URL analytics and reporting.
- Database migration support.

## Author

**Harshitha Ratna M**

GitHub: [Harshi-shetty123](https://github.com/Harshi-shetty123)
