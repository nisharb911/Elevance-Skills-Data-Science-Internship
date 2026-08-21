Dynamic Knowledge Chatbot

Internship Project 3

A Retrieval-Augmented Generation (RAG) chatbot with a dynamically expanding knowledge base. The system monitors configured documents and web sources, detects new or modified information, updates a FAISS vector database, and uses the latest indexed information to generate grounded answers with Google Gemini.

Project Objective

The objective of this project is to implement a chatbot that can automatically incorporate new information into its responses over time without rebuilding the complete application.

Expected Outcome

A chatbot that can:

Collect information from configured sources.

Detect new or modified information.

Avoid reprocessing unchanged sources.

Split new content into smaller chunks.

Generate vector embeddings.

Update a FAISS vector database.

Retrieve relevant information for a user query.

Generate an answer using Gemini based on retrieved context.

Run periodic knowledge-base updates through a scheduler.

Key Features

Dynamic document ingestion – supports text documents and PDF/web-source workflows used by the project.

Change detection – identifies NEW, MODIFIED, and UNCHANGED sources.

Incremental vector update – removes old chunks for modified sources and adds the new chunks.

Semantic retrieval – uses Sentence Transformers embeddings and FAISS similarity search.

RAG response generation – sends retrieved context to Google Gemini.

Source display – shows the source documents used for an answer.

Scheduled updates – periodically checks configured sources using APScheduler.

Streamlit interface – provides a simple chatbot UI and a manual knowledge-base update option.

Technology Stack

Python 3.11

Streamlit

Google Gemini / Google GenAI SDK

Sentence Transformers

FAISS

NumPy

BeautifulSoup

Requests

PyPDF

APScheduler

python-dotenv

Project Architecture

                         ┌──────────────────────┐
                         │   Local Documents    │
                         │      TXT / PDF       │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │     Web Sources      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                           Source Monitoring
                                    │
                         ┌──────────┴───────────┐
                         │ NEW / MODIFIED /     │
                         │ UNCHANGED            │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         Text Cleaning & Chunking
                                    │
                                    ▼
                              Embeddings
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FAISS Vector DB   │
                         └──────────┬───────────┘
                                    │
                           User Question
                                    │
                                    ▼
                              Retriever
                                    │
                                    ▼
                           Relevant Chunks
                                    │
                                    ▼
                              Gemini LLM
                                    │
                                    ▼
                              Final Answer
                                    │
                                    ▼
                              Streamlit UI

Folder Structure

DYNAMIC_KNOWLEDGE_CHATBOT/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── .env.example
│
├── data/
│   ├── sources/
│   │   ├── documents/
│   │   │   └── company_information.txt
│   │   └── urls.txt
│   │
│   └── processed/
│       ├── source_metadata.json
│       └── web_source_metadata.json
│
├── vector_db/
│   ├── index.faiss
│   └── metadata.json
│
├── src/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── retriever.py
│   ├── updater.py
│   ├── web_updater.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── document_loader.py
│   ├── text_processor.py
│   └── test_pipeline.py
│
├── scheduler/
│   ├── __init__.py
│   └── scheduler.py
│
└── screenshots/
    ├── 01_streamlit_chatbot.png
    ├── 02_dynamic_update.png
    ├── 03_retriever_test.png
    └── 04_scheduler.png

The exact filenames in src/ may vary slightly depending on the implementation. Keep the files that exist in your working project.

Setup

1. Create and activate the environment

conda create -n dynamic_knowledge_bot python=3.11 -y
conda activate dynamic_knowledge_bot

If Conda is not available in a normal Command Prompt, use the Anaconda Prompt.

2. Install dependencies

pip install -r requirements.txt

3. Configure Gemini API key

Create a .env file:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY

Never commit .env to GitHub.

4. Build the initial vector database

python -m src.test_pipeline

5. Test the updater

python -m src.updater

6. Test web-source monitoring

python -m src.web_updater

7. Test retrieval

python -m src.test_retriever

8. Test the RAG chatbot

python -m src.test_chatbot

9. Run the Streamlit application

streamlit run app.py

Open the local URL shown by Streamlit, normally:

http://localhost:8501

10. Run the automatic scheduler

From the project root:

python -m scheduler.scheduler

The scheduler periodically checks configured sources. Press CTRL+C to stop it.

Dynamic Update Demonstration

The most important demonstration is the following:

Ask the chatbot a question about information that is not currently in the knowledge base.

Add new information to data/sources/documents/company_information.txt.

Run the updater or use the Update Knowledge Base button.

The updater detects the source as MODIFIED.

Old chunks from that source are removed.

New chunks are embedded and added to FAISS.

Ask the same question again.

The chatbot now retrieves the new information and uses it in the answer.

During development, the vector count increased from 4 to 5 after new information was added, confirming that the vector database was updated.

Example

New information added during testing:

Our company introduced an automated knowledge synchronization process in August 2026.
The synchronization system periodically checks configured sources and updates the knowledge
base whenever new information is detected.

After the update, the retriever returned this new content and the RAG chatbot could use it in its response.

Validation Performed

The following tests were successfully performed during development:

Initial document loading.

Text cleaning and chunk creation.

Embedding generation with 384-dimensional embeddings.

FAISS index creation and persistence.

NEW source detection.

UNCHANGED source detection and skipping.

MODIFIED source detection.

Removal of old chunks for a modified source.

Addition of updated chunks.

Web-source status checking.

Scheduled automatic updates.

Semantic retrieval from FAISS.

Gemini response generation using retrieved context.

Streamlit chatbot interaction.

Dynamic update demonstration.

Important Security Notes

Do not commit .env.

Do not expose the Gemini API key in screenshots, source code, or GitHub.

Use .env.example with a placeholder key name only.

Avoid committing unnecessary model caches or generated temporary files.

Internship Submission

Recommended submission package:

Project-3-Dynamic-Knowledge-Chatbot/
├── GitHub Repository
├── README.md
├── Project_Report.pdf
├── Project_Report.docx
├── requirements.txt
├── screenshots/
├── source code
└── demo notes

Author

NRB

Internship Project – Data Science / Generative AI