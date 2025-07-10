import os
from datetime import timedelta
from src.api.auth import create_access_token


if __name__=="__main__":
    subject = "alice"
    scopes = ["ingest", "search"]
    token = create_access_token(subject=subject, scopes=scopes, expires_delta=timedelta(days=1))
    print(f"Bearer: {token}")