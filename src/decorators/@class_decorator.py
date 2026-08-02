from functools import wraps
from types import FunctionType


class ClassDecorator:
    def __init__(self, some_arg: str):
        self.some_property = some_arg

    def __call__(self, func: FunctionType):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("class Decorator")
            return func(*args, **kwargs)

        return wrapper


@ClassDecorator(some_arg="some str")
def some_func():
    pass
