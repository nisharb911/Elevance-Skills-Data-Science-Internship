from datetime import datetime


class ConversationMemory:
    """
    Stores conversation history for the current Streamlit session.
    """

    def __init__(self):
        self.messages = []

    def add_message(
        self,
        role,
        text=None,
        image_analysis=None,
        image_name=None
    ):
        """
        Add one interaction to conversation memory.
        """

        message = {
            "role": role,
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "image_name": image_name,
            "image_analysis": image_analysis
        }

        self.messages.append(message)

    def get_messages(self):
        """
        Return the complete conversation history.
        """

        return self.messages

    def get_last_message(self):
        """
        Return the most recent message.
        """

        if not self.messages:
            return None

        return self.messages[-1]

    def get_last_image_analysis(self):
        """
        Return the most recent visual analysis.
        """

        for message in reversed(self.messages):

            if message.get("image_analysis") is not None:
                return message["image_analysis"]

        return None

    def clear(self):
        """
        Clear the current conversation.
        """

        self.messages.clear()

    def count(self):
        """
        Return number of stored messages.
        """

        return len(self.messages)