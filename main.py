from fastapi import FastAPI, Header, HTTPException
import re
import time

app = FastAPI()

API_KEY = "mysecretkey"

# --- Simple scam keywords detector ---
def is_scam_message(msg: str):
    keywords = ["bank", "upi", "account", "blocked", "urgent", "link", "verify", "otp"]
    score = sum(word in msg.lower() for word in keywords)
    return score >= 2

# --- Persona reply generator ---
def persona_reply(msg: str):
    replies = [
        "Oh sir, I am not understanding. What should I do now?",
        "Is this serious? I am little confused.",
        "Can you please explain again? I am old person.",
        "I will check. One minute please."
    ]
    return replies[int(time.time()) % len(replies)]

# --- Intelligence extractor ---
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

    message = data.get("message", "")

    scam = is_scam_message(message)
    reply = persona_reply(message) if scam else "Hello, how can I help you?"

    extracted = extract_info(message)

    return {
        "is_scam": scam,
        "reply": reply,
        "extracted_intelligence": extracted,
        "status": "running"
    }
