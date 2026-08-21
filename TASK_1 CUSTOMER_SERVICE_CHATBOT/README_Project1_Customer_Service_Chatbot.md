# AI Customer Service Chatbot with Sentiment Analysis

## 1. Project Overview

This project is a real-time AI Customer Service Chatbot developed as part of the **Data Science / GenAI internship project**.

The chatbot combines:

- **Sentiment Analysis** – detects whether a customer message is positive, negative, neutral, or uncertain.
- **Semantic Search / Retrieval** – finds relevant information from a company FAQ/knowledge base.
- **Response Strategy** – changes the communication style according to customer sentiment.
- **Google Gemini** – generates a natural-language customer-service response using the retrieved information.
- **Streamlit** – provides the web-based chat interface.
- **Conversation History** – keeps previous messages available during the Streamlit session.

### Main objective

The system should answer customer questions accurately while avoiding invented information and responding appropriately to customer emotions.

---

## 2. Project Architecture

```text
Customer Message
       |
       v
   Streamlit UI
       |
       v
  generate_response()
       |
       +--------------------+
       |                    |
       v                    v
Sentiment Analysis     Semantic Retrieval
       |                    |
       v                    v
Sentiment +           Relevant FAQ sections
Confidence                  |
       |                    |
       +---------+----------+
                 |
                 v
          Response Strategy
                 |
                 v
        Gemini Prompt Builder
                 |
                 v
          Google Gemini API
                 |
                 v
        Customer Response
                 |
                 v
          Streamlit UI
```

---

## 3. Folder Structure

```text
CUSTOMER_SERVICE_CHATBOT/
│
├── app.py
├── .env
├── .gitignore
├── requirements.txt
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   └── sentiment_test.csv
│
├── knowledge/
│   └── company_faq.txt
│
├── src/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── embeddings.py
│   ├── evaluate_sentiment.py
│   ├── knowledge_base.py
│   ├── response_strategy.py
│   ├── retriever.py
│   ├── sentiment.py
│   └── similarity.py
│
└── tests/
    ├── __init__.py
    ├── test_response_strategy.py
    ├── test_retriever.py
    └── test_sentiment.py
```

---

## 4. What Each File Does

| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface, chat history, sentiment display and chatbot interaction |
| `src/chatbot.py` | Main orchestration layer; connects sentiment, retrieval, strategy and Gemini |
| `src/sentiment.py` | Loads the sentiment model and analyzes customer emotion |
| `src/response_strategy.py` | Defines response behavior for positive/negative/neutral/uncertain sentiment |
| `src/retriever.py` | Converts FAQ sections into embeddings and performs semantic retrieval |
| `src/embeddings.py` | Loads the embedding model and creates vector representations |
| `src/knowledge_base.py` | Loads `knowledge/company_faq.txt` |
| `src/similarity.py` | Similarity-related helper functionality |
| `src/evaluate_sentiment.py` | Evaluates sentiment model performance using test data |
| `data/sentiment_test.csv` | Sentiment evaluation/test dataset |
| `knowledge/company_faq.txt` | Company policies and customer-service information |
| `tests/` | Automated tests for important components |
| `requirements.txt` | Python dependency list |
| `.env` | Local API key configuration; never commit this file |
| `.streamlit/config.toml` | Streamlit configuration |

---

## 5. Technology Stack

### Programming
- Python

### User Interface
- Streamlit

### NLP / Sentiment
- Hugging Face Transformers
- CardiffNLP Twitter RoBERTa sentiment model

### Semantic Retrieval
- Sentence-transformer embedding model
- NumPy
- Cosine-style similarity through normalized vector dot product

### Generative AI
- Google Gemini API
- `google-genai` Python SDK

### Configuration
- `python-dotenv`

### Testing
- pytest

---

## 6. How the Chatbot Works

### Step 1 – Customer enters a message

Example:

```text
My order has been delayed and I am extremely frustrated.
```

`app.py` receives the message and calls:

```python
generate_response(user_input)
```

---

### Step 2 – Sentiment analysis

`src/sentiment.py` analyzes the message.

Example result:

```text
Sentiment: negative
Confidence: approximately 93%
```

The sentiment is used to decide how the chatbot should communicate.

---

