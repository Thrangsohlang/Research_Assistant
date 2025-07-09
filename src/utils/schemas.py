from pydantic import BaseModel, Field
from typing import List, Dict


class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural-language query to embed and search")
    k: int = Field(10, gt=0, le=100, description="Max number of matches to return")
    min_score: float = Field(0.25, ge=0.25, le=1.0, description="Filter out low-confidence results")
    
    
class SearchResult(BaseModel):
    id: str
    score: float
    metadata: Dict
    document: str
    
class SearchResponse(BaseModel):
    results: List[SearchResult]