from functools import lru_cache

from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


@lru_cache
def student_web():
    router = APIRouter(prefix="/students")
    templates = Jinja2Templates(directory="web/templates")

    student_list_template = "student_list.html"

    @router.get("/list", response_class=HTMLResponse)
    def student_list(request: Request):
        ...

    @router.get("/create", response_class=HTMLResponse)
    def create_student_form():
        ...

    @router.get("/update", response_class=HTMLResponse)
    def update_student_form():
        ...

    return router
