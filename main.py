from fastapi import FastAPI, Header, HTTPException
import re
import time
import random
import json
from datetime import datetime
import os

app = FastAPI()

# -------- API KEY FROM ENV --------
API_KEY = os.getenv("API_KEY")

os.makedirs("logs", exist_ok=True)
MEMORY = {}

# -------- PERSONA SELECTION --------
def choose_persona(msg: str):
    text = msg.lower()

    if "job" in text:
        return {"age": 21, "role": "confused student"}
    if "parcel" in text or "courier" in text:
        return {"age": 38, "role": "housewife"}
    if "investment" in text:
        return {"age": 30, "role": "IT employee"}

    return {"age": 62, "role": "confused old man"}

# -------- SAVE CONVERSATION --------
def save_conversation(conversation_id, data):
    filename = f"logs/{conversation_id}.json"
    try:
        with open(filename, "r") as f:
            old = json.load(f)
    except:
        old = []

    old.append(data)

    with open(filename, "w") as f:
        json.dump(old, f, indent=2)

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
def persona_reply(cid, msg, persona):
    time.sleep(random.uniform(1.5, 3.5))

    history = MEMORY.get(cid, [])
    text = msg.lower()

    if "upi" in text:
        return f"Sir, which app should I open to send money? Can you send UPI again? I am {persona['age']} years old."

    if "link" in text or "http" in text:
        return f"I opened the link but it is asking many details. What to enter? I am {persona['role']}."

    if "otp" in text:
        return "I received some number. Where should I type this OTP?"

    replies = [
        f"Sir, I am {persona['age']} years old {persona['role']}. I don't understand these bank things.",
        "One minute, network is slow. I am checking.",
        "Can you explain again? I am confused.",
        "I will try, but I don't know where to click."
    ]

    return replies[len(history) % len(replies)]

# -------- API ENDPOINT --------
@app.post("/honeypot")
def honeypot(data: dict, x_api_key: str = Header(None)):

    if API_KEY is None or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    start_time = time.time()

    conversation_id = data.get("conversation_id", "unknown")
    message = data.get("message", "")
    history = data.get("history", [])

    MEMORY.setdefault(conversation_id, []).append(message)

    persona = choose_persona(message)

    is_scam, confidence = detect_scam(message)
    reply = persona_reply(conversation_id, message, persona) if is_scam else "Hello, how can I help you?"

    extracted = extract_info(message)
    tactics = detect_tactics(message)

    duration = round(time.time() - start_time, 3)

    response = {
        "timestamp": datetime.utcnow().isoformat(),
        "conversation_id": conversation_id,
        "is_scam": is_scam,
        "persona": f"{persona['age']} year old {persona['role']}",
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

    save_conversation(conversation_id, response)

    return response
