from fastapi import FastAPI
from app import models, routers
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.router)