
# FastAPI URL Shortener

A RESTful URL Shortener API built using Python, FastAPI, SQLAlchemy, and SQLite.

The application converts long URLs into short, shareable links. It supports duplicate URL detection, URL redirection, and click tracking.

This project is being developed incrementally to demonstrate practical backend engineering concepts, clean architecture, database operations, API development, and automated testing.

## Features

- Create short URLs from original URLs.
- Generate secure, random short codes.
- Detect duplicate URLs and reuse existing short codes.
- Validate input URLs using Pydantic.
- Store URL records in an SQLite database.
- Redirect short URLs to their original destinations.
- Track the number of clicks for each short URL.
- Return appropriate HTTP errors for invalid requests and unknown short codes.
- Automated API tests using pytest.
- Continuous integration using GitHub Actions.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| SQLAlchemy | ORM and database operations |
| SQLite | Database |
| Pydantic | Request validation and response schemas |
| Uvicorn | ASGI application server |
| Pytest | Automated testing |
| Git & GitHub | Version control and collaboration |
| GitHub Actions | Continuous integration |

## Project Structure

```text
fastapi-url-shortener/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── urls.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   └── url.py
│   │
│   ├── repositories/
│   │   └── url_repository.py
│   │
│   ├── schemas/
│   │   └── url.py
│   │
│   ├── services/
│   │   └── url_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_main.py
│   └── test_urls.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Architecture

The application follows a layered architecture to separate API handling, business logic, and database operations.

```text
Client
  |
  v
FastAPI Routes
  |
  v
Service Layer
  |
  v
Repository Layer
  |
  v
SQLAlchemy ORM
  |
  v
SQLite Database
```

### Layer Responsibilities

**API Layer**
- Defines HTTP endpoints.
- Handles incoming requests.
- Validates request data.
- Returns appropriate HTTP responses.

**Service Layer**
- Contains business logic.
- Generates unique short codes.
- Handles duplicate URL detection.
- Coordinates URL retrieval and click tracking.

**Repository Layer**
- Handles database queries.
- Creates and retrieves URL records.
- Updates click counts.

**Model Layer**
- Defines the database table structure using SQLAlchemy.

**Schema Layer**
- Defines request and response validation using Pydantic.

## Database Design

### URLs Table

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| original_url | String | Original long URL |
| short_code | String | Unique generated short code |
| click_count | Integer | Number of redirects |
| created_at | DateTime | Record creation timestamp |

### Database Constraints

- `id` is the primary key.
- `short_code` is unique.
- `original_url` is unique to prevent duplicate records.
- `click_count` defaults to zero.

## API Endpoints

Base URL:

`http://127.0.0.1:8765`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health check |
| POST | `/urls/` | Create a short URL |
| GET | `/urls/{short_code}` | Redirect to original URL |

### 1. Health Check

**Request**

```http
GET /
```

**Response**

```json
{
  "message": "URL Shortener API is running"
}
```

### 2. Create Short URL

**Request**

```http
POST /urls/
```

**Request Body**

```json
{
  "original_url": "https://example.com/products"
}
```

**Successful Response — 201 Created**

```json
{
  "id": 1,
  "original_url": "https://example.com/products",
  "short_code": "abc123",
  "short_url": "http://127.0.0.1:8765/urls/abc123",
  "click_count": 0,
  "created_at": "2026-10-24T10:30:00"
}
```

The generated short code will be different for each new URL.

**Duplicate URL Handling**

If the same original URL is submitted again, the application returns the existing short code instead of creating another database record.

### 3. Redirect Short URL

**Request**

```http
GET /urls/abc123
```

**Successful Response**

```http
307 Temporary Redirect
Location: https://example.com/products
```

The application increments the click count before returning the redirect response.

**Unknown Short Code**

```http
404 Not Found
```

```json
{
  "detail": "Short URL not found"
}
```

## How It Works

### URL Creation

1. The client submits an original URL.
2. FastAPI validates the request using Pydantic.
3. The service checks whether the original URL already exists.
4. If it exists, the existing record is returned.
5. Otherwise, a secure random short code is generated.
6. The repository stores the URL in SQLite.
7. The API returns the generated short URL.

### URL Redirection

1. The client opens a generated short URL.
2. FastAPI receives the short code.
3. The service retrieves the corresponding database record.
4. If no record exists, the API returns HTTP 404.
5. If found, the click count is incremented.
6. FastAPI returns an HTTP 307 redirect to the original URL.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/Harshi-shetty123/fastapi-url-shortener.git

cd fastapi-url-shortener
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Application

```bash
uvicorn app.main:app --reload --port 8765
```

The API will be available at:

`http://127.0.0.1:8765`

### 5. Explore API Documentation

Open the following URL in your browser:

`http://127.0.0.1:8765/docs`

FastAPI provides interactive Swagger documentation for testing the endpoints.

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

The tests cover:

- API health check.
- Successful short URL creation.
- Duplicate URL handling.
- Invalid URL validation.
- Successful URL redirection.
- Click count increment.
- Unknown short code handling.

## Continuous Integration

GitHub Actions is configured to execute the automated test suite when changes are pushed or pull requests are created.

Workflow configuration:

`.github/workflows/ci.yml`

This helps identify regressions before merging changes into the main branch.

## Engineering Decisions

### Secure Random Short Codes

The application uses Python's `secrets` module to generate unpredictable URL-safe short codes.

### Duplicate Prevention

The database enforces uniqueness for original URLs and short codes. The service also checks for existing URLs before creating new records.

### Layered Architecture

Separating routes, services, repositories, schemas, and models keeps the code maintainable and makes individual responsibilities easier to understand.

### Database Transactions

Database write operations use commits and rollbacks to maintain database consistency when an operation fails.

### Automated Testing

Pytest and FastAPI's TestClient are used to verify API behavior against an isolated in-memory SQLite database.

## Planned Improvements

- Retrieve URL details using a short code.
- List all created URLs.
- Add pagination and filtering.
- Support URL expiration.
- Add URL deletion.
- Improve error handling.
- Add API rate limiting.
- Add authentication and user-specific URLs.
- Explore Redis caching for frequently accessed URLs.
- Add production database support using PostgreSQL.

## Learning Outcomes

This project provides practical experience with:

- Designing RESTful APIs using FastAPI.
- Implementing layered backend architecture.
- Building database-backed applications using SQLAlchemy.
- Writing reusable business logic.
- Validating API requests and responses.
- Handling database transactions and uniqueness constraints.
- Implementing HTTP redirects.
- Tracking application usage.
- Writing automated API tests.
- Managing feature branches and pull requests.
- Configuring CI workflows using GitHub Actions.

## Author

**Harshitha Ratna M**

GitHub: [Harshi-shetty123](https://github.com/Harshi-shetty123)

---
