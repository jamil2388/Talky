from app.services.stt_service import STTService
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService
from app.services.conversation_manager import ConversationManager

class ConversationService:
    def __init__(
        self,
        stt_service: STTService,
        llm_service: LLMService,
        tts_service: TTSService,
        conversation_manager: ConversationManager
    ):
        self.stt_service = stt_service
        self.llm_service = llm_service
        self.tts_service = tts_service
        self.conversation_manager = conversation_manager

    def _format_context_as_prompt(self) -> str:
        context = self.conversation_manager.get_context()
        prompt_lines = []
        for turn in context:
            role = "User" if turn["role"] == "user" else "AI"
            prompt_lines.append(f"{role}: {turn['content']}")
        # Add next expected response instruction
        prompt_lines.append("AI:")
        return "\n".join(prompt_lines)

    def process_user_turn(self, audio_path: str) -> dict:
        # 1. Transcribe speech to text
        user_text = self.stt_service.transcribe(audio_path)
        
        # 2. Add user turn to context history
        self.conversation_manager.add_turn(role="user", content=user_text)
        
        # 3. Format history as prompt and generate LLM response
        prompt = self._format_context_as_prompt()
        ai_text = self.llm_service.generate(prompt)
        
        # 4. Add AI response to context history
        self.conversation_manager.add_turn(role="ai", content=ai_text)
        
        # 5. Convert response text to speech
        tts_audio_path = self.tts_service.convert_text_to_speech(ai_text)
        
        return {
            "user_text": user_text,
            "ai_text": ai_text,
            "audio_path": tts_audio_path
        }

    def start_conversation(self) -> dict:
        # AI initiates: generate response based on system prompt / empty context
        prompt = "AI starts the conversation with a simple sentence or question. AI:"
        ai_text = self.llm_service.generate(prompt)
        
        # Add AI response to history
        self.conversation_manager.add_turn(role="ai", content=ai_text)
        
        # Convert response text to speech
        tts_audio_path = self.tts_service.convert_text_to_speech(ai_text)
        
        return {
            "ai_text": ai_text,
            "audio_path": tts_audio_path
        }
