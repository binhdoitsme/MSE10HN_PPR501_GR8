from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

def home():
    router = APIRouter(prefix="/home")
    templates = Jinja2Templates(directory="web/templates")

    @router.get("/", response_class=HTMLResponse)
    def home(request: Request):
        fake_results = [
            {"name": "Pepe smiling", "icon": ":pepe-smile7:"},
            {"name": "Pepe smirking", "icon": ":pepe-smirk:"},
            {"name": "Pepe smirking", "icon": ":pepe-smirk:"}
        ]
        return templates.TemplateResponse(
            "home.html", {"request": request, "results": fake_results}
        )

    return router
