# API Sentinel Backend

Backend foundation for the API Sentinel SaaS described in the PRD.

## Stack
- Django 5.2 LTS
- Django REST Framework 3.18
- PostgreSQL
- Redis + Celery
- JWT via PyJWT
- OpenAPI import via JSON
- Safe/non-destructive scan engine

## What is implemented
- JWT register/login/refresh/me
- Multi-tenant organizations and memberships
- Projects and project API keys
- Environments and APIs
- OpenAPI endpoint inventory import
- Authentication profiles
- Scan jobs with Celery
- Safe baseline scan checks
- Findings/evidence/comments/status/assignment
- HTML/JSON reports
- Audit log
- OpenAPI schema/Swagger docs
- Docker Compose for web/worker/db/redis

## Safety model
Scans require an explicit authorization confirmation and are designed to be non-destructive. The included engine focuses on specification-driven and low-impact HTTP checks, not exploit payloads or destructive testing.

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

API docs: http://localhost:8000/api/docs/

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Run Celery separately:

```bash
celery -A config worker -l INFO
```

## First API flow

1. `POST /api/v1/auth/register/`
2. Create a project under the returned organization.
3. Create an environment.
4. Create an API service.
5. Import an OpenAPI spec.
6. `POST /api/v1/scans/run/` with `authorization_confirmed=true`.
7. Poll `GET /api/v1/scans/{id}/`.
8. Read findings from `GET /api/v1/findings/?project=<project-id>`.
9. Generate a report with `POST /api/v1/reports/generate/`.

## Important production hardening before public deployment
- Replace the dev secret and database credentials.
- Use a real secret manager for API credentials.
- Add refresh-token rotation/revocation storage.
- Put workers behind a controlled egress policy.
- Add strict SSRF target validation before allowing arbitrary URLs.
- Add automated security and integration tests for tenant isolation.
- Add rate limiting and WAF controls at the edge.
- Add proper email delivery and password-reset UX.
- Add CI/CD security scans for this backend itself.
