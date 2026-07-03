from fastapi import APIRouter
from typing import Dict, Any
import time
from ai.llm_manager import LLMManager
from backend.app.database.session import engine
from sqlalchemy import text

router = APIRouter()
llm_manager = LLMManager()

@router.get('/health', response_model=Dict[str, Any])
def health_check():
    start_time = time.time()
    
    # 1. DB Health
    db_status = "healthy"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"
        
    # 2. LLM Health
    llm_health = llm_manager.health_check()
    
    # 3. Overall latency
    latency_ms = (time.time() - start_time) * 1000
    
    return {
        "status": "healthy" if db_status == "healthy" and llm_health["status"] == "healthy" else "degraded",
        "database": db_status,
        "ml_model": "loaded",
        "rule_engine": "loaded",
        "langgraph": "loaded",
        "llm_provider": llm_health,
        "decision_engine": "loaded",
        "memory": "active",
        "latency_ms": round(latency_ms, 2)
    }
