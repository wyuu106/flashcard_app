from pydantic import BaseModel

class CardCreate(BaseModel):
    word: str
    meaning: set

class CardResponse(BaseModel):
    id: int
    word: str
    maening: str

    class Config:
       from_attributes = True  # SQLAlchemy対応

class CardList(BaseModel):
    words: list[CardResponse]