from fastapi import FastAPI, Header, HTTPException
import requests
import re
import time

app = FastAPI()
API_KEY = "mysecretkey"

# -------- Memory for sessions --------
SESSIONS = {}

# -------- Root for tester --------
@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/honeypot")
def honeypot_get():
    return {"status": "ready"}

# -------- Scam detection --------
def is_scam(text: str):
    keywords = ["bank", "otp", "upi", "verify", "urgent", "account", "link", "pay"]
    return any(k in text.lower() for k in keywords)

# -------- Intelligence extraction --------
def extract_info(text: str):
    return {
        "upi_ids": re.findall(r'\b[\w\.-]+@[\w\.-]+\b', text),
        "phishing_links": re.findall(r'https?://\S+', text),
        "bank_accounts": re.findall(r'\b\d{9,18}\b', text),
    }

# -------- Persona reply --------
def persona_reply(text: str):
    t = text.lower()
    if "otp" in t:
        return "I got some number. Where should I enter this OTP?"
    if "link" in t:
        return "I opened the link. What details should I fill?"
    if "upi" in t or "pay" in t:
        return "Which app should I use to send money? Please guide me."
    return "Why is my account being suspended?"

# -------- GUVI callback --------
def send_to_guvi(session_id, info):
    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json={
                "sessionId": session_id,
                "upi_ids": info["upi_ids"],
                "phishing_links": info["phishing_links"],
                "bank_accounts": info["bank_accounts"]
            },
            timeout=3
        )
    except:
        pass  # do not break API if callback fails

# -------- Main Honeypot --------
@app.post("/honeypot")
def honeypot(data: dict = None, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Safety for tester
    if not isinstance(data, dict):
        return {"status": "success", "reply": "Hello?"}

    session_id = data.get("sessionId")
    message_obj = data.get("message", {})
    text = message_obj.get("text", "")

    if not session_id or not text:
        return {"status": "success", "reply": "Hello?"}

    # Maintain session history
    SESSIONS.setdefault(session_id, []).append(text)

    # Detect scam & extract info
    scam = is_scam(text)
    info = extract_info(text)

    # If intelligence found, send to GUVI
    if scam and (info["upi_ids"] or info["phishing_links"] or info["bank_accounts"]):
        send_to_guvi(session_id, info)

    reply = persona_reply(text)

    # EXACT expected response format
    return {
        "status": "success",
        "reply": reply
    }
