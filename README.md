# Research Assistant

A research assistant application that answers questions with citations from a private archive of research papers using NLP and vector search technologies.

## Features

* **Document Ingestion**: Read and parse documents (PDF, DOCX, TXT) into page-level text.
* **Text Chunking**: Split pages into paragraphs and token-based chunks with overlap to meet model token limits.
* **Metadata Generation**: Create rich metadata for each chunk using an LLM.
* **Embeddings**: Generate vector embeddings for text chunks.
* **Storage & Search**: Upsert embeddings and metadata into ChromaDB and perform similarity searches.

## Requirements

* Python 3.12
* Dependencies:

  * `chromadb`
  * `sentence-transformers` 
  * PDF parsing library (`pymupdf`)
  * Tokenizer (`tiktoken`)

## Installation

```bash
# Clone the repository
git clone https://github.com/Thrangsohlang/Research_Assistant.git
cd research_assistant

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
research-assistant/
├── chroma_db/           # ChromaDB database
├── Files/               # Files containing chunks
├── frontend/            # frontend folder
├── src/                         # Core application code
│   ├── __init__.py
│   ├── detect_new_journals.py   # Watchdog-based detection stub
│   ├── chunking.py              # Chunking logic and metadata processing
│   ├── embedding.py             # Embedding model wrapper (all-MiniLM)
│   ├── storage.py               # ChromaDB client setup and upsert function
├── requirements.txt     # Python dependencies
└── README.md            # Project overview
```


## License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for details.

