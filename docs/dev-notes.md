# PagePal Development Notes

Centralized instructions for running, testing, and maintaining the project locally.

---

## 1. Development Modes (Option A vs Option B)

There are two ways to run the backend:

### Option A — Backend on Mac, DB in Docker (Preferred for daily dev)
- Pros: Fastest reload/debug loop, easy local editing.
- Cons: Not containerized so not gauranteed to work on other machines
- Notes: I prefer to use this during active dev work

How to run Option A:
1. Start Docker Desktop.
2. Run DB only:
   ```bash
   docker compose up -d db
   ```
3. Activate virtual environment:
   ```bash
   source venv_pagepal/bin/activate
   ```
4. Start backend locally:
   ```bash
   PYTHONPATH=. uvicorn backend.app:app --reload
   ```

---

### Option B — Backend + DB in Docker (Prod-like dress rehearsal)
- Pros: Matches production environment closely, fewer surprises on deploy.
- Cons: Slower feedback cycle than Option A.
- Notes: I like to use this before deployment to ensure everything works in a containerized setup.

How to run Option B:
1. Start Docker Desktop.
2. Run everything in Docker:
   ```bash
   docker compose up -d --build
   ```
3. Run migrations inside backend container:
   ```bash
   docker compose exec backend alembic upgrade head
   ```
4. Run seeds inside backend container:
   ```bash
   docker compose exec backend python scripts/seed_reference_data.py
   ```

---

## 2. Starting a Development Session (Option A)

1. Start Docker Desktop.  
   If it's stuck:  
   ```bash
   pkill -f Docker
   ```
   then reopen Docker Desktop.

2. Start DB only:
   ```bash
   docker compose up -d db
   ```

3. Activate Python virtual environment:
   ```bash
   source venv_pagepal/bin/activate
   ```

4. Start backend:
   ```bash
   PYTHONPATH=. uvicorn backend.app:app --reload
   ```

5. Start frontend:
   ```bash
   cd frontend
   npm run dev
   ```
   Open: `http://localhost:5173`

---

## 3. Running Tests

Run all tests:
```bash
PYTHONPATH=. pytest
```

Run a specific file:
```bash
PYTHONPATH=. pytest tests/test_books_db.py
```

Run a specific test function:
```bash
PYTHONPATH=. pytest tests/test_chunks_db.py -k test_chunks_table_crud
```

Test conventions:
- Files: `test_*.py` or `*_test.py`
- Use `assert` instead of `print`
- All tests live in `/tests/`

---

## 4. Database Setup & Usage

### 4.1 Migrations (Alembic)
The schema is managed via Alembic

Apply migrations:
```bash
# Option A (backend local)
alembic upgrade head

# Option B (backend in Docker)
docker compose exec backend alembic upgrade head
```

### 4.2 Seed Data
Run seed script (idempotent):
```bash
# Option A
python scripts/seed_reference_data.py

# Option B
docker compose exec backend python scripts/seed_reference_data.py
```

### 4.3 Bulk Data Initialization
For large imports (languages, chapter patterns, spaCy models), write SQL or Python scripts and run them against the DB container.

---

## 5. Logging in the Backend

Global logging in `app.py`:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
```

In other files:
```python
import logging
log = logging.getLogger(__name__)
```

---

## 6. Switching Between Local & Prod

`.env` is used for for environment-specific configs.

Example vars:
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=...
PAGEPAL_API_KEY=...
```

In production:
- Set `CORS_ORIGINS` to the frontend domain.
- Use the managed Postgres `DATABASE_URL` from the hosting platform.

---

## 7. Ending a Development Session

1. Stop frontend (CTRL+C in its terminal).
2. Stop backend:
   - Option A: CTRL+C in backend terminal.
   - Option B: `docker compose down`
3. Optionally commit changes:
   ```bash
   git add .
   git commit -m "message"
   ```

---

## 8. Quick Smoke Test Before Coding

- `/docs` loads in browser.
- `GET /languages` returns JSON.
- Highlight-to-explain works end-to-end.