from pydantic import BaseModel

class StartConversationResponse(BaseModel):
    ai_text: str

class ConversationResponse(BaseModel):
    user_text: str
    ai_text: str
