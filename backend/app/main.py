"""FastAPI application entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, settings_summary
from app.core.database import engine
from app.api import api_router

from app.models import *
from app.models import Base


def create_app() -> FastAPI:
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title=settings.project_name, version="0.1.0")

    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API routes
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/healthz", tags=["health"], summary="Liveness check")
    def healthz() -> dict[str, str]:
        """Simple endpoint for uptime monitoring."""
        return {"status": "ok"}

    @app.get("/readyz", tags=["health"], summary="Readiness check")
    def readyz() -> dict[str, str]:
        """Endpoint used by orchestration to verify dependencies."""
        return {"status": "ready"}

    @app.get("/settings", tags=["info"], summary="Useful settings for diagnostics")
    def get_settings() -> dict[str, str]:
        """Expose non-sensitive settings for debugging."""
        return {key: str(value) for key, value in settings_summary().items()}

    return app


app = create_app()
