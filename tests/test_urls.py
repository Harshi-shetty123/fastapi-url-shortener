
from datetime import datetime, timedelta, timezone

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.models.url import URL


test_engine = create_engine(
    "sqlite://",
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


def create_test_url(client, original_url="https://example.com/products"):
    return client.post(
        "/urls/",
        json={"original_url": original_url}
    )


def test_create_short_url(client):
    response = create_test_url(client)

    assert response.status_code == 201
    assert response.json()["original_url"] == "https://example.com/products"
    assert response.json()["click_count"] == 0


def test_duplicate_url(client):
    first = create_test_url(client)
    second = create_test_url(client)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["short_code"] == second.json()["short_code"]


def test_invalid_url(client):
    response = client.post(
        "/urls/",
        json={"original_url": "invalid-url"}
    )

    assert response.status_code == 422


def test_redirect_url(client):
    created = create_test_url(client)
    code = created.json()["short_code"]

    response = client.get(
        f"/urls/{code}",
        follow_redirects=False
    )

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/products"


def test_click_count(client):
    created = create_test_url(client)
    code = created.json()["short_code"]

    client.get(f"/urls/{code}", follow_redirects=False)
    client.get(f"/urls/{code}", follow_redirects=False)

    response = client.get(f"/urls/{code}/details")

    assert response.json()["click_count"] == 2


def test_unknown_short_code(client):
    response = client.get(
        "/urls/unknowncode",
        follow_redirects=False
    )

    assert response.status_code == 404


def test_get_url_details(client):
    created = create_test_url(client)
    code = created.json()["short_code"]

    response = client.get(f"/urls/{code}/details")

    assert response.status_code == 200
    assert response.json()["short_code"] == code


def test_list_urls(client):
    create_test_url(client, "https://example.com/one")
    create_test_url(client, "https://example.com/two")

    response = client.get("/urls/")

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["items"]) == 2


def test_pagination(client):
    create_test_url(client, "https://example.com/one")
    create_test_url(client, "https://example.com/two")
    create_test_url(client, "https://example.com/three")

    response = client.get("/urls/?skip=0&limit=2")

    assert response.status_code == 200
    assert response.json()["total"] == 3
    assert len(response.json()["items"]) == 2


def test_delete_url(client):
    created = create_test_url(client)
    code = created.json()["short_code"]

    response = client.delete(f"/urls/{code}")

    assert response.status_code == 204

    details = client.get(f"/urls/{code}/details")
    assert details.status_code == 404


def test_delete_unknown_url(client):
    response = client.delete("/urls/unknowncode")

    assert response.status_code == 404


def test_create_url_with_expiration(client):
    expiration = (
        datetime.now(timezone.utc) + timedelta(days=7)
    ).isoformat()

    response = client.post(
        "/urls/",
        json={
            "original_url": "https://example.com/temporary",
            "expires_at": expiration
        }
    )

    assert response.status_code == 201
    assert response.json()["expires_at"] is not None


def test_reject_past_expiration(client):
    expiration = (
        datetime.now(timezone.utc) - timedelta(days=1)
    ).isoformat()

    response = client.post(
        "/urls/",
        json={
            "original_url": "https://example.com/expired",
            "expires_at": expiration
        }
    )

    assert response.status_code == 422


def test_expired_url(client):
    created = client.post(
        "/urls/",
        json={
            "original_url": "https://example.com/expired",
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(days=1)
            ).isoformat()
        }
    )

    code = created.json()["short_code"]

    db = TestingSessionLocal()
    url = db.query(URL).filter(URL.short_code == code).first()
    url.expires_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)
    db.commit()
    db.close()

    response = client.get(
        f"/urls/{code}",
        follow_redirects=False
    )

    assert response.status_code == 410
