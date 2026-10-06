import pytest
import os
import time
from app.services.tts_service import TTSService
from app.config import cleanup_audio_files

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
    assert audio_path.endswith(".wav")
    assert "g_1.wav" in audio_path
    assert str(output_dir) in audio_path
    
    # Cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)

def test_tts_service_fails_on_empty_text():
    service = TTSService()
    with pytest.raises(ValueError):
        service.convert_text_to_speech("")

def test_cleanup_audio_files_prunes_old_files(tmp_path):
    test_dir = tmp_path / "cleanup_audio"
    test_dir.mkdir()
    
    # Create 5 dummy wav files with different modification times
    files = []
    for i in range(1, 6):
        f = test_dir / f"file_{i}.wav"
        f.write_bytes(b"dummy audio content")
        # Ensure distinct modification times
        os.utime(f, (time.time() - (6 - i), time.time() - (6 - i)))
        files.append(f)
        
    # Run cleanup with max_files = 2
    cleanup_audio_files(str(test_dir), max_files=2)
    
    remaining_files = sorted(os.listdir(test_dir))
    assert len(remaining_files) == 2
    # The newest two should remain (file_4.wav and file_5.wav)
    assert "file_4.wav" in remaining_files
    assert "file_5.wav" in remaining_files
    assert "file_1.wav" not in remaining_files
