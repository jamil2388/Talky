import pytest
from pydantic import ValidationError
from app.schemas.conversation import StartConversationResponse, ConversationResponse

def test_start_conversation_response_valid():
    data = {"ai_text": "Hello! How can I help you today?"}
    response = StartConversationResponse(**data)
    assert response.ai_text == "Hello! How can I help you today?"

def test_start_conversation_response_invalid():
    with pytest.raises(ValidationError):
        # Missing required ai_text field
        StartConversationResponse()

def test_conversation_response_valid():
    data = {
        "user_text": "Hello, how are you?",
        "ai_text": "I am doing well, thank you!"
    }
    response = ConversationResponse(**data)
    assert response.user_text == "Hello, how are you?"
    assert response.ai_text == "I am doing well, thank you!"

def test_conversation_response_invalid():
    with pytest.raises(ValidationError):
        # Missing user_text
        ConversationResponse(ai_text="I am doing well, thank you!")
    
    with pytest.raises(ValidationError):
        # Missing ai_text
        ConversationResponse(user_text="Hello, how are you?")
