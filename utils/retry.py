import time


def retry(retries, timeout):
    def decorator(func):
        def wrapper(*args, **kwargs):

            def block():
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")

            if not retries:
                while True:
                    r = block()
                    if r:
                        return r
                    time.sleep(timeout)
            else:
                for _ in range(retries):
                    r = block()
                    if r:
                        return r
                    time.sleep(timeout)
                        
            return None
        return wrapper
    return decorator
