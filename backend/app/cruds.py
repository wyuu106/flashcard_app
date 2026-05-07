from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from app import models, schemas

# 作成
def create_card(db: Session, card: schemas.CardCreate):
    db_card = models.Card(
        word = card.word,
        meaning = card.meaning
    )

    db.add(db_card)
    db.commit()
    db.refresh(db_card)

    return db_card

# 更新
def update_card(db: Session, id: int, new_card: schemas.CardCreate):
    card = db.query(models.Card).filter(models.Card.id == id).first()

    card.word = new_card.word
    card.meaning = new_card.meaning

    db.commit()
    db.refresh(card)

    return card

# 削除
def delete_card(db: Session, id: int):
    db_card = db.query(models.Card).filter(models.Card.id == id).one_or_none()

    if not db_card:
        raise HTTPException(status_code=404, detail="Card not Found")

    db.delete(db_card)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# 一覧取得
def get_cards(db: Session):
    return db.query(models.Card).all()

# １件取得
def get_card(db: Session, id: int):
    card = db.query(models.Card).filter(models.Card.id == id).one_or_none()

    if not card:
        raise HTTPException(status_code=404, detail='Card not Found')
    
    return card