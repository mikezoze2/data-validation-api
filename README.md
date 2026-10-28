\# Data Validation API



A lightweight REST API built with Python and FastAPI to validate contact records, check email and phone number formats, and detect duplicate email addresses.



\## Features



\* Validate contact names, email addresses, and international phone number formats.

\* Detect duplicate email addresses case-insensitively.

\* Normalize surrounding whitespace for validation.

\* Return record-level validation errors.

\* Reject missing fields and unexpected input fields.

\* Limit each request to 1,000 records.

\* Provide a health-check endpoint.

\* Expose interactive API documentation through Swagger UI.

\* Include automated tests for business logic and HTTP endpoints.



\## Tech Stack



\* Python 3.14+

\* FastAPI

\* Pydantic

\* Uvicorn

\* pytest

\* HTTPX



\## Project Structure



```text

data-validation-api/

├── app/

│   ├── main.py

│   ├── schemas.py

│   └── validation.py

├── tests/

│   ├── test\_api.py

│   └── test\_validation.py

├── .gitignore

├── README.md

└── requirements.txt

```



\## Installation



Clone the repository:



```bash

git clone https://github.com/mikezoze2/data-validation-api.git

cd data-validation-api

```



Create a virtual environment:



\*\*Windows PowerShell\*\*



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



\*\*Linux or macOS\*\*



```bash

python -m venv .venv

source .venv/bin/activate

```



Install dependencies:



```bash

python -m pip install -r requirements.txt

```



\## Run the API



```bash

python -m uvicorn app.main:app --reload

```



The API will be available at:



\* Health check: `http://127.0.0.1:8000/health`

\* Interactive documentation: `http://127.0.0.1:8000/docs`

\* OpenAPI schema: `http://127.0.0.1:8000/openapi.json`



\## API Usage



\### Health Check



\*\*Request\*\*



```http

GET /health

```



\*\*Example response\*\*



```json

{

&#x20; "status": "ok",

&#x20; "service": "data-validation-api"

}

```



\### Validate Contact Records



\*\*Request\*\*



```http

POST /api/v1/validate

Content-Type: application/json

```



\*\*Example payload\*\*



```json

{

&#x20; "records": \[

&#x20;   {

&#x20;     "name": "Alice",

&#x20;     "email": "alice@example.com",

&#x20;     "phone": "+22890000000"

&#x20;   },

&#x20;   {

&#x20;     "name": "Bob",

&#x20;     "email": "alice@example.com",

&#x20;     "phone": "+22891111111"

&#x20;   },

&#x20;   {

&#x20;     "name": "",

&#x20;     "email": "invalid-email",

&#x20;     "phone": "invalid"

&#x20;   }

&#x20; ]

}

```



\*\*Example response\*\*



```json

{

&#x20; "total": 3,

&#x20; "valid": 1,

&#x20; "invalid": 2,

&#x20; "duplicates": 1,

&#x20; "results": \[

&#x20;   {

&#x20;     "index": 0,

&#x20;     "valid": true,

&#x20;     "duplicate": false,

&#x20;     "errors": \[]

&#x20;   },

&#x20;   {

&#x20;     "index": 1,

&#x20;     "valid": false,

&#x20;     "duplicate": true,

&#x20;     "errors": \[

&#x20;       "email duplicates an earlier record"

&#x20;     ]

&#x20;   },

&#x20;   {

&#x20;     "index": 2,

&#x20;     "valid": false,

&#x20;     "duplicate": false,

&#x20;     "errors": \[

&#x20;       "name must be a non-empty string",

&#x20;       "email must be a valid email address",

&#x20;       "phone must use international format, such as +22890000000"

&#x20;     ]

&#x20;   }

&#x20; ]

}

```



The `index` field is zero-based. Duplicate detection is case-insensitive and considers earlier records in the same request.



\## Run Tests



Run the complete test suite:



```bash

python -m pytest -v

```



The current test suite covers business rules, malformed records, duplicate detection, API responses, and request limits.



\## Validation Rules and Limitations



\* Names must be non-empty strings.

\* Email addresses are checked against a practical format pattern; this is not a complete implementation of every email standard.

\* Phone numbers must match the international `+` format, followed by 8 to 15 digits in total.

\* Phone number validation checks syntax only. It does not verify whether a number exists or is reachable.

\* Email validation does not verify mailbox ownership or deliverability.

\* Duplicate detection applies only within a single request.

\* The API does not persist submitted records.



\## Scope



This project is a portfolio-oriented API demonstrating input validation, duplicate detection, REST endpoint design, data schemas, and automated testing.



It is not intended to replace a production-grade data-quality platform without additional security, monitoring, deployment, and operational controls.



\## License



No license has been specified yet. All rights remain with the copyright holder unless a license is added to this repository.
