from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="English proficiency placement test API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    """Simple liveness probe used by tests and monitoring."""
    return {"status": "ok"}



FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@app.get("/")
def serve_index():
    """Serve the main UI page."""
    index = FRONTEND_DIR / "index.html"
    if not index.exists():
        return {"message": "Frontend not found. Open /docs for the API."}
    return FileResponse(index)


if FRONTEND_DIR.exists():
    app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
    app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
