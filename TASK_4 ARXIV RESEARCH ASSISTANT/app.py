import streamlit as st

from src.rag_pipeline import ResearchRAG


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="ArXiv Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# LOAD RAG PIPELINE ONCE
# ---------------------------------------------------------

@st.cache_resource(show_spinner="Loading research models and FAISS index...")
def load_rag():
    return ResearchRAG(top_k=5, min_similarity=0.60)


rag = load_rag()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🔬 ArXiv Research Assistant")
st.caption(
    "Semantic Search • FAISS • Retrieval-Augmented Generation • Qwen LLM"
)

st.markdown(
    """
Ask technical questions about the indexed arXiv research collection.
The assistant retrieves relevant research chunks first and then generates
an evidence-based response using the retrieved context.
"""
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ System Information")

    st.subheader("Architecture")
    st.write("Retrieval-Augmented Generation (RAG)")

    st.subheader("Embedding Model")
    st.write("all-MiniLM-L6-v2")

    st.subheader("Vector Database")
    st.write("FAISS")

    st.subheader("Language Model")
    st.write("Qwen2.5-0.5B-Instruct")

    st.subheader("Indexed Vectors")
    st.write(f"{rag.retriever.index.ntotal:,}")

    st.subheader("Top K Results")
    st.write(rag.top_k)

    st.subheader("Minimum Similarity")
    st.write(f"{rag.min_similarity:.2f}")

    st.divider()

    st.header("📚 Features")
    st.write("• Research Question Answering")
    st.write("• Semantic Paper Search")
    st.write("• Retrieved Source Inspection")
    st.write("• Paper Summarization")
    st.write("• Conversation History")

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.rerun()


# ---------------------------------------------------------
# MAIN TABS
# ---------------------------------------------------------

tab_chat, tab_search, tab_summary = st.tabs(
    ["💬 Research Assistant", "🔎 Paper Search", "📄 Paper Summary"]
)


# =========================================================
# TAB 1 — RESEARCH ASSISTANT
# =========================================================

with tab_chat:

    st.subheader("Research Question")

    question = st.text_area(
        "Enter your research question",
        placeholder=(
            "Example: How do Transformers improve neural machine translation?"
        ),
        height=120,
        label_visibility="collapsed",
        key="research_question",
    )

    ask_button = st.button(
        "🚀 Ask Research Assistant",
        type="primary",
        use_container_width=False,
    )

    if ask_button:

        if not question.strip():
            st.warning("Please enter a research question.")
        else:

            with st.spinner("Searching research papers and generating answer..."):

                result = rag.ask(
                    question.strip(),
                    conversation_history=st.session_state.messages,
                )

            st.session_state.last_result = result

            st.session_state.messages.append(
                {
                    "question": question.strip(),
                    "answer": result["answer"],
                }
            )

    result = st.session_state.last_result

    if result:

        st.divider()

        st.subheader("🤖 Research Answer")

        st.markdown(result["answer"])

        sources = result.get("sources", [])

        if sources:

            st.subheader("📚 Retrieved Research Sources")

            for i, source in enumerate(sources, start=1):

                title = source.get("title", "Unknown Paper")
                paper_id = source.get("paper_id", "Unknown")
                score = source.get("score", 0.0)
                year = source.get("year", "Unknown")
                categories = source.get("categories", [])
                technical_terms = source.get("technical_terms", [])
                text = source.get("text", "")

                with st.expander(
                    f"{i}. {title}  |  Similarity: {score:.4f}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Paper ID:** {paper_id}")
                        st.write(f"**Year:** {year}")

                    with col2:
                        st.write(f"**Similarity Score:** {score:.4f}")
                        st.write(f"**Categories:** {categories}")

                    if technical_terms:
                        st.write(
                            "**Technical Terms:** "
                            + ", ".join(map(str, technical_terms))
                        )

                    st.markdown("**Retrieved Research Text**")
                    st.write(text)

        else:
            st.info(
                "No sufficiently relevant research sources were retrieved "
                "for this question."
            )


# =========================================================
# TAB 2 — PAPER SEARCH
# =========================================================

with tab_search:

    st.subheader("🔎 Semantic Paper Search")

    search_query = st.text_input(
        "Search the research collection",
        placeholder="Example: neural machine translation",
    )

    search_k = st.slider(
        "Number of papers",
        min_value=1,
        max_value=10,
        value=5,
    )

    search_button = st.button(
        "🔍 Search Papers",
        type="primary",
    )

    if search_button:

        if not search_query.strip():
            st.warning("Please enter a search query.")
        else:

            with st.spinner("Searching indexed research papers..."):

                search_results = rag.retriever.search(
                    query=search_query.strip(),
                    top_k=search_k,
                )

            if not search_results:

                st.info("No research papers were found.")

            else:

                st.success(
                    f"Found {len(search_results)} relevant research result(s)."
                )

                for i, paper in enumerate(search_results, start=1):

                    title = paper.get("title", "Unknown Paper")
                    paper_id = paper.get("paper_id", "Unknown")
                    score = paper.get("score", 0.0)
                    year = paper.get("year", "Unknown")
                    categories = paper.get("categories", [])
                    keywords = paper.get("keywords", [])

                    with st.expander(
                        f"{i}. {title}  |  Score: {score:.4f}"
                    ):

                        st.write(f"**Paper ID:** {paper_id}")
                        st.write(f"**Year:** {year}")
                        st.write(f"**Categories:** {categories}")

                        if keywords:
                            st.write(
                                "**Keywords:** "
                                + ", ".join(map(str, keywords))
                            )

                        st.write(
                            f"**Semantic Similarity:** {score:.4f}"
                        )

                        st.markdown("**Research Text Preview**")
                        text = paper.get("text", "")

                        if len(text) > 3000:
                            st.write(text[:3000] + "...")
                        else:
                            st.write(text)


# =========================================================
# TAB 3 — PAPER SUMMARY
# =========================================================

with tab_summary:

    st.subheader("📄 Research Paper Summarizer")

    st.write(
        "First use the Paper Search tab to identify a relevant paper. "
        "Then paste its research content below for summarization."
    )

    summary_title = st.text_input(
        "Paper Title",
        placeholder="Enter the paper title",
    )

    summary_text = st.text_area(
        "Research Content",
        placeholder="Paste the research paper content here...",
        height=300,
    )

    summary_button = st.button(
        "📝 Generate Summary",
        type="primary",
    )

    if summary_button:

        if not summary_text.strip():

            st.warning("Please provide research content to summarize.")

        else:

            summary_prompt = f"""
Summarize the following computer science research paper.

Paper Title:
{summary_title or "Unknown"}

Research Content:
{summary_text}

Create a technically accurate summary using these sections:

1. Research Problem
2. Proposed Approach
3. Key Findings
4. Important Technical Concepts
5. Practical Significance
6. Limitations

Rules:
- Use ONLY information supported by the provided research content.
- Do not invent experiments, results, methods, or conclusions.
- If information is not available, write:
  "Not clearly specified in the provided content."
- Keep the explanation understandable to a computer science student.
"""

            with st.spinner("Generating research summary..."):

                summary = rag.llm.generate_answer(
                    question="Summarize this research paper.",
                    context=summary_prompt,
                )

            st.subheader("📋 Generated Summary")
            st.markdown(summary)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "ArXiv Research Assistant | Semantic Search • FAISS • RAG • Qwen LLM"
)
