# 🎙️ Sportomic Podcast Q&A Bot

An AI-powered Podcast Question Answering System that allows users to ask questions about the Elon Musk × Nikhil Kamath podcast and receive:

* ✅ Context-aware answers
* ✅ Supporting transcript evidence
* ✅ Timestamp references
* ✅ One-click navigation to the relevant section of the podcast

## 🚀 Live Demo

Deployed Application:

https://sportomic-podcast-bot-jfdhsh7tfpqugcqkwk8kth.streamlit.app/

---

## 📌 Problem Statement

Users often struggle to find specific information within long-form podcast content.

This project transforms a podcast into an interactive knowledge base where users can ask natural language questions and instantly receive relevant answers along with timestamps.

---

## 🏗️ System Architecture

Podcast Video
↓
OpenAI Whisper
↓
Transcript Generation
↓
Chunking
↓
OpenAI text-embedding-3-small
↓
FAISS Vector Database
↓
Semantic Search
↓
GPT-4o-mini
↓
Answer + Timestamp + Video Link

---

## ⚙️ Tech Stack

### AI Models

* OpenAI Whisper
* OpenAI text-embedding-3-small
* GPT-4o-mini

### Frameworks & Libraries

* Streamlit
* FAISS
* NumPy
* Python

---

## 🔄 Workflow

### 1. Podcast Transcription

The podcast is transcribed using OpenAI Whisper, producing timestamped transcript segments.

### 2. Chunking

The transcript is divided into smaller chunks to improve retrieval quality.

### 3. Embedding Generation

Each chunk is converted into vector embeddings using OpenAI's text-embedding-3-small model.

### 4. Vector Search

FAISS stores the embeddings and performs semantic similarity search for user queries.

### 5. Answer Generation

The most relevant transcript chunk is passed to GPT-4o-mini, which generates a contextual answer and supporting evidence.

### 6. Timestamp Retrieval

The corresponding timestamp is displayed along with a direct YouTube jump link.

---

## ✨ Features

* Natural language querying
* Semantic search using embeddings
* Context-aware answers
* Transcript evidence
* Timestamp retrieval
* Direct video navigation
* Streamlit web interface

---

## 📂 Project Structure

```text
sportomic-podcast-bot/
│
├── app.py
├── requirements.txt
├── README.md
│
└── embeddings/
    ├── faiss_index.bin
    └── chunks.pkl
```

---

## 🛠️ Installation

### Clone Repository

```bash
git clone https://github.com/Gautham-Ashok/sportomic-podcast-bot.git
cd sportomic-podcast-bot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure API Key

Create Streamlit Secrets:

```toml
OPENAI_API_KEY="your_api_key"
```

### Run Application

```bash
streamlit run app.py
```

---

## 📊 Accuracy Validation

The retrieved transcript chunks were manually verified against the original podcast.

Generated answers were cross-checked with transcript evidence and timestamps were validated against the source video.

---

## ⚠️ Current Limitations

* Timestamp precision is chunk-level rather than sentence-level.
* Retrieval quality depends on transcript accuracy.
* Some answers may span multiple transcript chunks.
* Further improvements can be made using reranking and sentence-level retrieval.

---

## 🔮 Future Enhancements

* Sentence-level timestamp retrieval
* Hybrid keyword + semantic search
* Multi-podcast support
* Chat history
* Speaker identification
* Advanced reranking models

---

## 👨‍💻 Author

**Gautham Ashok**

GitHub: https://github.com/Gautham-Ashok

LinkedIn: https://www.linkedin.com/in/gautham-ashok-763233251

---

## 📄 Assignment Submission

Built as part of the Sportomic AI Labs Technical Assignment.

Focus Areas:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* LLM-Powered Question Answering
* Podcast Intelligence Systems

```
```
