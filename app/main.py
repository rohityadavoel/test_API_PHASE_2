"""
Main FastAPI application initialization.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, consultations, transactions, reviews, chat, analytics

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI startup and shutdown."""
    logger.info("App started")
    yield
    logger.info("App shutting down")

app = FastAPI(
    title="Consulting Platform Backend",
    version="1.0.0",
    description="Phase 1 backend for the Consulting Platform",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(consultations.router)
app.include_router(transactions.router)
app.include_router(reviews.router)
app.include_router(chat.router)
app.include_router(analytics.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Consulting Platform API"}
