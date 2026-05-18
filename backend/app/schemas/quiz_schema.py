from pydantic import BaseModel

class QuizQuestion(BaseModel):
    card_id: int
    word: str
    choices: list[str]


class QuizStartResponse(BaseModel):
    session_id: str
    questions: list[QuizQuestion]


class QuizAnswerRequest(BaseModel):
    session_id: str
    card_id: int
    answer: str


class QuizAnswerResponse(BaseModel):
    is_correct: bool
    correct_count: int


class QuizFinishResponse(BaseModel):
    correct_count: int
    total_questions: int