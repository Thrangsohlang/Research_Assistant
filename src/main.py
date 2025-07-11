from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.upload import router as upload_router
from src.api.search import router as search_router
from src.api.retrieve import router as retrieve_router

app = FastAPI(
    title="Research Assistant API",
    version="0.1.0",
    docs_url="/docs"  # TODO: make the docs
)

# origins
origins = [
    "http://localhost:3000",       # React dev server
    "http://127.0.0.1:3000", 
    "http://localhost:8000",
    "http://localhost:8001",
]


# add the middle-ware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# mount routers
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(retrieve_router)