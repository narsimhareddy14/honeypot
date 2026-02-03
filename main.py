from fastapi import FastAPI, Header, HTTPException
import re
import time

app = FastAPI()
API_KEY = "mysecretkey"

# ---------- ROOT (tester needs) ----------
@app.get("/")
def root():
    return {"status": "alive"}

# ---------- GET honeypot (tester needs) ----------
@app.get("/honeypot")
def honeypot_get():
    return {"status": "ready"}

# ---------- Helpers ----------
def detect_scam(msg: str):
    keywords = ["bank", "upi", "otp", "link", "urgent", "account", "verify"]
    score = sum(word in msg.lower() for word in keywords)
    return score >= 2, round(min(0.5 + 0.1 * score, 0.99), 2)

def extract_info(text: str):
    return {
        "upi_ids": re.findall(r'\b[\w\.-]+@[\w\.-]+\b', text),
        "phishing_links": re.findall(r'https?://\S+', text),
        "bank_accounts": re.findall(r'\b\d{9,18}\b', text),
    }

def persona_reply(msg: str):
    if "otp" in msg.lower():
        return "I received some number. Where should I type this OTP?"
    if "link" in msg.lower():
        return "I opened the link. What details should I enter?"
    if "upi" in msg.lower():
        return "Which app should I open to send money? Please explain again."
    return "Please explain again, I am confused."

# ---------- POST honeypot ----------
@app.post("/honeypot")
def honeypot_post(data: dict = {}, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Tester empty body safety
    message = data.get("message") if isinstance(data, dict) else ""

    if not message:
        return {"status": "ok", "message": "Honeypot reachable"}

    start = time.time()

    is_scam, confidence = detect_scam(message)
    reply = persona_reply(message)
    extracted = extract_info(message)

    return {
        "is_scam": is_scam,
        "reply": reply,
        "extracted_intelligence": extracted,
        "confidence": confidence,
        "response_time_sec": round(time.time() - start, 2)
    }
