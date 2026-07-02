import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.core.logging import set_correlation_id
import time
import logging

logger = logging.getLogger(__name__)

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Handle correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        set_correlation_id(correlation_id)
        request.state.correlation_id = correlation_id
        
        # Logging request
        start_time = time.time()
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Logging response
        process_time = time.time() - start_time
        logger.info(f"Completed request: {request.method} {request.url.path} with status {response.status_code} in {process_time:.4f}s")
        
        # Security headers
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
