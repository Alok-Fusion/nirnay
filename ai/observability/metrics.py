import time
import logging
from typing import Dict, Any, Callable
from functools import wraps

logger = logging.getLogger(__name__)

def trace_agent(agent_name: str):
    """Decorator to trace agent execution time and record in audit trail."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(state: Dict[str, Any], *args, **kwargs):
            start_time = time.time()
            logger.info(f"[{agent_name}] Started.")
            
            try:
                result_state = func(state, *args, **kwargs)
                duration = time.time() - start_time
                
                # Append to audit trail
                audit_entry = {
                    "agent": agent_name,
                    "duration_seconds": round(duration, 3),
                    "status": "success",
                    "timestamp": time.time()
                }
                
                # If the function returns a dict to update the state
                if isinstance(result_state, dict):
                    if "audit_trail" in result_state:
                        result_state["audit_trail"].append(audit_entry)
                    else:
                        result_state["audit_trail"] = [audit_entry]
                
                logger.info(f"[{agent_name}] Completed in {duration:.3f}s")
                return result_state
                
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"[{agent_name}] Failed in {duration:.3f}s: {e}")
                # We do NOT swallow the exception here. We must re-raise it so the global 
                # LangGraph wrapper (safe_agent_wrapper) can set next_agent="END".
                raise e
                
        return wrapper
    return decorator
