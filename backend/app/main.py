from fastapi import FastAPI
from app.routers import user_router, card_router, quiz_router
from app.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://flashcard-app-ecru-six.vercel.app" # 最後に / つけないように
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(card_router.router)
app.include_router(quiz_router.router)