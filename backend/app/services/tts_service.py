import wave
import os
import re
from piper.voice import PiperVoice

def get_backend_dir() -> str:
    # backend/app/services/tts_service.py -> backend/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class TTSService:
    def __init__(self, model_path: str = None, output_dir: str = None):
        if model_path is None:
            model_path = os.path.join(get_backend_dir(), "voices", "en_US-hfc_female-medium.onnx")
        if output_dir is None:
            output_dir = os.path.join(get_backend_dir(), "audio", "generated")
        self.model_path = model_path
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            
        # Load Piper voice model
        self.voice = PiperVoice.load(self.model_path)

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
        
        with wave.open(filepath, "wb") as wav_file:
            # Configure wav file parameters based on voice config
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.voice.config.sample_rate)
            
            for chunk in self.voice.synthesize(text):
                wav_file.writeframes(chunk.audio_int16_bytes)
        
        return filepath
