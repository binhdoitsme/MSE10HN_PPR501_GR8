from functools import lru_cache

from business.student_services import StudentForm, StudentService
from fastapi import APIRouter
from utils.responses import (
    Response,
    default_exception_handling,
    json_on_success,
    success_with_data,
)


@lru_cache()
def student_api(service: StudentService):
    router = APIRouter(prefix="/students")

    @router.get("/")
    @default_exception_handling
    @json_on_success
    def get_all_students() -> Response:
        """Define an endpoint. Must return Pydantic compatible data type."""
        all_students = service.get_all_students()
        return success_with_data(all_students)

    @router.get("/{id:int}")
    @default_exception_handling
    @json_on_success
    def get_student_by_id(id: int) -> Response:
        find_student = service.get_student_by_id(id)
        return success_with_data(find_student)

    @router.post("/")
    @default_exception_handling
    @json_on_success
    def create_student(form: StudentForm) -> Response:
        new_student = service.create_student(form=form)
        return success_with_data(new_student)

    @router.put("/{id:int}")
    @default_exception_handling
    @json_on_success
    def update_student(id: int, form: StudentForm) -> Response:
        assert id == form.id,"ID should be equal to ID of Form"
        updated_student = service.update_student(form=form)
        return success_with_data(updated_student)

    @router.delete("/{id:int}")
    @default_exception_handling
    @json_on_success
    def delete_student(id: int) -> Response:
        deleted_student = service.delete_student(id=id)
        return success_with_data(deleted_student)

    return router
