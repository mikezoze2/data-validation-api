from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "data-validation-api",
    }


def test_validate_endpoint_accepts_valid_records() -> None:
    response = client.post(
        "/api/v1/validate",
        json={
            "records": [
                {
                    "name": "Alice",
                    "email": "alice@example.com",
                    "phone": "+22890000000",
                }
            ]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["valid"] == 1
    assert data["invalid"] == 0
    assert data["duplicates"] == 0


def test_validate_endpoint_detects_duplicate_emails() -> None:
    response = client.post(
        "/api/v1/validate",
        json={
            "records": [
                {
                    "name": "Alice",
                    "email": "alice@example.com",
                    "phone": "+22890000000",
                },
                {
                    "name": "Alice Dupont",
                    "email": "ALICE@example.com",
                    "phone": "+22891111111",
                },
            ]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["valid"] == 1
    assert data["invalid"] == 1
    assert data["duplicates"] == 1


def test_validate_endpoint_rejects_missing_fields() -> None:
    response = client.post(
        "/api/v1/validate",
        json={
            "records": [
                {
                    "name": "Alice",
                    "email": "alice@example.com",
                }
            ]
        },
    )

    assert response.status_code == 422


def test_validate_endpoint_rejects_unknown_fields() -> None:
    response = client.post(
        "/api/v1/validate",
        json={
            "records": [
                {
                    "name": "Alice",
                    "email": "alice@example.com",
                    "phone": "+22890000000",
                    "unexpected": "value",
                }
            ]
        },
    )

    assert response.status_code == 422


def test_validate_endpoint_rejects_more_than_1000_records() -> None:
    records = [
        {
            "name": f"Contact {index}",
            "email": f"contact{index}@example.com",
            "phone": "+22890000000",
        }
        for index in range(1001)
    ]

    response = client.post(
        "/api/v1/validate",
        json={"records": records},
    )

    assert response.status_code == 422