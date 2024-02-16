#!/usr/bin/env python3

import app.api.routers.home as home
import app.api.routers.explorer as explorer
from app.api.database import Base, engine

from fastapi import FastAPI

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Configure app routes
app.include_router(home.router)
app.include_router(explorer.router, prefix="/explorer")
