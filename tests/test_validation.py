import pytest

from app.validation import validate_records


def test_validate_records_counts_valid_and_invalid_records() -> None:
    records = [
        {
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "+22890000000",
        },
        {
            "name": "",
            "email": "invalid-email",
            "phone": "invalid",
        },
    ]

    result = validate_records(records)

    assert result["total"] == 2
    assert result["valid"] == 1
    assert result["invalid"] == 1
    assert result["duplicates"] == 0


def test_validate_records_detects_duplicate_emails_case_insensitively() -> None:
    records = [
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

    result = validate_records(records)

    assert result["total"] == 2
    assert result["duplicates"] == 1
    assert result["valid"] == 1
    assert result["invalid"] == 1
    assert result["results"][1]["duplicate"] is True


def test_validate_records_handles_empty_input() -> None:
    result = validate_records([])

    assert result["total"] == 0
    assert result["valid"] == 0
    assert result["invalid"] == 0
    assert result["duplicates"] == 0
    assert result["results"] == []


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"name": "Alice", "phone": "+22890000000"},
        {"name": None, "email": "alice@example.com", "phone": "+22890000000"},
        {"name": "Alice", "email": 123, "phone": "+22890000000"},
        {"name": "Alice", "email": "alice@example.com", "phone": None},
        {"name": "   ", "email": "alice@example.com", "phone": "+22890000000"},
    ],
)
def test_invalid_records_return_validation_errors(record: dict) -> None:
    result = validate_records([record])

    assert result["total"] == 1
    assert result["valid"] == 0
    assert result["invalid"] == 1
    assert result["results"][0]["errors"]


def test_validate_records_trims_surrounding_whitespace() -> None:
    records = [
        {
            "name": " Alice ",
            "email": " alice@example.com ",
            "phone": " +22890000000 ",
        }
    ]

    result = validate_records(records)

    assert result["valid"] == 1
    assert result["invalid"] == 0


def test_duplicate_email_is_reported_even_when_other_fields_are_invalid() -> None:
    records = [
        {
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "+22890000000",
        },
        {
            "name": "",
            "email": "ALICE@example.com",
            "phone": "invalid",
        },
    ]

    result = validate_records(records)

    assert result["duplicates"] == 1
    assert result["invalid"] == 1
    assert result["results"][1]["duplicate"] is True


@pytest.mark.parametrize(
    "phone",
    [
        "22890000000",
        "+228",
        "+0123456789",
        "+228 ABC",
        "",
    ],
)
def test_rejects_invalid_phone_formats(phone: str) -> None:
    result = validate_records(
        [
            {
                "name": "Alice",
                "email": "alice@example.com",
                "phone": phone,
            }
        ]
    )

    assert result["invalid"] == 1
    assert any("phone" in error for error in result["results"][0]["errors"])
