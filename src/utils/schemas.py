from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


# define the schema for upload
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
    
# upload request # TODO: Need to write a logic to check schema version or put schema version to chromadb
class UploadRequest(BaseModel):
    schema_version: str = Field("v0.1", description="Version of the chunk schema")  # put a default value here
    chunks: List[ChunkSchema]
   


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
    
    
# schema defination for Auth
class TokenData(BaseModel):
    sub: str                    # subject (user-identification)
    scopes: List[str] = []      # allowed scopes for this token
    exp: Optional[int] = None   # expiration timestamp
    iss: Optional[str] = None
    
class User(BaseModel):
    id: str
    username: str
    scopes: List[str] = []
    
    
# configuration
class Settings(BaseSettings):
    jwt_secret_key: SecretStr = Field(...)  # set via JWT_SECRET_KEY env var
    jwt_algorithm: str #= "HS256"
    jwt_access_token_expire_minutes: int = 60
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'  # to ignore extra environmental variables
    )
   