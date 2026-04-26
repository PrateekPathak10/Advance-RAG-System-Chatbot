# 🚀 Advanced RAG Assistant

### Production-Ready Retrieval-Augmented Generation System

A fully deployed **end-to-end RAG (Retrieval-Augmented Generation)** system that allows users to upload documents and ask intelligent, context-aware questions using a modern AI pipeline.

---

## 🌐 Live Demo

* 🔗 **Link:** https://advance-rag-system-chatbot-grfvuzhxhltinlwjxrxdp6.streamlit.app/

---

## 🧠 Overview

This system enables:

> 📄 Upload document → ❓ Ask question → 🤖 Get accurate, grounded answer

Built with a **production mindset**, this project handles:

* Token limits
* Memory constraints (free-tier deployment)
* Real-time user interaction

---

## ⚙️ Tech Stack

### 🧩 Backend

* FastAPI
* LangChain
* ChromaDB (Vector Store)
* Groq (LLaMA3 LLM)

### 🎨 Frontend

* Streamlit

### 🔍 Retrieval

* Semantic Search (Embeddings)
* BM25 (Keyword Search)

### ☁️ Deployment

* Docker
* Render (Backend)
* Streamlit Cloud (Frontend)

---

## 🏗️ System Architecture

```text
User (Streamlit UI)
        ↓
FastAPI Backend (Render)
        ↓
Query Rewriting
        ↓
Hybrid Retrieval (BM25 + Vector Search)
        ↓
Reranking (Lightweight in production)
        ↓
Context Limiting & Token Control
        ↓
Groq LLaMA3 (LLM)
        ↓
Final Answer + Sources
```

---

## ✨ Key Features

### 🔁 Query Rewriting

Improves user queries before retrieval for better results.

---

### 🧠 Hybrid Retrieval

Combines:

* Semantic search (vector embeddings)
* Keyword search (BM25)

---

### 📊 Reranking System

* High-quality reranker locally
* Lightweight fallback in production (memory optimized)

---

### ⚡ Streaming Responses

Real-time token streaming for better UX.

---

### 🔄 Background Document Processing

* Upload → processed asynchronously
* Status tracking enabled
* Faster perceived performance

---

### 🧩 Environment-Based Optimization

* **Local:** High-quality embeddings & reranking
* **Production:** Lightweight models for low memory usage

---

### 🛑 Token Control System (Important)

Prevents LLM crashes by:

* Limiting retrieved documents
* Dynamically trimming context
* Ensuring prompts stay within token limits

---

## 🚀 How It Works

### 1️⃣ Upload Document

* PDF is uploaded via UI
* Stored on backend

### 2️⃣ Background Processing

* Chunking
* Embedding
* Vector DB storage

### 3️⃣ Ask Question

* Query is rewritten
* Relevant chunks retrieved
* Context built with token control

### 4️⃣ Answer Generation

* LLM generates answer
* Sources returned for transparency

---

## 🚀 Run Locally

### 1. Clone Repo

```bash
git clone https://github.com/PrateekPathak10/Advance-RAG-System-Chatbot.git
cd Advance-RAG-System-Chatbot
```

### 2. Setup Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Create `.env`

```env
GROQ_API_KEY=your_key
HF_TOKEN=your_token
ENV=local
```

### 4. Run Backend

```bash
uvicorn app:app --reload
```

### 5. Run Frontend

```bash
streamlit run streamlit.py
```

---

## 🐳 Docker Setup

```bash
docker compose up --build
```

---

## ☁️ Deployment Strategy

### Backend (Render)

* Docker-based deployment
* Memory optimized (<512MB)
* Environment-aware system

### Frontend (Streamlit Cloud)

* Lightweight UI
* Connected via REST API

---

## ⚡ Performance Optimizations

* Lazy loading of embeddings & DB
* Chunk limiting (≤150 chunks)
* Context trimming (~3000 chars)
* Background ingestion
* API-based embeddings (no heavy models)

---

## 🧠 Engineering Highlights

* Designed a **multi-stage RAG pipeline**
* Implemented **hybrid retrieval (BM25 + embeddings)**
* Solved **LLM token limit issues using dynamic context control**
* Optimized system to run under **free-tier constraints**
* Built **environment-aware architecture**

---

## 📌 Challenges Solved

| Problem                    | Solution                              |
| -------------------------- | ------------------------------------- |
| Memory crashes             | Lightweight embeddings + lazy loading |
| Token overflow (413 error) | Context trimming + doc limiting       |
| Slow uploads               | Background ingestion                  |
| Poor UX                    | Streaming + status updates            |

---

## 📈 Future Improvements

* RAG evaluation (RAGAS)
* Chat history memory
* Multi-document querying
* Authentication system
* Advanced reranking (cross-encoder API)

---
## ⭐ If you found this useful

Give it a ⭐ — it helps!
