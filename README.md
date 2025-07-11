# Research Assistant

A research assistant application that answers questions with citations from a private archive of research papers using NLP and vector search technologies.

## Features

* **Document Ingestion**: Read and parse documents (PDF, DOCX, TXT) into page-level text.
* **Text Chunking**: Split pages into paragraphs and token-based chunks with overlap to meet model token limits.
* **Metadata Generation**: Create rich metadata for each chunk using an LLM.
* **Embeddings**: Generate vector embeddings for text chunks.
* **Storage & Search**: Upsert embeddings and metadata into ChromaDB and perform similarity searches.
* **APIs**  
  - `PUT /api/upload` — ingest pre-chunked JSON (with optional `schema_version`)  
  - `POST /api/similarity_search` — semantic search (query + optional `k` & `min_score`)  
  - `GET /api/{journal_id}` — retrieve all chunks for a given document  
  - JWT-based auth & role-based scopes (`ingest`, `search`, `retrieve`)  
* **Frontend UI**  
  - **Token Panel** — paste and save your JWT for API calls  
  - **Upload Form** — select a JSON file of chunks and (optionally) override schema version  
  - **Retrieve Form** — load an entire journal by its `source_doc_id`  
  - **Search Bar & Results** — ask questions, adjust `k` & `min_score`, and view cited chunks  


## Requirements

### Backend
* Python 3.12
- Dependencies (see `requirements.txt`):
  - `fastapi`, `uvicorn`
  - `chromadb`
  - `sentence-transformers`
  - `python-jose[cryptography]`
  - `python-dotenv`
  - PDF parsing (`pymupdf`)
  - Tokenizer (`tiktoken`)

### Frontend
- Node.js 16+
- Yarn or npm
- Dependencies (in `frontend/`):
  - `react`, `react-dom`, `typescript`, `vite`
  - `axios`

### 1. Clone the repository

```bash
git clone https://github.com/Thrangsohlang/Research_Assistant.git
cd Research_Assistant
```

### 2. Backend Setup
#### 1. Create Environment and Install dependencies 
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
#### 2. Configure environment variables
Create a .env in the project root:
```bash
JWT_SECRET_KEY=<your-generated-secret>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Run and copy the secret key in the above JWT_SECRET_KEY
```bash
python -m src.utils.generate_jwt_secret_key
```

#### 3. Start the FastAPI server
```bash
uvicorn src.api.main:app --reload
```

### 3. Frontend Setup
#### 1. Navigate to the frontend folder
```bash
cd frontend
```

#### 2. Install JS dependencies
```bash
npm install
```

#### 3. Start the React dev server
```bash
npm start
```
## Usage
### 1. Generate JWT tokens for 'admin' with scopes['ingest', 'retrieve', 'search']
```bash
python -m src.utils.create_token
```
### 2. In the browser, open the Token panel, paste your token, and click Save.

### 3. Ingest data:

Click Upload JSON, choose your raw chunks-array file, and optionally override schema_version.

### 4. Retrieve a document:

Enter the source_doc_id (e.g. extension_brief_mucuna.pdf) and click Load.

### 5. Search:

Type a query, optionally set k and min_score, then hit Search. Cited chunks appear below.

## Project Structure

```
research-assistant/
├── chroma_db/           # ChromaDB database
├── Files/               # Files containing chunks
├── frontend/            # frontend folder
|   ├── public/
│   └── src/
│       ├── components/          # TokenPanel, UploadForm, RetrieveForm, SearchBar, ResultsList
│       ├── api/                 # Axios client (auto-attaches JWT)
│       └── App.tsx
├── src/     # Core application code
|   ├── api/                     # contains the FastAPI router
|   ├── utils/                   # Contains the utility function                  
│   ├── __init__.py
│   ├── detect_new_journals.py   # Watchdog-based detection stub
│   ├── chunking.py              # Chunking logic and metadata processing
│   ├── journal_retriever.py     # Embedding model wrapper (all-MiniLM)
│   ├── similarity_search.py     # ChromaDB client setup and upsert function
|   ├── main.py                  # Contains the entry point to FastAPI
├── requirements.txt     # Python dependencies
└── README.md            # Project overview
```


## License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for details.

