import time


def retry(retries, timeout):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(timeout)
            return None
        return wrapper
    return decorator
