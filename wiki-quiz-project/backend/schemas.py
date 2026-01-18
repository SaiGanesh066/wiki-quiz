from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class GenerateRequest(BaseModel):
    url: str

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class QuizResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict[str, List[str]]
    sections: List[str]
    quiz: List[QuizQuestion]
    related_topics: List[str]

class HistoryItem(BaseModel):
    id: int
    url: str
    title: str
    created_at: str
