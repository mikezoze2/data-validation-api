from fastapi import FastAPI

from app.schemas import (
    HealthResponse,
    RecordInput,
    ValidationRequest,
    ValidationResponse,
)
from app.validation import validate_records


app = FastAPI(
    title="Data Validation API",
    description=(
        "A small API for validating contact records "
        "and detecting duplicate email addresses."
    ),
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="data-validation-api",
    )


@app.post(
    "/api/v1/validate",
    response_model=ValidationResponse,
    tags=["Validation"],
)
def validate(request: ValidationRequest) -> ValidationResponse:
    records = [
        record.model_dump()
        for record in request.records
    ]

    result = validate_records(records)

    return ValidationResponse(**result)
