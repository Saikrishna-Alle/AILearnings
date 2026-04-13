# Backend Starter (Phase 1)

## Run

```bash
cd backend
pip install -r requirements/base.txt
uvicorn app.main:app --reload
```

## Notes
- API is versioned at `/api/v1`.
- Dummy user context defaults to `demo_user_1`.
- Current persistence is in-memory for MVP speed.
- SQLAlchemy models are included as Phase 2 migration targets.
