#!/usr/bin/env python3

import api.routers.home as home
import api.routers.explorer as explorer
from api.database import Base, engine  # Import Base and engine

from fastapi import FastAPI

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(home.router)
app.include_router(explorer.router, prefix="/explorer")
