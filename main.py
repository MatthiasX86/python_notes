from typing import TypedDict, cast

steps = ("first", "second", "third", "fourth", "fifth", "sixth")


class First(TypedDict):
    first: int


class Second(TypedDict):
    second: int


class Third(First, Second):
    pass


first_obj: First = {"first": 1}

second_obj: Second = {"second": 2}

other: Third = {**first_obj, **second_obj}

print(first_obj)

print(first_obj)

prices = {"k": 30, "m": 20, "c": 40}

print(prices)

print(prices.items())

sorted_prices = dict(sorted(prices.items(), key=lambda x: x[1]))

print(sorted_prices)
