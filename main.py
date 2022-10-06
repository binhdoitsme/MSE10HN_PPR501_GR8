import logging
import os
import sys
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.student_api import student_api
from business.student_services import StudentService
from db import db_init
from db.student_repository import StudentRepositoryOnSqlAlchemy
from web.home import home
from web.student import student_web

DEFAULT_DB = "student.db"


def setup_services():
    db_path = os.path.join(os.getcwd(), DEFAULT_DB)
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    db_session = Session(bind=engine)
    student_repository = StudentRepositoryOnSqlAlchemy(db_session)
    return StudentService(student_repository)


def setup_routers(app: FastAPI):
    student_service = setup_services()
    app.include_router(student_api(student_service), prefix="/api")
    app.include_router(student_web())
    app.include_router(home())
    return app


def initialize_db(db_file: Optional[str] = None):
    db_init.initialize_db(db_file if db_file else DEFAULT_DB)


def perform_standalone_crawling(*args, **kwargs):
    ...


def __help__():
    print("Usage: python main.py [command] [--arg1=val1] ...")
    print("Possible commands are: startserver, initdb, crawl")


def main(*args: tuple[str], **kwargs: dict[str, Any]):
    _, command, *other_args = args
    if command == "startserver":
        return start_server(*other_args, **kwargs)
    if command == "initdb":
        return initialize_db(*other_args, **kwargs)
    if command == "crawl":
        return perform_standalone_crawling(*other_args, **kwargs)
    else:
        return __help__()


def start_server(*args, **kwargs):
    is_development = "--dev" in args
    _app = "main:app" if is_development else app
    uvicorn.run(_app, reload=is_development, **kwargs)


app = setup_routers(FastAPI())
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    args = [x for x in sys.argv if "=" not in x]
    kwargs = {
        x.split("=")[0].replace("-", ""): x.split("=")[1] for x in sys.argv if "=" in x
    }
    main(*args, **kwargs)
