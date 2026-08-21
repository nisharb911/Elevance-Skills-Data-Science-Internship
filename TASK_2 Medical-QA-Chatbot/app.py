import streamlit as st
from src.medical_retriever import MedicalRetriever


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MedQuAD Medical Q&A",
    page_icon="🩺"
)


# ============================================================
# LOAD RETRIEVER
# ============================================================

@st.cache_resource
def load_retriever():
    return MedicalRetriever()


retriever = load_retriever()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# HEADER
# ============================================================

st.title("🩺 MedQuAD Medical Q&A Chatbot")

st.write(
    "Ask medical questions and get answers "
    "from the MedQuAD dataset."
)


# ============================================================
# DISPLAY PREVIOUS QUESTIONS AND ANSWERS
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"**You:** {message['content']}"
        )

    else:

        st.markdown(
            f"**Medical Q&A:** {message['content']}"
        )

        st.caption(
            f"Source: {message['source']}"
        )

    st.divider()


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.text_input(
    "Enter your medical question:",
    key="question_input"
)


# ============================================================
# SEARCH
# ============================================================

if st.button("Search"):

    if not question.strip():

        st.warning(
            "Please enter a medical question."
        )

    else:

        with st.spinner("Searching MedQuAD..."):

            results = retriever.search(
                question,
                top_k=1
            )

        # Store user's question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Store answer
        if results:

            result = results[0]

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result["answer"],
                    "source": result["source"]
                }
            )

        else:

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "No relevant answer was found "
                        "in the MedQuAD dataset."
                    ),
                    "source": "MedQuAD"
                }
            )

        # Clear input and refresh
        st.rerun()


# ============================================================
# CLEAR CHAT
# ============================================================

if st.session_state.messages:

    if st.button("Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.caption(
    "This chatbot provides information from the MedQuAD "
    "dataset for educational purposes only."
)