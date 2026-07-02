import logging
from pythonjsonlogger import jsonlogger
import contextvars
import uuid

# Context variable to hold the correlation ID for the current request
correlation_id_var = contextvars.ContextVar("correlation_id", default="")

class CorrelationIdFilter(logging.Filter):
    """Injects the correlation ID into the log record."""
    def filter(self, record):
        record.correlation_id = correlation_id_var.get()
        return True

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove default handlers
    for handler in logger.handlers:
        logger.removeHandler(handler)

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s'
    )
    logHandler.setFormatter(formatter)
    
    # Add correlation id filter
    logHandler.addFilter(CorrelationIdFilter())
    logger.addHandler(logHandler)

setup_logging()
logger = logging.getLogger(__name__)

def get_correlation_id() -> str:
    """Gets or generates a correlation ID."""
    cid = correlation_id_var.get()
    if not cid:
        cid = str(uuid.uuid4())
        correlation_id_var.set(cid)
    return cid

def set_correlation_id(cid: str):
    correlation_id_var.set(cid)
