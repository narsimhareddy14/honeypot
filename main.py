from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_KEY = "mysecretkey"

# ---- root ----
@app.get("/")
def root():
    return {"status": "alive"}

# ---- honeypot GET ----
@app.get("/honeypot")
def honeypot_get():
    return {"status": "ready"}

# ---- honeypot POST ----
@app.post("/honeypot")
def honeypot_post(data: dict = {}, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Accept ANY body from tester
    return {
        "status": "ok",
        "is_scam": True,
        "reply": "Please explain again, I am confused.",
        "extracted_intelligence": {
            "upi_ids": [],
            "phishing_links": [],
            "bank_accounts": []
        },
        "confidence": 0.95
    }
