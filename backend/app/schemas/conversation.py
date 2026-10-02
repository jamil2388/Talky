from pydantic import BaseModel
from typing import Optional

class StartConversationResponse(BaseModel):
    ai_text: str
    audio_url: Optional[str] = None

class ConversationResponse(BaseModel):
    user_text: str
    ai_text: str
    audio_url: Optional[str] = None

