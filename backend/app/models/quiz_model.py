from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from uuid import uuid4
from app.db import Base

# １連のクイズ（１０問）の情報
class QuizSession(Base):
    __tablename__ = 'quiz_session'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    total_questions: Mapped[int] = mapped_column(Integer, default=10)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String)