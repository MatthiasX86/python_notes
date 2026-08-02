from functools import wraps
from types import FunctionType

type NameType = str


def decorator_factory(name: NameType, position: str | None) -> FunctionType:
    def _decorator_factory(func: FunctionType):

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Dear {name} : {position}")
            func(*args, **kwargs)
            print("Best regards")
            print("your new boss")

        return wrapper

    return _decorator_factory


@decorator_factory(name="Matthew", position="Software engineer")
def greeting_message(name: NameType):
    """Function displaying greeting message"""
    print(f"Welcome to the company! {name}")


greeting_message("Matthew")
