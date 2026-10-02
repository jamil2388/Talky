import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.conversation import router as conversation_router

app = FastAPI(title="Local Voice Conversation Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_backend_dir() -> str:
    # backend/app/main.py -> backend/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

backend_dir = get_backend_dir()
generated_dir = os.path.join(backend_dir, "audio", "generated")
recorded_dir = os.path.join(backend_dir, "audio", "recorded")

# Ensure audio directories exist and mount generated audio statically
os.makedirs(generated_dir, exist_ok=True)
os.makedirs(recorded_dir, exist_ok=True)
app.mount("/audio", StaticFiles(directory=generated_dir), name="audio")

app.include_router(conversation_router, prefix="/api/conversation")

