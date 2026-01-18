import os, json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.4
)


PROMPT = PromptTemplate(
    input_variables=["title", "text", "sections", "summary"],
    template="""
You are a quiz generator.

From the Wikipedia content below, generate JSON STRICTLY in this format:
{{
  "key_entities": {{
    "people": [],
    "organizations": [],
    "locations": []
  }},
  "quiz": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "...",
      "difficulty": "easy|medium|hard",
      "explanation": "..."
    }}
  ],
  "related_topics": ["...", "...", "..."]
}}

Rules:
- Generate 5 to 10 MCQ questions.
- Each question must have 4 options.
- The answer must exactly match one option.
- Explanation must be short (1 line).
- Difficulty must be easy/medium/hard only.
- Related topics must be Wikipedia-style titles.

TITLE: {title}

SUMMARY: {summary}

SECTIONS: {sections}

TEXT:
{text}
"""
)

def generate_quiz(title: str, text: str, sections: list, summary: str):
    prompt = PROMPT.format(title=title, text=text, sections=sections, summary=summary)
    response = llm.invoke(prompt).content

    # response may include markdown, attempt to extract JSON safely
    start = response.find("{")
    end = response.rfind("}")
    cleaned = response[start:end+1]

    return json.loads(cleaned)
