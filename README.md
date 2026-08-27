# College RAG Assistant

A Production-Grade RAG (Retrieval-Augmented Generation) application for college guidelines using FastAPI, Amazon Bedrock, and FAISS.

## Features
- Local PDF ingestion with PyMuPDF
- Amazon Titan Text Embeddings V2
- Amazon Nova Lite for answer generation
- FAISS vector store
- Source citations (file and page)

## Setup

1. **Environment Variables**:
Ensure you have your AWS credentials configured via the AWS CLI (`aws configure`) or environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`). Set the appropriate `.env` values (see `.env` file).

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Data Preparation**:
Place your college guidelines PDFs in the `data/raw/` folder. (We provide mock PDFs for testing).

## Usage

### Ingesting Documents
Run the ingestion script to process the PDFs and create the FAISS index:
```bash
python scripts/ingest_all.py
```
*Alternatively, you can start the API and send a POST request to `/ingest`.*

### Starting the API
```bash
uvicorn app.main:app --reload
```

### Endpoints

- `GET /health` : Verify system health
- `POST /ingest` : Trigger document ingestion
- `POST /ask` : Ask a question

Example request to `/ask`:
```json
{
  "question": "What is the minimum attendance required?"
}
```

Example response:
```json
{
  "answer": "Students require 75% attendance in all courses to be eligible for the end-semester exams.",
  "sources": [
    {
      "file": "Academic Regulations.pdf",
      "page": 1
    }
  ]
}
```

## Architecture
- **Core**: Configuration and Exceptions
- **Providers**: Interactions with external systems (Bedrock, PyMuPDF)
- **Services**: Business logic (Ingestion, Retrieval, RAG)
- **API**: FastAPI route definitions
