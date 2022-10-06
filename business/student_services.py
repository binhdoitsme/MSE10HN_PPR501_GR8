from datetime import date
from typing import NamedTuple, Optional, Sequence, TypeVar

from pydantic import BaseModel

from business.domain.student import Student, StudentId, StudentRepository

T = TypeVar("T")


class StudentForm(NamedTuple):
    id: Optional[int]
    first_name: str
    last_name: str
    dob: date
    hometown: str
    final_mark: float

    def to_student(self):
        return Student(
            id=StudentId(self.id),
            first_name=self.first_name,
            last_name=self.last_name,
            dob=self.dob,
            final_mark=self.final_mark,
        )


class StudentResult(BaseModel):
    id: int
    first_name: str
    last_name: str
    dob: str
    hometown: str
    final_mark: float

    @staticmethod
    def from_(student: Student):
        return StudentResult(
            id=student.id.value,
            first_name=student.first_name,
            last_name=student.last_name,
            dob=student.dob.strftime("%Y-%m-%d"),
            hometown=student.hometown,
            final_mark=student.final_mark,
        )


MaybeStudentResult = Optional[StudentResult]


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def __hash__(self) -> int:
        return id(self)

    def get_all_students(self) -> Sequence[StudentResult]:
        return [StudentResult.from_(s) for s in self.repository.find()]

    def get_student_by_id(self, id: int) -> MaybeStudentResult:
        ...

    def create_student(self, form: StudentForm) -> MaybeStudentResult:
        ...

    def update_student(self, form: StudentForm) -> MaybeStudentResult:
        ...

    def delete_student(self, id: int) -> bool:
        ...
