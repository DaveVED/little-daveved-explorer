from sqlalchemy.orm import Session

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.api.database import SessionLocal
from app.api.models.coordinate import get_all_coordinates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

selectable_explorer_options = [
    {
        "title": "Option 1: Map Selection",
        "description": "Select a location on the map and confirm the details. This option allows you to directly interact with the map to pinpoint your current location or a destination you recommend.",
        "selected": False
    },
    {
        "title": "Option 2: Form Submission",
        "description": "Fill out the form and submit your suggestion. Use this option if you prefer to input your location or suggestion directly through our form.",
        "selected": False
    }
]
is_option_selected = False

def get_db():
    """
    Dependency that creates a new SQLAlchemy SessionLocal instance to be used for a single request.
    This pattern ensures that each request gets a clean database session and that the session is always closed properly, helping to prevent resource leaks and maintaining the integrity of the connection pool.
    
    Yields:
        Session: An instance of the database session that can be used to perform database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def explorer(request: Request, db: Session = Depends(get_db)):
    """
    Route to serve the explorer page, querying all coordinates from the database
    and passing them to the Jinja2 template for rendering.

    Args:
        request: The request object, necessary for Jinja2Templates to generate responses.
        db: The SQLAlchemy database session, obtained through dependency injection.

    Returns:
        A TemplateResponse object that represents the rendered HTML page.
    """
    coordinates_query = get_all_coordinates(db)
    
    # This remap is required, so we can create the dynamic map on page load.
    # For example, var coordinates = JSON.parse('{{ coordinates | tojson | safe }}');
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
        "title": "Explorer",
        "coordinates": coordinates
    }
    return templates.TemplateResponse("explorer/explorer.html", context)

@router.get("/get-selectable-options", response_class=HTMLResponse)
def get_selectable_options(request: Request):
    context = {
        "request": request,
        "title": "Explorer",
        "options": selectable_explorer_options,
        "isOptionSelected": is_option_selected
    }

    return templates.TemplateResponse("explorer/getting_started_options.html", context)

@router.get("/toggle-selectable-option/{option_id}", response_class=HTMLResponse)
def set_selectable_options(request: Request, option_id: int):
    adjusted_option_id = option_id - 1

    # Clear out all options
    for option in selectable_explorer_options:
        option["selected"] = False
    
    if 0 <= adjusted_option_id < len(selectable_explorer_options):
        selectable_explorer_options[adjusted_option_id]["selected"] = True
    
    is_option_selected = True
    context = {
        "request": request,
        "title": "Explorer",
        "options": selectable_explorer_options,
        "isOptionSelected": is_option_selected
    }

    return templates.TemplateResponse("explorer/getting_started_options.html", context)
