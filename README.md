🛡️ Agentic Honey-Pot for Scam Detection & Intelligence Extraction

An AI-powered Agentic Honey-Pot system that detects scam messages and autonomously engages scammers using believable human personas to extract actionable intelligence such as UPI IDs, bank account numbers, and phishing links through multi-turn conversations.

Built for India AI Impact Buildathon – Fraud Detection & User Safety.

🚀 What This System Does

This is not a chatbot.

This system behaves like a real human victim, keeps scammers engaged, and strategically extracts scam intelligence while maintaining realistic conversation flow.

Core Capabilities

Detects scam intent from incoming messages

Dynamically selects a human persona (old man, student, housewife, etc.)

Maintains multi-turn conversation using memory

Uses human-like delay and confusion behavior

Extracts:

UPI IDs

Phishing links

Bank account numbers

Scam tactics (OTP request, urgency, payment request)

Returns structured intelligence in JSON format

Designed to work with a Mock Scammer API

🧠 Why This Is Special
Normal Bot	This Honeypot
Static replies	Dynamic persona-based replies
No memory	Conversation memory
Just detection	Intelligence extraction
Bot feel	Human feel
No metrics	Engagement metrics
No learning	Structured scam logs (local)
🧩 Architecture
Mock Scammer API → Honeypot API → Persona Agent → Intelligence Extractor → JSON Response

📡 API Endpoint
POST /honeypot
Headers
x-api-key: YOUR_API_KEY

Request Body
{
  "conversation_id": "123",
  "message": "Your bank account is blocked. Send OTP to abc@upi",
  "history": []
}

Response Format
{
  "conversation_id": "123",
  "is_scam": true,
  "persona": "62 year old confused man",
  "reply": "I received some number. Where should I type this OTP?",
  "engagement_metrics": {
    "turns": 3,
    "response_time_sec": 2.1
  },
  "extracted_intelligence": {
    "upi_ids": ["abc@upi"],
    "phishing_links": ["http://fake.com"],
    "bank_accounts": [],
    "tactics": ["OTP request", "Phishing link"]
  },
  "confidence": 0.97
}

⚙️ Tech Stack

Python

FastAPI

Regex-based intelligence extraction

Dynamic persona engine

In-memory conversation tracking

🌍 Deployment

Deployed on Render as a public API service.

Start Command:

uvicorn main:app --host 0.0.0.0 --port 10000


Environment Variable:

API_KEY=your_api_key

🧪 Testing

Open:

/docs


Use Swagger UI to simulate multi-turn scam conversations.

🏆 Hackathon Objective Alignment

This solution directly satisfies:

Scam intent detection

Agent handoff to autonomous AI persona

Multi-turn conversation handling

Intelligence extraction

Structured JSON reporting

Low latency and stable API behavior

💡 Key Idea

“This system does not block scammers. It traps them, talks to them, and turns them into data.”

👤 Author

Chinureddy Anugu
India AI Impact Buildathon Participant
