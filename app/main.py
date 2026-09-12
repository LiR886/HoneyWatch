from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import Base, engine
from app.routers import dashboard, honeypot


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="A defensive web honeypot for capturing and detecting suspicious authentication activity.",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(honeypot.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}
