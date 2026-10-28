from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import datetime
import os

from app.db.init_db import init_database
from app.api.auth import router as auth_router
from app.api.student import router as student_router
from app.api.faculty import router as faculty_router
from app.api.syllabus import router as syllabus_router
from app.api.quiz import router as quiz_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes SQLite database and seed records on application startup."""
    init_database()
    yield


app = FastAPI(
    title="Smart Study Management System Core Platform",
    description="Enterprise-grade EdTech platform with adaptive scheduling, syllabus ingestion, and quiz generator.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for open client communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health", tags=["Health Probe"])
def health_check():
    """Health and readiness probe."""
    return {
        "status": "ok",
        "service": "smart-study-management-system",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


# Include API Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(student_router, prefix="/api/v1")
app.include_router(faculty_router, prefix="/api/v1")
app.include_router(syllabus_router, prefix="/api/v1")
app.include_router(quiz_router, prefix="/api/v1")

# Mount Static UI Files
if os.path.exists("public"):
    if os.path.exists("public/pages"):
        app.mount("/pages", StaticFiles(directory="public/pages"), name="pages")
    if os.path.exists("public/js"):
        app.mount("/js", StaticFiles(directory="public/js"), name="js")
    if os.path.exists("public/css"):
        app.mount("/css", StaticFiles(directory="public/css"), name="css")
    app.mount("/", StaticFiles(directory="public", html=True), name="public")
