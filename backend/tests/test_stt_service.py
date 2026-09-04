import pytest
from unittest.mock import MagicMock
from app.services.stt_service import STTService

def test_stt_service_transcription_success():
    """Verify STT service successfully transcribes audio."""
    # Mocking the service to return a known text for a given path
    stt_service = STTService()
    
    # We will need a sample audio file for real testing, 
    # but for unit testing we can mock the engine interaction.
    # For now, let's just define the test structure.
    
    # Mocking the engine's transcription method
    stt_service.engine.transcribe = MagicMock(return_value="hello world")
    
    text = stt_service.transcribe("path/to/test_audio.wav")
    assert text == "hello world"
    stt_service.engine.transcribe.assert_called_once_with("path/to/test_audio.wav")

def test_stt_service_transcription_failure():
    """Verify STT service handles transcription errors."""
    stt_service = STTService()
    
    # Mocking the engine to raise an exception
    stt_service.engine.transcribe = MagicMock(side_effect=Exception("Transcription failed"))
    
    with pytest.raises(Exception, match="Transcription failed"):
        stt_service.transcribe("path/to/invalid_audio.wav")
