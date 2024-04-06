from utils.thread_with_return_value import ThreadWithReturnValue


class ThreadService:

    def create_thread(self, function, args=None):
        thread = ThreadWithReturnValue(
            daemon=True, target=function, args=[] if args is None else args)
        thread.start()
        result = thread.join()
        return result
