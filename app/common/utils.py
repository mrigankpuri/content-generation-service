import logging
from typing import Any, Dict
from functools import wraps
from app.core.exceptions import GenerationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_execution_time(func):
    """Decorator to log function execution time."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def validate_parameters(parameters: Dict[str, Any], required_params: list) -> None:
    """Validate that all required parameters are present."""
    missing_params = [param for param in required_params if param not in parameters]
    if missing_params:
        raise GenerationError(f"Missing required parameters: {', '.join(missing_params)}") 