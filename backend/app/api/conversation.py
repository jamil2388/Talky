from fastapi import APIRouter, File, UploadFile, Depends
from app.schemas.conversation import StartConversationResponse, ConversationResponse
from app.services.stt_service import STTService
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService
from app.services.conversation_manager import ConversationManager
from app.services.conversation_service import ConversationService
import os
import re

router = APIRouter()

def get_backend_dir() -> str:
    # backend/app/api/conversation.py -> backend/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_next_recorded_filename(recorded_dir: str = None) -> str:
    if recorded_dir is None:
        recorded_dir = os.path.join(get_backend_dir(), "audio", "recorded")
    if not os.path.exists(recorded_dir):
        os.makedirs(recorded_dir, exist_ok=True)
    max_num = 0
    pattern = re.compile(r"^r_(\d+)\.wav$")
    for filename in os.listdir(recorded_dir):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    return os.path.join(recorded_dir, f"r_{max_num + 1}.wav")

# Dependency provider
def get_conversation_service():
    stt_service = STTService()
    llm_service = LLMService()
    tts_service = TTSService(output_dir=os.path.join(get_backend_dir(), "audio", "generated"))
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
    # Save recorded file to backend/audio/recorded/r_N.wav
    recorded_path = get_next_recorded_filename()
    with open(recorded_path, "wb") as buffer:
        buffer.write(await audio.read())
    
    result = conversation_service.process_user_turn(recorded_path)
            
    return ConversationResponse(
        user_text=result["user_text"],
        ai_text=result["ai_text"]
    )

