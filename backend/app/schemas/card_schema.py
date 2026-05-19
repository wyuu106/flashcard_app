from pydantic import BaseModel

# カード作成時の入力
class CardCreate(BaseModel):
    word: str
    meaning: str

# カード作成時の返り値
class CardResponse(BaseModel):
    id: int
    word: str
    meaning: str

    class Config:
       from_attributes = True  # SQLAlchemy対応