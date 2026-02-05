from fastapi import FastAPI, Header, HTTPException, Request
import re
import requests

app = FastAPI()
API_KEY = "mysecretkey"

@app.get("/")
def root():
    return {"status": "alive"}

@app.post("/honeypot")
async def honeypot(request: Request, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()

    session_id = body.get("sessionId")
    message_obj = body.get("message", {})
    text = message_obj.get("text", "")

    if not session_id or not text:
        return {"status": "success", "reply": "Hello?"}

    # Extract scam intelligence
    info = {
        "bankAccounts": re.findall(r'\b\d{9,18}\b', text),
        "upiIds": re.findall(r'\b[\w\.-]+@[\w\.-]+\b', text),
        "phishingLinks": re.findall(r'https?://\S+', text),
        "phoneNumbers": re.findall(r'\+?\d{10,13}', text),
        "suspiciousKeywords": [w for w in ["urgent","verify","blocked","otp","upi","pay","link"] if w in text.lower()]
    }

    # Send to GUVI (mandatory)
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(body.get("conversationHistory", [])) + 1,
        "extractedIntelligence": info,
        "agentNotes": "Scammer using urgency and verification tactics"
    }

    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=5
        )
    except:
        pass

    # Human-like reply
    reply = "Why is my account being suspended?"

    return {
        "status": "success",
        "reply": reply
    }
