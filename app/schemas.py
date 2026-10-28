from pydantic import BaseModel, ConfigDict, Field


class RecordInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Full name of the contact")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number in international format")


class ValidationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    records: list[RecordInput] = Field(
        description="Records to validate",
        max_length=1000,
    )


class RecordResult(BaseModel):
    index: int
    valid: bool
    duplicate: bool
    errors: list[str]


class ValidationResponse(BaseModel):
    total: int
    valid: int
    invalid: int
    duplicates: int
    results: list[RecordResult]


class HealthResponse(BaseModel):
    status: str
    service: str
