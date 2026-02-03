from fastapi import FastAPI, Header, HTTPException
import time
import re
import os

app = FastAPI()

API_KEY = "mysecretkey"

# ---------- ROOT (tester needs this) ----------
@app.get("/")
def root():
    return {"status": "alive"}

# ---------- GET honeypot (tester needs this) ----------
@app.get("/honeypot")
def honeypot_get():
    return {"status": "ready"}

# ---------- Helpers ----------
def detect_scam(msg: str):
    keywords = ["bank", "upi", "otp", "link", "urgent", "account", "verify"]
    score = sum(word in msg.lower() for word in keywords)
    return score >= 2

def extract_info(text: str):
    return {
        "upi_ids": re.findall(r'\b[\w\.-]+@[\w\.-]+\b', text),
        "phishing_links": re.findall(r'https?://\S+', text),
        "bank_accounts": re.findall(r'\b\d{9,18}\b', text),
    }

# ---------- POST honeypot ----------
@app.post("/honeypot")
def honeypot(data: dict, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Tester empty body handle
    message = ""
    if isinstance(data, dict):
        message = data.get("message") or ""

    if not message:
        return {"status": "ok", "message": "Honeypot reachable"}

    is_scam = detect_scam(message)
    extracted = extract_info(message)

    return {
        "is_scam": is_scam,
        "reply": "I am confused, can you explain again?",
        "extracted_intelligence": extracted,
        "confidence": 0.95
    }
