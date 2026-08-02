from collections.abc import Callable
from functools import wraps


def signature(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Dear interns")
        func(*args, **kwargs)
        print("Best regards,")
        print("your new boss")

    return wrapper


type Name = str


@signature
def greeting_message(x: Name):
    print(f"welcome to the company! {x}")


greeting_message("Peter")
