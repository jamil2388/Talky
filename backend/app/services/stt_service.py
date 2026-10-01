import os
from faster_whisper import WhisperModel

class FasterWhisperEngine:
    def __init__(self, model_size_or_path: str = "base", device: str = "cpu", compute_type: str = "int8"):
        self.model_size_or_path = model_size_or_path
        self.device = device
        self.compute_type = compute_type
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = WhisperModel(
                self.model_size_or_path,
                device=self.device,
                compute_type=self.compute_type
            )
        return self._model

    def transcribe(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at {audio_path}")
        # segments, info = self.model.transcribe(audio_path, beam_size=5, vad_filter=True)
        segments, info = self.model.transcribe(audio_path, beam_size=5, vad_filter=True)
        text = " ".join([segment.text for segment in segments]).strip()
        return text

class STTService:
    def __init__(self, model_size_or_path: str = "base"):
        self.engine = FasterWhisperEngine(model_size_or_path=model_size_or_path)

    def transcribe(self, audio_path: str) -> str:
        return self.engine.transcribe(audio_path)

