from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.orm import Session
from api.database import SessionLocal
from fastapi.templating import Jinja2Templates
from api.models.coordinate import add_coordinate, get_all_coordinates
from api.util.validators import parse_coordinates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def explorer(request: Request, db: Session = Depends(get_db)):
    coordinates_query = get_all_coordinates(db)
    coordinates = [
        {
            "latitude": coordinate.latitude,
            "longitude": coordinate.longitude,
            "type": coordinate.type,
            "created_by": coordinate.created_by,
            "created_on": coordinate.created_on.strftime('%Y-%m-%d %H:%M:%S')
        } for coordinate in coordinates_query
    ]
    context = {
        "request": request,
        "title": "World Map",
        "coordinates": coordinates
    }
    return templates.TemplateResponse("explorer/explorer.html", context)