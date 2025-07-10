from fastapi import APIRouter, HTTPException, Depends, Security
from src.utils.schemas import SearchRequest, SearchResponse, SearchResult
from src.chunking import embed_texts, get_chroma_collection
from src.similarity_search import semantic_search
from src.api.auth import get_current_user
from src.api.auth import User as AuthUser

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
        query_emb = embed_texts(payload.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Query embedding error: {e}")
    
    try:
        collection = get_chroma_collection()
        hits = semantic_search(
            collection=collection,
            query_embedding=query_emb,
            k=payload.k,
            min_score=payload.min_score
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector Search error: {e}")
    
    # results
    results = [SearchResult(**h) for h in hits]
    print(current_user)
    return SearchResponse(results=results)