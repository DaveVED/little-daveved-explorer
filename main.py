#!/usr/bin/env python3

import api.routers.home as home
import api.routers.explorer as explorer

from fastapi import FastAPI

app = FastAPI()

app.include_router(home.router)
app.include_router(explorer.router, prefix="/explorer")