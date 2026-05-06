from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.db import Base
from uuid import uuid4

class Cards(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(String, primary_key=True, default=uuid4())
    word: Mapped[str] = mapped_column(String)
    meaning: Mapped[str] = mapped_column(String)