from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import triage, adoption, medical, lostfound, reminders, petbot, diet

app = FastAPI(title="Pawzio AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage.router)
app.include_router(adoption.router)
app.include_router(medical.router)
app.include_router(lostfound.router)
app.include_router(reminders.router)
app.include_router(petbot.router)
app.include_router(diet.router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "app": "Pawzio AI Backend", "version": "1.0.0"}

@app.get("/")
def root():
    return {"message": "Pawzio AI Backend 🐾", "docs": "/docs"}