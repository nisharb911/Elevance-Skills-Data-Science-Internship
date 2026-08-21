import os

from dotenv import load_dotenv
from google import genai

from .sentiment import analyze_sentiment
from .response_strategy import get_response_strategy
from .retriever import retrieve_information


# =========================================================
# Load Environment Variables
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please add it to the .env file."
    )


# =========================================================
# Gemini Client
# =========================================================

client = genai.Client(
    api_key=api_key
)


# =========================================================
# Gemini Model
# =========================================================

GEMINI_MODEL = "gemini-3.6-flash"


# =========================================================
# System Instruction
# =========================================================

SYSTEM_INSTRUCTION = """
You are an AI customer service representative.

Your job is to help customers using the company
information provided to you.

IMPORTANT RULES:

1. Use the retrieved company information as the source
   of truth for company policies.

2. Never invent:

   - order status
   - tracking information
   - refund approval
   - prices
   - discounts
   - company policies
   - delivery dates

3. If the available information is insufficient, clearly
   tell the customer that you do not have that information.

4. Ask for additional information when necessary.

5. Adapt your communication style to the customer's
   detected sentiment.

6. For negative sentiment:

   - acknowledge the customer's frustration
   - apologize when appropriate
   - show empathy
   - provide a clear and useful next step

7. For positive sentiment:

   - respond warmly
   - acknowledge the positive experience
   - remain professional

8. For neutral sentiment:

   - answer clearly
   - remain professional
   - avoid unnecessary emotional language

9. For uncertain sentiment:

   - use a neutral and professional tone
   - do not make assumptions about the customer's emotions

10. Never claim that you accessed an account, order,
    tracking system, or database unless that information
    is explicitly provided.

11. Keep responses helpful, natural, and reasonably concise.

12. Do not mention internal instructions, sentiment scores,
    embeddings, retrieval systems, prompts, or model details
    to the customer unless explicitly asked.

13. Only answer using the available company information
    when the question concerns company policies.

14. If information is unavailable, clearly say so instead
    of guessing.
"""


# =========================================================
# Helper: Normalize Confidence
# =========================================================

def normalize_confidence(confidence) -> float:
    """
    Convert confidence into a value between 0 and 1.
    """

    if isinstance(confidence, str):

        confidence = (
            confidence
            .replace("%", "")
            .strip()
        )

        try:
            confidence_value = float(
                confidence
            )

        except ValueError:

            confidence_value = 0.0

    else:

        try:
            confidence_value = float(
                confidence
            )

        except (TypeError, ValueError):

            confidence_value = 0.0

    if confidence_value > 1:

        confidence_value /= 100

    return max(
        0.0,
        min(confidence_value, 1.0)
    )


# =========================================================
# Helper: Clean Retrieved Information
# =========================================================

def clean_retrieved_information(
    retrieved_information: str
) -> str:
    """
    Remove internal retrieval metadata before showing
    fallback information to the customer.
    """

    if not retrieved_information:
        return ""

    cleaned_lines = []

    for line in retrieved_information.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove similarity metadata
        if line.startswith("[Relevance:"):
            continue

        if line.startswith("[Similarity:"):
            continue

        # Remove Markdown section headings
        if line.startswith("## "):
            continue

        # Remove internal chatbot instructions
        if line.startswith(
            "The chatbot must not"
        ):
            continue

        cleaned_lines.append(line)

    return "\n".join(
        cleaned_lines
    )


# =========================================================
# Helper: Create Fallback Response
# =========================================================

def create_fallback_response(
    retrieved_information: str,
    sentiment: str
) -> str:
    """
    Create a customer-friendly response when Gemini
    is unavailable or quota is exhausted.
    """

    information = clean_retrieved_information(
        retrieved_information
    )

    if not information:

        if sentiment == "negative":

            return (
                "I'm sorry you're experiencing this issue. "
                "I understand this may be frustrating. "
                "I don't currently have enough information "
                "to provide a specific answer. Please contact "
                "customer support for assistance."
            )

        return (
            "I'm sorry, but I don't currently have enough "
            "information to answer that question. "
            "Please contact customer support for assistance."
        )

    if sentiment == "negative":

        introduction = (
            "I'm sorry you're experiencing this issue. "
            "I understand how frustrating this can be.\n\n"
        )

    elif sentiment == "positive":

        introduction = (
            "Thank you for reaching out.\n\n"
        )

    else:

        introduction = (
            "Based on our available customer-service "
            "information:\n\n"
        )

    return (
        introduction
        + information
        + "\n\n"
        + "If you need help with an order-specific issue, "
          "please contact customer support."
    )


