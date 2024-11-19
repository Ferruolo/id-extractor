import time
import random
from functools import wraps


def retry_with_backoff(max_retries=5, base_delay=1, max_delay=32, jitter=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise e

                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (2 ** (retries - 1)), max_delay)

                    # Add jitter if enabled
                    if jitter:
                        delay = delay * (0.5 + random.random())

                    print(f"Attempt {retries} failed. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
            return None

        return wrapper

    return decorator

