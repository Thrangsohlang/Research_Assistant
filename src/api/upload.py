from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Dict

from src.utils.schemas import UploadRequest, ChunkSchema
from src.api.auth import get_current_user
from src.api.auth import User as AuthUser
from src.chunking import prepare_upsert_payload, upsert, get_chroma_collection

from src.utils.logger_RA import logger
# router
router = APIRouter()


 
# upload endpoint
@router.put("/api/upload",
            status_code=status.HTTP_202_ACCEPTED,
            # dependencies=[Security(get_current_user, scopes=["ingest"])],
            summary="Ingest pre-chunked docs",
            description="Accepts a batch of journal chunks, embeds them, and stores them in ChromaDB")
async def upload_chunks(payload: UploadRequest, current_user: AuthUser = Security(get_current_user, scopes=["ingest"])):
    try:
        logger.log_info(f"Current_User: {current_user}")
        chunks_dict = jsonable_encoder(payload.chunks) 
        
        ids, embeddings, metadatas, documents = prepare_upsert_payload(chunks_dict) 
        logger.log_info(
            f"[upload_chunks] Prepared upsert payload: "
            f"{len(ids)} ids, {len(embeddings)} embeddings"
        )
        
    
    except Exception as e:
        logger.log_error(f"Failed to upsert payload: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Faled to prepart upsert payload: {e}"
        )
        
        
    try:
        collection = get_chroma_collection()
        result = upsert(collection, ids, embeddings, metadatas, documents)
        
        logger.log_info(
            f"[upload_chunks] Upsert successful: "
            f"{len(ids)} chunks into collection '{collection.name}'"
        )
    
    except Exception as e:
        logger.log_error(f"[upload_chunks] Upsert failure: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Upsert failure: {e}"
        )
    logger.log_info("[upload_chunks] Request completed successfully")
    return {
        "success": True,
        "upserted_count": len(ids),
        "details": result
    }