from fastapi import APIRouter, HTTPException
from src.utils.schemas import SearchRequest, SearchResponse, SearchResult
from src.chunking import embed_texts, get_chroma_collection
from src.similarity_search import semantic_search

# router
router = APIRouter()

@router.post(
    "/api/similarity_search",
    response_model=SearchResponse,
    summary="Run a semantic similarity search over the chunks"
)
async def similarity_search(payload: SearchRequest):
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
    return SearchResponse(results=results)