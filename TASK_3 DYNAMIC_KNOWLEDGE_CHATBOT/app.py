import json
from pathlib import Path

import streamlit as st

from src.chatbot import RAGChatbot
from src.updater import KnowledgeBaseUpdater
from src.web_updater import WebKnowledgeUpdater
from src.vector_store import VectorStore


# ============================================
# CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Dynamic Knowledge Chatbot",
    page_icon="🤖",
    layout="wide"
)


DOCUMENT_FOLDER = Path(
    "data/sources/documents"
)

URL_FILE = Path(
    "data/sources/urls.txt"
)

DOCUMENT_METADATA = Path(
    "data/processed/source_metadata.json"
)

WEB_METADATA = Path(
    "data/processed/web_source_metadata.json"
)


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_document_count():

    if not DOCUMENT_FOLDER.exists():

        return 0

    files = list(
        DOCUMENT_FOLDER.glob("*.txt")
    )

    files += list(
        DOCUMENT_FOLDER.glob("*.pdf")
    )

    return len(files)


def get_url_count():

    if not URL_FILE.exists():

        return 0

    with open(
        URL_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        urls = [
            line.strip()
            for line in file
            if line.strip()
            and not line.startswith("#")
        ]

    return len(urls)


def get_last_updates():

    updates = []

    for metadata_file in [
        DOCUMENT_METADATA,
        WEB_METADATA
    ]:

        if not metadata_file.exists():

            continue

        try:

            with open(
                metadata_file,
                "r",
                encoding="utf-8"
            ) as file:

                metadata = json.load(
                    file
                )

            for source_data in metadata.get(
                "sources",
                {}
            ).values():

                if "last_updated" in source_data:

                    updates.append(
                        source_data[
                            "last_updated"
                        ]
                    )

        except Exception:

            continue

    if not updates:

        return "No updates yet"

    return max(updates)


def update_knowledge_base():

    with st.spinner(
        "Updating knowledge base..."
    ):

        document_updater = (
            KnowledgeBaseUpdater()
        )

        document_updater.update_all_sources()

        web_updater = (
            WebKnowledgeUpdater()
        )

        web_updater.update_all_urls()

    st.success(
        "Knowledge base update completed successfully."
    )


# ============================================
# SESSION STATE
# ============================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "chatbot" not in st.session_state:

    st.session_state.chatbot = None


# ============================================
# HEADER
# ============================================

st.title(
    "🤖 Dynamic Knowledge Chatbot"
)

st.write(
    """
An AI-powered Retrieval-Augmented Generation chatbot
that automatically expands its knowledge base from
documents and web sources.
"""
)


# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.header(
        "📊 Knowledge Base"
    )

    vector_store = VectorStore()

    vector_store.load()

    vector_count = (
        vector_store.count()
    )

    document_count = (
        get_document_count()
    )

    url_count = (
        get_url_count()
    )

    last_update = (
        get_last_updates()
    )

    st.metric(
        "Vector Count",
        vector_count
    )

    st.metric(
        "Documents",
        document_count
    )

    st.metric(
        "Web Sources",
        url_count
    )

    st.divider()

    st.write(
        "**Last Update**"
    )

    st.caption(
        last_update
    )

    st.divider()

    st.subheader(
        "🔄 Knowledge Base"
    )

    if st.button(
        "Update Knowledge Base",
        use_container_width=True
    ):

        update_knowledge_base()

        st.rerun()

    st.divider()

    st.caption(
        "Dynamic Knowledge Chatbot"
    )

    st.caption(
        "RAG + FAISS + Sentence Transformers + Gemini"
    )


# ============================================
# CHATBOT INITIALIZATION
# ============================================

if st.session_state.chatbot is None:

    try:

        with st.spinner(
            "Loading chatbot..."
        ):

            st.session_state.chatbot = (
                RAGChatbot()
            )

    except Exception as error:

        st.error(
            f"Unable to initialize chatbot: {error}"
        )

        st.stop()


chatbot = (
    st.session_state.chatbot
)


# ============================================
# CHAT HISTORY
# ============================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander(
                "📚 Sources"
            ):

                for source in message[
                    "sources"
                ]:

                    st.write(
                        f"• {source}"
                    )


# ============================================
# CHAT INPUT
# ============================================

question = st.chat_input(
    "Ask a question about the knowledge base..."
)


if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    # Assistant response
    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Searching knowledge base..."
        ):

            try:

                result = chatbot.ask(
                    question
                )

                answer = result[
                    "answer"
                ]

                sources = result[
                    "sources"
                ]

                st.markdown(
                    answer
                )

                if sources:

                    with st.expander(
                        "📚 Sources"
                    ):

                        for source in sources:

                            st.write(
                                f"• {source}"
                            )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    }
                )

            except Exception as error:

                error_message = (
                    f"Error generating response: {error}"
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )