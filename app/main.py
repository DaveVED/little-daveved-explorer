#!/usr/bin/env python3

import app.api.routers.home as home
import app.api.routers.explorer as explorer
from app.api.database import Base, engine

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Configure app routes
app.include_router(home.router)
app.include_router(explorer.router, prefix="/explorer")
