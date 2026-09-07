import pyttsx3
import os
import uuid

class TTSService:
    def __init__(self, output_dir: str = "generated_audio"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.engine = pyttsx3.init()

    def convert_text_to_speech(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(self.output_dir, filename)
        
        # Configure pyttsx3 (basic configuration)
        self.engine.setProperty('rate', 150)
        
        # Save to file
        self.engine.save_to_file(text, filepath)
        self.engine.runAndWait()
        
        return filepath
