import logging
import os

from sqlalchemy import Table, create_engine, func
from sqlalchemy.orm import Session
from business.domain.student import StudentId

from db.student_repository import StudentRecord


def initialize_db(db_path: str):
    """Initialize SQLite db on given path & create table"""
    logger = logging.getLogger(__name__)
    logger.info("[initialize_db] Initializing DB...")
    full_path = os.path.join(os.getcwd(), db_path)
    if not os.path.exists(full_path):
        open(full_path, mode="w").close()

    engine = create_engine(f"sqlite:///{full_path}", echo=True)
    student_records: Table = StudentRecord.__table__
    if not student_records.exists(bind=engine):
        student_records.create(bind=engine)
    logger.info("[initialize_db] DB initialization completed!")


def init_student_id(session: Session):
    if StudentId._currvalue > 0:
        return
    logger = logging.getLogger(__name__)
    latest_id = session.query(func.max(StudentRecord.id)).scalar()
    StudentId.set_init_value(latest_id or 0)
    logger.info(f"[{__name__}] StudentID updated to {StudentId._currvalue}")
