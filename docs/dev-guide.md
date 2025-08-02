# PagePal Development Workflow

Steps to start and stop dev sessions.

---

## Starting a Development Session

### 1. Start Docker Desktop
Make sure Docker Desktop is running before continuing.
- If it's stuck, run: `pkill -f Docker` and then reopen Docker Desktop.

### 2. Start PostgreSQL via Docker Compose

From the root of the project (`pagepalai/`):

```bash
docker compose up -d db
```

Verify it's running:

```bash
docker ps
```

`pagepal-db` should show up.

---

### 3. Activate Python Virtual Environment

From the root folder:

```bash
source venv_pagepal/bin/activate
```

---

### 4. Start FastAPI Backend

```bash
PYTHONPATH=. uvicorn backend.app:app --reload
```

Check for this log to confirm success:

```
INFO:     Application startup complete.
```

---

### 5. Start Frontend (Vite)

From the `frontend/` folder:

```bash
cd frontend
npm run dev
```

Open the browser to:

```
http://localhost:5173
```

---

## Ending a Development Session

### 1. Stop Frontend (in its terminal)

Hit `CTRL+C` to stop the Vite dev server.

---

### 2. Stop FastAPI Backend (in its terminal)

Hit `CTRL+C` to stop the backend server.

---

### 3. Shut Down Docker Containers

From the root project directory:

```bash
docker compose down
```

This stops and removes containers, but keeps the DB volume and tables.

---

### 4. Optional: Save Git Changes

```bash
git add .
git commit -m "{enter message here}"
```

---