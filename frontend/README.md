# Frontend Starter (Phase 1)

## Run

```bash
cd frontend
npm install
npm run dev
```

## Environment
Create `.env.local`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Notes
- App Router pages map directly to MVP domains.
- Data is server-fetched from FastAPI.
- Dummy user session is stored under `src/mocks/session.ts`.
