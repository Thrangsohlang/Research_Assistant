from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Dict
from src.api.auth import get_current_user
from src.api.auth import User as AuthUser

from src.chunking import prepare_upsert_payload, upsert, get_chroma_collection

# router
router = APIRouter()


# define the schema
class ChunkSchema(BaseModel):
    id: str
    source_doc_id: str
    chunk_index: int
    section_heading: str
    journal: str
    publish_year: int
    usage_count: int
    attributes: List[str]
    link: str
    text: str
    
# upload request
class UploadRequest(BaseModel):
    schema_version: str = Field(..., description="Version of the chunk schema")
    chunks: List[ChunkSchema]
    
# upload endpoint
@router.put("/api/upload",
            status_code=status.HTTP_202_ACCEPTED,
            # dependencies=[Security(get_current_user, scopes=["ingest"])],
            summary="Ingest pre-chunked docs",
            description="Accepts a batch of journal chunks, embeds them, and stores them in ChromaDB")
async def upload_chunks(payload: UploadRequest, current_user: AuthUser = Security(get_current_user, scopes=["ingest"])):
    try:
        chunks_dict = jsonable_encoder(payload.chunks) 
        ids, embeddings, metadatas, documents = prepare_upsert_payload(chunks_dict) 
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Faled to prepart upsert payload: {e}"
        )
        
    try:
        collection = get_chroma_collection()
        result = upsert(collection, ids, embeddings, metadatas, documents)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upsert failure: {e}"
        )
    
    return {
        "success": True,
        "upserted_count": len(ids),
        "details": result
    }