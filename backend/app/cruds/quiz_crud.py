from sqlalchemy.orm import Session
from fastapi import HTTPException
import random
from app.models import card_model, quiz_model
from app.schemas import quiz_schema
from app.quiz_util import create_choices


def start_quiz(db: Session, user_id: str):
    cards = db.query(card_model.Card).filter(
        card_model.Card.user_id == user_id
        ).all()
    
    if len(cards) < 10:
        raise HTTPException(status_code=400, detail="カードが不足しています")

    db_quizsession = quiz_model.QuizSession(
        user_id = user_id,
        status = 'in_progress'
    )
    
    db.add(db_quizsession)
    db.commit()
    db.refresh(db_quizsession)

    selected_cards = random.sample(cards, 10)

    all_meaning = [card.meaning for card in cards]

    questions = []

    for question_card in selected_cards:
        questions.append(
            quiz_schema.QuizQuestion(
                card_id = question_card.id,
                word = question_card.word,
                choices = create_choices(question_card.meaning, all_meaning)
            )
        )

    return {
        'session_id': db_quizsession.id,
        'questions': questions
    }


def answer_quiz(db: Session, request: quiz_schema.QuizAnswerRequest, user_id: str):
    quiz_session = db.query(quiz_model.QuizSession).filter(
        quiz_model.QuizSession.id == request.session_id,
        quiz_model.QuizSession.user_id == user_id
    ).first()

    if not quiz_session:
        raise HTTPException(404)
    
    if quiz_session.status != 'in_progress':
        raise HTTPException(400, detail='このクイズは終了しています')
    
    question_card = db.query(card_model.Card).filter(
        card_model.Card.id == request.card_id,
        card_model.Card.user_id == user_id
    ).first()

    if not question_card:
        raise HTTPException(404)
    
    is_correct = question_card.meaning == request.answer
    
    if is_correct:
        quiz_session.correct_count += 1
        db.commit()

    return {
        'is_correct': is_correct,
        'correct_count': quiz_session.correct_count
    }

def finish_quiz(db: Session, session_id: str, user_id: str):
    quiz_session = db.query(quiz_model.QuizSession).filter(
        quiz_model.QuizSession.id == session_id,
        quiz_model.QuizSession.user_id == user_id
    ).first()

    if not quiz_session:
        raise HTTPException(404)
    
    quiz_session.status = 'finished'

    db.commit()

    return {
        'correct_count': quiz_session.correct_count,
        'total_questions': quiz_session.total_questions
    }