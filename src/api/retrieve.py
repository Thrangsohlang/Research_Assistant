from fastapi import APIRouter, HTTPException
from src.chunking import get_chroma_collection
from src.journal_retriever import retrieve_journal

# router
router = APIRouter()


@router.get(
    "/api/{journal_id}",
    summary="Fetch all chunks for a given journal document"
)
async def get_journal(journal_id: str):
    collection = get_chroma_collection()
    try:
        data = retrieve_journal(collection, journal_id)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {e}")
    
    return data