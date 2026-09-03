from fastapi import FastAPI
from app.api.conversation import router as conversation_router

app = FastAPI(title="Local Voice Conversation Assistant")

app.include_router(conversation_router, prefix="/api/conversation")
