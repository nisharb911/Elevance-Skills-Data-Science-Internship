class ContextManager:
    """
    Extracts relevant context from conversation history.
    """

    REFERENCE_WORDS = {
        "it",
        "this",
        "that",
        "these",
        "those",
        "they",
        "them",
        "one",
        "ones"
    }

    def __init__(self, memory):
        self.memory = memory

    def has_reference(self, question):
        """
        Detect whether the current question contains
        a contextual reference.
        """

        words = question.lower().split()

        return any(
            word.strip(".,?!") in self.REFERENCE_WORDS
            for word in words
        )

    def get_relevant_context(self, question):
        """
        Retrieve the most relevant previous context.

        Current implementation focuses on the most recent
        visual analysis and previous conversation messages.
        """

        context = {
            "current_question": question,
            "previous_messages": [],
            "latest_image_analysis": None,
            "has_contextual_reference": False
        }

        messages = self.memory.get_messages()

        if not messages:
            return context

        context["has_contextual_reference"] = (
            self.has_reference(question)
        )

        # Keep recent conversation context.
        context["previous_messages"] = messages[-6:]

        # Retrieve latest visual evidence.
        context["latest_image_analysis"] = (
            self.memory.get_last_image_analysis()
        )

        return context