from fastapi import FastAPI

from app.config.settings import Settings, get_settings
from app.db.db import app_lifespan
from app.routes import ALL_ROUTERS
from app.views import *

settings: Settings = get_settings()

app = FastAPI(
    title=settings.title,
    summary=settings.summary,
    description=settings.description,
    version=settings.version,
    contact=settings.contact,
    lifespan=app_lifespan,
)

for router in ALL_ROUTERS:
    app.include_router(router)
