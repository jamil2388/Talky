from fastapi import APIRouter, File, UploadFile
from app.schemas.conversation import StartConversationResponse, ConversationResponse

router = APIRouter()

@router.post("/start", response_model=StartConversationResponse)
async def start_conversation():
    # Return mock response data for now to satisfy TDD Phase 1
    return StartConversationResponse(ai_text="Hi! What are you doing today?")

@router.post("", response_model=ConversationResponse)
async def process_conversation(audio: UploadFile = File(...)):
    # Return mock response data for now to satisfy TDD Phase 1
    return ConversationResponse(
        user_text="How are you?",
        ai_text="I am good. What are you doing?"
    )
