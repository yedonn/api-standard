from datetime import datetime
import os
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from app.utilities.handler_utils import (
    validation_exception_handler, http_exception_handler, generic_exception_handler
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from app.utilities.consul_utils import register_service
from app.core.config import settings
from app.api.v1 import index
from app.websocket.websocket_endpoint import ws_router
from app.queue.router_queue import broker
from app.core.logging import logger
from app.core.trace_id import TraceIDMiddleware

app = FastAPI(
    title=settings.SERVICE_NAME,
    description=f"This API exposes endpoints of {settings.SERVICE_NAME.lower()}",
    version="1.0.0",
    contact={
        "name": "SEKE Yed Raoul",
        "email": "sekeyedraoul@icloud.com",
        "phone": "+225 0102132040"
    },
    servers=[
        {
            "url": f"http://{settings.API_GATEWAY_URL}:{settings.API_GATEWAY_PORT}/{settings.SERVICE_NAME.lower().replace(' ', '-')}",
            "description": f"Server running in {os.getenv('ENVIRONMENT', 'development')} environment"
        }
    ]
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register service at startup
@app.on_event("startup")
async def startup_event():
    register_service()

# Middleware pour le logging et la limitation de débit
app.add_middleware(TraceIDMiddleware)
# app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(index.router, prefix="/api")
app.add_websocket_route("/ws", ws_router, "websocket")
app.add_websocket_route("/ws/{client_id}", ws_router, "websocket")

Instrumentator().instrument(app).expose(app)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

# Gestion des exceptions
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, port=settings.SERVICE_PORT)
