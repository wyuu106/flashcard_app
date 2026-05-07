from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app.db import Base

class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # id は自動生成される
    word: Mapped[str] = mapped_column(String)
    meaning: Mapped[str] = mapped_column(String)