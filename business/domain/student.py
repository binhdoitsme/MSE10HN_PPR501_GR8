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


class Student:
    id: StudentId
    first_name: str
    last_name: str
    dob: date
    hometown: str
    final_mark: float

    @classmethod
    def validate_inputs(
        cls,
        first_name: str,
        last_name: str,
        dob: date,
        hometown: str,
        final_mark: float,
    ):
        errors = []
        if not first_name.strip() or len(first_name.strip()) > 20:
            errors.append(f"Invalid first name: {first_name}")
        if not last_name.strip() or len(last_name.strip()) > 20:
            errors.append(f"Invalid last name: {last_name}")
        if not hometown.strip() or len(hometown.strip()) > 128:
            errors.append(f"Invalid hometown: {hometown}")
        if final_mark < 0 or final_mark > 10:
            errors.append(f"Invalid final mark: {final_mark}")
        if len(errors) > 0:
            raise ValueError(";".join(errors))

    def __init__(
        self,
        id: StudentId,
        first_name: str,
        last_name: str,
        dob: date,
        hometown: str,
        final_mark: float,
    ):
        self.__class__.validate_inputs(
            first_name, last_name, dob, hometown, final_mark
        )
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.hometown = hometown
        self.final_mark = final_mark

    @property
    def fullname(self, reversed=False):
        if reversed:
            return f"{self.last_name} {self.first_name}"
        return f"{self.first_name} {self.last_name}"


class StudentRepository(Protocol):
    def find(self) -> Sequence[Student]:
        ...

    def find_by(self, id: Optional[StudentId] = None, **kwargs) -> Sequence[Student]:
        ...

    def save(self, student: Student) -> Student:
        ...

    def remove(self, student: Student):
        ...
