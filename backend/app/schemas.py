from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        from_attributes = True
        

class CardCreate(BaseModel):
    word: str
    meaning: str

class CardResponse(BaseModel):
    id: int
    word: str
    meaning: str

    class Config:
       from_attributes = True  # SQLAlchemy対応