from fastapi import FastAPI, Header, HTTPException
import re
import time
import random

app = FastAPI()
API_KEY = "mysecretkey"

# -------- MEMORY STORE (per conversation) --------
MEMORY = {}

# -------- PERSONA --------
PERSONA = {
    "age": 62,
    "style": "confused, polite, slow with technology"
}

# -------- SCAM DETECTION --------
def detect_scam(msg: str):
    keywords = ["bank", "upi", "account", "blocked", "urgent", "link", "verify", "otp", "pay"]
    score = sum(word in msg.lower() for word in keywords)
    is_scam = score >= 2
    confidence = min(0.5 + 0.1 * score, 0.99)
    return is_scam, round(confidence, 2)

# -------- EXTRACT INTELLIGENCE --------
def extract_info(text: str):
    upi_pattern = r'\b[\w\.-]+@[\w\.-]+\b'
    url_pattern = r'https?://\S+'
    account_pattern = r'\b\d{9,18}\b'

    return {
        "upi_ids": re.findall(upi_pattern, text),
        "phishing_links": re.findall(url_pattern, text),
        "bank_accounts": re.findall(account_pattern, text),
    }

# -------- TACTICS --------
def detect_tactics(msg: str):
    tactics = []
    t = msg.lower()
    if "otp" in t:
        tactics.append("OTP request")
    if "http" in t:
        tactics.append("Phishing link")
    if "upi" in t:
        tactics.append("UPI payment request")
    if "urgent" in t:
        tactics.append("Urgency pressure")
    return tactics

# -------- SMART PERSONA REPLY --------
def persona_reply(cid, msg):
    time.sleep(random.uniform(1.5, 3.5))

    history = MEMORY.get(cid, [])

    text = msg.lower()

    # Lead scammer to reveal more info
    if "upi" in text:
        return "Sir, which app should I open to send money? Can you send UPI again?"

    if "link" in text or "http" in text:
        return "I opened the link sir but it is asking many details. What to enter?"

    if "otp" in text:
        return "I received some number sir. Where should I type this OTP?"

    # Generic confusion replies
    replies = [
        "Sir, I am 62 years old. I don't understand these bank things.",
        "One minute sir, network is slow. I am checking.",
        "Can you explain again? I am confused.",
        "I will try sir, but I don't know where to click."
    ]

    return replies[len(history) % len(replies)]

# -------- API ENDPOINT --------
@app.post("/honeypot")
def honeypot(data: dict, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    start_time = time.time()

    conversation_id = data.get("conversation_id", "unknown")
    message = data.get("message", "")
    history = data.get("history", [])

    # Update memory
    MEMORY.setdefault(conversation_id, []).append(message)

    is_scam, confidence = detect_scam(message)

    reply = persona_reply(conversation_id, message) if is_scam else "Hello, how can I help you?"

    extracted = extract_info(message)
    tactics = detect_tactics(message)

    duration = round(time.time() - start_time, 3)

    return {
        "conversation_id": conversation_id,
        "is_scam": is_scam,
        "persona": f"{PERSONA['age']} year old confused man",
        "reply": reply,
        "engagement_metrics": {
            "turns": len(history) + 1,
            "response_time_sec": duration
        },
        "extracted_intelligence": {
            **extracted,
            "tactics": tactics
        },
        "confidence": confidence
    }
