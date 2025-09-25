# Di Cho Tien Loi

Modern multi-platform application that helps households coordinate grocery shopping, manage fridge inventory, and plan meals. The project consists of a FastAPI backend, a cross-platform mobile frontend, and supporting documentation.

## Project Layout

- `backend/` — FastAPI service with Celery workers, Alembic migrations, and testing setup.
- `frontend/` — React Native / Expo application (structure scaffolded, implementation TBD).
- `docs/` — Additional technical documentation (architecture, data model, integrations).
- `docker-compose.yml` — Local development stack (FastAPI, worker, PostgreSQL, Redis, MinIO).

## Getting Started

1. Install Docker and Docker Compose.
2. Copy `backend/.env.example` to `backend/.env` and adjust secrets.
3. Run `docker-compose up --build` to bring up the stack.
4. Access FastAPI docs at `http://localhost:8000/docs` once the backend is running.

For detailed backend setup instructions, see `backend/README.md`.
