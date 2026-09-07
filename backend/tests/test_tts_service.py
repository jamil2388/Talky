import pytest
import os
from app.services.tts_service import TTSService

def test_tts_service_generates_audio_file(tmp_path):
    # Setup
    output_dir = tmp_path / "audio"
    output_dir.mkdir()
    service = TTSService(output_dir=str(output_dir))
    text = "Hello, how are you?"
    
    # Execution
    audio_path = service.convert_text_to_speech(text)
    
    # Verification
    assert os.path.exists(audio_path)
    assert audio_path.endswith(".mp3")
    assert str(output_dir) in audio_path
    
    # Cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)

def test_tts_service_fails_on_empty_text():
    service = TTSService()
    with pytest.raises(ValueError):
        service.convert_text_to_speech("")
