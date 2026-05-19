from pydantic import BaseModel

# ユーザー登録時の入力
class UserCreate(BaseModel):
    name: str
    password: str

# ユーザー登録時の返り値
class UserResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True