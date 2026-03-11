from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing; lock this down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = openai.OpenAI(
    base_url="https://api.llm7.io/v1",
    api_key=os.getenv("LLM7_API_KEY", ""),
)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"ok": True, "message": "API is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        resp = client.chat.completions.create(
            model="default",
            messages=[
                {"role": "user", "content": req.prompt}
            ],
        )
        return {"reply": resp.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
