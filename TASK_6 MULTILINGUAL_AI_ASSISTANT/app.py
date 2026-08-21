import streamlit as st

from src.multilingual_pipeline import MultilingualPipeline


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Multilingual AI Assistant",
    page_icon="🌐",
    layout="wide",
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "pipeline" not in st.session_state:
    st.session_state.pipeline = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "initialized" not in st.session_state:
    st.session_state.initialized = False


# ---------------------------------------------------------
# INITIALIZE PIPELINE
# ---------------------------------------------------------

if not st.session_state.initialized:

    with st.spinner(
        "Loading multilingual AI models..."
    ):
        st.session_state.pipeline = MultilingualPipeline()

        loaded = st.session_state.pipeline.retriever.load()

        if not loaded:
            st.warning(
                "Knowledge base index not found. "
                "Please run: python -m src.build_index"
            )

    st.session_state.initialized = True


pipeline = st.session_state.pipeline


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🌐 Multilingual Conversational AI Assistant")

st.markdown(
    """
This chatbot demonstrates multilingual conversational AI with:

- 🌐 Automatic language detection
- 🔄 Language switching
- 🧠 Conversation memory
- 🎯 Intent detection
- 🔎 Cross-lingual semantic retrieval
- 💬 Context-aware responses
- 🇬🇧 English
- 🇮🇳 Hindi
- 🇮🇳 Marathi
- 🇮🇳 Gujarati
"""
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Assistant Information")

    st.write(
        "**Supported Languages**"
    )

    st.write(
        "🇬🇧 English\n\n"
        "🇮🇳 Hindi\n\n"
        "🇮🇳 Marathi\n\n"
        "🇮🇳 Gujarati"
    )

    st.divider()

    st.write(
        "**AI Components**"
    )

    st.write(
        "Sentence Transformers\n\n"
        "FAISS\n\n"
        "LangDetect\n\n"
        "Structured Conversation Memory"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        if pipeline:
            pipeline.memory.clear()

        st.rerun()


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and "metadata" in message
        ):

            metadata = message["metadata"]

            with st.expander(
                "🔎 AI Analysis"
            ):

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(
                        "**Language**"
                    )

                    st.write(
                        metadata["language"]
                    )

                with col2:
                    st.write(
                        "**Intent**"
                    )

                    st.write(
                        metadata["intent"]
                    )

                with col3:
                    st.write(
                        "**Confidence**"
                    )

                    st.write(
                        f"{metadata['confidence']:.2f}"
                    )

                if metadata["is_mixed"]:
                    st.info(
                        "Mixed-language input detected."
                    )

                if metadata["retrieval"]:
                    st.write(
                        "**Retrieved Knowledge**"
                    )

                    for result in metadata[
                        "retrieval"
                    ]:

                        document = result[
                            "document"
                        ]

                        score = result[
                            "score"
                        ]

                        st.write(
                            f"• {document['category']} "
                            f"(score: {score:.3f})"
                        )


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

user_input = st.chat_input(
    "Type your message in English, Hindi, Marathi, or Gujarati..."
)


if user_input:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Process query
    with st.chat_message("assistant"):

        with st.spinner(
            "Understanding your message..."
        ):

            result = pipeline.process(
                user_input
            )

        response = result[
            "response"
        ]

        st.markdown(response)

        metadata = {
            "language": result[
                "language"
            ]["language"],

            "intent": result[
                "final_intent"
            ],

            "confidence": result[
                "intent"
            ]["confidence"],

            "is_mixed": result[
                "language"
            ]["is_mixed"],

            "retrieval": result[
                "retrieval"
            ],
        }

        with st.expander(
            "🔎 AI Analysis"
        ):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(
                    "**Detected Language**"
                )

                st.write(
                    metadata["language"]
                )

            with col2:
                st.write(
                    "**Intent**"
                )

                st.write(
                    metadata["intent"]
                )

            with col3:
                st.write(
                    "**Confidence**"
                )

                st.write(
                    f"{metadata['confidence']:.2f}"
                )

            if metadata["is_mixed"]:
                st.info(
                    "Mixed-language input detected."
                )

            if metadata["retrieval"]:

                st.write(
                    "**Cross-Lingual Retrieval**"
                )

                for item in metadata[
                    "retrieval"
                ]:

                    document = item[
                        "document"
                    ]

                    score = item[
                        "score"
                    ]

                    st.write(
                        f"• {document['category']} "
                        f"— {score:.3f}"
                    )

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "metadata": metadata,
        }
    )