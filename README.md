# AI Skill Platform

## One-click local run
- Docker: `docker compose up --build`
- PowerShell helper: `./scripts/dev-up.ps1`

## Local credentials
- Admin: `admin@ail.dev` / `admin123`
- Student: `student@ail.dev` / `student123`

## What is implemented
- Full FastAPI + PostgreSQL backend for all MVP domains
- Basic auth + role guards (admin/student)
- Next.js UI for all modules with API states and validation
- Pagination/filters for courses/feed/admin views
- Integration tests for critical journey flows
- CI workflow (backend tests + frontend lint/build)
- Staging deploy workflow via webhook
