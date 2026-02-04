from fastapi import FastAPI, Header, HTTPException
import re
import time

app = FastAPI()
API_KEY = "mysecretkey"

# ---------------- Tester required routes ----------------
@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/honeypot")
def honeypot_get():
    return {"status": "ready"}

# ---------------- Scam Detection ----------------
def detect_scam(msg: str):
    keywords = ["bank", "upi", "otp", "link", "urgent", "account", "verify", "pay"]
    score = sum(word in msg.lower() for word in keywords)
    confidence = min(0.5 + 0.1 * score, 0.99)
    return score >= 2, round(confidence, 2)

# ---------------- Intelligence Extraction ----------------
def extract_info(text: str):
    return {
        "upi_ids": re.findall(r'\b[\w\.-]+@[\w\.-]+\b', text),
        "phishing_links": re.findall(r'https?://\S+', text),
        "bank_accounts": re.findall(r'\b\d{9,18}\b', text),
    }

# ---------------- Persona Reply ----------------
def persona_reply(msg: str):
    text = msg.lower()

    if "otp" in text:
        return "I received a number. Where should I enter this OTP?"
    if "link" in text:
        return "I opened the link. What details should I fill?"
    if "upi" in text:
        return "Which app should I use to send money? I am confused."
    if "bank" in text:
        return "My bank app is slow. Please explain again."

    return "Please explain again, I am confused."

# ---------------- Honeypot POST ----------------
@app.post("/honeypot")
def honeypot_post(data: dict = None, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Handle tester empty or weird body safely
    if not isinstance(data, dict):
        return {"status": "ok", "message": "Honeypot reachable"}

    message = data.get("message", "")

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
        "engagement_metrics": {
            "response_time_sec": round(time.time() - start, 2)
        }
    }
