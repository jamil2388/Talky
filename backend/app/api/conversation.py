from fastapi import APIRouter, File, UploadFile, Depends
from app.schemas.conversation import StartConversationResponse, ConversationResponse
from app.services.stt_service import STTService
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService
from app.services.conversation_manager import ConversationManager
from app.services.conversation_service import ConversationService
import os

router = APIRouter()

# Dependency provider
def get_conversation_service():
    stt_service = STTService()
    llm_service = LLMService()
    tts_service = TTSService(output_dir="backend/generated_audio")
    conversation_manager = ConversationManager()
    return ConversationService(
        stt_service=stt_service,
        llm_service=llm_service,
        tts_service=tts_service,
        conversation_manager=conversation_manager
    )

@router.post("/start", response_model=StartConversationResponse)
async def start_conversation(
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    result = conversation_service.start_conversation()
    return StartConversationResponse(ai_text=result["ai_text"])

@router.post("", response_model=ConversationResponse)
async def process_conversation(
    audio: UploadFile = File(...),
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    # Save uploaded file temporarily
    temp_path = f"temp_{audio.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await audio.read())
    
    try:
        result = conversation_service.process_user_turn(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    return ConversationResponse(
        user_text=result["user_text"],
        ai_text=result["ai_text"]
    )
