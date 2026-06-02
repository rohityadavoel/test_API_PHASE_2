"""
Reviews router.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/reviews", tags=["reviews"])

# Post + top-rated (stubbed)
