from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import aioredis
from app.core.config import settings


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: object, limit: int, window: int) -> None:
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.redis: aioredis.Redis | None = None  # Type hint for redis connection

    async def __aenter__(self) -> None:
        self.redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.redis:
            await self.redis.close()

    async def dispatch(self, request: Request, call_next) -> object:
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        try:
            async with self:  # Use context manager for redis connection
                current_count = await self.redis.get(key)
                if current_count and int(current_count) >= self.limit:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")
                await self.redis.incr(key)
                await self.redis.expire(key, self.window)
                # Log successful rate limiting here (optional)
        except aioredis.ConnectionError:
            # Log Redis connection error here
            raise HTTPException(status_code=500, detail="Internal server error. Redis connection failed.")
        response = await call_next(request)
        return response