# Backend Starter

## Run Locally

```bash
cd backend
pip install -r requirements/base.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Auth (Seeded)
- Admin: `admin@ail.dev` / `admin123`
- Student: `student@ail.dev` / `student123`

## DB Defaults
- Host: `localhost`
- Port: `5432`
- User: `root`
- Password: `root`
- Database: `ail`

Default connection:

```bash
postgresql+psycopg://root:root@localhost:5432/ail
```

Override with `DATABASE_URL`.

## Coverage
- All core MVP domains are PostgreSQL-backed.
- Role-based auth is enabled (`student`, `admin`).
- Admin routes are role-guarded.
