from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Skeleton middleware; plug Redis counters here for production throttling."""

    async def dispatch(self, request, call_next):
        return await call_next(request)
