from fastapi import FastAPI
from src.api.upload import router as upload_router
from src.api.search import router as search_router
from src.api.retrieve import router as retrieve_router

app = FastAPI(
    title="Research Assistant API",
    version="0.1.0",
    docs_url="/docs"  # TODO: make the docs
)

# mount routers
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(retrieve_router)