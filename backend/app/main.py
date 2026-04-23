import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.db.database import init_db
from backend.app.routes.chat import router as chat_router
from backend.app.routes.voice import router as voice_router
from backend.app.routes.upload import router as upload_router
from backend.app.routes.auth import router as auth_router
from utils.logger import logger

# Import all models so SQLAlchemy registers them before init_db runs
import backend.app.db.models  # User model
import backend.app.db.chat_history  # ChatSession, ChatMessage


app = FastAPI(
    title="MediBot API",
    description="Medical Chatbot with Voice, Vision, Text and PDF support",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs("uploads/audio", exist_ok=True)
app.mount(
    "/audio",
    StaticFiles(directory="uploads/audio"),
    name="audio",
)


app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(voice_router)
app.include_router(upload_router)


@app.on_event("startup")
async def startup():
    logger.info("MediBot API starting up...")
    await init_db()
    logger.info("Database tables created successfully")
    logger.info("MediBot API is ready")


@app.get("/")
async def root():
    return {"message": "MediBot API is running", "docs": "/docs", "health": "/health"}


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "service": "MediBot API",
        "version": "1.0.0",
    }