import os
import json

from google import genai


class ResponseGenerator:
    """
    Generates evidence-based responses using Gemini.
    The model receives visual evidence, conversation context,
    and reasoning results rather than relying on unsupported
    free-form generation.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = "gemini-3.6-flash"

    def generate(
        self,
        question,
        visual_evidence,
        reasoning_result,
        conversation_context
    ):
        """
        Generate a response grounded in the supplied evidence.
        """

        evidence_text = json.dumps(
            visual_evidence,
            indent=2,
            ensure_ascii=False
        )

        reasoning_text = json.dumps(
            reasoning_result,
            indent=2,
            ensure_ascii=False
        )

        context_text = json.dumps(
            conversation_context,
            indent=2,
            ensure_ascii=False
        )

        prompt = f"""
You are an evidence-based multimodal AI assistant.

Answer the user's question using ONLY the evidence and
conversation context provided below.

Do not invent visual information.

If the evidence does not contain enough information to
answer the question, explicitly say that the information
is insufficient.

If the reasoning result contains a resolved reference,
use that reference when answering the question.

If clarification is required, do not invent an answer.
Instead, ask the clarification question.

Keep the answer concise, natural, and helpful.

USER QUESTION:
{question}

VISUAL EVIDENCE:
{evidence_text}

REASONING RESULT:
{reasoning_text}

CONVERSATION CONTEXT:
{context_text}

Return only the final natural-language answer.
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        return response.text.strip()