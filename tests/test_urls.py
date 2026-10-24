
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_create_short_url(client):
    response = client.post(
        "/urls/",
        json={"original_url": "https://example.com/products"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["original_url"] == "https://example.com/products"
    assert data["short_code"]
    assert data["short_url"].endswith(
        f"/urls/{data['short_code']}"
    )
    assert data["click_count"] == 0


def test_duplicate_url_returns_existing_code(client):
    payload = {
        "original_url": "https://example.com/products"
    }

    first_response = client.post("/urls/", json=payload)
    second_response = client.post("/urls/", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    assert (
        first_response.json()["short_code"]
        == second_response.json()["short_code"]
    )


def test_invalid_url_is_rejected(client):
    response = client.post(
        "/urls/",
        json={"original_url": "not-a-valid-url"}
    )

    assert response.status_code == 422


def test_redirect_short_url(client):
    create_response = client.post(
        "/urls/",
        json={"original_url": "https://example.com/products"}
    )

    short_code = create_response.json()["short_code"]

    response = client.get(
        f"/urls/{short_code}",
        follow_redirects=False
    )

    assert response.status_code == 307
    assert response.headers["location"] == (
        "https://example.com/products"
    )


def test_redirect_increments_click_count(client):
    create_response = client.post(
        "/urls/",
        json={"original_url": "https://example.com/products"}
    )

    short_code = create_response.json()["short_code"]

    client.get(
        f"/urls/{short_code}",
        follow_redirects=False
    )

    client.get(
        f"/urls/{short_code}",
        follow_redirects=False
    )

    final_response = client.post(
        "/urls/",
        json={"original_url": "https://example.com/products"}
    )

    assert final_response.json()["click_count"] == 2


def test_redirect_unknown_short_code(client):
    response = client.get(
        "/urls/doesnotexist",
        follow_redirects=False
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Short URL not found"
