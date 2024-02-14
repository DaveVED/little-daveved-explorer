#!/usr/bin/env python3

import api.routers.home as home
import api.routers.world_map as world_map

from fastapi import FastAPI

app = FastAPI()

app.include_router(home.router)
app.include_router(world_map.router, prefix="/world-map")