from src.language_detector import LanguageDetector
from src.embeddings import MultilingualEmbedder
from src.retriever import MultilingualRetriever
from src.conversation_memory import ConversationMemory
from src.intent_detector import IntentDetector
from src.response_engine import ResponseEngine


class MultilingualPipeline:
    """
    Complete multilingual conversational pipeline.

    Handles:
    - language detection
    - multilingual embeddings
    - semantic retrieval
    - intent detection
    - conversation memory
    - language switching
    - response generation
    """

    def __init__(self):
        print("\nInitializing Multilingual AI Assistant...\n")

        self.language_detector = LanguageDetector()

        self.embedder = MultilingualEmbedder()

        self.retriever = MultilingualRetriever(
            self.embedder
        )

        self.memory = ConversationMemory()

        self.intent_detector = IntentDetector(
            self.embedder
        )

        self.response_engine = ResponseEngine()

        print("\nMultilingual AI Assistant initialized.\n")

    def process(self, user_message: str):
        # ----------------------------------------
        # 1. Language detection
        # ----------------------------------------
        language_info = self.language_detector.detect_language(
            user_message
        )

        language_code = language_info["code"]

        # ----------------------------------------
        # 2. Intent detection
        # ----------------------------------------
        intent_result = self.intent_detector.detect(
            user_message
        )

        intent = intent_result["intent"]

        # ----------------------------------------
        # 3. Context-aware intent handling
        # ----------------------------------------
        if intent == "ambiguous":
            previous_intent = self.memory.current_intent

            # If the new message is very short, preserve
            # the previous intent where possible.
            if (
                previous_intent
                and len(user_message.split()) <= 5
            ):
                intent = previous_intent

        # ----------------------------------------
        # 4. Cross-lingual retrieval
        # ----------------------------------------
        retrieval_results = []

        if self.retriever.index is not None:
            retrieval_results = self.retriever.search(
                user_message,
                top_k=3,
                intent=intent
            )

        # ----------------------------------------
        # 5. Generate response in latest language
        # ----------------------------------------
        response = self.response_engine.generate(
            intent=intent,
            language_code=language_code,
            retrieved_results=retrieval_results,
        )

        # ----------------------------------------
        # 6. Store conversation
        # ----------------------------------------
        self.memory.add_turn(
            user_message=user_message,
            assistant_message=response,
            language=language_code,
            intent=intent,
        )

        return {
            "response": response,
            "language": language_info,
            "intent": intent_result,
            "final_intent": intent,
            "retrieval": retrieval_results,
            "memory": self.memory.get_context(),
        }