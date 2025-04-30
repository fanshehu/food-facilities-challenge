"""Main application entry point."""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from src.api.routes import router as api_router

app = FastAPI(
    title="Mobil Food Facilities Permit API",
    description="API for accessing mobile food facilities permits data in San Francisco",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "ui", "static")

# Mount static files for UI
app.mount("/ui", StaticFiles(directory=static_dir), name="ui")

@app.get("/", tags=["root"])
async def root():
    """Root endpoint that redirects to UI."""
    return RedirectResponse(url="/ui/index.html")


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
