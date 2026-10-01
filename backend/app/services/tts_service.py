import pyttsx3
import os
import re

def get_backend_dir() -> str:
    # backend/app/services/tts_service.py -> backend/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class TTSService:
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = os.path.join(get_backend_dir(), "audio", "generated")
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        self.engine = pyttsx3.init()

    def _get_next_filename(self) -> str:
        max_num = 0
        pattern = re.compile(r"^g_(\d+)\.wav$")
        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                match = pattern.match(filename)
                if match:
                    num = int(match.group(1))
                    if num > max_num:
                        max_num = num
        return os.path.join(self.output_dir, f"g_{max_num + 1}.wav")

    def convert_text_to_speech(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        filepath = self._get_next_filename()
        
        # Configure pyttsx3
        self.engine.setProperty('rate', 150)
        
        # Save to file
        self.engine.save_to_file(text, filepath)
        self.engine.runAndWait()
        
        return filepath

