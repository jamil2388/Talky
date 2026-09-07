from typing import List, Dict

class ConversationManager:
    def __init__(self, max_turns: int = 3):
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []

    def add_turn(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        
        # Keep only the last max_turns * 2 messages (each turn is 1 user + 1 AI)
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]

    def get_context(self) -> List[Dict[str, str]]:
        return self.history
