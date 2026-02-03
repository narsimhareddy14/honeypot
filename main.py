from fastapi import FastAPI, Header, HTTPException
import re
import time

app = FastAPI()
API_KEY = "mysecretkey"

# --- Scam detector ---
def is_scam_message(msg: str):
    keywords = ["bank", "upi", "account", "blocked", "urgent", "link", "verify", "otp"]
    score = sum(word in msg.lower() for word in keywords)
    return score >= 2

# --- Persona reply ---
def persona_reply(history):
    replies = [
        "Oh sir, I am not understanding. What should I do now?",
        "Is this serious? I am little confused.",
        "Can you explain again? I am old person.",
        "One minute sir, I will check."
    ]
    return replies[len(history) % len(replies)]

# --- Extract intelligence ---
def extract_info(text: str):
    upi_pattern = r'\b[\w.-]+@[\w.-]+\b'
    url_pattern = r'https?://\S+'
    account_pattern = r'\b\d{9,18}\b'

    return {
        "upi_ids": re.findall(upi_pattern, text),
        "phishing_links": re.findall(url_pattern, text),
        "bank_accounts": re.findall(account_pattern, text),
    }

@app.post("/honeypot")
def honeypot(data: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    conversation_id = data.get("conversation_id", "unknown")
    message = data.get("message", "")
    history = data.get("history", [])

    start_time = time.time()

    scam = is_scam_message(message)
    reply = persona_reply(history) if scam else "Hello, how can I help you?"

    extracted = extract_info(message)

    duration = round(time.time() - start_time, 3)

    return {
        "conversation_id": conversation_id,
        "is_scam": scam,
        "reply": reply,
        "engagement_metrics": {
            "turns": len(history) + 1,
            "response_time_sec": duration
        },
        "extracted_intelligence": extracted,
        "confidence": 0.90
    }
