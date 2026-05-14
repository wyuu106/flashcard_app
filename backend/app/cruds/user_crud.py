from sqlalchemy.orm import Session
from fastapi import Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import user_model
from app.schemas import user_schema
from app.auth import hash_password, verify_password, create_access_token

# ユーザー登録
def create_user(db: Session, user: user_schema.UserCreate):
    exist_user = db.query(user_model.User).filter(user_model.name == user.name).first()
    if exist_user:
        raise HTTPException(status_code=400, detail='このユーザー名は既に使われています')
    
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail='パスワードは6文字以上')

    db_user = user_model.User(
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# ユーザー一覧
def get_users(db: Session):
    return db.query(user_model.User).all()

# ユーザー削除
def delete_user(db: Session, id: str):
    db_user = db.query(user_model.User).filter(user_model.User.id == id).one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="該当するユーザーが見つかりませんでした")

    db.delete(db_user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ログイン
def login(db: Session, form_data: OAuth2PasswordRequestForm):
    user = db.query(user_model.User).filter(user_model.User.name == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="ユーザーが見つかりませんでした")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="パスワードが違います")

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }