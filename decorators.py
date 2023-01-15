"""
Contains utility decorators
"""

import time

def timer_dec(func_to_measure):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func_value = func_to_measure(*args, **kwargs)
        print(f"Execution time = {time.time() - start_time} seconds.")
        return func_value
    return wrapper