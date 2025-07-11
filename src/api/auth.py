import os
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes

from src.utils.schemas import TokenData, User, Settings
from src.utils.logger_RA import logger



# initialize settings
settings= Settings() # type:ignore

 
    
# Example usage: NOTE: In production replace with real database
_USERS_DB = {
    "alice": {"id": "alice", "username": "alice", "scopes": ["ingest", "search"]},
    "bob":   {"id": "bob",   "username": "bob",   "scopes": ["search", "retrieve"]},
    "admin": {"id": "admin", "username": "admin", "scopes": ["ingest", "search", "retrieve", "admin"]}
}

def get_user(user_id: str) -> Optional[User]:
    user = _USERS_DB.get(user_id)
    
    if not user:
        return None
    return User(**user)


# Token creation utility
def create_access_token(
    subject: str,
    scopes: List[str],
    expires_delta: Optional[timedelta] = None 
) -> str:
    logger.log_info(f"[auth] Creating token for subject='{subject}' scopes={scopes}")
    to_encode = {
        "sub": subject,
        "scopes": scopes,
        "iss": "Research-Assistant"
    }
    
    # get the expire time
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    
    to_encode.update({"exp": expire})
    
    # encode jwt
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key.get_secret_value(), algorithm=settings.jwt_algorithm
    )
    
    logger.log_info(f"[auth] Token created for subject='{subject}', expires={expire.isoformat()}")
    
    return encoded_jwt

# auth dependency
bearer_schema = HTTPBearer(auto_error=False)

def get_current_user(
    security_scopes: SecurityScopes,
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_schema),
) -> User:
    logger.log_info(f"[auth] get_current_user called, required_scopes={security_scopes.scopes}")
    if credentials is None or credentials.scheme.lower() != "bearer":
        logger.log_error("[auth] Missing or invalid authorization scheme")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Missing or invalid authorization scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # token
    token = credentials.credentials
    
    logger.log_info(f"[auth] Decoding token for user lookup")
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            options={"require": ["exp","sub", "scopes", "iss"]},
            issuer="Research-Assistant"
        )
        
        token_data = TokenData(**payload)
        
        logger.log_info(f"[auth] Token valid for subject='{token_data.sub}', scopes={token_data.scopes}")
    
    except jwt.ExpiredSignatureError:
        logger.log_error("[auth] Token has expired")
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except jwt.PyJWTError as e:
        logger.log_error(f"[auth] Token validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    # get user
    user = get_user(token_data.sub)
    
    if not user:
        logger.log_error(f"[auth] User not found: '{token_data.sub}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found!",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    # Ensure the token's scope include all security_scopes
    missing = [scope for scope in security_scopes.scopes if scope not in token_data.scopes]
    
    if missing:
        logger.log_error(f"[auth] Insufficient scopes for user='{user.username}', missing={missing}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required scopes not granted: {missing}",
            headers={"WWW-Authenticate": f'Bearer scope: "{', '.join(security_scopes.scopes)}"'}
        )
    
    logger.log_info(f"[auth] Authenticated user='{user.username}' with scopes={user.scopes}")
    return user

    
if __name__=="__main__":
    print(f"Algorithm: {settings.jwt_algorithm}")
    print(f"Actual Secret Key value: {settings.jwt_secret_key.get_secret_value()}")