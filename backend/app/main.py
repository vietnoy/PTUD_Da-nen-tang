"""FastAPI application entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBearer
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings, settings_summary
from app.core.database import engine
from app.api import api_router

from app.models import *
from app.models import Base


class UTF8Middleware(BaseHTTPMiddleware):
    """Middleware để đảm bảo UTF-8 encoding cho tất cả responses."""
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        if 'content-type' in response.headers:
            content_type = response.headers['content-type']
            if 'charset' not in content_type:
                response.headers['content-type'] = f'{content_type}; charset=utf-8'
        else:
            response.headers['content-type'] = 'application/json; charset=utf-8'
        return response


def create_app() -> FastAPI:
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.project_name,
        version="0.1.0",
        swagger_ui_init_oauth={
            "usePkceWithAuthorizationCodeGrant": True,
        }
    )

    # Thêm UTF-8 middleware
    app.add_middleware(UTF8Middleware)

    # Configure CORS - cho phép tất cả origins trong development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Trong production nên giới hạn cụ thể
        allow_credentials=False,  # Phải là False khi allow_origins=["*"]
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
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
