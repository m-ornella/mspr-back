from pydantic import BaseModel
from typing import Optional

class AnswerBase(BaseModel):
    content: str
    question_id: int
    user_id: int

class AnswerCreate(AnswerBase):
    pass

class AnswerUpdate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int

    class Config:
        orm_mode = True
