"""
Decorators in Python are functions that take other function as argument and
modify its behavior by wrapping it with some logic.
"""
from typing import Callable
import functools


def my_decorator(func: Callable) -> Callable:

    @functools.wraps(func)  # Keep the meta information of func
    def wrapper(*args, **kwargs):
        print("Logic before the function is called")
        result = func(*args, **kwargs)
        print("Logic after the function is called")
        return result

    return wrapper


def my_func(order: str) -> None:
    print(f"Executing my {order} function")


my_func = my_decorator(my_func)
my_func("first")

"""
Python provides a syntax suggar for decorating functions
"""


@my_decorator
def my_func2(order: str) -> None:
    print(f"Executing my {order} function")


print()
my_func2(order="second")
