from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re
import requests

app = FastAPI()
API_KEY = "mysecretkey"

# ---------- Models ----------
class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: list
    metadata: dict

# ---------- Routes for tester ----------
@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/honeypot")
def honeypot_get():
    return {"status": "ready"}

# ---------- Helpers ----------
def extract_info(text: str):
    return {
        "upi_ids": re.findall(r'\b[\w\.-]+@[\w\.-]+\b', text),
        "phishing_links": re.findall(r'https?://\S+', text),
        "bank_accounts": re.findall(r'\b\d{9,18}\b', text),
    }

def persona_reply(text: str):
    t = text.lower()
    if "otp" in t:
        return "I got some number. Where should I enter this OTP?"
    if "link" in t:
        return "I opened the link. What details should I fill?"
    if "upi" in t or "pay" in t:
        return "Which app should I use to send money? Please guide me."
    return "Why is my account being suspended?"

def send_to_guvi(session_id, info):
    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json={
                "sessionId": session_id,
                **info
            },
            timeout=3
        )
    except:
        pass

# ---------- Main Honeypot ----------
@app.post("/honeypot")
def honeypot(req: HoneypotRequest, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = req.message.text
    info = extract_info(text)

    if any(info.values()):
        send_to_guvi(req.sessionId, info)

    reply = persona_reply(text)

    return {
        "status": "success",
        "reply": reply
    }