### Step 3 – Semantic retrieval

`src/retriever.py` converts the customer question into an embedding and compares it with the FAQ section embeddings.

Example:

```text
Customer:
How long does delivery take?

Retrieved:
## Order Delivery
Standard delivery usually takes 3 to 7 business days...
```

The system retrieves the most relevant sections instead of sending the entire knowledge base to the model.

---

### Step 4 – Response strategy

`src/response_strategy.py` provides guidance based on sentiment.

Example for negative sentiment:

```text
Acknowledge frustration.
Apologize when appropriate.
Show empathy.
Provide a clear next step.
```

---

### Step 5 – Gemini prompt

`src/chatbot.py` combines:

1. Conversation history
2. Customer message
3. Sentiment
4. Sentiment confidence
5. Response strategy
6. Retrieved company information

These are sent to Gemini.

The system instruction also tells Gemini not to invent:

- order status
- tracking information
- refund approval
- prices
- discounts
- company policies
- delivery dates

---

### Step 6 – Final response

Gemini generates the final customer-service response.

The Streamlit application displays:

- chatbot response
- sentiment
- confidence

---

## 7. Knowledge Base

The main source of business information is:

```text
knowledge/company_faq.txt
```

The current project uses multiple FAQ sections, including areas such as:

- Company Overview
- Payments
- Order Delivery
- Delayed Orders
- Returns
- Refunds

The retriever currently creates embeddings for the knowledge-base sections and selects the most relevant sections for a question.

### Important principle

The chatbot must treat the knowledge base as the source of truth.

If information is not available, the chatbot should say that it does not have enough information instead of inventing an answer.

---

## 8. Environment Setup From Scratch

### Step 1 – Open Command Prompt / Anaconda Prompt

Go to the project folder:

```bat
cd /d D:\Internship\CUSTOMER_SERVICE_CHATBOT
```

### Step 2 – Activate the environment

```bat
conda activate customer_service_bot
```

Verify Python:

```bat
python --version
```

Verify pip:

```bat
python -m pip --version
```

### Step 3 – Install dependencies

```bat
python -m pip install -r requirements.txt
```

If a package needs to be installed separately, use:

```bat
python -m pip install package-name
```

Using `python -m pip` is preferred because it ensures pip belongs to the currently active Python environment.

---

## 9. Configure Gemini API Key

Create/edit:

```text
D:\Internship\CUSTOMER_SERVICE_CHATBOT\.env
```

Add:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Do not put the API key directly into Python source code.

Do not commit `.env` to GitHub.

Your `.gitignore` should contain at least:

```text
.env
__pycache__/
.pytest_cache/
*.pyc
```

---

## 10. Run the Project

From the project root:

```bat
cd /d D:\Internship\CUSTOMER_SERVICE_CHATBOT
```

Activate the environment:

```bat
conda activate customer_service_bot
```

Start Streamlit:

