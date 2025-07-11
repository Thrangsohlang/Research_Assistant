from fastapi import APIRouter, HTTPException, Depends, Security
from src.utils.schemas import SearchRequest, SearchResponse, SearchResult
from src.chunking import embed_texts, get_chroma_collection
from src.similarity_search import semantic_search
from src.api.auth import get_current_user
from src.api.auth import User as AuthUser
from src.utils.logger_RA import logger

# router
router = APIRouter()

@router.post(
    "/api/similarity_search",
    # dependencies=[Security(get_current_user, scopes=["search"])],
    response_model=SearchResponse,
    summary="Run a semantic similarity search over the chunks"
)
async def similarity_search(payload: SearchRequest, current_user: AuthUser = Security(get_current_user, scopes=["search"])):
    try:
        logger.log_info(
        f"[similarity_search] User={current_user.username} querying: "
        f"'{payload.query}', k={payload.k}, min_score={payload.min_score}"
        )
        query_emb = embed_texts(payload.query)
    except Exception as e:
        logger.log_error(f"[similarity_search] Embedding error: {e}")
        raise HTTPException(status_code=500, detail= f"Query embedding error: {e}")
    
    try:
        collection = get_chroma_collection()
        hits = semantic_search(
            collection=collection,
            query_embedding=query_emb,
            k=payload.k,
            min_score=payload.min_score
        )
        logger.log_info(
            f"[similarity_search] Retrieved {len(hits)} hits from collection '{collection.name}'"
        )
        
    except Exception as e:
        logger.log_error(f"[similarity_search] Vector search error: {e}")
        raise HTTPException(status_code=500, detail=f"Vector Search error: {e}")
    
    # results
    results = [SearchResult(**h) for h in hits]
    logger.log_info("[similarity_search] Response prepared successfully")
    return SearchResponse(results=results)