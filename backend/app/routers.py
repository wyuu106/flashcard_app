from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas, cruds
from app.auth import get_current_user

router = APIRouter()

# ユーザー登録
@router.post('/users', response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return cruds.create_user(db, user)

# カード作成
@router.post("/cards", response_model=schemas.CardResponse)
def create_card(
    card: schemas.CardCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    user_id = current_user.id
    return cruds.create_card(db, card, user_id)

# カード更新
@router.put("/cards/{card_id}", response_model=schemas.CardResponse)
def update_card(card_id: int, new_card: schemas.CardCreate, db: Session = Depends(get_db)):
    return cruds.update_card(db, card_id, new_card)

# カード削除
@router.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    cruds.delete_card(db, card_id)

# カード一覧取得
@router.get("/cards", response_model=list[schemas.CardResponse])
def get_cards(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user_id = current_user.id
    return cruds.get_cards(db, user_id)

# カード1件取得
@router.get("/cards/{card_id}", response_model=schemas.CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    return cruds.get_card(db, card_id)