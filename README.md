# 🤖 Portfolio Chatbot — RAG-based Personal AI Assistant

🔗 **Live Demo**: https://chatbot.zid.web.id/

---

## 📌 Overview

A **context-aware AI chatbot** designed to transform a traditional portfolio into an **interactive conversational interface** 💬

Instead of reading static CVs, users can directly ask about:

* Experience
* Skills
* Projects

The system responds with **relevant, data-driven answers** using a lightweight **RAG (Retrieval-Augmented Generation)** approach.

---

## ⚙️ Architecture

```id="g7k2df"
User Input
   ↓
Intent Detection
   ↓
Topic Mapping
   ↓
Context Retrieval (data.txt)
   ↓
Prompt Injection
   ↓
OpenAI API
   ↓
Response (UI)
```

---

## 🧠 Core Features

* 💬 Clean & Responsive UI
* 🧠 Lightweight RAG system
* 🎯 Keyword-based topic routing
* 📂 Structured knowledge base (section-based)
* 🔍 Portfolio relevance scoring
* 🧵 Conversation history support
* ⚡ FastAPI backend (fast & efficient)

---

## 🔬 Technical Breakdown

### 📥 Context Retrieval

Only relevant data is injected into the model:

```python id="zq8n2k"
context = retrieve_context(user_input)
```

✔ Improves accuracy
✔ Reduces token usage
✔ Minimizes hallucination

---

### 🏷️ Topic Routing

```python id="o3k9xp"
KEYWORD_TOPIC → TOPIC_MAP → SECTIONS
```

Maps user queries into structured knowledge domains.

---

### 📂 Knowledge Structure

Stored in:

```id="k8f3mz"
data.txt
```

Format:

```id="y1l0sm"
==== SECTION NAME ====
content...
```

---

### 🔍 Portfolio Ranking

```python id="a2d7mf"
score += 1 if word in text else 0
```

Ensures only relevant projects are returned.

---

### 🧩 Prompt Injection

```python id="p9w4jt"
system_prompt = BASE_PROMPT + context
```

Constrains the model to grounded responses.

---

## 🖥️ Tech Stack

**Backend**

* FastAPI
* Python
* OpenAI API

**Frontend**

* TailwindCSS
* Vanilla JavaScript
* Lucide Icons

---

## 📁 Project Structure

```id="q6n8vr"
.
├── index.html        # UI
├── main.py           # Backend
├── data.txt          # Knowledge base
├── prompt.txt        # Prompt config
├── .env              # API key
```

---

## 🔌 API Endpoint

### POST `/chat`

```json id="d4j1xp"
{
  "message": "What are your skills?",
  "history": []
}
```

---

## 🎯 Design Decisions

* File-based knowledge → simple & portable
* Keyword routing → deterministic & lightweight
* No embeddings → avoid overengineering
* Limited history → token efficiency

---

## 🚀 Future Improvements

* Embedding-based retrieval
* Vector database (FAISS / Pinecone)
* Streaming responses
* Multi-language support
* Docker deployment

---

## 👤 Author

**Fida Yuzida**

---

## ⭐ Final Thought

> Turning a portfolio into a conversation
> creates a more engaging way to explore a candidate 🚀
