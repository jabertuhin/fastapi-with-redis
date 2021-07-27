from fastapi import FastAPI

from app.routers import health


app = FastAPI()


app.include_router(health.router)