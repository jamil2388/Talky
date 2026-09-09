import pytest
import os
import shutil
from app.services.stt_service import STTService
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService
from app.services.conversation_manager import ConversationManager
from app.services.conversation_service import ConversationService

@pytest.fixture
def temp_audio_dir(tmp_path):
    output_dir = tmp_path / "test_generated_audio"
    output_dir.mkdir()
    yield str(output_dir)
    # Cleanup
    if output_dir.exists():
        shutil.rmtree(output_dir)

def test_full_pipeline_user_initiated_conversation(temp_audio_dir):
    # Setup services
    stt_service = STTService()
    llm_service = LLMService()
    tts_service = TTSService(output_dir=temp_audio_dir)
    conversation_manager = ConversationManager()
    
    # Initialize the core orchestrator
    conversation_service = ConversationService(
        stt_service=stt_service,
        llm_service=llm_service,
        tts_service=tts_service,
        conversation_manager=conversation_manager
    )
    
    # Create a dummy audio file representing user speaking
    dummy_audio_path = os.path.join(temp_audio_dir, "user_speech.wav")
    with open(dummy_audio_path, "wb") as f:
        f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00")
    
    # Execution
    result = conversation_service.process_user_turn(dummy_audio_path)
    
    # Verification
    assert "user_text" in result
    assert "ai_text" in result
    assert "audio_path" in result
    
    assert result["user_text"] == "placeholder text"  # Check STT output
    assert result["ai_text"] == "I am a helpful assistant."  # Check LLM output
    assert os.path.exists(result["audio_path"])  # Check TTS file output
    assert result["audio_path"].endswith(".mp3")
    assert temp_audio_dir in result["audio_path"]

def test_full_pipeline_ai_initiated_conversation(temp_audio_dir):
    # Setup services
    stt_service = STTService()
    llm_service = LLMService()
    tts_service = TTSService(output_dir=temp_audio_dir)
    conversation_manager = ConversationManager()
    
    conversation_service = ConversationService(
        stt_service=stt_service,
        llm_service=llm_service,
        tts_service=tts_service,
        conversation_manager=conversation_manager
    )
    
    # Execution
    result = conversation_service.start_conversation()
    
    # Verification
    assert "ai_text" in result
    assert "audio_path" in result
    assert result["ai_text"] == "I am a helpful assistant."
    assert os.path.exists(result["audio_path"])
    assert result["audio_path"].endswith(".mp3")
