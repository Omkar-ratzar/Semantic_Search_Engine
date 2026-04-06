from functools import wraps
import traceback
from log import logger

def safe_execution(
    component="GENERAL",
    rethrow=False,
    default_return=None,
    log_args=False
):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)

            except Exception as e:
                err_msg = f"[{component}] {fn.__name__} failed: {str(e)}"

                if log_args:
                    err_msg += f" | args={args}, kwargs={kwargs}"

                logger.error(err_msg)
                logger.debug(traceback.format_exc())

                if rethrow:
                    raise

                return default_return

        return wrapper
    return decorator
