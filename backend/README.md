# Backend Starter (Phase 1)

## Run

```bash
cd backend
pip install -r requirements/base.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Database Defaults
- Host: `localhost`
- Port: `5432`
- User: `root`
- Password: `root`
- Database: `ail`

Connection string (default):

```bash
postgresql+psycopg://root:root@localhost:5432/ail
```

You can override with `DATABASE_URL`.

## Notes
- API is versioned at `/api/v1`.
- Dummy user context defaults to `demo_user_1`.
- PostgreSQL-backed now: courses, modules, lessons, enrollments, lesson completion, learning paths, assessments, attempts, dashboard progress, admin progress.
- Still in-memory: social feed/posts, certificates.
