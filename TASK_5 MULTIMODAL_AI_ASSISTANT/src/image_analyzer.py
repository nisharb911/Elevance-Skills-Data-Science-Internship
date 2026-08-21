import json
from PIL import Image
from google import genai
from dotenv import load_dotenv
import os


load_dotenv()


class ImageAnalyzer:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured in the .env file."
            )

        self.client = genai.Client(api_key=api_key)

        self.model_name = "gemini-3.6-flash"

    def analyze(self, image: Image.Image, question: str = ""):

        prompt = f"""
You are the visual analysis component of a multimodal AI assistant.

Analyze the provided image carefully.

Your task is NOT to provide a long final answer to the user.
Instead, extract structured visual evidence that another reasoning
component can use later.

Identify:

1. Objects visible in the image
2. Important visual features
3. Visible text, if any
4. Possible abnormalities or notable conditions
5. Relevant relationships between objects
6. Uncertainty or limitations
7. Confidence for the observations

User question:
{question if question else "No specific question was provided."}

Return ONLY valid JSON using exactly this structure:

{{
    "objects": [],
    "visual_features": [],
    "visible_text": [],
    "notable_conditions": [],
    "relationships": [],
    "uncertainties": [],
    "overall_confidence": 0.0
}}

Do not invent information that cannot reasonably be observed.
If something is uncertain, mention it in "uncertainties".
Confidence must be a number between 0.0 and 1.0.
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt, image]
        )

        raw_text = response.text.strip()

        # Remove Markdown JSON fences if the model adds them.
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")
            raw_text = raw_text.strip()

        try:
            analysis = json.loads(raw_text)

        except json.JSONDecodeError:

            analysis = {
                "objects": [],
                "visual_features": [],
                "visible_text": [],
                "notable_conditions": [],
                "relationships": [],
                "uncertainties": [
                    "The vision model did not return valid structured JSON."
                ],
                "overall_confidence": 0.0,
                "raw_response": raw_text
            }

        return analysis