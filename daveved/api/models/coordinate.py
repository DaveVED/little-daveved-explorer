from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.orm import Session
from daveved.api.database import Base
from datetime import datetime
from typing import List

class Coordinate(Base):
    """
    Represents a geographical coordinate stored in the database.
    
    Attributes:
        id (Integer): The primary key for the coordinate.
        latitude (Float): The latitude of the coordinate.
        longitude (Float): The longitude of the coordinate.
        type (String): The type of location this coordinate represents.
        created_by (String): The identifier of the user who created this coordinate.
        created_on (DateTime): The datetime when the coordinate was created, defaults to the current time.
    """
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    type = Column(String, index=True)
    created_by = Column(String, index=True)
    created_on = Column(DateTime, default=datetime.utcnow)  # Default to the current time

def add_coordinate(db: Session, latitude: float, longitude: float, type: str, user: str) -> Coordinate:
    """
    Adds a new coordinate to the database.

    Args:
        db (Session): The database session used to add the coordinate.
        latitude (float): The latitude of the coordinate.
        longitude (float): The longitude of the coordinate.
        type (str): The type of location the coordinate represents.
        user (str): The identifier of the user who is adding the coordinate.

    Returns:
        Coordinate: The newly added Coordinate object.
    """
    new_coordinate = Coordinate(latitude=latitude, longitude=longitude, type=type, created_by=user)
    db.add(new_coordinate)
    db.commit()
    db.refresh(new_coordinate)
    return new_coordinate

def get_all_coordinates(db: Session) -> List[Coordinate]:
    """
    Retrieves all coordinates from the database.

    Args:
        db (Session): The database session used to query for coordinates.

    Returns:
        List[Coordinate]: A list of all Coordinate objects in the database.
    """
    return db.query(Coordinate).all()
