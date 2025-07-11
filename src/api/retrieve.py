from fastapi import APIRouter, HTTPException, Depends, Security
from src.chunking import get_chroma_collection
from src.journal_retriever import retrieve_journal
from src.api.auth import get_current_user
from src.api.auth import User as AuthUser
from src.utils.logger_RA import logger

# router
router = APIRouter()


@router.get(
    "/api/{journal_id}",
    # dependencies=[Security(get_current_user, scopes=["retrieve"])], 
    summary="Fetch all chunks for a given journal document"
)
async def get_journal(journal_id: str, current_user: AuthUser = Security(get_current_user, scopes=["retrieve"])):
    logger.log_info(
        f"[get_journal] User={current_user.username} requesting journal_id='{journal_id}'"
    )
    collection = get_chroma_collection()
    try:
        data = retrieve_journal(collection, journal_id)
        logger.log_info(
            f"[get_journal] Retrieved {len(data.get('documents', []))} chunks "
            f"for journal_id='{journal_id}' from collection '{collection.name}'"
        )
        
    except ValueError as e:
        logger.log_error(f"[get_journal] Not found error for journal_id='{journal_id}': {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.log_error(f"[get_journal] Retrieval error for journal_id='{journal_id}': {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval error: {e}")
    
    logger.log_info(f"[get_journal] Completed request for journal_id='{journal_id}' successfully")
    return data