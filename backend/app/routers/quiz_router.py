from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import user_model
from app.schemas import quiz_schema
from app.cruds import quiz_crud
from app.auth import get_current_user

router = APIRouter()

@router.post('/start', response_model=quiz_schema.QuizStartResponse)
def start_quiz(
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    return quiz_crud.start_quiz(db, user_id)

@router.post('/answer', response_model=quiz_schema.QuizAnswerResponse)
def answer_quiz(
    request: quiz_schema.QuizAnswerRequest,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    return quiz_crud.answer_quiz(db, request, user_id)

@router.post('/finish', response_model=quiz_schema.QuizFinishResponse)
def finish_quiz(
    session_id: str,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    return quiz_crud.finish_quiz(db, session_id, user_id)