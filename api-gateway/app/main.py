import json
import os
import uuid
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
import httpx
from prometheus_client import Counter, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import ValidationError
from fastapi_utilities import repeat_every
import uvicorn
from app.utilities.global_utils import validate_token
from app.core.config import settings
from app.utilities.handler_utils import (
    validation_exception_handler, http_exception_handler, generic_exception_handler
)
from app.utilities.consul_utils import register_service, update_service_cache, service_cache
from app.utilities.path_utils import EXCLUDED_PATHS
from app.core.rater_limiter import RateLimiterMiddleware
from app.core.logging import log_message
from app.core.trace_id import TraceIDMiddleware

# Application FastAPI
app = FastAPI(
    title=settings.SERVICE_NAME,
    description=f"This API exposes endpoints of {settings.SERVICE_NAME.lower()}.",
    version="1.0.0",
    contact={
        "name": "SEKE Yed Raoul",
        "email": "sekeyedraoul@icloud.com",
        "phone": "+225 0102132040"
    },
    servers=[
        {
            "url": f"http://{settings.SERVICE_URL}:{settings.SERVICE_PORT}/{settings.SERVICE_NAME.lower().replace(' ', '-')}",
            "description": f"Server running in {os.getenv('ENVIRONMENT', 'development')} environment"
        }
    ]
)

# Register service and update routes cache on startup
@app.on_event("startup")
@repeat_every(seconds=30)
def update_routes():
    update_service_cache()
    register_service()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Rate Limiting and Trace ID Middlewares
app.add_middleware(TraceIDMiddleware)
app.add_middleware(RateLimiterMiddleware, limit=settings.RATE_LIMIT_PER_MINUTE, window=60)

# Proxy route handler for microservices
@app.api_route("/{service}/{endpoint:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"], include_in_schema=False)
async def proxy_request(service: str, endpoint: str, request: Request):
    # Validate token if the request path is not excluded
    excluded_paths = EXCLUDED_PATHS.get(request.method, [])
    if not any(pattern.match(endpoint) for pattern in excluded_paths):
        validate_token(request, 'customer-service')

    service_url = service_cache.get(service)
    if not service_url:
        raise HTTPException(status_code=503, detail=f"Service {service} unavailable")

    # Handle Swagger documentation requests
    if endpoint == "api_docs":
        return await fetch_service_openapi_docs(service_url)

    if endpoint == "docs":
        return get_swagger_ui_html(
            openapi_url=f"/{service}/api_docs",
            title=f"{service} API Docs",
            swagger_ui_parameters={"docExpansion": "none", "displayRequestDuration": True}
        )

    trace_id = request.headers.get("trace_id", str(uuid.uuid4()))  # Retrieve or generate trace_id

    # Proxy the actual request to the microservice
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=f"{service_url}/{endpoint}",
                headers={**request.headers, "trace_id": trace_id},
                params=dict(request.query_params),
                content=await request.body()
            )
            response.raise_for_status()
            return JSONResponse(status_code=response.status_code, content=response.json())

    except httpx.HTTPStatusError as http_exc:
        if http_exc.response.status_code == 405:
            raise HTTPException(status_code=405, detail="HTTP method not allowed for this endpoint.")
        else:
            # Tenter de décoder la réponse en JSON si c'est possible
            try:
                error_content = http_exc.response.json()
            except json.JSONDecodeError:
                # Si ce n'est pas un JSON valide, on renvoie le texte brut
                error_content = http_exc.response.text
            return JSONResponse(content=error_content, status_code=http_exc.response.status_code)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")

# Function to fetch OpenAPI docs from a microservice
async def fetch_service_openapi_docs(service_url: str):
    url = f"{service_url}/openapi.json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return JSONResponse(status_code=e.response.status_code, content={"error": f"Failed to get docs: {e.response.status_code}"})
    except httpx.RequestError as e:
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"error": f"Request error: {e}"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": f"Unexpected error: {e}"})


Instrumentator().instrument(app).expose(app)

# Health check endpoint
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

# Exception handlers
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Application entry point
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=settings.SERVICE_PORT)