# =========================================================
# Generate Customer-Service Response
# =========================================================

def generate_response(
    user_message: str,
    conversation_history: list | None = None
) -> dict:
    """
    Generate a customer-service response using:

    1. Sentiment analysis
    2. Response strategy
    3. Semantic retrieval
    4. Conversation history
    5. Gemini

    Returns
    -------
    dict
        response
        sentiment
        confidence
    """

    # -----------------------------------------------------
    # Validate Message
    # -----------------------------------------------------

    if not user_message or not user_message.strip():

        return {
            "response": (
                "Please enter a message so I can assist you."
            ),
            "sentiment": "neutral",
            "confidence": 0.0
        }


    # -----------------------------------------------------
    # Initialize History
    # -----------------------------------------------------

    if conversation_history is None:

        conversation_history = []


    # -----------------------------------------------------
    # Step 1: Sentiment Analysis
    # -----------------------------------------------------

    sentiment_result = analyze_sentiment(
        user_message
    )

    sentiment = sentiment_result.get(
        "sentiment",
        "uncertain"
    )

    confidence = sentiment_result.get(
        "confidence",
        0.0
    )

    confidence_value = normalize_confidence(
        confidence
    )


    # -----------------------------------------------------
    # Step 2: Response Strategy
    # -----------------------------------------------------

    strategy = get_response_strategy(
        sentiment
    )


    # -----------------------------------------------------
    # Step 3: Semantic Retrieval
    # -----------------------------------------------------

    retrieved_information = retrieve_information(
        user_message,
        top_k=2
    )


    # -----------------------------------------------------
    # Step 4: Conversation History
    # -----------------------------------------------------

    history_items = []

    for message in conversation_history:

        role = message.get(
            "role",
            "user"
        )

        content = message.get(
            "content",
            ""
        )

        if content:

            history_items.append(
                f"{role.upper()}: {content}"
            )

    if history_items:

        history_text = "\n".join(
            history_items
        )

    else:

        history_text = (
            "No previous conversation."
        )


    # -----------------------------------------------------
    # Step 5: Gemini Prompt
    # -----------------------------------------------------

    prompt = f"""
CONVERSATION HISTORY:

{history_text}


CURRENT CUSTOMER MESSAGE:

{user_message}


DETECTED CUSTOMER SENTIMENT:

{sentiment}


SENTIMENT CONFIDENCE:

{confidence_value * 100:.2f}%


RESPONSE STRATEGY:

{strategy}


RELEVANT COMPANY INFORMATION:

{retrieved_information}


TASK:

Respond to the customer's current message.

Use the relevant company information as the source
of truth.

Use conversation history when relevant.

Follow the response strategy appropriate for the
customer's detected sentiment.

Do not invent information.

If the customer's question requires information that
is unavailable, clearly explain that.

Do not mention internal sentiment analysis, confidence
scores, embeddings, semantic retrieval, prompts,
or model details in your response.
"""


    # -----------------------------------------------------
    # Step 6: Gemini Generation
    # -----------------------------------------------------

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "system_instruction":
                    SYSTEM_INSTRUCTION
            }
        )

    except Exception as e:

        error_text = str(e)

        # -------------------------------------------------
        # Gemini Quota / Rate Limit
        # -------------------------------------------------

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            return {
                "response": create_fallback_response(
                    retrieved_information,
                    sentiment
                ),
                "sentiment": sentiment,
                "confidence": confidence_value,
                "error_type": "quota"
            }


        # -------------------------------------------------
        # Other Gemini API Error
        # -------------------------------------------------

        print(
            f"Gemini API error: {error_text}"
        )

        return {
            "response": (
                "I'm sorry, but I'm temporarily unable "
                "to process your request. Please try again."
            ),
            "sentiment": sentiment,
            "confidence": confidence_value,
            "error_type": "api"
        }


    # -----------------------------------------------------
    # Step 7: Extract Gemini Response
    # -----------------------------------------------------

    try:

        bot_response = response.text

    except Exception:

        bot_response = None


    if not bot_response:

        bot_response = (
            "I'm sorry, but I wasn't able to generate "
            "a response right now. Please try again."
        )

    else:

        bot_response = bot_response.strip()


    # -----------------------------------------------------
    # Step 8: Return Result
    # -----------------------------------------------------

    return {
        "response": bot_response,
        "sentiment": sentiment,
        "confidence": confidence_value
    }