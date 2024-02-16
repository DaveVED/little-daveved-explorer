from pydantic import BaseModel

from sqlalchemy.orm import Session

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import HTTPException

from app.api.database import SessionLocal
from app.api.models.coordinate import get_all_coordinates, add_coordinate

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

class CoordinateUpdate(BaseModel):
    latitude: float
    longitude: float
    created_by: str
    type: str

@router.post("/update-selection")
def update_selection(coordinate_update: CoordinateUpdate, db: Session = Depends(get_db)):
    """
    Update the selection based on user input.

    Args:
        coordinate_update (CoordinateUpdate): Request body containing latitude, longitude, and name.
        db (Session): Database session.

    Returns:
        A message indicating the update was successful or an error.
    """
    try:
        # Use the data from coordinate_update to update the selection
        # For example, create or update a model instance
        
        # Write the coordinate to the database
        new_coordinate = add_coordinate(
            db=db,
            latitude=coordinate_update.latitude,
            longitude=coordinate_update.longitude,
            type=coordinate_update.type,
            user=coordinate_update.created_by
        )

        coordinates = get_all_coordinates(db)

        return {"message": f"Selection updated for {coordinate_update.created_by} at ({coordinate_update.latitude}, {coordinate_update.longitude}). Coordinate ID: {new_coordinate.id}", "coordinates": coordinates}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while updating the selection.")