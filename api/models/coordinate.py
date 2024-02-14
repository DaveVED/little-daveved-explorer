from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.orm import Session
from api.database import Base
from datetime import datetime

class Coordinate(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    type = Column(String, index=True)  # Ensure you have defined coordinate types elsewhere
    created_by = Column(String, index=True)  # This should ideally reference a user ID from a users table
    created_on = Column(DateTime, default=datetime.utcnow)

def add_coordinate(db: Session, latitude: float, longitude: float, type: str, user: str) -> Coordinate:
    new_coordinate = Coordinate(latitude=latitude, longitude=longitude, type=type, created_by=user)
    db.add(new_coordinate)
    db.commit()
    db.refresh(new_coordinate)
    return new_coordinate
