# Wiki Quiz Generator 

A full-stack web app that generates quizzes from any Wikipedia article URL using an LLM.  
It scrapes content from Wikipedia, extracts important entities, and generates multiple-choice questions.

---

## Live Demo

- **Frontend (Vercel):** https://wiki-quiz-bice.vercel.app/
- **Backend (Render):** https://wiki-quiz-2.onrender.com  
---

## Features

Enter any Wikipedia URL and generate a quiz  
Automatically extracts:
- Title
- Summary
- Key Entities (People, Organizations, Locations)
Generates quiz questions using Gemini LLM  
Stores quizzes in SQLite database
History page (Past quizzes list)  
View quiz details anytime  
Clean UI with tabs (Generate Quiz / Past Quizzes)

---

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript (Vanilla JS)

### Backend
- FastAPI (Python)
- SQLite
- SQLAlchemy ORM
- Requests + BeautifulSoup (Scraping)
- Gemini API + LangChain (Quiz generation)

### Deployment
- Frontend hosted on **Vercel**
- Backend hosted on **Render**

---

## 📂 Project Structure
wiki-quiz-project/
│
├── backend/
│ ├── main.py
│ ├── scraper.py
│ ├── llm_quiz.py
│ ├── db.py
│ ├── models.py
│ ├── schemas.py
│ ├── requirements.txt
│ └── wikiquiz.db
│
├── frontend/
│ └── index.html
│
└── README.md


---

## How to Run Locally

### Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO/wiki-quiz-project

Backend Setup:

Go to backend folder:
cd backend

Create virtual environment:
python -m venv venv

Activate venv:
 Windows:
venv\Scripts\activate

Create .env file inside backend/:
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY

Run FastAPI backend:
uvicorn main:app --reload

Backend will run at:
http://127.0.0.1:8000

Frontend Setup:
Open the frontend file:
frontend/index.html

## Screenshots

### Generate Quiz Page
![Generate Quiz](screenshots/Screenshot%202026-01-18%20175729.png)

### Quiz Result Page
![Quiz Result](screenshots/Screenshot%202026-01-18%20175802.png)

### Past Quizzes Page
![Past Quizzes](screenshots/Screenshot%202026-01-18%20175818.png)

### Quiz Details Page
![Quiz Details](screenshots/Screenshot%202026-01-18%20175840.png)
