import streamlit as st

from src.chatbot import generate_response


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="AI Customer Service Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# Custom CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666666;
        margin-bottom: 30px;
    }

    .sentiment-positive {
        background-color: #e8f5e9;
        padding: 8px 12px;
        border-radius: 8px;
        color: #2e7d32;
        font-weight: 600;
    }

    .sentiment-negative {
        background-color: #ffebee;
        padding: 8px 12px;
        border-radius: 8px;
        color: #c62828;
        font-weight: 600;
    }

    .sentiment-neutral {
        background-color: #f5f5f5;
        padding: 8px 12px;
        border-radius: 8px;
        color: #424242;
        font-weight: 600;
    }

    .sentiment-uncertain {
        background-color: #fff8e1;
        padding: 8px 12px;
        border-radius: 8px;
        color: #f57f17;
        font-weight: 600;
    }

    .confidence {
        font-size: 14px;
        color: #666666;
        margin-top: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Header
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🤖 AI Customer Service Chatbot'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent customer support with sentiment analysis '
    'and semantic search'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header("⚙️ Chatbot Information")

    st.markdown(
        """
        **Features**

        - 🧠 AI-powered responses
        - 😊 Sentiment detection
        - 🔎 Semantic knowledge retrieval
        - 💬 Emotion-aware responses
        - 📚 FAQ knowledge base
        """
    )

    st.divider()

    st.subheader("Supported Topics")

    st.markdown(
        """
        - Payments
        - Orders
        - Delivery
        - Returns
        - Refunds
        - Customer support
        """
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# Session State
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# Helper: Sentiment Display
# =========================================================

def display_sentiment(
    sentiment: str,
    confidence: float
):
    """
    Display sentiment and confidence.
    """

    if sentiment == "positive":

        css_class = "sentiment-positive"
        emoji = "😊"

    elif sentiment == "negative":

        css_class = "sentiment-negative"
        emoji = "😟"

    elif sentiment == "neutral":

        css_class = "sentiment-neutral"
        emoji = "😐"

    else:

        css_class = "sentiment-uncertain"
        emoji = "❓"

    st.markdown(
        f"""
        <div class="{css_class}">
            {emoji} Sentiment: {sentiment.capitalize()}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="confidence">
            Confidence: {confidence:.2%}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# Display Previous Messages
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and "sentiment" in message
        ):

            display_sentiment(
                message.get(
                    "sentiment",
                    "uncertain"
                ),
                message.get(
                    "confidence",
                    0.0
                )
            )


# =========================================================
# Chat Input
# =========================================================

user_input = st.chat_input(
    "Type your customer question here..."
)


# =========================================================
# Process Customer Message
# =========================================================

if user_input:

    # -----------------------------------------------------
    # Save user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # -----------------------------------------------------
    # Previous conversation
    #
    # Exclude the current user message because it is already
    # passed separately to generate_response().
    # -----------------------------------------------------

    previous_messages = (
        st.session_state.messages[:-1]
    )


    # -----------------------------------------------------
    # Generate Assistant Response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🤔 Analyzing your message..."
        ):

            try:

                result = generate_response(
                    user_message=user_input,
                    conversation_history=previous_messages
                )


                # -------------------------------------------------
                # Extract result
                # -------------------------------------------------

                response = result.get(
                    "response",
                    "Sorry, I could not generate a response."
                )

                sentiment = result.get(
                    "sentiment",
                    "uncertain"
                )

                confidence = result.get(
                    "confidence",
                    0.0
                )


                # -------------------------------------------------
                # Normalize confidence
                # -------------------------------------------------

                try:

                    confidence = float(
                        confidence
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    confidence = 0.0


                if confidence > 1:

                    confidence /= 100


                confidence = max(
                    0.0,
                    min(confidence, 1.0)
                )


                # -------------------------------------------------
                # Display response
                # -------------------------------------------------

                st.markdown(
                    response
                )


                # -------------------------------------------------
                # Display sentiment
                # -------------------------------------------------

                display_sentiment(
                    sentiment,
                    confidence
                )


                # -------------------------------------------------
                # Save assistant message
                # -------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "sentiment": sentiment,
                        "confidence": confidence
                    }
                )


            except Exception as e:

                # -------------------------------------------------
                # Unexpected application error
                # -------------------------------------------------

                print(
                    f"Application error: {e}"
                )

                error_message = (
                    "Sorry, something went wrong while "
                    "processing your request. Please try again."
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sentiment": "uncertain",
                        "confidence": 0.0
                    }
                )