from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import user_model
from app.schemas import card_schema
from app.cruds import card_crud
from app.utils.auth import get_current_user

router = APIRouter()

# カード作成
@router.post("/cards", response_model=card_schema.CardResponse)
def create_card(
    card: card_schema.CardCreate,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    user_id = current_user.id
    return card_crud.create_card(db, card, user_id)

# カード更新
@router.put("/cards/{id}", response_model=card_schema.CardResponse)
def update_card(
    id: int,
    new_card: card_schema.CardCreate,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    user_id = current_user.id
    return card_crud.update_card(db, id, user_id, new_card)

# カード削除
@router.delete("/cards/{id}")
def delete_card(
    id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    user_id = current_user.id
    card_crud.delete_card(db, id, user_id)

# カード一覧取得
@router.get("/cards", response_model=list[card_schema.CardResponse])
def get_cards(
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user_id = current_user.id
    return card_crud.get_cards(db, user_id)

# カード1件取得
@router.get("/cards/{id}", response_model=card_schema.CardResponse)
def get_card(
    id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    user_id = current_user.id
    return card_crud.get_card(db, id, user_id)

# 全カード取得
@router.get('/all_cards', response_model = list[card_schema.CardResponse])
def get_all_cards(db: Session = Depends(get_db)):
    return card_crud.get_all_cards(db)