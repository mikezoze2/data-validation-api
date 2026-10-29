import re
from collections.abc import Mapping, Sequence
from typing import Any

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)

PHONE_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")


def _validate_record(record: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    name = record.get("name")
    email = record.get("email")
    phone = record.get("phone")

    if not isinstance(name, str) or not name.strip():
        errors.append("name must be a non-empty string")

    if not isinstance(email, str) or not EMAIL_PATTERN.fullmatch(email.strip()):
        errors.append("email must be a valid email address")

    if not isinstance(phone, str) or not PHONE_PATTERN.fullmatch(phone.strip()):
        errors.append(
            "phone must use international format, such as +22890000000"
        )

    return errors


def validate_records(
    records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    total = len(records)
    valid = 0
    invalid = 0
    duplicates = 0

    seen_emails: set[str] = set()
    results: list[dict[str, Any]] = []

    for index, record in enumerate(records):
        errors = _validate_record(record)

        email = record.get("email")
        normalized_email = (
            email.strip().casefold()
            if isinstance(email, str)
            else ""
        )

        is_duplicate = bool(
            normalized_email and normalized_email in seen_emails
        )

        if normalized_email:
            seen_emails.add(normalized_email)

        if is_duplicate:
            duplicates += 1
            errors.append("email duplicates an earlier record")

        if errors:
            invalid += 1
        else:
            valid += 1

        results.append(
            {
                "index": index,
                "valid": not errors,
                "duplicate": is_duplicate,
                "errors": errors,
            }
        )

    return {
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "duplicates": duplicates,
        "results": results,
    }
