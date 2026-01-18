from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class QuizRecord(Base):
    __tablename__ = "quiz_records"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), unique=True, index=True)
    title = Column(String(300))
    summary = Column(Text)
    extracted_text = Column(Text)
    result_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
