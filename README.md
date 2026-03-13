# 🐾 Pawzio AI Backend

FastAPI backend powering all 5 AI features of the Pawzio pet care app.

---

## 📁 Folder Structure

```
pawzio-backend/
├── .env                        ← you create this (copy from .env.example)
├── .env.example                ← template
├── requirements.txt
├── app/
│   ├── main.py                 ← FastAPI entry point
│   ├── core/
│   │   ├── config.py           ← loads .env variables
│   │   ├── gemini.py           ← Gemini AI client
│   │   └── security.py        ← API key verification
│   ├── models/
│   │   └── schemas.py          ← all request/response types
│   ├── routers/
│   │   ├── triage.py           ← POST /api/v1/triage/symptom-check
│   │   ├── adoption.py         ← POST /api/v1/adoption/match
│   │   ├── medical.py          ← POST /api/v1/medical/summarize
│   │   ├── lostfound.py        ← POST /api/v1/lostfound/analyze-image
│   │   └── reminders.py        ← POST /api/v1/reminders/generate
│   └── services/
│       ├── triage_service.py
│       ├── adoption_service.py
│       ├── ocr_service.py
│       ├── vision_service.py
│       └── reminder_service.py
└── tests/
    └── test_all.py
```

---

## ⚡ Setup (5 Steps)

### Step 1 — Get Gemini API Key
Go to: https://aistudio.google.com/app/apikey
Click "Create API Key" and copy it.

### Step 2 — Create .env file
```bash
cp .env.example .env
```
Open `.env` and fill in:
```
GEMINI_API_KEY=paste_your_gemini_key_here
APP_API_KEY=pawzio-secret-123
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5 — Test it
Open browser: http://localhost:8000/docs
You'll see all 5 endpoints with interactive testing UI.

---

## 📱 Connect to Mobile App

Open `services/chatbotApi.ts` in your Expo app and set:

```ts
export const CHATBOT_CONFIG = {
  BASE_URL: "http://YOUR_PC_IP:8000",  // e.g. http://192.168.1.5:8000
  API_KEY:  "pawzio-secret-123",        // same as APP_API_KEY in .env
};
```

> **Find your PC IP:**
> - Windows: run `ipconfig` in terminal → look for IPv4 Address
> - Mac/Linux: run `ifconfig` → look for inet address
> - Both your PC and phone must be on the SAME WiFi network

---

## 🔌 API Endpoints

| Feature | Method | Endpoint | Auth |
|---|---|---|---|
| Health Check | GET | `/health` | None |
| Symptom Triage | POST | `/api/v1/triage/symptom-check` | X-API-Key |
| Adoption Match | POST | `/api/v1/adoption/match` | X-API-Key |
| Medical OCR | POST | `/api/v1/medical/summarize` | X-API-Key |
| Lost & Found | POST | `/api/v1/lostfound/analyze-image` | X-API-Key |
| Care Reminders | POST | `/api/v1/reminders/generate` | X-API-Key |

All protected endpoints require header: `X-API-Key: pawzio-secret-123`

---

## 🧪 Run Tests
```bash
# Make sure server is running first, then:
pip install pytest requests
pytest tests/ -v
```

---

## 🚀 Deploy to Cloud (Optional)

### Railway (easiest — free tier)
1. Push code to GitHub
2. Go to https://railway.app
3. New Project → Deploy from GitHub
4. Add environment variables (GEMINI_API_KEY, APP_API_KEY)
5. Railway gives you a public URL like `https://pawzio-backend.up.railway.app`
6. Use that URL in your mobile app's `chatbotApi.ts`

### Render (also free)
1. Go to https://render.com
2. New Web Service → connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Add env vars and deploy
