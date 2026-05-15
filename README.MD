# Document Q&A App (RAG-Based PDF Question Answering)

A lightweight Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural language questions about their contents.

The application uses semantic search over embedded document chunks to retrieve relevant context and generate grounded answers using an LLM.

It supports:
- Multi-PDF upload
- Source citations
- Retrieval transparency
- Configurable retrieval parameters


# Features

- Upload 1–3 PDF documents
- Ask natural language questions
- Semantic document retrieval using vector embeddings
- Answers generated using GPT-4o-mini
- Source citations with page references
- Retrieval transparency through retrieved chunk inspection
- Configurable chunking and retrieval parameters
- Simple Streamlit-based UI

# Prerequisites

- Python 3.11 (look at the foot notes for installation of python 3.11)
- OpenAI API Key

This project requires Python 3.11 due to compatibility requirements with modern LangChain/OpenAI dependencies.

---
# Quick Start

## 1. Install Python 3.11

### Ubuntu/Debian

```bash
sudo apt install python3.11 python3.11-venv
```

### Fedora

```bash
sudo dnf install python3.11
```

### macOS (Homebrew)

```bash
brew install python@3.11
```

Verify installation:

```bash
python3.11 --version
```

---

## 2. Clone Repository

```bash
git clone https://github.com/absagargupta/streamlit_app_RAG.git
cd streamlit_app_RAG
```

---

## 3. Configure Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## 4. Run Application

Make the script executable:

```bash
chmod +x run.sh
```

Start the application:

```bash
./run.sh
```

The application will start locally at:

```text
http://localhost:8501
```

---

## Setup Simplification

A lightweight shell script (`run.sh`) was added to simplify environment setup and application startup using a single command workflow.

# Example Usage

1. Upload 1–3 PDF files
2. Ask natural language questions such as:
   - "What technical skills are mentioned?"
   - "Summarize the candidate's work experience"
   - "What patents are listed?"
3. Review generated answers and citations
4. Inspect retrieved chunks in the retrieval transparency section

# Architecture
The application follows a simple Retrieval-Augmented Generation (RAG) pipeline:

```text
PDF Upload
   ↓
PDF Parsing
   ↓
Text Chunking
   ↓
Embedding Generation
   ↓
Vector Storage (ChromaDB)
   ↓
Semantic Retrieval
   ↓
LLM Prompting
   ↓
Answer + Citations
```

# Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Store | ChromaDB |
| PDF Parsing | PyPDFLoader |
| Framework | Minimal LangChain usage |

# Project Structure

```text
document-qa-app/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── pdf_processor.py
│   ├── vector_store.py
│   ├── rag_pipeline.py
│   └── prompts.py
```
# Limitations

- Designed for small-scale usage (1–3 PDFs)
- No OCR support for scanned/image PDFs
- No persistent vector database storage
- No authentication or multi-user support
- Retrieval quality may degrade for extremely large documents

# Design Decisions

## Minimal LangChain Usage

LangChain was used only for:
- PDF loading
- text chunking
- embedding integration
- vector store integration

The retrieval and prompting pipeline was implemented explicitly to keep the RAG flow transparent and easier to reason about.

---

## In-Memory Vector Store

An in-memory ChromaDB setup was used to keep the architecture simple and lightweight for the assignment scope.

---

## Retrieval Transparency

The application exposes retrieved chunks used during answer generation. This improves explainability and helps debug retrieval quality.

---

## Centralized Configuration

Chunking, retrieval, and model-related parameters were centralized into a dedicated config module to improve maintainability and experimentation.

---

## Chunking Strategy

RecursiveCharacterTextSplitter was used with:
- chunk_size = 400
- chunk_overlap = 50

This balances retrieval precision and contextual completeness.

# Future Improvements

Potential future enhancements include:

- Persistent vector storage
- Hybrid search (keyword + semantic retrieval)
- Reranking retrieved chunks
- Dockerized deployment
- Conversation memory
- Evaluation framework integration

