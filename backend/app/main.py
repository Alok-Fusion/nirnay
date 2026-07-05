from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.middleware.request_context import RequestContextMiddleware
from backend.app.middleware.rate_limiter import RateLimitMiddleware
from backend.app.middleware.error_handler import custom_exception_handler
from backend.app.api.v1.auth.routes import router as auth_router
from backend.app.api.v1.transactions.routes import router as tx_router
from backend.app.api.v1.users.routes import router as users_router
from backend.app.api.v1.accounts.routes import router as accounts_router
from backend.app.api.v1.recipients.routes import router as recipients_router
from backend.app.api.v1.risk.routes import router as risk_router
from backend.app.api.v1.analytics.routes import router as analytics_router
from backend.app.api.v1.admin.routes import router as admin_router
from backend.app.api.v1.system.routes import router as system_router
from backend.app.api.v1.conversation.routes import router as conversation_router
import logging
from backend.app.core.logging import setup_logging

# Setup structured logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="NIRNAY AI-Powered Financial Decision Intelligence API"
)

# Exception handlers
app.add_exception_handler(Exception, custom_exception_handler)

# Middleware (Order matters - added bottom-up for Starlette)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(RequestContextMiddleware)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(accounts_router, prefix=f"{settings.API_V1_STR}/accounts", tags=["accounts"])
app.include_router(tx_router, prefix=f"{settings.API_V1_STR}/transactions", tags=["transactions"])
app.include_router(recipients_router, prefix=f"{settings.API_V1_STR}/recipients", tags=["recipients"])
app.include_router(risk_router, prefix=f"{settings.API_V1_STR}/risk", tags=["risk"])
app.include_router(analytics_router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(admin_router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(system_router, prefix=f"{settings.API_V1_STR}/system", tags=["system"])
app.include_router(conversation_router, prefix=f"{settings.API_V1_STR}/conversation", tags=["conversation"])

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing NIRNAY Enterprise Backend...")
    # Validate LLM Manager startup
    from ai.llm_manager import LLMManager
    llm = LLMManager()
    status = llm.health_check()
    if status["status"] != "healthy":
        logger.warning(f"Startup Warning: LLM providers degraded: {status}")
    else:
        logger.info("Startup Check: LLM providers connected.")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
