from fastapi import FastAPI
from app import models, routers
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)