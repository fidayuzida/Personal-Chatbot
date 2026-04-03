# 🤖 Fida's Personal AI — Context-Aware Portfolio Chatbot

🔗 Live Demo: https://chatbot.zid.web.id/

---

## 📌 Overview

Personal AI chatbot berbasis web yang berfungsi sebagai **interactive portfolio assistant**.

Sistem ini mengimplementasikan pendekatan **lightweight RAG (Retrieval-Augmented Generation)** untuk memastikan setiap jawaban:

* relevan
* berbasis data
* tidak hallucinate

---

## ⚙️ Architecture

```id="gk8p2x"
User Input
   ↓
Keyword & Intent Detection
   ↓
Topic Mapping
   ↓
Context Retrieval (data.txt)
   ↓
Dynamic Prompt Injection
   ↓
OpenAI API (LLM)
   ↓
Response (UI)
```

---

## 🧠 Core Concepts

### 1. Retrieval-Augmented Generation (RAG-lite)

Alih-alih mengirim seluruh knowledge ke model, sistem hanya mengirim **context yang relevan**.

```python id="u2pt4j"
context = retrieve_context(user_input)
```

✔ Lebih efisien
✔ Lebih akurat
✔ Minim hallucination

---

### 2. Keyword-Based Topic Routing

Mapping keyword → topic:

```python id="4i9b6q"
KEYWORD_TOPIC = {
    "magang": "pengalaman",
    "skill": "skill",
    "portfolio": "portfolio"
}
```

Kemudian diarahkan ke section:

```python id="4cbz7o"
TOPIC_MAP = {
    "pengalaman": ["PENGALAMAN MAGANG", "PENGALAMAN PART-TIME"]
}
```

---

### 3. Section-Based Knowledge Parsing

Data di-parse dari file:

```id="w5jvha"
data.txt
```

Dengan format:

```id="g1m1kg"
==== SECTION NAME ====
content...
```

Diubah menjadi dictionary untuk retrieval cepat.

---

### 4. Portfolio Relevance Scoring

Portfolio tidak diambil mentah — tapi di-ranking:

```python id="9qf2v1"
score += 1 if word in text else 0
```

✔ Query "IoT" → hanya project IoT yang muncul
✔ Lebih precise dibanding dump semua data

---

### 5. Dynamic System Prompt Injection

```python id="q2zkv5"
dynamic_system = BASE_PROMPT + context
```

LLM hanya boleh menjawab berdasarkan context tersebut.

---

## 🖥️ Tech Stack

### Backend

* FastAPI (REST API)
* OpenAI API (LLM)
* Python

### Frontend

* HTML + TailwindCSS
* Vanilla JavaScript
* Lucide Icons

---

## 📁 Project Structure

```id="o7l5nc"
.
├── index.html        # Chat UI
├── main.py           # Backend logic
├── data.txt          # Knowledge base
├── prompt.txt        # System prompt
├── .env              # API key
```

---

## 🔌 API Design

### POST `/chat`

Request:

```json id="u9p1g4"
{
  "message": "Apa skill kamu?",
  "history": []
}
```

Response:

```json id="m2w7kx"
{
  "reply": "Saya memiliki pengalaman di..."
}
```

---

## 🚀 Run Locally

```bash id="k7c2az"
git clone https://github.com/yourusername/personal-ai-chatbot.git
cd personal-ai-chatbot
pip install fastapi uvicorn python-dotenv openai
```

```env id="8h0qj2"
OPENAI_API_KEY=your_api_key_here
```

```bash id="z9x2pl"
uvicorn main:app --reload
```

---

## 🎯 Design Decisions

* **No database** → cukup file-based untuk simplicity & speed
* **Keyword routing** → lebih predictable dibanding embedding (untuk skala kecil)
* **Limited history (last 8)** → menjaga token usage tetap efisien
* **Temperature rendah (0.3)** → jawaban lebih konsisten

---

## 📌 Future Improvements

* Embedding-based retrieval (FAISS / vector DB)
* Streaming response
* Multi-turn memory optimization
* Fine-tuned prompt strategy
* Deployment scaling (Docker + reverse proxy)

---

## 👤 Author

**Fida Yuzida**

---

## ⭐ Notes

Project ini menunjukkan pendekatan praktis untuk membangun:

* AI assistant personal
* lightweight RAG system
* context-aware chatbot tanpa overengineering
