import sys
import os
import time

"""
This script expects a text string: python verify_tts.py "Hello, welcome to Talky!"
"""

# Ensure backend root is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.tts_service import TTSService

def main():
    text = "Hello, welcome to Talky! How are you doing today?"
    if len(sys.argv) > 1:
        text = sys.argv[1]

    print(f"Initializing TTSService (pyttsx3)...")
    tts_service = TTSService()
    print(f"Generating audio for text: \"{text}\"")
    
    start_time = time.time()
    audio_path = tts_service.convert_text_to_speech(text)
    end_time = time.time()
    
    print("\n--- TTS Output Generated ---")
    print(f"Audio File Path : {audio_path}")
    print(f"Time Taken     : {end_time - start_time:.4f} seconds")
    print("----------------------------")

if __name__ == "__main__":
    main()
