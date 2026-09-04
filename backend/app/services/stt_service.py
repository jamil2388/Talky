class MockSTTEngine:
    def transcribe(self, audio_path: str) -> str:
        # Placeholder for actual STT implementation
        return "placeholder text"

class STTService:
    def __init__(self):
        self.engine = MockSTTEngine()

    def transcribe(self, audio_path: str) -> str:
        return self.engine.transcribe(audio_path)
