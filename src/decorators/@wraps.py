from functools import wraps
from logging import INFO, basicConfig, info
from types import FunctionType
from typing import ParamSpec

basicConfig(level=INFO)

P = ParamSpec("P")


def simple_decorator(func: FunctionType):
    """
    This is just a simple decorator the prove that we can keep our original
    function's metadata
    """

    @wraps(func)
    def wrapper_func(*args: P.args, **kwargs: P.kwargs) -> FunctionType:
        msg = (
            f"Calling function '{func.__name__}' with args: {args} and kwargs: {kwargs}"
        )

        info(msg)
        return func(*args, **kwargs)

    return wrapper_func


@simple_decorator
def add(a: int, b: int) -> int:
    return a + b


print(add(2, 3))
