import time


def retry(retries, timeout):
    def decorator(func):
        def wrapper(*args, **kwargs):

            def block():
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(timeout)

            if not retries:
                while True:
                    r = block()
                    if r:
                        return r
            else:
                for _ in range(retries):
                    return block()
                        
            return None
        return wrapper
    return decorator
