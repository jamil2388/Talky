class MockTTSService:
    def convert_text_to_speech(self, text: str) -> str:
        return "mock_audio.mp3"

class MockConversationService:
    def __init__(self, tts_service):
        self.tts_service = tts_service
    
    def process_user_turn(self, audio_path: str) -> dict:
        return {
            "user_text": "mocked user text",
            "ai_text": "mocked ai text",
            "audio_path": self.tts_service.convert_text_to_speech("mocked ai text")
        }
    
    def start_conversation(self) -> dict:
        return {
            "ai_text": "mocked ai text",
            "audio_path": self.tts_service.convert_text_to_speech("mocked ai text")
        }
