#!/usr/bin/env python3

import daveved.api.routers.home as home
import daveved.api.routers.explorer as explorer
from daveved.api.database import Base, engine

from fastapi import FastAPI

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Configure app routes
app.include_router(home.router)
app.include_router(explorer.router, prefix="/explorer")
