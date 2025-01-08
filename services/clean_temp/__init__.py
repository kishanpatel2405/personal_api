import os
from datetime import time


def attempt_delete(file_path, retries=3, delay=1):
    for attempt in range(retries):
        try:
            os.remove(file_path)
            return True
        except PermissionError:
            time.sleep(delay)
        except Exception as e:
            return False
    return False
