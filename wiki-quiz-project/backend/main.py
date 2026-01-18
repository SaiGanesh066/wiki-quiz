from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

from db import Base, engine, get_db
from models import QuizRecord
from schemas import GenerateRequest, QuizResponse, HistoryItem
from scraper import scrape_wikipedia
from llm_quiz import generate_quiz

Base.metadata.create_all(bind=engine)

app = FastAPI()

# React frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate", response_model=QuizResponse)
def generate(req: GenerateRequest, db: Session = Depends(get_db)):
    url = req.url.strip()

    # if already exists, return cached
    existing = db.query(QuizRecord).filter(QuizRecord.url == url).first()
    if existing:
        data = json.loads(existing.result_json)
        return {
            "id": existing.id,
            "url": existing.url,
            "title": existing.title,
            "summary": existing.summary,
            "sections": data.get("sections", []),
            "key_entities": data["key_entities"],
            "quiz": data["quiz"],
            "related_topics": data["related_topics"],
        }

    try:
        scraped = scrape_wikipedia(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scraping failed: {e}")

    try:
        quiz_json = generate_quiz(
            title=scraped["title"],
            text=scraped["text"],
            sections=scraped["sections"],
            summary=scraped["summary"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM failed: {e}")

    # include sections in output json
    quiz_json["sections"] = scraped["sections"]

    record = QuizRecord(
        url=url,
        title=scraped["title"],
        summary=scraped["summary"],
        extracted_text=scraped["text"],
        result_json=json.dumps(quiz_json)
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "url": record.url,
        "title": record.title,
        "summary": record.summary,
        "sections": scraped["sections"],
        "key_entities": quiz_json["key_entities"],
        "quiz": quiz_json["quiz"],
        "related_topics": quiz_json["related_topics"],
    }

@app.get("/history", response_model=list[HistoryItem])
def history(db: Session = Depends(get_db)):
    items = db.query(QuizRecord).order_by(QuizRecord.created_at.desc()).all()
    return [
        {
            "id": i.id,
            "url": i.url,
            "title": i.title,
            "created_at": i.created_at.isoformat(),
        }
        for i in items
    ]

@app.get("/quiz/{quiz_id}", response_model=QuizResponse)
def quiz_details(quiz_id: int, db: Session = Depends(get_db)):
    record = db.query(QuizRecord).filter(QuizRecord.id == quiz_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not found")

    data = json.loads(record.result_json)

    return {
        "id": record.id,
        "url": record.url,
        "title": record.title,
        "summary": record.summary,
        "sections": data.get("sections", []),
        "key_entities": data["key_entities"],
        "quiz": data["quiz"],
        "related_topics": data["related_topics"],
    }
