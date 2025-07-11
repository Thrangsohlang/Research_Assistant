## Design Rationale

### 1. Event-Driven Ingestion

Rather than using a polling loop, I adopted an event-driven approach (e.g., filesystem events via Python’s **watchdog**, or S3 → Lambda in AWS) for detecting newly arrived journal files. This strategy offers:

- **Lower latency**: Handlers fire immediately upon file creation, instead of waiting for the next polling interval.  
- **Resource efficiency**: Eliminates continuous wake-sleep cycles and directory scans, keeping CPU usage minimal during idle periods.  
- **Cloud compatibility**: Mirrors production patterns (e.g., S3 event notifications), allowing a seamless transition from local prototypes to serverless architectures.

---

### 2. Vector Database: ChromaDB

For my vector store, I selected **ChromaDB** based on the following criteria:

1. **Open-Source & Self-Hosted**  
   - MIT-licensed with no vendor lock-in.  
   - Ideal for sensitive, private archives of journal content.

2. **Zero-Ops Local Setup**  
   - Installable via `pip install chromadb`.  
   - Bundled persistence (SQLite/DuckDB) removes the need for external databases.

3. **Python-First API**  
   - Native integration with my Python ingestion and embedding scripts.  
   - Simple, intuitive methods for creating collections, upserting vectors, and querying.

4. **Powerful Metadata Filtering**  
   - Native support for arbitrary metadata fields (e.g. `publish_year`, `usage_count`, `section_heading`) allows efficient faceted search without additional indices.

5. **Embeddings Agnostic**  
   - Compatible with any embedding generator (OpenAI, HuggingFace, custom models) without proprietary constraints.

---

### 3. Optional & Future Enhancements

In addition to the core pipeline and APIs, I’ve implemented:

- **React-based Frontend UI**  
  - Token management panel for JWT authentication.  
  - Forms for JSON ingestion and document retrieval.  
  - Search interface with adjustable parameters (`k` and `min_score`).

- **Role-Based Access Control**  
  - JWT-issued tokens with scoped permissions (`ingest`, `search`, `retrieve`).  
  - Secure endpoints using FastAPI’s dependency injection.

#### Planned Improvements

- **User Management**: I will integrate a user database for registration, login, and token revocation.  
- **Retry & Monitoring**: I will add robust retry logic (e.g., exponential backoff) and pipeline health metrics (Prometheus/Grafana).  
- **Additional APIs**: Summary, comparison, and other LLM-driven content-generation endpoints.  
- **Unit & Integration Tests**: I will expand coverage across ingestion, search, and retrieval workflows.  
- **Scaling**: I will evaluate managed vector-store options (e.g., Pinecone, Weaviate) for high-volume deployments.
```
::contentReference[oaicite:0]{index=0}
