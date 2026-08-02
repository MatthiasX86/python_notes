from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    age: int
    __salary: int
    position: str

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, new_salary: int):
        self.__salary = new_salary

    @salary.deleter
    def salary(self):
        raise AttributeError("cannot delete salary")


matthew = Employee("matthew", 40, 0, "Software Engineer")

print(matthew.salary)


class Other:
    __x: int = 2

    @classmethod
    def change_x(cls, new_x):
        if new_x > 3000:
            raise ValueError("nope")
        cls.__x = new_x

    def __init__(self, name: str):
        self.name = name

    def __call__(self) -> None:
        """
        We have a callable here for a reason
        """


some_var = Other.__dict__["_x"]

peter = Other(name="peter")

print(peter.__x)

print(callable(peter))
