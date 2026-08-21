Multilingual Conversational AI Assistant

Project Overview

A multilingual customer-service conversational AI assistant supporting English, Hindi, Marathi, and Gujarati. The system detects language, handles code-mixed input, detects intent, maintains conversation memory, performs cross-lingual semantic retrieval with multilingual embeddings and FAISS, re-ranks retrieved knowledge using intent, and returns context-aware responses.

Objectives

Automatic language detection

Support three additional languages beyond English

Language switching within one conversation

Mixed-language/code-mixed input handling

Conversation context retention

Cross-lingual intent detection

Multilingual semantic retrieval

Context-aware language-appropriate responses

Open-source implementation

Supported Languages

English, Hindi, Marathi, Gujarati.

Main Features

Automatic language detection using LangDetect and Unicode script signals.

Multilingual embeddings using paraphrase-multilingual-MiniLM-L12-v2.

FAISS semantic retrieval.

Intent detection for order status, delivery, cancellation, refund, returns, address change, payment and product information.

Conversation memory through Streamlit session state / conversation memory.

Mixed-language detection for inputs such as Mera order अभी तक नहीं आया.

Intent-aware retrieval re-ranking.

Streamlit chat interface with an AI Analysis panel.

Architecture

User Message
    ↓
Language Detection + Script Analysis
    ↓
Mixed-Language Detection
    ↓
Conversation Memory
    ↓
Intent Detection
    ↓
Multilingual Sentence Embedding
    ↓
FAISS Semantic Retrieval
    ↓
Intent-Aware Re-ranking
    ↓
Context-Aware Response
    ↓
Response in Appropriate Language

Technology Stack

Component

Technology

Language

Python 3.11

UI

Streamlit

Embeddings

Sentence Transformers

Multilingual Model

paraphrase-multilingual-MiniLM-L12-v2

Vector Search

FAISS

Language Detection

LangDetect + Unicode script detection

Data

Pandas

Numerical Processing

NumPy

ML Runtime

PyTorch

Project Structure

MULTILINGUAL_AI_ASSISTANT/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── knowledge_base.csv
├── src/
│   ├── embeddings.py
│   ├── language_detector.py
│   ├── intent_detector.py
│   ├── conversation_memory.py
│   ├── response_engine.py
│   ├── multilingual_pipeline.py
│   ├── retriever.py
│   └── build_index.py
├── evaluation/
│   └── test_retrieval.py
├── vectorstore/
│   ├── multilingual.faiss
│   └── documents.pkl
└── screenshots/

Installation

conda create -n multilingual_ai python=3.11
conda activate multilingual_ai
pip install -r requirements.txt

Build the index:

python -m src.build_index

Test retrieval:

python -m evaluation.test_retrieval

Run the application:

python -m streamlit run app.py

Open http://localhost:8501.

Cross-Lingual Retrieval

The knowledge base is stored in English, but the multilingual embedding model maps semantically equivalent queries from different languages into a shared vector space.

Example:

Where is my order?
मेरा ऑर्डर कहाँ है?
माझी ऑर्डर कुठे आहे?
મારું ઓર્ડર ક્યાં છે?

These queries can retrieve the same Order Status knowledge.

Intent-Aware Re-ranking

Semantic retrieval can sometimes confuse related categories such as Order Status and Address Change. The system retrieves multiple candidates and increases the score of documents whose category matches the detected intent.

Conversation Continuity

Example:

Where is my order?
मेरा ऑर्डर कब आएगा?
आणि address बदलायचा असेल तर?
Can I cancel it?
મને રિફંડ જોઈએ છે.

The language can change on every turn without resetting the conversation.

Mixed-Language Example

Mera order अभी तक नहीं आया

This combines Latin-script and Devanagari text and is handled as a mixed-language input.

Functional Validation

Test

Result

English

PASS

Hindi

PASS

Marathi

PASS

Gujarati

PASS

Language switching

PASS

Mixed Hindi/English input

PASS

Order status intent

PASS

Delivery intent

PASS

Address change intent

PASS

Cancellation intent

PASS

Refund intent

PASS

FAISS index creation

PASS

Cross-lingual retrieval

PASS

Streamlit application

PASS

These are functional validation results, not a statistically rigorous benchmark.

Limitations

Very short messages can be difficult for language detection.

Hindi and Marathi both use Devanagari, so short inputs may be ambiguous.

Cross-lingual similarity scores can vary by language.

The knowledge base is controlled and domain-specific.

The project is a retrieval-oriented prototype rather than a production-scale multilingual LLM.

Testing used a controlled set of examples rather than a large benchmark dataset.

Future Scope

Add more Indian and international languages.

Use a stronger language-identification model.

Add a multilingual generative LLM.

Add persistent conversation storage.

Create a larger multilingual evaluation dataset.

Add automated accuracy, retrieval and context metrics.

Deploy to the cloud.

Conclusion

The project demonstrates multilingual conversational AI using open-source components. It supports four languages, language switching, mixed-language input, intent detection, conversation memory, cross-lingual semantic retrieval, intent-aware re-ranking, and a Streamlit interface.