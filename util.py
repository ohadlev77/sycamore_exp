"""
Contains utility functions and decorators.
"""

import time
from datetime import datetime
from typing import Any, Optional

def timer_dec(message_prefix: Optional[str] = None) -> Any:
    """
    Measures an execution time (in seconds) of a function and prints it.
    To be used as a decorator.

    Args:
        message_prefix (Optional[str]): A prefix to the message printed by this function,
        while the format message is: "{PREFIX}{TIME_TAKEN} seconds."

    Returns:
        (Any): returns the value that `func_to_measure` returns, can be of any type.
    """

    if message_prefix is None:
        message_prefix = "Execution time = "

    def decorator(func_to_measure):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            func_value = func_to_measure(*args, **kwargs)

            time_taken = round(time.perf_counter() - start_time, 2)
            print(f"{message_prefix}{time_taken} seconds.")

            return func_value

        return wrapper
    return decorator

def timestamp(datetime_obj: datetime) -> str:
    """
    Defines a timestamp format to be used in this library.

    Args:
        datetime_obj (datetime): the `datetime.datetime` object to format.

    Returns:
        (str): a timestamp of the format: "D%d.%m.%y_T%H.%M.%S". E.g, for 01/05/2023, 10:30:45,
        the formatted timestamp is "D01.01.2023_T10.30.45".
    """

    return datetime_obj.strftime("D%d.%m.%y_T%H.%M.%S")