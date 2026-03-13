# 🧠 Nexus RAG Engine

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Nexus RAG Engine** is a production-grade, modular Retrieval-Augmented Generation system designed for enterprise knowledge management. It features hybrid search (keyword + vector), intelligent re-ranking, and citation support, all wrapped in a scalable FastAPI backend and a sleek Streamlit UI.

---

## 🚀 Key Features

- **Hybrid Search Architecture**: Combines semantic search (Vector DB) with keyword search (BM25) for high-precision retrieval.
- **Intelligent Re-ranking**: Uses Cross-Encoders to re-rank retrieved documents, ensuring the most relevant context reaches the LLM.
- **Modular LLM Integration**: Plug-and-play support for OpenAI (GPT-4), Anthropic (Claude 3), and Local LLMs (via Ollama/LlamaCPP).
- **Citation Awareness**: Every answer includes precise citations to source documents.
- **Production Ready**: Fully dockerized with FastAPI, Pydantic type validation, and async processing.

## 🏗️ Architecture

`mermaid
graph TD
    User[User / Client] -->|Query| API[FastAPI Gateway]
    API -->|1. Retrieve| HybridSearch[Hybrid Search Engine]
    HybridSearch -->|Vector| VectorDB[(ChromaDB / FAISS)]
    HybridSearch -->|Keyword| BM25[BM25 Index]
    API -->|2. Re-rank| ReRanker[Cross-Encoder Re-ranker]
    API -->|3. Generate| LLM[LLM Engine (OpenAI/Local)]
    LLM -->|Response + Citations| API
    API -->|Display| UI[Streamlit Dashboard]
`

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (optional)
- OpenAI API Key (or local model)

### Quick Start
1. **Clone the repository**
   \\\ash
   git clone https://github.com/rahulsunil112/nexus-rag-engine.git
   cd nexus-rag-engine
   \\\

2. **Set up environment**
   \\\ash
   cp .env.example .env
   # Add your OPENAI_API_KEY in .env
   \\\

3. **Run with Docker**
   \\\ash
   docker-compose up --build
   \\\

4. **Access the UI**
   - Streamlit UI: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## 🧩 Project Structure

\\\
nexus-rag-engine/
├── src/
│   ├── api/                 # FastAPI routes and controllers
│   ├── core/                # Core RAG logic (Retrieval, Generation)
│   ├── ingestion/           # Document processors (PDF, Txt)
│   └── models/              # Pydantic data models
├── ui/                      # Streamlit frontend application
├── tests/                   # Unit and integration tests
├── Dockerfile               # Container definition
├── docker-compose.yml       # Orchestration
└── requirements.txt         # Python dependencies
\\\

## 👨‍💻 Author

**Rahul Sunil**
*AI Engineer @ Certa.ai*
[LinkedIn](https://www.linkedin.com/in/rahulsunil2/)

---
*Built with ❤️ for the Open Source Community.*