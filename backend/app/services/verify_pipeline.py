import sys
import os
import time

"""
This script verifies the full pipeline (STT -> LLM -> TTS) in one go:
python verify_pipeline.py ../generated_audio/r2.wav
"""

# Ensure backend root is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.stt_service import STTService
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService
from app.services.conversation_manager import ConversationManager
from app.services.conversation_service import ConversationService

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_pipeline.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        sys.exit(1)

    print("Initializing full conversation orchestration pipeline...")
    stt_service = STTService()
    llm_service = LLMService()
    tts_service = TTSService()
    conversation_manager = ConversationManager()

    conversation_service = ConversationService(
        stt_service=stt_service,
        llm_service=llm_service,
        tts_service=tts_service,
        conversation_manager=conversation_manager
    )

    print(f"\nProcessing input audio: {audio_path}")
    start_time = time.time()
    result = conversation_service.process_user_turn(audio_path)
    end_time = time.time()

    print("\n--- Pipeline Execution Result ---")
    print(f"User Transcribed Text (STT) : {result.get('user_text')}")
    print(f"AI Generated Response (LLM) : {result.get('ai_text')}")
    print(f"Generated Audio Path (TTS)  : {result.get('audio_path')}")
    print(f"Total Pipeline Time Taken   : {end_time - start_time:.4f} seconds")
    print("---------------------------------")

if __name__ == "__main__":
    main()
