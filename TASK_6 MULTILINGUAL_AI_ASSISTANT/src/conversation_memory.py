from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ConversationMemory:
    """
    Maintains conversational context independently of language.

    This allows the user to switch between English, Hindi,
    Marathi and Gujarati without starting a new conversation.
    """

    history: List[Dict] = field(default_factory=list)

    current_language: Optional[str] = None
    previous_language: Optional[str] = None

    current_intent: Optional[str] = None

    entities: Dict = field(default_factory=dict)

    def add_turn(
        self,
        user_message: str,
        assistant_message: str,
        language: str,
        intent: str,
    ):
        self.previous_language = self.current_language
        self.current_language = language
        self.current_intent = intent

        self.history.append(
            {
                "role": "user",
                "content": user_message,
                "language": language,
                "intent": intent,
            }
        )

        self.history.append(
            {
                "role": "assistant",
                "content": assistant_message,
                "language": language,
            }
        )

    def get_recent_history(self, turns=6):
        return self.history[-turns:]

    def get_context(self):
        return {
            "current_language": self.current_language,
            "previous_language": self.previous_language,
            "current_intent": self.current_intent,
            "entities": self.entities,
            "history": self.get_recent_history(),
        }

    def update_entities(self, entities: Dict):
        if entities:
            self.entities.update(entities)

    def get_last_user_message(self):
        for item in reversed(self.history):
            if item["role"] == "user":
                return item["content"]

        return None

    def clear(self):
        self.history.clear()
        self.current_language = None
        self.previous_language = None
        self.current_intent = None
        self.entities.clear()