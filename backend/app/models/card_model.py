from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from app.db import Base

# カード情報テーブル
class Card(Base):
    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # id は自動生成される
    word: Mapped[str] = mapped_column(String)
    meaning: Mapped[str] = mapped_column(String)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id")) # ユーザーテーブルとの外部キー