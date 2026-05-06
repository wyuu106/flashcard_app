from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas, cruds

router = APIRouter()

# 作成
@router.post("/cards", response_model=schemas.CardResponse)
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    return cruds.create_card(db, card)

# 更新
@router.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(id: int, card: schemas.CardCreate, db: Session = Depends(get_db)):
    return cruds.update_card(db, id, card)

# 削除
@router.delete("/cards/{card_id}")
def delete_card(id: int, db: Session = Depends(get_db)):
    cruds.delete_card(db, id)

# 一覧取得
@router.get("/cards", response_model=list[schemas.CardList])
def get_cards(db: Session = Depends(get_db)):
    return cruds.get_cards(db)

# 1件取得
@router.get("/cards/{card_id}", response_model=schemas.CardResponse)
def get_card(id: int, db: Session = Depends(get_db)):
    return cruds.get_card(db, id)
