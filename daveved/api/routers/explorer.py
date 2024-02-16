from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from daveved.api.database import SessionLocal
from daveved.api.models.coordinate import get_all_coordinates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

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

@router.get("/")
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
        "title": "World Map",
        "coordinates": coordinates
    }
    return templates.TemplateResponse("explorer/explorer.html", context)
