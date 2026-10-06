import os

def get_backend_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MAX_AUDIO_FILES = int(os.getenv("MAX_AUDIO_FILES", "20"))
MAX_TURNS = int(os.getenv("MAX_TURNS", "3"))
VOICE_MODEL_PATH = os.path.join(get_backend_dir(), "voices", "en_US-hfc_female-medium.onnx")
GENERATED_AUDIO_DIR = os.path.join(get_backend_dir(), "audio", "generated")
RECORDED_AUDIO_DIR = os.path.join(get_backend_dir(), "audio", "recorded")

def cleanup_audio_files(directory: str, max_files: int = MAX_AUDIO_FILES):
    if not os.path.exists(directory):
        return
    wav_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                wav_files.append((filepath, os.path.getmtime(filepath)))
    
    # Sort by modification time (oldest first)
    wav_files.sort(key=lambda x: x[1])
    
    while len(wav_files) > max_files:
        oldest_file, _ = wav_files.pop(0)
        try:
            os.remove(oldest_file)
        except OSError:
            pass
