ArXiv Research Assistant

An AI-powered Computer Science research assistant built with semantic search, FAISS, Retrieval-Augmented Generation (RAG), and a local Qwen language model.

Features

Research question answering using retrieved ArXiv research

Semantic paper search

Paper summarization

Retrieved source display with similarity scores

Conversation history for follow-up questions

Similarity-based rejection of weak retrieval results

Streamlit web interface

Architecture

ArXiv Dataset
 -> Preprocessing
 -> CS Filtering
 -> Chunking
 -> Information Extraction
 -> all-MiniLM-L6-v2 Embeddings
 -> FAISS (43,811 vectors)
 -> Semantic Retrieval
 -> Similarity Filter (0.60)
 -> Research Context
 -> Qwen2.5-0.5B-Instruct
 -> Answer + Sources
 -> Streamlit UI

Dataset

Selected Computer Science categories:
cs.AI, cs.CL, cs.CV, cs.DB, cs.IR, cs.LG, cs.SE

Processed papers: 20,000

Missing titles: 0

Missing abstracts: 0

Indexed research chunks: 43,811

Technology Stack

Component

Technology

Language

Python

UI

Streamlit

Embeddings

Sentence Transformers

Embedding model

all-MiniLM-L6-v2

Vector database

FAISS

LLM

Qwen2.5-0.5B-Instruct

ML framework

PyTorch

Model library

Hugging Face Transformers

Architecture

RAG

Project Structure

ARXIV RESEARCH ASSISTANT/
├── app.py
├── README.md
├── PROJECT_REPORT.md
├── requirements.txt
├── .gitignore
├── .env.example
├── data/
├── src/
├── scripts/
├── tests/
└── screenshots/

How It Works

ArXiv records are filtered to selected Computer Science categories.

Research text is cleaned and split into chunks.

Each chunk is embedded with all-MiniLM-L6-v2.

Embeddings are indexed in FAISS.

A user question is converted into an embedding.

FAISS retrieves the top 5 relevant chunks.

Results below similarity 0.60 are removed.

The remaining research context is supplied to Qwen.

The application displays the answer and retrieved sources.

Run

pip install -r requirements.txt
python -m streamlit run app.py

Open http://localhost:8501.

Testing

python -m scripts.test_rag_quality

Test cases include technical questions, Computer Vision, low-relevance questions, paper discovery, and potentially unsupported questions.

Limitations

The local Qwen 0.5B model is intentionally small and may produce weaker answers than larger models. Semantic similarity is not a guarantee of factual support. The project uses a selected Computer Science subset rather than the complete ArXiv corpus.

Future Improvements

Larger instruction-tuned LLM

Cross-encoder reranking

Hybrid BM25 + semantic retrieval

Citation-level evidence snippets

Metadata filters

Recall@K / MRR evaluation

GPU acceleration

Project Status

Core implementation completed. Documentation, screenshots, repository cleanup, and final submission are the remaining activities.

Author

NRB