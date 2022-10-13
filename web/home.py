from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

def home():
    router = APIRouter()

    @router.get("/", response_class=RedirectResponse)
    def home(request: Request):
        return "/students/list"

    return router
