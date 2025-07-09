from fastapi import FastAPI
from src.api.upload import router as upload_router

app = FastAPI(
    title="Research Assistant API",
    version="0.1.0",
    docs_url="/docs"  # TODO: make the docs
)

# mount routers
app.include_router(upload_router)