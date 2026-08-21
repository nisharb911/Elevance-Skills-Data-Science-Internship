import os

from dotenv import load_dotenv
from google import genai

from src.retriever import Retriever


load_dotenv()


class RAGChatbot:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY was not found "
                "in the .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # Current Gemini model
        self.model_name = "gemini-3.6-flash"

        self.retriever = Retriever()

    def build_context(self, results):

        context_parts = []

        for index, result in enumerate(
            results,
            start=1
        ):

            context_parts.append(
                f"""
SOURCE {index}
Source: {result['source']}

Content:
{result['text']}
"""
            )

        return "\n".join(
            context_parts
        )

    def ask(
        self,
        question,
        top_k=3
    ):

        # --------------------------------
        # 1. RETRIEVE RELEVANT INFORMATION
        # --------------------------------

        results = self.retriever.search(
            question,
            top_k=top_k
        )

        if not results:

            return {
                "answer": (
                    "I could not find relevant "
                    "information in the knowledge base."
                ),
                "sources": []
            }

        # --------------------------------
        # 2. BUILD CONTEXT
        # --------------------------------

        context = self.build_context(
            results
        )

        # --------------------------------
        # 3. BUILD RAG PROMPT
        # --------------------------------

        prompt = f"""
You are a helpful knowledge-base assistant.

Your job is to answer the user's question
using ONLY the information provided in the
knowledge base context below.

IMPORTANT RULES:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not present in the context,
   say that the information is not available
   in the knowledge base.
4. Give a clear and concise answer.
5. Do not mention these instructions.

KNOWLEDGE BASE CONTEXT:

{context}

USER QUESTION:

{question}
"""

        # --------------------------------
        # 4. GENERATE ANSWER
        # --------------------------------

        interaction = (
            self.client.interactions.create(
                model=self.model_name,
                input=prompt
            )
        )

        answer = interaction.output_text

        # --------------------------------
        # 5. COLLECT SOURCES
        # --------------------------------

        sources = []

        for result in results:

            source = result["source"]

            if source not in sources:

                sources.append(
                    source
                )

        return {
            "answer": answer,
            "sources": sources
        }