from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
def world_map_root(request: Request):
    context = {
        "request": request,
        "title": "World Map"
    }

    response = templates.TemplateResponse("world-map/map.html", context)

    return response