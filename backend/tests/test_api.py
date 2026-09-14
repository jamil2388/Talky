import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.conversation import get_conversation_service
from tests.mock_services import MockConversationService, MockTTSService

def get_mock_conversation_service():
    return MockConversationService(tts_service=MockTTSService())

app.dependency_overrides[get_conversation_service] = get_mock_conversation_service
client = TestClient(app)

def test_post_conversation_start_endpoint():
    response = client.post("/api/conversation/start")
    assert response.status_code == 200
    json_data = response.json()
    assert "ai_text" in json_data
    assert json_data["ai_text"] == "mocked ai text"

def test_post_conversation_endpoint_valid():
    # Simulate uploading a mock WAV audio file
    dummy_audio_content = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    files = {"audio": ("test.wav", dummy_audio_content, "audio/wav")}
    
    response = client.post("/api/conversation", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert "user_text" in json_data
    assert "ai_text" in json_data
    assert json_data["user_text"] == "mocked user text"
    assert json_data["ai_text"] == "mocked ai text"

def test_post_conversation_endpoint_missing_audio():
    # If we don't supply "audio", FastAPI should return 422 validation error
    response = client.post("/api/conversation")
    assert response.status_code == 422
