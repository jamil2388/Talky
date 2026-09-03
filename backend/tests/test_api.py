import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_conversation_start_endpoint():
    response = client.post("/api/conversation/start")
    assert response.status_code == 200
    json_data = response.json()
    assert "ai_text" in json_data
    assert isinstance(json_data["ai_text"], str)
    assert len(json_data["ai_text"]) > 0

def test_post_conversation_endpoint_valid():
    # Simulate uploading a mock WAV audio file
    dummy_audio_content = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    files = {"audio": ("test.wav", dummy_audio_content, "audio/wav")}
    
    response = client.post("/api/conversation", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert "user_text" in json_data
    assert "ai_text" in json_data
    assert isinstance(json_data["user_text"], str)
    assert isinstance(json_data["ai_text"], str)

def test_post_conversation_endpoint_missing_audio():
    # If we don't supply "audio", FastAPI should return 422 validation error
    response = client.post("/api/conversation")
    assert response.status_code == 422
