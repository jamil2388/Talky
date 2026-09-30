import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.conversation import router as conversation_router

app = FastAPI(title="Local Voice Conversation Assistant")

# Ensure generated_audio directory exists and mount statically
os.makedirs("generated_audio", exist_ok=True)
app.mount("/audio", StaticFiles(directory="generated_audio"), name="audio")

app.include_router(conversation_router, prefix="/api/conversation")

