from pydantic import BaseModel

# クイズ１問の情報セット
class QuizQuestion(BaseModel):
    card_id: int
    word: str
    choices: list[str]

# クイズスタート関数の返り値
class QuizStartResponse(BaseModel):
    session_id: str
    questions: list[QuizQuestion]

# フロントから送られてくる回答の情報
class QuizAnswerRequest(BaseModel):
    session_id: str
    card_id: int # 出題されたカードのid
    answer: str # 答えとして選んだ選択肢（meaning）

# 回答の正誤判定の返り値
class QuizAnswerResponse(BaseModel):
    is_correct: bool
    correct_count: int

# クイズ終了関数の返り値
class QuizFinishResponse(BaseModel):
    correct_count: int
    total_questions: int