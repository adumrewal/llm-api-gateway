import os
import json
import time

from fastapi import FastAPI, Request, Response, status
from logzero import logger
from .base import router as base_router

from heimdall import __version__
from heimdall.core import logging_core as log_core
from heimdall.core import observability_core as obs_core

log_core.initialize()

SERVICE_NAME = os.getenv("ELASTIC_APM_SERVICE_NAME")
ELASTIC_APM_ENVIRONMENT = os.getenv("ELASTIC_APM_ENVIRONMENT", "not_specified")


def app_add_middlewares(app: FastAPI):
    @app.middleware("http")
    async def handle(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", None)
        logger.info(
            "request received method=%s path=%s",
            request.method,
            request.url,
            extra={
                "heimdall_meta": {
                    "topic": request.url,
                    "request_id": request_id,
                    "event": "initiated",
                }
            },
        )
        start_time = time.perf_counter()
        response = await call_next(request)
        total_time = time.perf_counter() - start_time
        time_in_ms = int(total_time * 1000)
        logger.info(
            "status_code=%s time_taken=%s ms method=%s path=%s",
            response.status_code,
            time_in_ms,
            request.method,
            request.url,
            extra={
                "heimdall_meta": {
                    "topic": request.url,
                    "request_id": request_id,
                    "event": "completed",
                }
            },
        )
        return response

def app_add_default_apis(app: FastAPI):
    @app.get("/health")
    def health_check():
        return Response(
            content=json.dumps({"message": SERVICE_NAME}),
            media_type="application/json",
            status_code=200,
        )
    
    @app.get("/.well-known/live", response_class=Response)
    @app.get("/.well-known/ready", response_class=Response)
    async def live_and_ready(response: Response):
        response.status_code = status.HTTP_204_NO_CONTENT

def app_include_routers(app: FastAPI):
    app.include_router(base_router)
    return None

def create_app() -> FastAPI:
    logger.info(
        {
            "name": "Creating FastAPI app",
            SERVICE_NAME: "Starting service",
            "env": ELASTIC_APM_ENVIRONMENT,
        },
        extra={
            "heimdall_meta": {
                "service": SERVICE_NAME,
                "env": ELASTIC_APM_ENVIRONMENT,
                "version": __version__,
                "event": "service_starting",
            }
        },
    )

    app = FastAPI(title="Heimdall Gateway Service", version=__version__)
    app_add_middlewares(app)
    obs_core.add_client_to_middleware(app)
    app_add_default_apis(app)
    app_include_routers(app)

    return app


app = create_app()
