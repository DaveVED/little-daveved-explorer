from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
def world_map_root(request: Request):
    context = {
        "request": request,
        "title": "Home"
    }

    response = templates.TemplateResponse("home.html", context)

    return response