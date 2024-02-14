from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.orm import Session
from api.database import SessionLocal
from fastapi.templating import Jinja2Templates
from api.models.coordinate import add_coordinate
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
    context = {
        "request": request,
        "title": "World Map"
    }
    return templates.TemplateResponse("explorer/explorer.html", context)

@router.post("/coordinates")
def explorer_coordinates(request: Request, coordinateContent: str = Form(...), mapOptions: str = Form(...), db: Session = Depends(get_db)):
    print("HELLO WORLD", "   ", coordinateContent, "   ", mapOptions)

    latitude, longtitude = parse_coordinates(coordinateContent)
    coordinate = add_coordinate(db, latitude, longtitude, "Test", "test222")

    context = {
        "request": request,
        "title": "World Map",
        "coordinateContent": coordinateContent,
        "mapOptions": mapOptions,
        "coordinate": coordinate
    }

    return templates.TemplateResponse("explorer/coordinate-form.html", context)