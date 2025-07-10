from fastapi import APIRouter, HTTPException, Depends, Security
from src.chunking import get_chroma_collection
from src.journal_retriever import retrieve_journal
from src.api.auth import get_current_user
from src.api.auth import User as AuthUser

# router
router = APIRouter()


@router.get(
    "/api/{journal_id}",
    # dependencies=[Security(get_current_user, scopes=["retrieve"])], 
    summary="Fetch all chunks for a given journal document"
)
async def get_journal(journal_id: str, current_user: AuthUser = Security(get_current_user, scopes=["retrieve"])):
    collection = get_chroma_collection()
    try:
        data = retrieve_journal(collection, journal_id)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {e}")
    
    return data