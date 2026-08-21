🩺 MedQuAD Medical Q&A Chatbot

Project Overview

This project is a Medical Question Answering chatbot developed using the MedQuAD (Medical Question Answering) dataset.

The objective is to allow a user to enter a medical question and retrieve the most relevant answer from the MedQuAD knowledge base.

The system combines semantic similarity and keyword matching. Sentence Transformers create question embeddings, FAISS performs vector similarity search, and keyword matching helps important medical terms influence the ranking. A simple Streamlit interface is used for interaction.

Disclaimer: This project is for educational and informational purposes only. It is not a medical diagnosis or treatment system.

Project Objective

Build a Medical Q&A chatbot using MedQuAD.

Prepare medical question-answer data for retrieval.

Generate semantic embeddings for questions.

Store and search embeddings using FAISS.

Combine semantic and keyword matching.

Display the best matching answer through Streamlit.

Technologies Used

Python

MedQuAD Dataset

Sentence Transformers

sentence-transformers/all-MiniLM-L6-v2

FAISS

Streamlit

Pickle

Regular Expressions

Project Structure

MEDQUAD_CHATBOT/
│
├── app.py
├── README.md
├── requirements.txt
│
├── models/
│   ├── medical_qa.index
│   └── qa_metadata.pkl
│
├── data/
│   └── MedQuAD dataset files
│
└── src/
    ├── __init__.py
    └── medical_retriever.py

End-to-End Working

1. MedQuAD Dataset

MedQuAD provides medical question-answer pairs collected from medical information sources. It is used as the chatbot's knowledge base.

2. Data Preprocessing

The raw data is cleaned and organized. Questions, answers, question IDs, focus, question type, synonyms, source information and URLs are stored as metadata.

The processed metadata is saved as:

models/qa_metadata.pkl

3. Sentence Embeddings

Questions are converted into numerical vectors using:

sentence-transformers/all-MiniLM-L6-v2

The same model converts a user's question into an embedding during search.

4. FAISS Index

The question embeddings are stored in:

models/medical_qa.index

FAISS is used to retrieve semantically similar medical questions efficiently.

5. Hybrid Retrieval

The retriever performs two types of matching:

Semantic matching: compares the user's question embedding with the FAISS index.

Keyword matching: extracts useful terms from the query and compares them with stored medical question terms. Common stop words are removed and IDF weighting gives more importance to less common terms.

The main scoring approach is:

Hybrid Score =
(0.60 × Semantic Score)
+
(0.40 × Keyword Score)
+
Phrase Bonus
+
Medical Term Bonus

6. Result Ranking

Semantic and lexical candidates are combined. The results are sorted using the hybrid score and duplicate questions are removed.

7. Streamlit Chatbot

The user enters a medical question in the Streamlit interface. The question is sent to the medical retriever, the best matching MedQuAD result is selected, and the answer and source are displayed.

Multiple questions can be asked during the same session.

Application Flow

User
  ↓
Streamlit UI
  ↓
Medical Question
  ↓
┌─────────────────────────────┐
│ Hybrid Medical Retriever    │
│                             │
│ Semantic Search + Keywords  │
└─────────────────────────────┘
  ↓
FAISS + Sentence Transformer
  ↓
Hybrid Ranking
  ↓
Best MedQuAD Answer
  ↓
Streamlit UI

How to Run

Activate the project environment:

conda activate customer_service_bot

Install dependencies:

pip install -r requirements.txt

Run the application from the project root:

python -m streamlit run app.py

Open the local Streamlit URL shown in the terminal, normally:

http://localhost:8501

Example Questions

What are the symptoms of influenza?

What causes diabetes?

What are the symptoms of arthritis?

What is insulin used for?

Key Features

MedQuAD-based medical Q&A

Sentence Transformer embeddings

FAISS semantic retrieval

Keyword matching

Hybrid result ranking

Streamlit chatbot interface

Multiple questions in one session

Source information with answers

Limitations

Answers are limited to information available in the MedQuAD knowledge base.

The system does not independently diagnose diseases.

Retrieval quality depends on dataset coverage and question similarity.

The chatbot is intended for educational and informational use only.

Conclusion

The project implements an end-to-end retrieval-based Medical Q&A chatbot using MedQuAD. The combination of semantic search, keyword matching and FAISS provides a practical way to retrieve relevant medical answers, while Streamlit provides a simple user interface.