```bat
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

You may also see a network URL generated by Streamlit.

---

## 11. Test the Retriever

Before running the complete application, semantic retrieval can be tested independently:

```bat
python -m src.retriever
```

Expected behavior:

```text
Loading embedding model...
Embedding model loaded successfully.
Creating knowledge-base embeddings...
Created embeddings for 11 sections.
```

The program then tests example questions such as:

```text
What payment methods do you accept?
How long does delivery take?
What is the refund policy?
When can I return a product?
How can I get my money back?
My package hasn't arrived yet.
Can I pay using UPI?
```

---

## 12. Test the Chatbot Directly

You can test the backend without Streamlit:

```bat
python -c "from src.chatbot import generate_response; print(generate_response('How long does delivery take?'))"
```

A successful response should return a dictionary similar to:

```python
{
    "response": "...",
    "sentiment": "neutral",
    "confidence": 0.93
}
```

---

## 13. Run Automated Tests

From the project root:

```bat
python -m pytest -q
```

For more detail:

```bat
python -m pytest -v
```

The tests currently cover components such as:

- sentiment analysis
- response strategy
- semantic retrieval

---

## 14. Sentiment Evaluation

The project contains:

```text
data/sentiment_test.csv
src/evaluate_sentiment.py
```

Run the evaluation script according to the functions currently implemented in `evaluate_sentiment.py`.

The purpose is to measure how accurately the sentiment model classifies the supplied test examples.

Useful evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

---

## 15. Example Test Scenarios

### Positive

```text
Thank you, the support team solved my issue quickly!
```

Expected:

```text
Positive sentiment
Warm and professional response
```

### Neutral

```text
What payment methods do you accept?
```

Expected:

```text
Neutral sentiment
Clear factual response
```

### Negative

```text
My order is late and I am extremely frustrated.
```

Expected:

```text
Negative sentiment
Empathy + apology when appropriate + useful next step
```

### Unknown information

```text
Where is order #123456 right now?
```

Expected behavior:

```text
The chatbot must not invent tracking information.
It should explain that it cannot access the order's live tracking
information and request the necessary information or direct the
customer to support.
```

---

## 16. Known Warnings vs Actual Errors

### Hugging Face warning

You may see:

```text
Warning: You are sending unauthenticated requests to the HF Hub.
```

This is generally a download/rate-limit warning, not a failure of the sentiment or embedding model.

### RoBERTa unexpected pooler keys

You may see:

```text
roberta.pooler.dense.weight | UNEXPECTED
roberta.pooler.dense.bias   | UNEXPECTED
```

The project logs indicated these can be ignored for this model/task loading scenario.

### Gemini 429 RESOURCE_EXHAUSTED

You may see:

```text
429 RESOURCE_EXHAUSTED
```

This means the Gemini API quota/rate limit has been reached. It is not a Streamlit, retriever, or sentiment-model error.

The application should handle this gracefully instead of crashing.

---

## 17. Troubleshooting

### `ModuleNotFoundError`

Check the active environment:

```bat
where python
python --version
```

Then install dependencies:

```bat
python -m pip install -r requirements.txt
```

### `GEMINI_API_KEY was not found`

Check `.env`:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Make sure `.env` is in the project root beside `app.py`.

### Streamlit starts but chatbot fails

Test the backend:

```bat
python -c "from src.chatbot import generate_response; print(generate_response('What payment methods do you accept?'))"
```

Then test retrieval:

```bat
python -m src.retriever
```

### Gemini quota error

Check the Gemini API quota/usage for the configured project. Do not repeatedly restart the application expecting a quota exhaustion error to disappear immediately.

---

## 18. Important Design Decisions

### Why sentiment analysis?

A customer-service bot should not respond to an angry customer in exactly the same style as it responds to a satisfied customer.

### Why semantic retrieval?

Keyword matching can miss questions that use different wording.

For example:

```text
How can I get my money back?
```

can still retrieve the `Refunds` section even though the wording does not exactly match the FAQ title.

### Why use a knowledge base?

It reduces hallucination risk by giving Gemini relevant company information.

### Why use Gemini?

Retrieval provides facts, while Gemini converts those facts into natural, conversational responses.

### Why keep the components separate?

The architecture separates:

```text
UI
↓
Chatbot orchestration
↓
Sentiment
↓
Retrieval
↓
Response strategy
↓
LLM
```

This makes the system easier to test, maintain and improve.

---

## 19. Recommended Final Project Checklist

Before submitting the internship project:

- [ ] Streamlit application opens successfully
- [ ] Sentiment detection works
- [ ] Positive/neutral/negative responses are appropriate
- [ ] FAQ retrieval works
- [ ] Gemini response generation works when quota is available
- [ ] Gemini quota errors are handled gracefully
- [ ] Conversation history works
- [ ] Automated tests pass
- [ ] Sentiment evaluation is completed
- [ ] `.env` is excluded from Git
- [ ] `__pycache__` and `.pytest_cache` are excluded from Git
- [ ] README is included
- [ ] Project screenshots are captured
- [ ] Final architecture diagram is included in presentation/report

---

## 20. Submission Summary

**Project:** AI Customer Service Chatbot with Sentiment Analysis

**Core flow:**

```text
Customer
   ↓
Streamlit
   ↓
Sentiment Analysis
   ↓
Semantic Retrieval
   ↓
Response Strategy
   ↓
Gemini
   ↓
Customer-Service Response
```

The project demonstrates the integration of traditional NLP, semantic search, retrieval-augmented prompting, generative AI and a practical web interface into one customer-service application.
