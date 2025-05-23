import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes.generation.router import router as generation_router
from app.api.v1.routes.health.router import router as health_router

app = FastAPI(
    title="Content Generation Service",
    description="Service for generating content using Azure AI Search and LangChain",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generation_router, prefix="/api/v1/generation", tags=["generation"])
app.include_router(health_router, prefix="/api/v1", tags=["health"])

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Content Generation Service",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload for debugging
    )

