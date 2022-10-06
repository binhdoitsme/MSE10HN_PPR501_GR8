import logging
import os

from sqlalchemy import Table, create_engine

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
