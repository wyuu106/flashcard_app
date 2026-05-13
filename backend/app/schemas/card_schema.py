from pydantic import BaseModel

class CardCreate(BaseModel):
    word: str
    meaning: str

class CardResponse(BaseModel):
    id: int
    word: str
    meaning: str

    class Config:
       from_attributes = True  # SQLAlchemy対応