from functools import lru_cache

from business.student_services import StudentService
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates


@lru_cache
def student_web(service: StudentService):
    router = APIRouter(prefix="/students")
    templates = Jinja2Templates(directory="web/templates")

    student_list_template = "student_list.html"

    @router.get("/list", response_class=HTMLResponse)
    def student_list(request: Request):
        context = {
            "request": request,
            "create_student_link": "/students/create",
            "update_student_link": "/students/update?id={id}",
            "delete_student_link": "/api/students/{id}",
            "students": service.get_all_students(),
        }
        return templates.TemplateResponse(student_list_template, context)

    @router.get("/create", response_class=HTMLResponse)
    def create_student_form():
        ...

    @router.get("/update", response_class=HTMLResponse)
    def update_student_form():
        ...

    return router
