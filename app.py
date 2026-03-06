from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

# You said you don't care if it's exposed, but env vars are still the cleaner option.
API_KEY = "YOUR_LLM7_TOKEN_HERE"

client = openai.OpenAI(
    base_url="https://api.llm7.io/v1",
    api_key=API_KEY,
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
        return {
            "reply": resp.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
