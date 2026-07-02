from fastapi import Request
from starlette.responses import JSONResponse
import logging
from backend.app.core.logging import get_correlation_id

logger = logging.getLogger(__name__)

async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error.",
            "correlation_id": get_correlation_id()
        }
    )
