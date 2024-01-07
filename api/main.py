from fastapi import FastAPI
import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from api.database.database import Base, engine
from api.handlers.routers import router
from api.schemas.responses import DetailResponse
from api.utils.middleware import log_middleware

# Initialize a FastAPI instance
app = FastAPI(
    title="FastAPI Starter",
    description="""
    This is a simple API demonstrating CRUD operations using FastAPI framework 
    utilizing SQLite3 as In-memory Database. It also includes basic logging
    utilizing as middleware for every http requests and responses. 

    It might be a good starter FastAPI framework for developing python based micro-services.

    This API does the following CRUD Operations:
    ============================================
    C -> Adds a fruit in the basket.
    R -> Reteives all fruits from the basket or specific fruit by ID
    U -> Updates fruit name or color for a specific fruit by ID
    D -> Deletes a fruit from the basket by ID

    """,
    version="0.1.0",
)


@app.on_event("startup")
async def startup():
    """Creates table in the database
    """
    Base.metadata.create_all(bind=engine)


@app.get(
    path="/",
    status_code=200,
    tags=["Default"],
)
async def index() -> DetailResponse:
    """Home Page

    Returns:
        DetailResponse: Returns a dictionary containing the message:
        {"message": f"The message that will be passed"}
    """
    return DetailResponse(message=f"Index Page")


@app.get(
    path="/health",
    status_code=200,
    tags=["Default"],
)
async def health() -> DetailResponse:
    """Health API endpoint

    Returns:
        DetailResponse: Returns a dictionary containing the message:
        {"message": f"The message that will be passed"}
    """
    return DetailResponse(message=f"Health OK")

# Prometheus Instrumentator
Instrumentator().instrument(app=app).expose(app=app, endpoint="/metrics", tags=["Default"])

# Custom Logging Middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

# Handlers/Routers
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
