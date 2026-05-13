from sqlalchemy.orm import Session
from fastapi import Response, Depends, HTTPException, status
from app.models import card_model
from app.schemas import card_schema

# カード作成
def create_card(db: Session, card: card_schema.CardCreate, user_id: str):
    db_card = card_model.Card(
        word = card.word,
        meaning = card.meaning,
        user_id = user_id
    )

    db.add(db_card)
    db.commit()
    db.refresh(db_card)

    return db_card

# カード更新
def update_card(db: Session, id: int, user_id: str, new_card: card_schema.CardCreate):
    card = db.query(card_model.Card).filter(
        card_model.Card.id == id,
        card_model.Card.user_id == user_id
        ).first()

    card.word = new_card.word
    card.meaning = new_card.meaning

    db.commit()
    db.refresh(card)

    return card

# カード削除
def delete_card(db: Session, id: int, user_id: str):
    db_card = db.query(card_model.Card).filter(
        card_model.Card.id == id,
        card_model.Card.user_id == user_id
        ).one_or_none()

    if not db_card:
        raise HTTPException(status_code=404, detail="該当するカードが見つかりませんでした")

    db.delete(db_card)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# カード一覧取得
def get_cards(db: Session, user_id: str):
    return db.query(card_model.Card).filter(
        card_model.Card.user_id == user_id
        ).all()

# カード１件取得
def get_card(db: Session, id: int, user_id: str):
    card = db.query(card_model.Card).filter(
        card_model.Card.id == id,
        card_model.Card.user_id == user_id
        ).one_or_none()

    if not card:
        raise HTTPException(status_code=404, detail='該当するカードが見つかりませんでした')
    
    return card