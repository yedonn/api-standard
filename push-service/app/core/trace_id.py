import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("trace_id", str(uuid.uuid4()))
        request.state.trace_id = trace_id  # Attacher le trace_id à la requête
        response = await call_next(request)
        response.headers["trace_id"] = trace_id  # Propager le trace_id dans la réponse
        return response