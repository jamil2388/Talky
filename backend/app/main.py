import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.conversation import router as conversation_router

app = FastAPI(title="Local Voice Conversation Assistant")

# Ensure audio directories exist and mount generated audio statically
os.makedirs("backend/audio/generated", exist_ok=True)
os.makedirs("backend/audio/recorded", exist_ok=True)
app.mount("/audio", StaticFiles(directory="backend/audio/generated"), name="audio")

app.include_router(conversation_router, prefix="/api/conversation")

