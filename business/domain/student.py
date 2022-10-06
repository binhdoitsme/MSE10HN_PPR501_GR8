from dataclasses import dataclass
from datetime import date
from typing import Optional, Protocol, Sequence


class StudentId:
    _currvalue: int = 0

    def __init__(self, value: Optional[int] = None) -> None:
        self.value = value if value else self.__class__.next_value()

    @classmethod
    def next_value(cls) -> int:
        cls._currvalue += 1
        return cls._currvalue


@dataclass
class Student:
    id: StudentId
    first_name: str
    last_name: str
    dob: date
    hometown: str
    final_mark: float


class StudentRepository(Protocol):
    def find(self) -> Sequence[Student]:
        ...

    def find_by(self, id: Optional[StudentId] = None, **kwargs) -> Sequence[Student]:
        ...

    def save(self, student: Student) -> Student:
        ...

    def remove(self, student: Student):
        ...
