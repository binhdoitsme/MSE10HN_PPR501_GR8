from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence
from business.domain.student import Student, StudentId, StudentRepository
from sqlalchemy import DATE, TIMESTAMP, Column, Float, Integer, String, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp

from db.base import Base


@dataclass
class StudentRecord(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(15), nullable=False)
    last_name = Column(String(15), nullable=False)
    dob = Column(DATE, nullable=False)
    email = Column(String(1024), nullable=False)
    hometown = Column(String(128), nullable=False)
    final_mark = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=current_timestamp)
    updated_at = Column(TIMESTAMP, default=current_timestamp)
    is_deleted = Column(Boolean, default=False)

    def to_domain(self):
        return Student(
            id=StudentId(self.id),
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            dob=self.dob,
            hometown=self.hometown,
            final_mark=self.final_mark,
        )

    @staticmethod
    def from_domain(student: Student):
        return StudentRecord(
            id=student.id.value,
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            dob=student.dob,
            hometown=student.hometown,
            final_mark=student.final_mark,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


class StudentRepositoryOnSqlAlchemy(StudentRepository):
    def __init__(self, session: Session):
        self.session = session

    def find(self) -> Sequence[Student]:
        return [s.to_domain() for s in self.session.query(StudentRecord).filter_by(is_deleted=False).all()]

    def find_by(self, id: Optional[StudentId] = None, **kwargs) -> Sequence[Student]:
        by_ = {**kwargs, "is_deleted": False}
        if id:
            by_["id"] = id.value
        return [s.to_domain() for s in self.session.query(StudentRecord).filter_by(**by_).all()]

    def save(self, student: Student) -> Student:
        id = student.id.value
        record = self.session.query(StudentRecord).filter_by(id=id).first()
        if not record:
            record = StudentRecord.from_domain(student)
            self.session.add(record)
        else:
            record.first_name = student.first_name
            record.last_name = student.last_name
            record.dob = student.dob
            record.email = student.email
            record.final_mark = student.final_mark
            record.is_deleted = False
            record.updated_at = datetime.now()
        self.session.commit()
        return record.to_domain()

    def remove(self, student_id: StudentId):
        record = (
            self.session.query(StudentRecord)
                .filter_by(id=student_id.value)
                .first()
        )
        if not record:
            raise ValueError("Not found")
        record.is_deleted = True
        self.session.commit()
