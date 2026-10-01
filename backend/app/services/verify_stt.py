import sys
import os
import time

"""
This script expects the file path to an audio file : python verify_stt.py path/to/sample.mp3
"""

# Ensure backend root is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.stt_service import STTService

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_stt.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        sys.exit(1)
    print(f"Initializing STTService (faster-whisper)...")
    stt_service = STTService()
    print(f"Transcribing {audio_path}...")
    start_time = time.time()
    text = stt_service.transcribe(audio_path)
    end_time = time.time()
    print("\n--- Transcription Result ---")
    print(text)
    print(f"Time Taken : {end_time - start_time} seconds")
    print("----------------------------")

if __name__ == "__main__":
    main()
