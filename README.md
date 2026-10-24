# FastAPI URL Shortener

A simple URL shortening service built with Python and FastAPI. It allows users to convert long URLs into shorter links and redirect visitors to the original URLs.

The project is structured to keep API routes, business logic, database operations, and data models separate.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

## Features

- Create short URLs
- Generate unique short codes
- Redirect to original URLs
- Track link clicks
- Store URL details in SQLite

## Project Structure

```text
app/
├── api/
│   └── routes/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/
└── main.py

tests/
requirements.txt
README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone git@github-personal:Harshi-shetty123/fastapi-url-shortener.git
cd fastapi-url-shortener
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
uvicorn app.main:app --reload --port 8765
```

### 5. Open API documentation

Once the server is running, visit:

http://127.0.0.1:8765/docs

## Development

This project is being developed incrementally, with a focus on clean code structure, API design, and database integration.
