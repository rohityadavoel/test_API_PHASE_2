"""
Chat router.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])

# POST /chat/message, GET /chat/history (stubbed)
