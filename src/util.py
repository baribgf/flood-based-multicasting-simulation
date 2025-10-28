from threading import Lock, current_thread

stdio_lock = Lock()
global_verbose = False
def report(msg: str, verbose=False) -> None:
    stdio_lock.acquire()
    print(
        (current_thread().name
            + ": " if global_verbose or verbose else ""
        ) + msg
    )
    stdio_lock.release()
