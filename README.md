# Semantic Search Engine

## Overview
This project is a lightweight semantic search engine designed to work on unstructured data stored in blob-like storage systems (local folders in the current setup). Instead of relying on keyword matching, it understands the meaning of content and retrieves relevant results based on intent.

It supports multiple file types including PDFs, DOCX, PPTX, text files, and even images. Images are converted into structured textual descriptions, allowing them to be searched just like documents.

The system continuously watches a directory for changes, processes new or updated files, and builds embeddings for efficient similarity-based search.

---

## Vision
The goal is to make unstructured data easily searchable without manual tagging or strict organization.

Real-world storage systems become messy over time. This project automatically understands and indexes content—documents and images—turning raw data into a searchable knowledge base.

---

## How It Works

The system is built as a pipeline:

### 1. File Monitoring
- Watches `data/` directory
- Tracks create, update, delete, rename events
- Stores metadata in MySQL (`NEW`, `PROCESSING`, `PROCESSED`)

### 2. Image Preprocessing
- Generates structured description (MiniCPM-V via Ollama)
- Extracts EXIF metadata
- Stores both in DB
- Converts images → searchable text

### 3. Content Extraction
- **PDF** → PyMuPDF
- **DOCX** → docx2txt
- **PPTX** → python-pptx
- **TXT** → direct read
- **Images** → fetched from DB (description + EXIF)

### 4. Chunking
- Splits text into overlapping chunks

### 5. Embedding Generation
- Converts chunks → vectors
- Normalizes and stores locally (`.npy`)

### 6. Search
- Query → embedding
- Cosine similarity
- Returns top-k results

---

## Architecture / Workflow

![Workflow](assets/architecture.png)

---

## Tech Stack

- Python
- MySQL
- SentenceTransformers (`BAAI/bge-small-en-v1.5`)
- Ollama (`minicpm-v`)
- Pillow (EXIF extraction)
- PyMuPDF
- python-pptx
- docx2txt
- watchdog
- NumPy

---

## Features

- Semantic search across multiple file formats
- Real-time file tracking
- Image understanding via LLM
- EXIF-aware indexing
- Incremental processing via status flags
- Chunk-based retrieval
- Document-level ranking
- Local-first design

---

### Prerequisites
- Python 3.9+
- MySQL
- Ollama
- (Optional) GPU

---


